import os, sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))
import src.transformation as tr
import polars as pl

def should_remove_street():
    staffs = pl.DataFrame({"street": ""})
    staffs = tr.remove_street_from_staffs(staffs=staffs)
    try: assert staffs.equals(pl.DataFrame({}))
    except AssertionError:
        print("should_remove_street failure")
        print(staffs)
    else:
        print("should_remove_street success")

def should_fold_brands_into_products():
    products = pl.DataFrame({"product_id":"1", "brand_id":"1", "category_id":"1"})
    brands = pl.DataFrame({"brand_id":"1", "name": "Trek"})
    categories = pl.DataFrame({"category_id":"1"})
    products = tr.fold_brands_and_categories_into_products(products=products, 
                                                           brands=brands, 
                                                           categories=categories)
    try: assert products.equals(pl.DataFrame({"product_id":"1","name": "Trek"}))
    except AssertionError:
        print("should_fold_brands_into_products failure")
        print(products)
    else:
        print("should_fold_brands_into_products success")

def should_make_manager_id_7_into_8():
    staffs = pl.DataFrame({"manager_id":[7,1]})
    staffs = tr.fix_manager_id(staffs)
    try: assert staffs.equals(pl.DataFrame({"manager_id":[8,1]}))
    except AssertionError:
        print("should_make_manager_id_7_into_8 failure")
        print(staffs)
    else:
        print("should_make_manager_id_7_into_8 success")

def should_remove_brand():
    products = pl.DataFrame({"product_name":"Trek Super Bike -  2016/2017", "brand_name": "Trek"})
    products = tr.trim_product_names(products=products)
    try: assert products.equals(pl.DataFrame({"product_name":"Super Bike","brand_name": "Trek"}))
    except AssertionError:
        print("should_remove_brand failure")
        print(products)
    else:
        print("should_remove_brand success")

should_remove_street()
should_fold_brands_into_products()
should_make_manager_id_7_into_8()
should_remove_brand()