import json
import logging
import uuid
from datetime import datetime, date

from models.product import Product
from services.product_service import ProductService

logger = logging.getLogger(__name__)


class DatabaseSeeder:
    """Utility class for seeding the database with initial data"""

    def __init__(self, db):
        self.db = db
        self.product_service = ProductService()

    def seed_products(self):
        """Seed the database with sample products"""
        try:
            if Product.query.count() > 0:
                logger.info("Products already exist, skipping seeding")
                return

            products_data = self._get_sample_products()

            logger.info(f"Seeding {len(products_data)} products...")

            for product_data in products_data:
                try:
                    product = Product(**product_data)
                    self.db.session.add(product)
                    self.db.session.flush()

                    search_text = product.get_search_text()
                    metadata = {
                        "category": product.category,
                        "subcategory": product.subcategory,
                        "brand": product.brand,
                        "price": product.price,
                        "rating": product.rating,
                        "in_stock": product.is_in_stock(),
                    }

                    self.product_service.vector_service.upsert_product_embedding(
                        product.id, search_text, metadata
                    )

                    product.embedding_id = product.id

                except Exception as e:
                    logger.error(
                        f"Error seeding product {product_data.get('name', 'Unknown')}: {str(e)}"
                    )
                    continue

            self.db.session.commit()
            logger.info("Products seeded successfully")

        except Exception as e:
            logger.error(f"Error seeding products: {str(e)}")
            self.db.session.rollback()
            raise

    def _get_sample_products(self):
        """Get sample farm product data"""
        return [
            {
                "id": str(uuid.uuid4()),
                "name": "Organic Strawberries",
                "description": "Fresh, juicy organic strawberries grown without pesticides. Hand-picked at peak ripeness for maximum sweetness and flavor.",
                "price": 8.99,
                "category": "Produce",
                "subcategory": "Berries",
                "brand": "Green Valley Farm",
                "rating": 4.9,
                "review_count": 1247,
                "image_url": "https://i5.walmartimages.com/seo/Fresh-USDA-Organic-Strawberries-1-lb-Container_fb148fa5-193e-479c-8e89-dca9d61e2ff7_1.0d26c201e069d9940a4d0cb0c85d776d.jpeg",
                "stock": 45,
                "features": ["Organic", "Non-GMO", "Locally Grown", "Seasonal"],
                "is_on_sale": False,
                "harvest_date": date(2024, 6, 15),
                "farm_location": "Green Valley, California",
                "is_seasonal": True,
                "organic_certified": True,
                "unit_type": "per pound",
                "season": "Summer",
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Free-Range Eggs",
                "description": "Farm-fresh eggs from happy, free-range chickens. Rich golden yolks with exceptional flavor and nutritional value.",
                "price": 5.99,
                "category": "Dairy & Eggs",
                "subcategory": "Eggs",
                "brand": "Sunny Side Farm",
                "rating": 4.8,
                "review_count": 892,
                "image_url": "https://storage.bhs.cloud.ovh.net/v1/AUTH_67da374e12f7497491105aaeeebf4835/public/products/5688_5688-Organic-Free-Range-Eggs--6,-large--Fermes-Valens.jpg",
                "stock": 28,
                "features": ["Free-Range", "Organic Feed", "No Antibiotics", "Omega-3"],
                "harvest_date": date(2024, 6, 18),
                "farm_location": "Sunny Meadows, Iowa",
                "is_seasonal": False,
                "organic_certified": True,
                "unit_type": "per dozen",
                "season": "Year-Round",
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Raw Organic Honey",
                "description": "Pure, unfiltered raw honey from local wildflower meadows. Never heated or processed to preserve natural enzymes and nutrients.",
                "price": 12.99,
                "original_price": 14.99,
                "category": "Pantry",
                "subcategory": "Sweeteners",
                "brand": "Golden Hive Apiaries",
                "rating": 4.9,
                "review_count": 567,
                "image_url": "https://pchelo-teka.ru/image/cache/catalog/products/honey/lipa/lip-350-1-552x828.jpg",
                "stock": 34,
                "features": ["Raw", "Unfiltered", "Local", "Organic"],
                "is_on_sale": True,
                "sale_percentage": 13,
                "harvest_date": date(2024, 5, 20),
                "farm_location": "Wildflower Ridge, Vermont",
                "is_seasonal": True,
                "organic_certified": True,
                "unit_type": "per jar (16 oz)",
                "season": "Spring",
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Heirloom Tomatoes",
                "description": "Colorful assortment of heritage tomato varieties. Grown using traditional methods for exceptional flavor and texture.",
                "price": 6.49,
                "category": "Produce",
                "subcategory": "Vegetables",
                "brand": "Heritage Garden Farm",
                "rating": 4.7,
                "review_count": 423,
                "image_url": "https://www.lipmanfamilyfarms.com/wp-content/uploads/2020/09/Heirloom-Tomato-hero@2x.png",
                "stock": 52,
                "features": ["Heirloom", "Vine-Ripened", "Pesticide-Free", "Non-GMO"],
                "harvest_date": date(2024, 6, 10),
                "farm_location": "Heritage Valley, North Carolina",
                "is_seasonal": True,
                "organic_certified": False,
                "unit_type": "per pound",
                "season": "Summer",
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Grass-Fed Ground Beef",
                "description": "Premium ground beef from 100% grass-fed and grass-finished cattle. Lean, flavorful, and ethically raised on open pastures.",
                "price": 9.99,
                "category": "Meat & Poultry",
                "subcategory": "Beef",
                "brand": "Open Range Ranch",
                "rating": 4.8,
                "review_count": 756,
                "image_url": "https://magnumopt.kz/upload/iblock/6e6/6e66e4486f12b3453ba027a4b8b6df00.png",
                "stock": 18,
                "features": ["Grass-Fed", "Grass-Finished", "No Hormones", "No Antibiotics"],
                "harvest_date": date(2024, 6, 12),
                "farm_location": "Open Range, Montana",
                "is_seasonal": False,
                "organic_certified": True,
                "unit_type": "per pound",
                "season": "Year-Round",
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Fresh Basil Bunch",
                "description": "Aromatic fresh basil grown in nutrient-rich soil. Perfect for pesto, salads, and Italian cuisine.",
                "price": 3.99,
                "category": "Produce",
                "subcategory": "Herbs",
                "brand": "Garden Fresh Herbs",
                "rating": 4.6,
                "review_count": 234,
                "image_url": "https://img.magnific.com/premium-photo/green-leafs-fresh-young-basil-isolated-basil-herb-leaves-isolated-top-view_117930-203.jpg",
                "stock": 67,
                "features": ["Fresh", "Aromatic", "Pesticide-Free", "Hand-Harvested"],
                "harvest_date": date(2024, 6, 17),
                "farm_location": "Herb Valley, Oregon",
                "is_seasonal": True,
                "organic_certified": True,
                "unit_type": "per bunch",
                "season": "Summer",
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Artisan Goat Cheese",
                "description": "Creamy, tangy goat cheese crafted in small batches. Made from the milk of pasture-raised goats.",
                "price": 8.49,
                "category": "Dairy & Eggs",
                "subcategory": "Cheese",
                "brand": "Hillside Creamery",
                "rating": 4.9,
                "review_count": 445,
                "image_url": "https://www.tablicakalorijnosti.ru/file/image/foodstuff/46ba9c9a7f1d4df69da8db203ef75008/3b23155b2ea749b4bdbd5c13c4a897db",
                "stock": 23,
                "features": ["Artisan", "Small Batch", "Pasture-Raised", "No Preservatives"],
                "harvest_date": date(2024, 6, 14),
                "farm_location": "Hillside Farm, Wisconsin",
                "is_seasonal": False,
                "organic_certified": True,
                "unit_type": "per 8 oz wheel",
                "season": "Year-Round",
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Baby Spinach",
                "description": "Tender baby spinach leaves, triple-washed and ready to eat. Perfect for salads, smoothies, and sautéing.",
                "price": 4.99,
                "category": "Produce",
                "subcategory": "Leafy Greens",
                "brand": "Leafy Greens Co.",
                "rating": 4.5,
                "review_count": 312,
                "image_url": "https://rusagro-prom.ru/upload/resize_cache/webp/upload/iblock/199/tzaq2a96v79o7b8vm0xaam5l4aqs19in.webp",
                "stock": 89,
                "features": ["Triple-Washed", "Ready-to-Eat", "Organic", "Hydroponic"],
                "harvest_date": date(2024, 6, 16),
                "farm_location": "Green Acres, Arizona",
                "is_seasonal": False,
                "organic_certified": True,
                "unit_type": "per 5 oz bag",
                "season": "Year-Round",
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Wild-Caught Salmon",
                "description": "Premium wild-caught Alaskan salmon. Rich in omega-3 fatty acids with a firm texture and delicate flavor.",
                "price": 18.99,
                "original_price": 21.99,
                "category": "Seafood",
                "subcategory": "Fish",
                "brand": "Alaska Wild Fisheries",
                "rating": 4.9,
                "review_count": 678,
                "image_url": "https://moretorg55.ru/thumb/2/96KKw_ktKLKfUM0t_bPecw/750r750/d/98ceadd657cc305880c1cc0e3d51c2ef.jpg",
                "stock": 12,
                "features": ["Wild-Caught", "Sustainable", "Omega-3 Rich", "Flash-Frozen"],
                "is_on_sale": True,
                "sale_percentage": 14,
                "harvest_date": date(2024, 6, 8),
                "farm_location": "Bristol Bay, Alaska",
                "is_seasonal": True,
                "organic_certified": False,
                "unit_type": "per pound",
                "season": "Summer",
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Organic Blueberries",
                "description": "Plump, sweet organic blueberries packed with antioxidants. Perfect for breakfast, baking, or snacking.",
                "price": 7.99,
                "category": "Produce",
                "subcategory": "Berries",
                "brand": "Berry Bliss Farm",
                "rating": 4.8,
                "review_count": 534,
                "image_url": "https://freshmart.com.ua/storage/web/cache/product/134/chornitsya.jpeg?w=1024&h=768&fit=resize&q=80&fm=pjpg&t=1571622149&s=edd1e6f76cb87987d824c15f6d8e0f46",
                "stock": 38,
                "features": ["Organic", "Antioxidant-Rich", "Hand-Picked", "Fresh"],
                "harvest_date": date(2024, 6, 14),
                "farm_location": "Blueberry Hill, Maine",
                "is_seasonal": True,
                "organic_certified": True,
                "unit_type": "per pint",
                "season": "Summer",
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Farm Fresh Milk",
                "description": "Creamy, pasteurized whole milk from grass-fed cows. Never homogenized for a natural cream layer on top.",
                "price": 5.49,
                "category": "Dairy & Eggs",
                "subcategory": "Milk",
                "brand": "Meadow Fresh Dairy",
                "rating": 4.7,
                "review_count": 892,
                "image_url": "https://images.pexels.com/photos/248412/pexels-photo-248412.jpeg",
                "stock": 56,
                "features": ["Grass-Fed", "Non-Homogenized", "Pasteurized", "Local"],
                "harvest_date": date(2024, 6, 18),
                "farm_location": "Meadow Lane Farm, New York",
                "is_seasonal": False,
                "organic_certified": True,
                "unit_type": "per half gallon",
                "season": "Year-Round",
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Sweet Corn",
                "description": "Just-picked sweet corn with tender, juicy kernels. At its peak sweetness when harvested at the perfect moment.",
                "price": 1.29,
                "category": "Produce",
                "subcategory": "Vegetables",
                "brand": "Sunshine Farms",
                "rating": 4.6,
                "review_count": 267,
                "image_url": "https://api.magonline.ru/thumbnail/740x494/08/287/8287.png",
                "stock": 120,
                "features": ["Just-Picked", "Sweet", "Non-GMO", "Peak Freshness"],
                "harvest_date": date(2024, 6, 18),
                "farm_location": "Cornfield Valley, Illinois",
                "is_seasonal": True,
                "organic_certified": False,
                "unit_type": "per ear",
                "season": "Summer",
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Pasture-Raised Chicken",
                "description": "Whole chicken raised on lush green pastures with access to sunshine and fresh air. Tender, flavorful meat with firm texture.",
                "price": 4.99,
                "category": "Meat & Poultry",
                "subcategory": "Chicken",
                "brand": "Happy Hen Farm",
                "rating": 4.8,
                "review_count": 445,
                "image_url": "https://papinalavka.ru/content/catalog_image/469/big_dsc_0766_2.jpg",
                "stock": 15,
                "features": ["Pasture-Raised", "No Antibiotics", "No Hormones", "Air-Chilled"],
                "harvest_date": date(2024, 6, 15),
                "farm_location": "Happy Hen Farm, Tennessee",
                "is_seasonal": False,
                "organic_certified": True,
                "unit_type": "per pound",
                "season": "Year-Round",
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Organic Avocados",
                "description": "Creamy, perfectly ripe organic avocados. Rich in healthy fats and perfect for guacamole, toast, or salads.",
                "price": 2.99,
                "category": "Produce",
                "subcategory": "Fruits",
                "brand": "Tropical Grove",
                "rating": 4.7,
                "review_count": 623,
                "image_url": "https://static.tildacdn.com/tild6364-6166-4164-b830-326539386432/IMG_5430_1.JPG",
                "stock": 78,
                "features": ["Organic", "Perfectly Ripe", "Creamy", "Nutrient-Dense"],
                "harvest_date": date(2024, 6, 12),
                "farm_location": "Avocado Valley, California",
                "is_seasonal": False,
                "organic_certified": True,
                "unit_type": "per each",
                "season": "Year-Round",
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Maple Syrup",
                "description": "Pure Grade A maple syrup tapped from Vermont sugar maples. Rich, complex flavor with notes of caramel and vanilla.",
                "price": 16.99,
                "category": "Pantry",
                "subcategory": "Sweeteners",
                "brand": "Vermont Maple Works",
                "rating": 4.9,
                "review_count": 389,
                "image_url": "https://cdn1.ozone.ru/multimedia/1037093476.jpg",
                "stock": 29,
                "features": ["Pure", "Grade A", "Vermont", "Small Batch"],
                "harvest_date": date(2024, 3, 15),
                "farm_location": "Maple Grove, Vermont",
                "is_seasonal": True,
                "organic_certified": True,
                "unit_type": "per 12 oz bottle",
                "season": "Spring",
            },
        ]