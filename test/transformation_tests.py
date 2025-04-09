import os, sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))
import src.transformation as tr
import polars as pl
import unittest

class TestTransformation(unittest.TestCase):

    def test_should_remove_street(self):
        staffs = pl.DataFrame({"street": ""})
        staffs = tr.remove_street_from_staffs(staffs=staffs)
        self.assertTrue(staffs.equals(pl.DataFrame({})))

    def test_should_fold_brands_into_products(self):
        products = pl.DataFrame({"product_id":"1", "brand_id":"1", "category_id":"1"})
        brands = pl.DataFrame({"brand_id":"1", "name": "Trek"})
        categories = pl.DataFrame({"category_id":"1"})
        products = tr.combine_into_products(products=products, 
                                                               brands=brands, 
                                                               categories=categories)
        self.assertTrue(products.equals(pl.DataFrame({"product_id":"1","name": "Trek"})))

    def test_should_make_manager_id_7_into_8(self):
        staffs = pl.DataFrame({"manager_id":[7,1]})
        staffs = tr.fix_manager_id(staffs)
        self.assertTrue(staffs.equals(pl.DataFrame({"manager_id":[8,1]})))

    def test_should_remove_brand(self):
        products = pl.DataFrame({"product_name":"Trek Super Bike -  2016/2017",
                                  "brand_name": "Trek"})
        products = tr.trim_product_names(products=products)
        self.assertTrue(products.equals(pl.DataFrame({"product_name":"Super Bike",
                                                      "brand_name": "Trek"})))

if __name__ == "__main__":
    unittest.main()