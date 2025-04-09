import polars as pl


# General cleanup

def format_null(dataframe: pl.DataFrame, column: str) -> pl.DataFrame:
    """Replace the NULL strings with actual null values."""
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
    """Make the manager id integer type."""
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

def combine_brands_into_products(products: pl.DataFrame, 
                                             brands: pl.DataFrame,
                                             ) -> pl.DataFrame:
    """Move the names of brands and categories into products to
    replace the id's.
    """
    products = products.join(brands, on="brand_id", how="inner")
    products = products.drop("brand_id")
    return products

def trim_product_names(products: pl.DataFrame) -> pl.DataFrame:
    """Remove the brand name and model year from the product name.

    Must be used after combining brands and categories with products.
    Strips quotation marks then removes the brand name in the brand 
    name column from the front of the string. Then removes any
    numbers and slashes from the end of the string.
    """
    products = products.with_columns(product_name=
        pl.col("product_name").str.strip_chars('"')
        .str.strip_prefix(pl.col("brand_name") + " ")
        .str.strip_chars_end("1234567890/")
        .str.strip_chars_end(" -"))
    return products

def make_product_categories(products: pl.DataFrame
                            ) -> pl.DataFrame:
    """Make category dataframe with product names and category names.

    Removes duplicate entries.
    """
    products = products.sort("product_id")
    products = products.unique(subset=["product_name", 
                                       "model_year"], 
                               keep="first")
    product_categories = products.select("product_id",
                                              "category_id")
    return product_categories

def drop_category_id_and_remove_duplicates(products: pl.DataFrame) -> pl.DataFrame:
    """Remove the category column and remove duplicates."""
    products = products.drop("category_id").sort("product_id")
    products = products.unique(subset=["product_name", 
                                       "model_year"], 
                               keep="first")
    return products


# Cleanup of stocks

def merge_duplicate_products(stocks: pl.DataFrame, 
                             products: pl.DataFrame,
                             ) -> pl.DataFrame:
    """Sum stocks of duplicate products.
    
    Must be used before removing duplicates in products.
    """
    joined = stocks.join(products, on="product_id")
    joined = joined.group_by(["product_name", "model_year", "store_name"]).agg(
        pl.col("quantity").sum(), pl.col("product_id").first())
    stocks = joined.select("product_id", "store_name", "quantity")
    return stocks


# Cleanup of orders

def remove_store_from_orders(orders: pl.DataFrame) -> pl.DataFrame:
    """Remove the column 'store'."""
    return orders.drop("store")

def __format_date(dataframe: pl.DataFrame, column) -> pl.DataFrame:
    """Change the format of column into date format."""
    dataframe = format_null(dataframe, column)
    dataframe = dataframe.with_columns(pl.col(column).str.to_date())
    return dataframe

def format_dates(orders: pl.DataFrame) -> pl.DataFrame:
    """Change format for the date columns in the orders table."""
    orders = __format_date(orders, "order_date")
    orders = __format_date(orders, "required_date")
    orders = __format_date(orders, "shipped_date")
    return orders

def replace_name_with_id(orders: pl.DataFrame, 
                         staffs: pl.DataFrame) -> pl.DataFrame:
    """Replace the name in orders with the corresponding staff id."""
    staffs = staffs.select(["staff_id", "first_name"])
    orders = orders.join(staffs, left_on="staff_name", 
                         right_on="first_name")
    orders = orders.drop("staff_name")
    return orders


# Cleanup of order_items

def remove_list_price_from_orderitems(order_items: pl.DataFrame,
                                      ) -> pl.DataFrame:
    """Remove the column 'list_price'."""
    return order_items.drop("list_price")

def remove_item_id(order_items: pl.DataFrame) -> pl.DataFrame:
    """Remove column 'item_id'."""
    return order_items.drop("item_id")

def remove_duplicate_products(order_items: pl.DataFrame, 
                              products: pl.DataFrame
                              ) -> pl.DataFrame:
    """Remove duplicate products and sum the quantities."""
    joined = order_items.join(products, on="product_id").sort("product_id")
    index = joined.group_by(["product_name", "model_year"]).agg(
        pl.col("product_id").agg_groups())
    joined.with_columns(pl.col("product_id").replace())
    joined = joined.group_by(["product_name", "model_year", "order_id"]).agg(
        pl.col("quantity").sum(), 
        pl.col("discount").first(),
        pl.col("product_id").first())
    order_items = joined.select("order_id", "product_id", "quantity", "discount")
    return order_items


# Cleanup of customers

def format_phone(customers: pl.DataFrame) -> pl.DataFrame:
    return format_null(customers, "phone")