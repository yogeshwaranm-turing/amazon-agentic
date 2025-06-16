import json
import random
import datetime

supplier_name_prefixes = [
    "Prairie Lakes", "Green Valley", "Central Market", "Pioneer Farms",
    "Coastal Trade", "Mountain Peak", "Sunrise Foods", "Riverside Distributors",
    "Blue Horizon", "Silver Oak", "Harvest Goods", "Urban Essentials"
]
supplier_name_suffixes = [
    "Dairy", "Produce", "Wholesale", "Imports", "Exports",
    "Trading Co", "Logistics", "Supply", "Foods", "Merchants"
]

first_names = ["Emerson", "Avery", "Jordan", "Taylor", "Morgan", "Riley", "Casey", "Quinn", "Alex", "Jamie"]
last_names  = ["Hill", "Brooks", "Reed", "Turner", "Kelly", "Parker", "Santos", "Morgan", "Lee", "Rivera"]

street_names = [
    "Market St", "Main Ave", "Oak Drive", "Pine Street", "Maple Road",
    "Elm Boulevard", "Cedar Lane", "Walnut Way", "River Road", "Lakeview Court"
]
city_state_pairs = [
    ("Sioux Falls", "SD"), ("Austin", "TX"), ("Portland", "OR"),
    ("Madison", "WI"), ("Orlando", "FL"), ("Boise", "ID"),
    ("Savannah", "GA"), ("Phoenix", "AZ"), ("Boulder", "CO"),
    ("Jacksonville", "NC")
]

def generateProductName(pid):
    adjectives = ["Innovative", "Sleek", "Advanced", "Compact", "Wireless", "Smart", "Portable", "Eco-Friendly"]
    product_types = ["Gadget", "Device", "Widget", "Tool", "Accessory", "Instrument"]
    return f"{random.choice(adjectives)} {random.choice(product_types)}"

def generateProductDescription(pid):
    details = [
        "Crafted with premium materials and innovative design.",
        "Engineered for optimal performance and energy efficiency.",
        "A versatile solution that adapts to your dynamic lifestyle.",
        "Designed for durability with attention to modern aesthetics.",
        "Offers exceptional quality paired with outstanding functionality.",
        "A perfect blend of style, performance, and reliability.",
        "Exemplifies advanced engineering and user-friendly features.",
        "Innovative by nature, this product elevates your everyday experience.",
        "Merges technology with elegance for a superior result.",
        "Thoughtfully designed to exceed industry standards."
    ]
    return random.choice(details)

def generateProducts():
    products_path = '/Users/luongpham/tau-bench/tau_bench/envs/ecommerce/data/products.json'
    with open(products_path, 'r') as f:
        products = json.load(f)
    suppliers_path = '/Users/luongpham/tau-bench/tau_bench/envs/ecommerce/data/suppliers.json'
    with open(suppliers_path, 'r') as sf:
        suppliers = json.load(sf)
    supplier_ids = list(suppliers.keys())
    max_num = max(int(pid.replace("PRD", "")) for pid in products)
    new_products = {}
    for i in range(900):
        prod_num = max_num + i + 1
        pid = f"PRD{prod_num:04d}"
        new_products[pid] = {
            "product_id": pid,
            "name": generateProductName(pid),
            "description": generateProductDescription(pid),
            "supplier_id": random.choice(supplier_ids),
            "unit_price": round(random.uniform(10, 1000), 2)
        }
    products.update(new_products)
    with open(products_path, 'w') as f:
        json.dump(products, f, indent=2)
    return products

