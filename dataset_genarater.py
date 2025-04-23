import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

NUM_RECORDS = 1000
# Set the date range for 2023 and 2024 only
START_DATE = pd.Timestamp("2023-01-01")
END_DATE = pd.Timestamp("2024-12-31")
OUTPUT_FILE = "clean_indian_shopping_data.csv"

categories = {
    'Electronics': ['Smartphone', 'Laptop', 'Headphones', 'Smartwatch', 'Bluetooth Speaker'],
    'Fashion': ['T-Shirt', 'Jeans', 'Saree', 'Sneakers', 'Kurtis'],
    'Groceries': ['Milk', 'Fruits', 'Vegetables', 'Rice', 'Atta'],
    'Home Appliances': ['Refrigerator', 'Washing Machine', 'Microwave', 'Geyser', 'Fan'],
    'Beauty & Personal Care': ['Shampoo', 'Face Wash', 'Lipstick', 'Perfume', 'Moisturizer'],
    'Books & Stationery': ['Notebook', 'Pen', 'Fiction Novel', 'Exam Guide', 'Diary']
}

price_ranges = {
    'Smartphone': (7000, 90000),
    'Laptop': (25000, 120000),
    'Headphones': (500, 8000),
    'Smartwatch': (2000, 25000),
    'Bluetooth Speaker': (1000, 15000),
    'T-Shirt': (300, 3000),
    'Jeans': (800, 4000),
    'Saree': (700, 10000),
    'Sneakers': (1000, 8000),
    'Kurtis': (400, 4000),
    'Milk': (50, 120),
    'Fruits': (40, 400),
    'Vegetables': (30, 500),
    'Rice': (50, 1800),
    'Atta': (40, 1200),
    'Refrigerator': (12000, 60000),
    'Washing Machine': (10000, 50000),
    'Microwave': (3000, 20000),
    'Geyser': (3000, 25000),
    'Fan': (1000, 8000),
    'Shampoo': (80, 800),
    'Face Wash': (60, 600),
    'Lipstick': (120, 1200),
    'Perfume': (500, 8000),
    'Moisturizer': (100, 900),
    'Notebook': (20, 200),
    'Pen': (10, 150),
    'Fiction Novel': (100, 800),
    'Exam Guide': (200, 1200),
    'Diary': (50, 500),
}

payment_methods = ['Credit Card', 'Debit Card', 'UPI', 'Net Banking', 'Paytm', 'Cash on Delivery']
order_statuses = ['Delivered', 'Shipped', 'Processing', 'Returned', 'Cancelled']

fake = Faker('en_IN')
data = []

for i in range(NUM_RECORDS):
    category = random.choice(list(categories.keys()))
    product = random.choice(categories[category])
    price = round(random.uniform(*price_ranges[product]), 2)
    quantity = random.randint(1, 5)
    total_amount = round(price * quantity, 2)
    # Generate order_date within 2023-2024
    days_range = (END_DATE - START_DATE).days
    order_date = START_DATE + pd.Timedelta(days=random.randint(0, days_range))
    # Delivery date logic
    delivery_days = random.randint(1, 7) if random.random() > 0.2 else None
    delivery_date = (order_date + pd.Timedelta(days=delivery_days)) if delivery_days else pd.NaT
    if pd.notna(delivery_date) and delivery_date > END_DATE:
        delivery_date = END_DATE
    order_status = random.choices(order_statuses, weights=[60, 15, 10, 10, 5])[0]
    review_rating = random.randint(1, 5) if order_status == 'Delivered' and random.random() > 0.2 else None

    data.append({
        "Order_ID": f"AMZ-{random.randint(10000, 99999)}",
        "Customer_ID": f"CUST-{random.randint(1000, 9999)}",
        "Customer_Name": fake.name(),
        "Customer_Age": random.randint(18, 65),
        "Gender": random.choice(['M', 'F']),
        "City": fake.city(),
        "State": fake.state(),
        "Pin_Code": fake.postcode(),
        "Product_ID": f"PID-{random.randint(1000, 9999)}",
        "Product_Name": product,
        "Category": category,
        "Brand": fake.company(),
        "Price": price,
        "Quantity": quantity,
        "Total_Amount": total_amount,
        "Payment_Method": random.choice(payment_methods),
        "Order_Status": order_status,
        "Order_Date": order_date.date(),
        "Delivery_Date": delivery_date.date() if pd.notna(delivery_date) else "",
        "Review_Rating": review_rating
    })

df = pd.DataFrame(data)
df.to_csv(OUTPUT_FILE, index=False)
print(f"Dataset generated: {OUTPUT_FILE}")
