from connection_handler import ConnectionHandler
from load_config import load_config
from mysql_handler import MySQLHandler
import transformation as tr
import os
import polars as pl


if __name__ == "__main__":
    # Setup database
    config = load_config()
    con = MySQLHandler(config["LOCAL"])
    with open(os.path.join("MySQL", "bike_store.sql")) as f:
        queries = f.read()
    queries = queries.split(";")
    for query in queries:
        if query.strip() != "":
            query = query.replace("bike_store", config["LOCAL"]["DB"])
            con.execute(query)

    # Extract
    staffs = pl.read_csv(os.path.join("Data", "staffs.csv"))
    stores = pl.read_csv(os.path.join("Data", "stores.csv"))
    con = ConnectionHandler()
    products = con.get_products()
    brands = con.get_brands()
    categories = con.get_categories()
    customers = con.get_customers()
    orders = con.get_orders()
    stocks = con.get_stocks()
    order_items = con.get_order_items()
    #products = pl.read_csv(os.path.join("Data", "products.csv"))
    #brands = pl.read_csv(os.path.join("Data", "brands.csv"))
    #categories = pl.read_csv(os.path.join("Data", "categories.csv"))
    #customers = pl.read_csv(os.path.join("Data", "customers.csv"))
    #orders = pl.read_csv(os.path.join("Data", "orders.csv"))
    #stocks = pl.read_csv(os.path.join("Data", "stocks.csv"))
    #order_items = pl.read_csv(os.path.join("Data", "order_items.csv"))

    # Transform
    order_items = tr.remove_list_price_from_orderitems(order_items)
    order_items = tr.remove_item_id(order_items)
    products = tr.combine_brands_into_products(products=products, 
                                               brands=brands)
    products = tr.trim_product_names(products)
    stocks = tr.merge_duplicate_products(stocks, products)
    order_items = tr.remove_duplicate_products(order_items, products)
    product_categories = tr.make_product_categories(products)
    products = tr.drop_category_id_and_remove_duplicates(products)

    staffs = tr.make_managerid_int(staffs)
    staffs = tr.fix_manager_id(staffs)
    staffs = tr.remove_street_from_staffs(staffs)
    staffs = tr.rename_to_first_name(staffs)
    staffs = tr.make_id_column(staffs)
    orders = tr.remove_store_from_orders(orders)
    orders = tr.replace_name_with_id(orders, staffs)
    orders = tr.format_dates(orders)
    
    customers = tr.format_phone(customers)

    # Load
    con.write_to_local_database(products, "products")
    con.write_to_local_database(stores, "stores")
    con.write_to_local_database(staffs, "staffs")
    con.write_to_local_database(customers, "customers")
    con.write_to_local_database(orders, "orders")
    con.write_to_local_database(stocks, "stocks")
    con.write_to_local_database(categories, "categories")
    con.write_to_local_database(product_categories, "product_categories")
    con.write_to_local_database(order_items, "order_items")
    