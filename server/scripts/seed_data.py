"""
Seed script: inserts mock farms + products into the DB and indexes them to Pinecone.
Run inside the server container:
    docker exec -it ecommerce-chatbot-server-1 python scripts/seed_data.py
Or locally:
    cd server && python scripts/seed_data.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import uuid
from datetime import date

from app import create_app
from models import db
from models.farm import Farm
from models.product import Product
from services.vector_service import VectorService

# ---------------------------------------------------------------------------
# Mock data
# ---------------------------------------------------------------------------

FARMS = [
    {
        "id": str(uuid.uuid4()),
        "name": "Ферма Алтын Дала",
        "description": "Семейная ферма в предгорьях Алматы. Выращиваем органические овощи и фрукты с 1998 года.",
        "location": "Алматинская область",
        "address": "с. Каскелен, Карасайский район",
        "latitude": 43.19,
        "longitude": 76.62,
        "phone": "+7 727 123-45-67",
        "email": "altyndala@farm.kz",
        "website": "https://altyndala.kz",
        "image_url": "https://images.unsplash.com/photo-1500651230702-0e2d8a49d4ad?w=800",
        "story": "Наша семья занимается земледелием уже три поколения. Мы используем только природные удобрения и бережём воду.",
        "practices": ["Органическое земледелие", "Капельный полив", "Компостирование"],
        "certifications": ["Органик KZ", "GlobalG.A.P."],
        "established_year": 1998,
        "acreage": 120.5,
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Молочная ферма Акбота",
        "description": "Современная молочная ферма с собственным стадом коров породы Голштин. Свежее молоко каждый день.",
        "location": "Акмолинская область",
        "address": "с. Степное, Целиноградский район",
        "latitude": 51.18,
        "longitude": 71.45,
        "phone": "+7 717 234-56-78",
        "email": "akbota@dairy.kz",
        "image_url": "https://images.unsplash.com/photo-1516467508483-a7212febe31a?w=800",
        "story": "Мы производим натуральное молоко и молочные продукты без добавок и консервантов.",
        "practices": ["Пастбищное содержание", "Без антибиотиков", "Ручная дойка"],
        "certifications": ["HACCP", "ISO 22000"],
        "established_year": 2005,
        "acreage": 350.0,
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Птицефабрика Жулдыз",
        "description": "Экологически чистое птицеводство. Куры на свободном выгуле, натуральный корм.",
        "location": "Жамбылская область",
        "address": "г. Тараз, пригород",
        "latitude": 42.90,
        "longitude": 71.37,
        "phone": "+7 726 345-67-89",
        "email": "zhuldyz@poultry.kz",
        "image_url": "https://images.unsplash.com/photo-1548550023-2bdb3c5beed7?w=800",
        "story": "Наши куры живут на свежем воздухе и питаются зерном без ГМО.",
        "practices": ["Свободный выгул", "Без ГМО", "Натуральный корм"],
        "certifications": ["Органик KZ"],
        "established_year": 2010,
        "acreage": 80.0,
    },
]

# We'll assign farm_location strings from the farms above
_farm_locations = [f["location"] for f in FARMS]

PRODUCTS = [
    # ── Овощи и фрукты ──────────────────────────────────────────────────────
    {
        "id": str(uuid.uuid4()),
        "name": "Томаты черри органические",
        "description": "Сладкие и сочные томаты черри, выращенные без пестицидов в теплицах Алматинской области.",
        "price": 850.0,
        "original_price": 1000.0,
        "category": "Овощи и фрукты",
        "subcategory": "Томаты",
        "brand": "Алтын Дала",
        "rating": 4.8,
        "review_count": 124,
        "image_url": "https://images.unsplash.com/photo-1592841200221-a6898f307baa?w=400",
        "stock": 200,
        "features": ["Органические", "Без пестицидов", "Тепличные", "Сочные"],
        "is_on_sale": True,
        "sale_percentage": 15,
        "harvest_date": date(2026, 4, 20),
        "farm_location": _farm_locations[0],
        "is_seasonal": False,
        "organic_certified": True,
        "unit_type": "за кг",
        "season": "Круглый год",
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Огурцы свежие",
        "description": "Хрустящие огурцы прямо с грядки. Идеальны для салатов и засолки.",
        "price": 450.0,
        "original_price": None,
        "category": "Овощи и фрукты",
        "subcategory": "Огурцы",
        "brand": "Алтын Дала",
        "rating": 4.6,
        "review_count": 89,
        "image_url": "https://images.unsplash.com/photo-1449300079323-02e209d9d3a6?w=400",
        "stock": 300,
        "features": ["Свежие", "Хрустящие", "Без ГМО"],
        "is_on_sale": False,
        "harvest_date": date(2026, 4, 21),
        "farm_location": _farm_locations[0],
        "is_seasonal": True,
        "organic_certified": True,
        "unit_type": "за кг",
        "season": "Лето",
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Яблоки Апорт алматинский",
        "description": "Знаменитые алматинские яблоки сорта Апорт. Крупные, ароматные, с насыщенным вкусом.",
        "price": 700.0,
        "original_price": None,
        "category": "Овощи и фрукты",
        "subcategory": "Яблоки",
        "brand": "Алтын Дала",
        "rating": 4.9,
        "review_count": 210,
        "image_url": "https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=400",
        "stock": 500,
        "features": ["Сорт Апорт", "Крупные", "Ароматные", "Местный сорт"],
        "is_on_sale": False,
        "harvest_date": date(2025, 9, 15),
        "farm_location": _farm_locations[0],
        "is_seasonal": True,
        "organic_certified": True,
        "unit_type": "за кг",
        "season": "Осень",
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Картофель молодой",
        "description": "Молодой картофель с нежной кожицей и рассыпчатой мякотью. Без нитратов.",
        "price": 300.0,
        "original_price": None,
        "category": "Овощи и фрукты",
        "subcategory": "Картофель",
        "brand": "Алтын Дала",
        "rating": 4.5,
        "review_count": 67,
        "image_url": "https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=400",
        "stock": 1000,
        "features": ["Молодой", "Без нитратов", "Рассыпчатый"],
        "is_on_sale": False,
        "harvest_date": date(2026, 4, 18),
        "farm_location": _farm_locations[0],
        "is_seasonal": True,
        "organic_certified": False,
        "unit_type": "за кг",
        "season": "Лето",
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Морковь органическая",
        "description": "Сладкая органическая морковь богатая бета-каротином. Выращена на чистых почвах.",
        "price": 280.0,
        "original_price": None,
        "category": "Овощи и фрукты",
        "subcategory": "Морковь",
        "brand": "Алтын Дала",
        "rating": 4.7,
        "review_count": 95,
        "image_url": "https://images.unsplash.com/photo-1447175008436-054170c2e979?w=400",
        "stock": 400,
        "features": ["Органическая", "Сладкая", "Богата бета-каротином"],
        "is_on_sale": False,
        "harvest_date": date(2026, 4, 10),
        "farm_location": _farm_locations[0],
        "is_seasonal": False,
        "organic_certified": True,
        "unit_type": "за кг",
        "season": "Круглый год",
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Клубника свежая",
        "description": "Ароматная клубника прямо с грядки. Сладкая, крупная, без химикатов.",
        "price": 1500.0,
        "original_price": 1800.0,
        "category": "Овощи и фрукты",
        "subcategory": "Ягоды",
        "brand": "Алтын Дала",
        "rating": 4.9,
        "review_count": 312,
        "image_url": "https://images.unsplash.com/photo-1464965911861-746a04b4bca6?w=400",
        "stock": 150,
        "features": ["Свежая", "Сладкая", "Без химикатов", "Сезонная"],
        "is_on_sale": True,
        "sale_percentage": 17,
        "harvest_date": date(2026, 4, 22),
        "farm_location": _farm_locations[0],
        "is_seasonal": True,
        "organic_certified": True,
        "unit_type": "за кг",
        "season": "Лето",
    },
    # ── Молочные продукты ────────────────────────────────────────────────────
    {
        "id": str(uuid.uuid4()),
        "name": "Молоко цельное 3.5%",
        "description": "Свежее цельное молоко от коров на пастбищном содержании. Жирность 3.5%, без добавок.",
        "price": 420.0,
        "original_price": None,
        "category": "Молочные продукты",
        "subcategory": "Молоко",
        "brand": "Акбота",
        "rating": 4.7,
        "review_count": 188,
        "image_url": "https://images.unsplash.com/photo-1550583724-b2692b85b150?w=400",
        "stock": 80,
        "features": ["Цельное", "3.5% жирность", "Без добавок", "Пастбищное"],
        "is_on_sale": False,
        "harvest_date": date(2026, 4, 22),
        "farm_location": _farm_locations[1],
        "is_seasonal": False,
        "organic_certified": False,
        "unit_type": "за литр",
        "season": "Круглый год",
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Творог домашний 9%",
        "description": "Натуральный домашний творог из цельного молока. Нежный, без кислинки, богат белком.",
        "price": 1200.0,
        "original_price": None,
        "category": "Молочные продукты",
        "subcategory": "Творог",
        "brand": "Акбота",
        "rating": 4.8,
        "review_count": 145,
        "image_url": "https://images.unsplash.com/photo-1589985270826-4b7bb135bc9d?w=400",
        "stock": 50,
        "features": ["9% жирность", "Без консервантов", "Богат белком", "Домашний"],
        "is_on_sale": False,
        "harvest_date": date(2026, 4, 21),
        "farm_location": _farm_locations[1],
        "is_seasonal": False,
        "organic_certified": False,
        "unit_type": "за кг",
        "season": "Круглый год",
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Сметана 20%",
        "description": "Густая сметана из натуральных сливок. Идеальна для заправки супов и приготовления соусов.",
        "price": 650.0,
        "original_price": None,
        "category": "Молочные продукты",
        "subcategory": "Сметана",
        "brand": "Акбота",
        "rating": 4.6,
        "review_count": 102,
        "image_url": "https://images.unsplash.com/photo-1563636619-e9143da7973b?w=400",
        "stock": 60,
        "features": ["20% жирность", "Густая", "Натуральные сливки", "Без загустителей"],
        "is_on_sale": False,
        "harvest_date": date(2026, 4, 20),
        "farm_location": _farm_locations[1],
        "is_seasonal": False,
        "organic_certified": False,
        "unit_type": "за 500г",
        "season": "Круглый год",
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Кефир натуральный 2.5%",
        "description": "Живой кефир с пробиотиками. Полезен для пищеварения, без искусственных добавок.",
        "price": 380.0,
        "original_price": None,
        "category": "Молочные продукты",
        "subcategory": "Кефир",
        "brand": "Акбота",
        "rating": 4.5,
        "review_count": 78,
        "image_url": "https://images.unsplash.com/photo-1571197119680-7c088f7f8fba?w=400",
        "stock": 90,
        "features": ["Живые культуры", "Пробиотики", "2.5% жирность", "Без добавок"],
        "is_on_sale": False,
        "harvest_date": date(2026, 4, 22),
        "farm_location": _farm_locations[1],
        "is_seasonal": False,
        "organic_certified": False,
        "unit_type": "за литр",
        "season": "Круглый год",
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Масло сливочное 82.5%",
        "description": "Настоящее деревенское сливочное масло. Жирность 82.5%, без растительных жиров.",
        "price": 1800.0,
        "original_price": 2100.0,
        "category": "Молочные продукты",
        "subcategory": "Масло",
        "brand": "Акбота",
        "rating": 4.9,
        "review_count": 230,
        "image_url": "https://images.unsplash.com/photo-1589985270826-4b7bb135bc9d?w=400",
        "stock": 40,
        "features": ["82.5% жирность", "Деревенское", "Без растительных жиров", "ГОСТ"],
        "is_on_sale": True,
        "sale_percentage": 14,
        "harvest_date": date(2026, 4, 19),
        "farm_location": _farm_locations[1],
        "is_seasonal": False,
        "organic_certified": False,
        "unit_type": "за 400г",
        "season": "Круглый год",
    },
    # ── Мясо и птица ─────────────────────────────────────────────────────────
    {
        "id": str(uuid.uuid4()),
        "name": "Курица деревенская целая",
        "description": "Домашняя курица свободного выгула. Натуральный корм, никаких гормонов.",
        "price": 2500.0,
        "original_price": None,
        "category": "Мясо и птица",
        "subcategory": "Курица",
        "brand": "Жулдыз",
        "rating": 4.8,
        "review_count": 156,
        "image_url": "https://images.unsplash.com/photo-1548550023-2bdb3c5beed7?w=400",
        "stock": 30,
        "features": ["Свободный выгул", "Без гормонов", "Натуральный корм", "Деревенская"],
        "is_on_sale": False,
        "harvest_date": date(2026, 4, 21),
        "farm_location": _farm_locations[2],
        "is_seasonal": False,
        "organic_certified": True,
        "unit_type": "за кг",
        "season": "Круглый год",
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Яйца куриные домашние (10 шт)",
        "description": "Яйца от кур свободного выгула с ярким желтком. Богаты витамином D и омега-3.",
        "price": 900.0,
        "original_price": None,
        "category": "Мясо и птица",
        "subcategory": "Яйца",
        "brand": "Жулдыз",
        "rating": 4.9,
        "review_count": 420,
        "image_url": "https://images.unsplash.com/photo-1582722872445-44dc5f7e3c8f?w=400",
        "stock": 200,
        "features": ["Свободный выгул", "Яркий желток", "Омега-3", "Без ГМО"],
        "is_on_sale": False,
        "harvest_date": date(2026, 4, 22),
        "farm_location": _farm_locations[2],
        "is_seasonal": False,
        "organic_certified": True,
        "unit_type": "10 штук",
        "season": "Круглый год",
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Баранина молодая (корейка)",
        "description": "Нежная корейка молодого барашка. Без запаха, мясо светлое, быстро готовится.",
        "price": 4500.0,
        "original_price": 5000.0,
        "category": "Мясо и птица",
        "subcategory": "Баранина",
        "brand": "Алтын Дала",
        "rating": 4.7,
        "review_count": 88,
        "image_url": "https://images.unsplash.com/photo-1529692236671-f1f6cf9683ba?w=400",
        "stock": 20,
        "features": ["Молодой барашек", "Без запаха", "Нежное мясо", "Охлаждённое"],
        "is_on_sale": True,
        "sale_percentage": 10,
        "harvest_date": date(2026, 4, 20),
        "farm_location": _farm_locations[0],
        "is_seasonal": False,
        "organic_certified": False,
        "unit_type": "за кг",
        "season": "Круглый год",
    },
    # ── Сезонные товары ───────────────────────────────────────────────────────
    {
        "id": str(uuid.uuid4()),
        "name": "Мёд цветочный весенний",
        "description": "Свежий весенний мёд с горных лугов Алматинской области. Собран в апреле 2026.",
        "price": 3500.0,
        "original_price": None,
        "category": "Сезонные товары",
        "subcategory": "Мёд",
        "brand": "Алтын Дала",
        "rating": 5.0,
        "review_count": 64,
        "image_url": "https://images.unsplash.com/photo-1587049352846-4a222e784d38?w=400",
        "stock": 25,
        "features": ["Натуральный", "Горный", "Весенний", "Без нагрева"],
        "is_on_sale": False,
        "harvest_date": date(2026, 4, 10),
        "farm_location": _farm_locations[0],
        "is_seasonal": True,
        "organic_certified": True,
        "unit_type": "за кг",
        "season": "Весна",
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Спаржа зелёная (пучок)",
        "description": "Нежная весенняя спаржа. Срезана сегодня утром, богата фолиевой кислотой.",
        "price": 1200.0,
        "original_price": None,
        "category": "Сезонные товары",
        "subcategory": "Зелень",
        "brand": "Алтын Дала",
        "rating": 4.6,
        "review_count": 33,
        "image_url": "https://images.unsplash.com/photo-1604977042946-1eecc30f269e?w=400",
        "stock": 40,
        "features": ["Сезонная", "Свежесрезанная", "Богата фолиевой кислотой", "Весенняя"],
        "is_on_sale": False,
        "harvest_date": date(2026, 4, 22),
        "farm_location": _farm_locations[0],
        "is_seasonal": True,
        "organic_certified": True,
        "unit_type": "за пучок",
        "season": "Весна",
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Редис ранний (пучок)",
        "description": "Хрустящий ранний редис. Первый урожай сезона, острый и сочный.",
        "price": 250.0,
        "original_price": None,
        "category": "Сезонные товары",
        "subcategory": "Зелень",
        "brand": "Алтын Дала",
        "rating": 4.4,
        "review_count": 41,
        "image_url": "https://images.unsplash.com/photo-1585670671903-e8242a404b88?w=400",
        "stock": 120,
        "features": ["Ранний урожай", "Хрустящий", "Сезонный", "Свежий"],
        "is_on_sale": False,
        "harvest_date": date(2026, 4, 22),
        "farm_location": _farm_locations[0],
        "is_seasonal": True,
        "organic_certified": False,
        "unit_type": "за пучок",
        "season": "Весна",
    },
]


# ---------------------------------------------------------------------------
# Seeding logic
# ---------------------------------------------------------------------------

def seed_farms(session):
    count = 0
    for data in FARMS:
        existing = session.get(Farm, data["id"])
        if existing:
            print(f"  [skip] Farm already exists: {data['name']}")
            continue
        farm = Farm(**data)
        session.add(farm)
        count += 1
        print(f"  [+] Farm: {data['name']}")
    return count


def seed_products(session):
    count = 0
    for data in PRODUCTS:
        existing = session.get(Product, data["id"])
        if existing:
            print(f"  [skip] Product already exists: {data['name']}")
            continue
        product = Product(**data)
        session.add(product)
        count += 1
        print(f"  [+] Product: {data['name']}")
    return count


def index_to_pinecone():
    print("\n--- Indexing products to Pinecone ---")
    vector_service = VectorService()
    try:
        vector_service.initialize()
    except Exception as e:
        print(f"  [!] Pinecone init failed: {e}")
        print("  [!] Skipping Pinecone indexing. Run scripts/index_all_products.py later.")
        return

    products = Product.query.filter_by(is_active=True).all()
    product_dicts = [
        {
            "id": p.id,
            "text": p.get_search_text(),
            "metadata": {
                "category": p.category,
                "subcategory": p.subcategory,
                "brand": p.brand,
                "price": p.price,
                "rating": p.rating,
                "in_stock": p.is_in_stock(),
            },
        }
        for p in products
    ]

    if product_dicts:
        vector_service.batch_upsert_products(product_dicts)
        print(f"  [+] Indexed {len(product_dicts)} products to Pinecone.")
    else:
        print("  [!] No products found to index.")


def main():
    print("=== Starting seed ===\n")
    app = create_app()
    with app.app_context():
        db.create_all()

        print("--- Seeding farms ---")
        farm_count = seed_farms(db.session)

        print("\n--- Seeding products ---")
        product_count = seed_products(db.session)

        db.session.commit()
        print(f"\n--- Committed: {farm_count} farm(s), {product_count} product(s) ---")

        index_to_pinecone()

    print("\n=== Seed complete ===")


if __name__ == "__main__":
    main()
