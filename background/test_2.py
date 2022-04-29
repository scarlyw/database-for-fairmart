from email.message import EmailMessage
import unittest
from dm_app_9 import app
import json

class TestLogin(unittest.TestCase):
    def setUp(self) -> None:
        app.testing = True
        self.client = app.test_client()
    
    def test_no_user(self):
        response = self.client.post("/login", data = json.dumps({"user_name" : "XXXX", "password" : "XXX"}))
        resp_json = response.data
        resp_dict = json.loads(resp_json)
        self.assertIn("result", resp_dict)
        result = resp_dict.get("result")
        self.assertEqual(result, "failed: user name does not exist")
    
    def test_wrong_password(self):
        response = self.client.post("/login", data = json.dumps({"user_name" : "yxd123", "password" : "XXX"}))
        resp_json = response.data
        resp_dict = json.loads(resp_json)
        self.assertIn("result", resp_dict)
        result = resp_dict.get("result")
        self.assertEqual(result, "failed")
        response = self.client.post("/login", data = json.dumps({"user_name" : "1800012428@pku.edu.cn", "password" : "XXX"}))
        resp_json = response.data
        resp_dict = json.loads(resp_json)
        self.assertIn("result", resp_dict)
        result = resp_dict.get("result")
        self.assertEqual(result, "failed")

    def test_right(self):
        response = self.client.post("/login", data = json.dumps({"user_name" : "yxd123", "password" : "202cb962ac59075b964b07152d234b70"}))
        resp_json = response.data
        resp_dict = json.loads(resp_json)
        self.assertIn("result", resp_dict)
        result = resp_dict.get("result")
        self.assertEqual(result, "success")
        response = self.client.post("/login", data = json.dumps({"user_name" : "1800012428@pku.edu.cn", "password" : "202cb962ac59075b964b07152d234b70"}))
        resp_json = response.data
        resp_dict = json.loads(resp_json)
        self.assertIn("result", resp_dict)
        result = resp_dict.get("result")
        self.assertEqual(result, "success")
 

# class TestRegister(unittest.TestCase):
#     def setUp(self) -> None:
#         app.testing = True
#         self.client = app.test_client()

#     def test_repeat_name(self):
#         response = self.client.post("/register", data = json.dumps({"user_name" : "zrt", "password" : "XXX"}))
#         resp_json = response.data
#         resp_dict = json.loads(resp_json)
#         self.assertIn("result", resp_dict)
#         result = resp_dict.get("result")
#         self.assertEqual(result, "failed")
    
#     def test_right(self):
#         response = self.client.post("/register", data = json.dumps({"user_name" : "cczyyds", "password" : "123456"}))
#         resp_json = response.data
#         resp_dict = json.loads(resp_json)
#         self.assertIn("result", resp_dict)
#         result = resp_dict.get("result")
#         self.assertEqual(result, "success")


# class TestPostProduct(unittest.TestCase):
#     def setUp(self) -> None:
#         app.testing = True
#         self.client = app.test_client()
    
#     def test_post_product(self):
#         response = self.client.post("/userpostproduct", data = json.dumps({"product_name" : "yuweil", "price" : 70.1, "source_id" : 3}))
#         resp_json = response.data
#         resp_dict = json.loads(resp_json)
#         self.assertIn("product_name", resp_dict)
#         product_name = resp_dict.get("product_name")
#         self.assertEqual(product_name, "yuweil")
#         self.assertIn("price", resp_dict)
#         price = resp_dict.get("price")
#         self.assertEqual(price, 70.1)
#         self.assertIn("availability_state", resp_dict)
#         availability_state = resp_dict.get("availability_state")
#         self.assertEqual(availability_state, 1)

class TestPostWanted(unittest.TestCase):
    def setUp(self) -> None:
        app.testing = True
        self.client = app.test_client()
    
    def test_post_wanted(self):
        response = self.client.post("/userpostwanted", data = json.dumps({"wanted_name" : "yuweil", "price" : 70.1, "source_id" : 3, "category_value" : 1, "description" : "一只喵"}))
        resp_json = response.data
        resp_dict = json.loads(resp_json)
        self.assertIn("wanted_name", resp_dict)
        wanted_name = resp_dict.get("wanted_name")
        self.assertEqual(wanted_name, "yuweil")
        self.assertIn("price", resp_dict)
        price = resp_dict.get("price")
        self.assertEqual(price, 70.1)
        self.assertIn("description", resp_dict)
        description = resp_dict.get("description")
        self.assertEqual(description, "一只喵")

