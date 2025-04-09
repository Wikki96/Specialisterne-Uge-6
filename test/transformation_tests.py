import os, sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))
import src.transformation as tr
import polars as pl
import polars.testing as pltest
import unittest

class TestTransformation(unittest.TestCase):

    def test_should_remove_street(self):
        staffs = pl.DataFrame({"street": ""})
        staffs = tr.remove_street_from_staffs(staffs=staffs)
        self.assertTrue(staffs.equals(pl.DataFrame({})))

    def test_should_combine_brands_into_products(self):
        products = pl.DataFrame({"product_id":"1", "brand_id":"1"})
        brands = pl.DataFrame({"brand_id":"1", "name": "Trek"})
        products = tr.combine_brands_into_products(products=products, 
                                                   brands=brands, )
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
        
    def test_make_product_categories_should_remove_duplicates(self):
        products = pl.DataFrame([{"product_name": "bike",
                                  "category_id": 1,
                                  "model_year": 0},
                                  {"product_name": "bike",
                                  "category_id": 1,
                                  "model_year": 0},])
        dummy = pl.DataFrame({"product_name": "bike",
                              "category_id": 1})
        categories = tr.make_product_categories(products)
        pltest.assert_frame_equal(categories, dummy)
        self.assertTrue(categories.equals(dummy))

    def test_merge_duplicate_products(self):
        stocks = pl.DataFrame([{"product_id": 1,
                                "store_name" : "store1",
                                "quantity": 2},
                                {"product_id": 2,
                                "store_name" : "store1",
                                "quantity": 3}])
        products = pl.DataFrame([{"product_id": 1,
                                  "product_name": "bike",
                                  "model_year": 0},
                                  {"product_id": 2,
                                  "product_name": "bike",
                                  "model_year": 0}])
        stocks = tr.merge_duplicate_products(stocks, products)
        dummy = pl.DataFrame({"product_id": 1,
                              "store_name" : "store1",
                              "quantity": 5})
        dummy = tr.merge_duplicate_products(stocks, products)
        self.assertTrue(stocks.equals(dummy))

if __name__ == "__main__":
    #test = TestTransformation("test_merge_duplicate_products")
    #test.debug()
    unittest.main()