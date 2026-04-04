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
                "image_url": "https://images.pexels.com/photos/1123972/pexels-photo-1123972.jpeg",
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
                "image_url": "https://images.pexels.com/photos/1294929/pexels-photo-1294929.jpeg",
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
                "image_url": "https://images.pexels.com/photos/1119278/pexels-photo-1119278.jpeg",
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
                "image_url": "https://images.pexels.com/photos/675951/pexels-photo-675951.jpeg",
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
                "image_url": "https://images.pexels.com/photos/103124/pexels-photo-103124.jpeg",
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
                "image_url": "https://images.pexels.com/photos/1128678/pexels-photo-1128678.jpeg",
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
                "image_url": "https://images.pexels.com/photos/1627592/pexels-photo-1627592.jpeg",
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
                "image_url": "https://images.pexels.com/photos/9609846/pexels-photo-9609846.jpeg",
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
                "image_url": "https://images.pexels.com/photos/1473167/pexels-photo-1473167.jpeg",
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
                "image_url": "https://images.pexels.com/photos/1590763/pexels-photo-1590763.jpeg",
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
                "image_url": "https://images.pexels.com/photos/1590763/pexels-photo-1590763.jpeg",
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
                "image_url": "https://images.pexels.com/photos/616363/pexels-photo-616363.jpeg",
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
                "image_url": "https://images.pexels.com/photos/494178/pexels-photo-494178.jpeg",
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
                "image_url": "https://images.pexels.com/photos/301488/pexels-photo-301488.jpeg",
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