def generateSuppliers(count):
    """
    Generate `count` new supplier entries and append them to suppliers.json.
    Each supplier has sequential SUPXXX IDs, a placeholder name, contact_email, address, city, state, and zip_code.
    """
    suppliers_path = '/Users/luongpham/tau-bench/tau_bench/envs/ecommerce/data/suppliers.json'
    # Load existing suppliers
    with open(suppliers_path, 'r') as sf:
        suppliers = json.load(sf)
    # Determine highest existing supplier number
    max_num = max(int(sid.replace("SUP", "")) for sid in suppliers)
    # Generate new suppliers
    for i in range(count):
        sup_num = max_num + i + 1
        sid = f"SUP{sup_num:03d}"
        # Generate a diverse, dynamic supplier name
        prefix = random.choice(supplier_name_prefixes)
        suffix = random.choice(supplier_name_suffixes)
        name = f"{prefix} {suffix}"
        # Build email domain from the generated name
        email_domain = name.lower().replace(" ", "").replace(".", "") + ".com"
        # Generate a random street address
        street = random.choice(street_names)
        address = f"{random.randint(100, 9999)} {street}"
        # Pick a random city/state pair
        city, state = random.choice(city_state_pairs)
        # Generate a realistic 5-digit zip code
        zip_code = f"{random.randint(10000, 99999)}"
        suppliers[sid] = {
            "supplier_id": sid,
            "name": name,
            "contact_email": f"sales@{email_domain}",
            "address": address,
            "city": city,
            "state": state,
            "zip_code": zip_code
        }
    # Write back updated suppliers
    with open(suppliers_path, 'w') as sf:
        json.dump(suppliers, sf, indent=2)
    return suppliers

def generateUsers(count):
    users_path = '/Users/luongpham/tau-bench/tau_bench/envs/ecommerce/data/users.json'
    with open(users_path, 'r') as uf:
        users = json.load(uf)
    max_num = max(int(uid.replace("USR", "")) for uid in users) if users else 0
    for i in range(count):
        user_num = max_num + i + 1
        uid = f"USR{user_num:03d}"
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        email = f"{first_name.lower()}.{last_name.lower()}{user_num:03d}@example.com"
        address = f"{random.randint(100,9999)} {random.choice(street_names)}"
        city, state = random.choice(city_state_pairs)
        zip_code = f"{random.randint(10000,99999)}"
        users[uid] = {
            "user_id": uid,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "address": address,
            "city": city,
            "state": state,
            "zip_code": zip_code,
            "country": "USA"
        }
    with open(users_path, 'w') as uf:
        json.dump(users, uf, indent=2)
    return users


# --- New function: generateSalesOrders ---
def generateSalesOrders(count):
    """
    Generate `count` new sales order entries and append them to sales_orders.json.
    Each order has sequential SOXXXX IDs, a random user_id in USR001–USR966,
    a random order_date between 2022-01-01 and today, and a random status.
    """
    sales_orders_path = '/Users/luongpham/tau-bench/tau_bench/envs/ecommerce/data/sales_orders.json'
    # Load existing sales orders
    with open(sales_orders_path, 'r') as sf:
        sales_orders = json.load(sf)
    # Determine highest existing order number
    max_num = max(int(soid.replace("SO", "")) for soid in sales_orders) if sales_orders else 0
    statuses = ['Pending', 'Confirmed', 'Delivered', 'Shipped', 'Cancelled']
    # Date range for order_date
    start = datetime.date(2022, 1, 1)
    end = datetime.date.today()
    delta_days = (end - start).days
    # Generate new orders
    for i in range(count):
        order_num = max_num + i + 1
        soid = f"SO{order_num:04d}"
        user_id = f"USR{random.randint(1, 966):03d}"
        # Random order date
        order_date = start + datetime.timedelta(days=random.randint(0, delta_days))
        order_date_str = order_date.isoformat()
        status = random.choice(statuses)
        sales_orders[soid] = {
            "sales_order_id": soid,
            "user_id": user_id,
            "order_date": order_date_str,
            "status": status
        }
    # Write back updated sales orders
    with open(sales_orders_path, 'w') as sf:
        json.dump(sales_orders, sf, indent=2)
    return sales_orders

