import polars as pl

# General

def format_null(dataframe: pl.DataFrame, column: str) -> pl.DataFrame:
    dataframe = dataframe.with_columns(
        pl.when(pl.col(column) == "NULL")
        .then(None)
        .otherwise(pl.col(column))
        .alias(column))
    return dataframe

# Cleanup of staffs

def remove_street_from_staffs(staffs: pl.DataFrame) -> pl.DataFrame:
    """Remove the 'street' column."""
    return staffs.drop("street")

def fix_manager_id(staffs: pl.DataFrame) -> pl.DataFrame:
    """Replace the manager id 7 with 8 to fix the assumed mistake"""
    staffs = staffs.with_columns(
        manager_id=pl.when(
            pl.col("manager_id")==7)
            .then(pl.lit(8))
            .otherwise(pl.col("manager_id"))
            )
    return staffs

def make_managerid_int(staffs: pl.DataFrame) -> pl.DataFrame:
    """Make the manager id integer type and 
    null values the proper type.
    """
    staffs = format_null(staffs, "manager_id")
    staffs = staffs.with_columns(
        manager_id = pl.col("manager_id").cast(pl.Int64))
    return staffs

def rename_to_first_name(staffs: pl.DataFrame) -> pl.DataFrame:
    """Rename the column 'name' to 'first_name'"""
    staffs = staffs.with_columns(first_name = pl.col("name"))
    return staffs.drop("name")

def make_id_column(staffs: pl.DataFrame) -> pl.DataFrame:
    """Make an id column for staffs."""
    return staffs.with_row_index("staff_id", 1)

# Cleanup of products

def combine_into_products(products: pl.DataFrame, 
                                             brands: pl.DataFrame, 
                                             categories: pl.DataFrame
                                             ) -> pl.DataFrame:
    """Move the names of brands and categories into products to
    replace the id's.
    """
    products = products.join(brands, on="brand_id", how="inner")
    products = products.join(categories, on="category_id", how="inner")
    products = products.drop("brand_id")
    products = products.drop("category_id")
    return products

def trim_product_names(products: pl.DataFrame) -> pl.DataFrame:
    """Removes the brand name and model year from the product name.
    Must be used after folding brands and categories into products.
    """
    products = products.with_columns(product_name=
        pl.col("product_name").str.strip_prefix(
            pl.col("brand_name") + " ")
        .str.strip_chars_end("1234567890/")
        .str.strip_chars_end(" -"))
    return products

def format_list_price(products: pl.DataFrame) -> pl.DataFrame:
    """Makes the prices have the correct decimal values"""
    products = products.with_columns(
        pl.when((pl.col("list_price")*100).ceil()%100 == 0)
        .then(pl.col("list_price").cast(pl.Int64))
        .otherwise((pl.col("list_price")*100).ceil()))
    return products

# Cleanup of orders

def remove_store_from_orders(orders: pl.DataFrame) -> pl.DataFrame:
    """Remove the column 'store'."""
    return orders.drop("store")

def __format_date(dataframe: pl.DataFrame, column) -> pl.DataFrame:
    dataframe = format_null(dataframe, column)
    dataframe = dataframe.with_columns(pl.col(column).str.to_date())
    return dataframe

def format_dates(orders: pl.DataFrame) -> pl.DataFrame:
    orders = __format_date(orders, "order_date")
    orders = __format_date(orders, "required_date")
    orders = __format_date(orders, "shipped_date")
    return orders

def replace_name_with_id(orders: pl.DataFrame, staffs: pl.DataFrame) -> pl.DataFrame:
    """Replace the name in orders with the corresponding staff id."""
    staffs = staffs.select(["staff_id", "first_name"])
    orders = orders.join(staffs, left_on="staff_name", right_on="first_name")
    orders = orders.drop("staff_name")
    return orders

# Cleanup of order_items

def does_list_price_match_product_price(order_items: pl.DataFrame,
                                        products: pl.DataFrame
                                        ) -> bool:
    """Check if list_price in order_items is redundant."""
    order_items = order_items.join(products, 
                                   on="product_id", 
                                   suffix="_products")
    does_it_match = order_items.select((pl.col("list_price").replace(".", ""))
                                       ).equals(
        order_items.select((pl.col("list_price_products").replace(".", ""))))
    return does_it_match

def remove_list_price_from_orderitems(order_items: pl.DataFrame,
                                      products: pl.DataFrame
                                      ) -> pl.DataFrame:
    """Remove the column 'list_price' if it is redundant."""
    if does_list_price_match_product_price(order_items, products):
        pass
    else:
        print("""WARNING: Prices don't match in order_items and products. 
              Data may be lost""")
    return order_items.drop("list_price")



# Cleanup of customers

def format_phone(customers: pl.DataFrame) -> pl.DataFrame:
    return format_null(customers, "phone")