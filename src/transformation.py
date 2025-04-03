import polars as pl

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

def fold_brands_and_categories_into_products(products: pl.DataFrame, 
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
    Must be used after folding brands and categories into products."""
    products = products.with_columns(product_name=
        pl.col("product_name").str.strip_prefix(
            pl.col("brand_name") + " ")
        .str.strip_chars_end("1234567890/")
        .str.strip_chars_end(" -"))
    return products

def remove_store_from_orders(orders: pl.DataFrame) -> pl.DataFrame:
    """Remove the column 'store'."""
    return orders.drop("store")

def does_list_price_match_product_price(order_items: pl.DataFrame,
                                        products: pl.DataFrame
                                        ) -> bool:
    """Check if list_price in order_items is redundant."""
    order_items = order_items.join(products, 
                                   on="product_id", 
                                   suffix="_products")
    does_it_match = order_items.select("list_price").equals(
        order_items.select("list_price_products"))
    return does_it_match

def remove_list_price_from_orderitems(order_items: pl.DataFrame
                                      ) -> pl.DataFrame:
    """Remove the column 'list_price' if it is redundant."""
    if does_list_price_match_product_price():
        pass
    else:
        print("""WARNING: Prices don't match in order_items and products. 
              Data may be lost""")
    return order_items.drop("list_price")