# class TestProductInfo(unittest.TestCase):
#     def setUp(self) -> None:
#         app.testing = True
#         self.client = app.test_client()
    
#     def test_product_info(self):
#         response = self.client.post("/productinfo", data = json.dumps({"product_id" : 41}))
#         resp_json = response.data
#         resp_dict = json.loads(resp_json)
#         self.assertIn("product_name", resp_dict)
#         product_name = resp_dict.get("product_name")
#         self.assertEqual(product_name, "赛博朋克")
#         self.assertIn("price", resp_dict)
#         price = resp_dict.get("price")
#         self.assertEqual(price, 299)

# class TestChangeWechat(unittest.TestCase):
#     def setUp(self) -> None:
#         app.testing = True
#         self.client = app.test_client()
    
#     def test_product_info(self):
#         response = self.client.post("/changeWeChat", data = json.dumps({"user_id" : 6, "WeChat_id" : "lcyyds"}))
#         resp_json = response.data
#         resp_dict = json.loads(resp_json)
#         self.assertIn("user_name", resp_dict)
#         user_name = resp_dict.get("user_name")
#         self.assertEqual(user_name, "lc_1228")
#         self.assertIn("WeChat_id", resp_dict)
#         WeChat_id = resp_dict.get("WeChat_id")
#         self.assertEqual(WeChat_id, "lcyyds")

# class TestBuyProduct(unittest.TestCase):
#     def setUp(self) -> None:
#         app.testing = True
#         self.client = app.test_client()
    
#     def test_buy_sold(self):
#         response = self.client.post("/buyproduct", data = json.dumps({"sold_product_id" : 12, "buyer_id" : 4, "time" : "2021-12-16 1:19"}))
#         resp_json = response.data
#         resp_dict = json.loads(resp_json)
#         self.assertIn("result", resp_dict)
#         result = resp_dict.get("result")
#         self.assertEqual(result, "failed")
#         self.assertIn("availability_state", resp_dict)
#         availability_state = resp_dict.get("availability_state")
#         self.assertEqual(availability_state, 2)
        
    
#     def test_buy_product(self):
#         response = self.client.post("/buyproduct", data = json.dumps({"sold_product_id" : 16, "buyer_id" : 5, "time" : "2021-12-16 1:25"}))
#         resp_json = response.data
#         resp_dict = json.loads(resp_json)
#         self.assertIn("result", resp_dict)
#         result = resp_dict.get("result")
#         self.assertEqual(result, "success")
#         self.assertIn("seller_wechat", resp_dict)
#         seller_wechat = resp_dict.get("seller_wechat")
#         self.assertEqual(seller_wechat, "userx_wechat")

class TestDeleteProduct(unittest.TestCase):
    def setUp(self) -> None:
        app.testing = True
        self.client = app.test_client()
    
    def test_delete_product(self):
        response = self.client.post("/deleteproduct", data = json.dumps({"deleteproduct_id" : 41}))
        resp_json = response.data
        resp_dict = json.loads(resp_json)
        self.assertIn("source_id", resp_dict)
        source_id = resp_dict.get("source_id")
        self.assertEqual(source_id, 0)

class TestWantedInfo(unittest.TestCase):
    def setUp(self) -> None:
        app.testing = True
        self.client = app.test_client()
    
    def test_wanted_info(self):
        response = self.client.post("/wantedinfo", data = json.dumps({"wanted_id" : 8}))
        resp_json = response.data
        resp_dict = json.loads(resp_json)
        self.assertIn("seller_wechat", resp_dict)
        seller_wechat = resp_dict.get("seller_wechat")
        self.assertEqual(seller_wechat, "jason")
        self.assertIn("email", resp_dict)
        email = resp_dict.get("email")
        self.assertEqual(email, "1800012428@pku.edu.cn")

class TestAddFavorite(unittest.TestCase):
    def setUp(self) -> None:
        app.testing = True
        self.client = app.test_client()
    
    def test_add_favorite(self):
        response = self.client.post("/addfavorite", data = json.dumps({"buyer_id" : 14, "product_id" : 42}))
        resp_json = response.data
        resp_dict = json.loads(resp_json)
        self.assertIn("state", resp_dict)
        state = resp_dict.get("state")
        self.assertEqual(state, 10)
        self.assertIn("product_name", resp_dict)
        product_name = resp_dict.get("product_name")
        self.assertEqual(product_name, "山村老师终极版")

if __name__ == '__main__':
    unittest.main()  # 进行测试