def generateSalesOrderItems(count):
    """
    Generate `count` new sales order item entries and append them to sales_order_items.json.
    Each item has sequential SOIXXXXX IDs, a random sales_order_id in SO0001–SO1060,
    a random product_id in PRD0001–PRD1980, and a random quantity 1–20.
    """
    soi_path = '/Users/luongpham/tau-bench/tau_bench/envs/ecommerce/data/sales_order_items.json'
    # Load existing items
    with open(soi_path, 'r') as sf:
        items = json.load(sf)
    # Determine highest existing item number
    max_num = max(int(soi.replace("SOI", "")) for soi in items) if items else 0
    for i in range(count):
        new_num = max_num + i + 1
        soi_id = f"SOI{new_num:05d}"
        # Random existing sales order
        so_num = random.randint(1, 1060)
        sales_order_id = f"SO{so_num:04d}"
        # Random existing product
        prod_num = random.randint(1, 1980)
        product_id = f"PRD{prod_num:04d}"
        quantity = random.randint(1, 20)
        items[soi_id] = {
            "so_item_id": soi_id,
            "sales_order_id": sales_order_id,
            "product_id": product_id,
            "quantity": quantity
        }
    # Write back updated items
    with open(soi_path, 'w') as sf:
        json.dump(items, sf, indent=2)
    return items

def generatePurchaseOrders(count):
    """
    Generate `count` new purchase order entries and append them to purchase_orders.json.
    Each order has sequential POXXXX IDs, a random supplier_id in SUP001–SUP401,
    and a random order_date between 2022-01-01 and today.
    """
    po_path = '/Users/luongpham/tau-bench/tau_bench/envs/ecommerce/data/purchase_orders.json'
    # Load existing purchase orders
    with open(po_path, 'r') as pf:
        purchase_orders = json.load(pf)
    # Determine highest existing PO number
    max_num = max(int(poid.replace("PO", "")) for poid in purchase_orders) if purchase_orders else 0
    # Date range for order_date
    start = datetime.date(2022, 1, 1)
    end = datetime.date.today()
    delta_days = (end - start).days
    for i in range(count):
        order_num = max_num + i + 1
        poid = f"PO{order_num:04d}"
        supplier_num = random.randint(1, 401)
        supplier_id = f"SUP{supplier_num:03d}"
        order_date = start + datetime.timedelta(days=random.randint(0, delta_days))
        order_date_str = order_date.isoformat()
        purchase_orders[poid] = {
            "purchase_order_id": poid,
            "supplier_id": supplier_id,
            "order_date": order_date_str
        }
    # Write back updated purchase orders
    with open(po_path, 'w') as pf:
        json.dump(purchase_orders, pf, indent=2)
    return purchase_orders


def generatePurchaseOrderItems(count):
    """
    Generate `count` new purchase order item entries and append them to purchase_order_items.json.
    Each item has sequential POIXXXXX IDs, a random purchase_order_id in PO0001–PO0915,
    a random product_id in PRD0001–PRD1980, a random quantity 1–500, and random unit_cost 1.00–100.00.
    """
    poi_path = '/Users/luongpham/tau-bench/tau_bench/envs/ecommerce/data/purchase_order_items.json'
    # Load existing items
    with open(poi_path, 'r') as pf:
        items = json.load(pf)
    # Determine highest existing item number
    max_num = max(int(poi.replace("POI", "")) for poi in items) if items else 0
    for i in range(count):
        new_num = max_num + i + 1
        poi_id = f"POI{new_num:05d}"
        # Random purchase order
        po_num = random.randint(1, 915)
        purchase_order_id = f"PO{po_num:04d}"
        # Random existing product
        prod_num = random.randint(1, 1980)
        product_id = f"PRD{prod_num:04d}"
        quantity = random.randint(1, 500)
        unit_cost = round(random.uniform(1, 100), 2)
        items[poi_id] = {
            "po_item_id": poi_id,
            "purchase_order_id": purchase_order_id,
            "product_id": product_id,
            "quantity": quantity,
            "unit_cost": unit_cost
        }
    # Write back updated items
    with open(poi_path, 'w') as pf:
        json.dump(items, pf, indent=2)
    return items

def main():
    # generateProducts()
    # generateSuppliers(300)
    # generateUsers(900)
    #generateSalesOrders(900)
    # generateSalesOrderItems(1500)
    # generatePurchaseOrders(900)
    generatePurchaseOrderItems(2000)

if __name__ == "__main__":
    main()