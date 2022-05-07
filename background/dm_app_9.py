from datetime import datetime
import os.path
from flask import Flask
from flask import Flask, make_response
from flask import Response
from flask import stream_with_context
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from flask import request
import json

from numpy import product
from init import db
from dm_database_3 import User, Product, History, Wanted, Correlation, Category, Favorites
from sqlalchemy import and_, or_
import base64
import os
from flask import Response
from flask import stream_with_context
import smtplib
from email.mime.text import MIMEText
from email.header import Header

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess'  # 一个字符串，密码。也可以是其他如加密过的

# connect with the mysql database
# The default database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/test_0'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(app)

# to_dict
# transform info into python dict
# forbidden to take null inputs
def to_dict(self):
    return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}

# take_price
# get the desired value
def take_price(x):
    return x.price


# take_category
# get the category number
def take_category(x):
    return x.category_id

# take_category
# get the category number
def take_id(x):
    return x.user_id


# user_post_product
# post: post a product
@app.route('/user_post_product', methods=['GET', 'POST', 'OPTIONS'])
def user_post_product():
    print("enter_user_post_product")
    info = json.loads(request.get_data())
    print(info)
    # directly return
    if request.method == 'GET':
        return
    # post a new product
    elif request.method == 'POST':
        # photo_picture_string = info["photo"]
        # basedir = os.path.abspath(os.path.dirname(__file__))
        # print(basedir)
        # path_photo_picture_folder = basedir + "\static\img\\"
        # photo_picture_name = info["clock"] + "-" + str(info["source_id"]) + ".png"
        # photo_picture_name = photo_picture_name.replace(":", "-")
        # print(photo_picture_name)
        # path_photo_picture_save = path_photo_picture_folder + photo_picture_name
        # print(path_photo_picture_save)

        # with open(path_photo_picture_save, 'w') as f:
        #     f.write(photo_picture_string)

        # url = '\static\img\\' + photo_picture_name
        url = '\static\img\\2022-4-2919-516-10.png'
        product_new = Product(category_id = info["category_id"],
                              user_id = info["user_id"], 
                              product_name = info["product_name"],
                              price = info["price"],
                              photo_path = url,
                              state = True,
                              put_timestamp = datetime.now(), 
                              product_description = info["product_description"])
        db.session.add(product_new)
        db.session.commit()
        dict1 = to_dict(product_new)
        db.session.close()
        res = make_response(json.dumps(dict1))
        res.headers["Access-Control-Allow-Origin"] = '*'
        return res

    # undefined behavior
    elif request.method == 'OPTIONS':
        print("product options error!")
        return


# user_post_wanted
# post: post a wanted
# need check: photo functions added
# no use for this function
@app.route('/user_post_wanted', methods=['GET', 'POST', 'OPTIONS'])
def user_post_wanted():
    info = json.loads(request.get_data())
    # directly return
    if request.method == 'GET':
        return
    # post a new product
    elif request.method == 'POST':
        wanted_new = Wanted(wanted_name=info["wanted_name"],
                            category_value=info["category_value"],
                            price=info["price"],
                            description=info["description"],
                            availability_state=1,
                            source_id=info["source_id"])
        db.session.add(wanted_new)
        db.session.commit()
        dict1 = to_dict(wanted_new)
        db.session.close()
        res = make_response(json.dumps(dict1))
        res.headers["Access-Control-Allow-Origin"] = '*'
        return res

    # undefined behavior
    elif request.method == 'OPTIONS':
        print("wanted options error!")
        return

# user_search_products
# post: show all products that have something in search
@app.route('/user_search_products', methods=['GET', 'POST', 'OPTIONS'])
def user_search_products():
    info = json.loads(request.get_data())
    # directly return
    print(info)
    if request.method == 'GET':
        return
    # search the posted items from a specific user
    elif request.method == 'POST':
        if info:
            # no category requirements
            if info["strategy_0"] == 0:
                search_result_cnt = Product.query.filter(
                    and_(Product.product_name.like("%" + info["key"] + "%"),
                         Product.state == True)).count()
                # failed to match any object
                if search_result_cnt == 0:
                    return_dict = []
                    res = make_response(json.dumps(return_dict))
                    res.headers["Access-Control-Allow-Origin"] = '*'
                    return res
                else:
                    search_result = Product.query.filter(
                        and_(Product.product_name.like("%" + info["key"] + "%"),
                         Product.state == True)).all()

            # have category requirements
            else:
                search_result_cnt = Product.query.filter(and_(Product.category_id == info["category_id"],
                                                         and_(Product.product_name.like("%" + info["key"] + "%"),
                                                              Product.state == True))).count()
                # failed to match any object
                if search_result_cnt == 0:
                    return_dict = []
                    res = make_response(json.dumps(return_dict))
                    res.headers["Access-Control-Allow-Origin"] = '*'
                    return res
                else:
                    search_result = Product.query.filter(and_(Product.category_id == info["category_id"],
                                                         and_(Product.product_name.like("%" + info["key"] + "%"),
                                                              Product.state == True))).all()
        else:
            search_result = Product.query.filter(Product.state == True).all()

        # only want one category
        # strategy_1: different strategies of presenting products
        # automatically present the product by id
        print("get_strategy")
        if info["strategy_1"] == 0:
            search_result_1 = search_result

        # sorted by price
        elif info["strategy_1"] == 1:
            search_result_1 = search_result
            search_result_1.sort(key = take_price)

        # sorted by category
        elif info["strategy_1"] == 2:
            search_result_1 = search_result
            search_result_1.sort(key = take_category)

        elif info["strategy_1"] == 3:
            search_result_1 = search_result
            search_result_1.sort(key = take_id)

        # change the type of list
        for i in range(len(search_result_1)):
            item_original = search_result_1[i]
            item_modify = to_dict(item_original)
            # basedir = os.path.abspath(os.path.dirname(__file__))
            # if item_modify["photo_path"]:
            #     path = item_modify["photo_path"]
            # else:
            # path = "\static\img\\2022-4-2919-516-10.png"       
            # path_photo_picture_save = basedir + path
            # # print(basedir)
            # # print(path_photo_picture_save)
            # with open(path_photo_picture_save, 'r') as f:
            #     photo = f.read()
            # item_modify["photo"] = photo
            search_result_1[i] = item_modify

        # print(search_result_1)
        # search_result_1["state"] = "success"
        res = make_response(json.dumps(search_result_1))
        res.headers["Access-Control-Allow-Origin"] = '*'
        return res

        # undefined behavior
    if request.method == 'OPTIONS':
        print("product options error!")
        return





# user_all_products
# post: show all products that have been posted by one specific user
@app.route('/user_all_products', methods = ['GET', 'POST', 'OPTIONS'])
def user_all_products():
    info = json.loads(request.get_data())
    # directly return
    if request.method == 'GET':
        return
    # search the posted items from a specific user
    elif request.method == 'POST':
        # strategy_first = 0, all products
        if (info["user_id"] == 0):
            return 
        if info["strategy_0"] == 0:
            search_result = Product.query.filter(Product.user_id == info["user_id"]).all()
        # only want one category
        else :           
            search_result = Product.query.filter(and_(Product.user_id == info["user_id"],
                                                          Product.category_id == info["category_id"])).all()

        # different sorting strategies
        # automatically present the product by id
        if info["strategy_1"] == 0:
            search_result_1 = search_result

        # sorted by price
        elif info["strategy_1"] == 1:
            search_result_1 = search_result
            search_result_1.sort(key = take_price)

        # sorted by category
        elif info["strategy_1"] == 2:
            search_result_1 = search_result
            search_result_1.sort(key = take_category)

        # change the type of list
        for i in range(len(search_result_1)):
            item_original = search_result_1[i]
            item_modify = to_dict(item_original)
            # basedir = os.path.abspath(os.path.dirname(__file__))
            # # print(basedir)
            # # if item_modify["photo_path"]:
            # #     path = item_modify["photo_path"]
            # # else:
            # path = "\static\img\\2022-4-2919-516-10.png"       
            # path_photo_picture_save = basedir + path
            # with open(path_photo_picture_save, 'r') as f:
            #     photo = f.read()
            # item_modify["photo"] = photo
            search_result_1[i] = item_modify

        res = make_response(json.dumps(search_result_1))
        res.headers["Access-Control-Allow-Origin"] = '*'
        print(res)
        return res

    # undefined behavior
    elif request.method == 'OPTIONS':
        print("product options error!")
        return


# user_all_wanted
# post: show all wanted that have been posted by one specific user
# no use for this function
@app.route('/userallwanted', methods=['GET', 'POST', 'OPTIONS'])
def user_all_wanted():
    info = json.loads(request.get_data())
    # directly return
    if request.method == 'GET':
        return
    # search the posted items from a specific user
    elif request.method == 'POST':
        # strategy_first = 0, all products
        if info["strategy_0"] == 0:
            if info["source_id"] != 0:
                search_result = Wanted.query.filter(Wanted.source_id == info["source_id"]).all()
            else:
                search_result = Wanted.query.filter(Wanted.source_id != 0).all()

        # only want one category
        elif info["strategy_0"] == 1:
            if info["source_id"] != 0:
                search_result = Wanted.query.filter(and_(Wanted.source_id == info["source_id"],
                                                         Wanted.category_value == info["category_value"])).all()
            else:
                search_result = Wanted.uery.filter(Wanted.category_value == info["category_value"]).all()

        # different sorting strategies
        # automatically present the product by id
        if info["strategy_1"] == 0:
            search_result_1 = search_result

        # sorted by price
        elif info["strategy_1"] == 1:
            search_result_1 = search_result
            search_result_1.sort(key=take_price)
            # print(search_result_1)

        # sorted by category
        elif info["strategy_1"] == 2:
            search_result_1 = search_result
            search_result_1.sort(key=take_category)

        # change the type of list
        for i in range(len(search_result_1)):
            item_original = search_result_1[i]
            item_modify = to_dict(item_original)
            search_result_1[i] = item_modify

        res = make_response(json.dumps(search_result_1))
        res.headers["Access-Control-Allow-Origin"] = '*'
        return res

    # undefined behavior
    elif request.method == 'OPTIONS':
        print("product options error!")
        return


# user_product_search
# post: search one specific posted items
# implemented by lexie, 2021.11.24
# no use for this function
@app.route('/userproductsearch', methods=['GET', 'POST', 'OPTIONS'])
def user_product_search():
    info = json.loads(request.get_data())
    if request.method == 'GET':
        return

    # search the posted items from a specific user
    elif request.method == 'POST':
        dict1 = to_dict(Product.query.first())
        print(dict1)
        # search product based on name and source id
        dict_result = to_dict(Product.query.filter(Product.product_name.in_(
            Product.query(Product.product_name)).filter(Product.source_id == info["source_id"])))

        res = make_response(json.dumps(dict_result))
        res.headers["Access-Control-Allow-Origin"] = '*'
        return res

    # undefined behavior
    elif request.method == 'OPTIONS':
        print("product options error!")
        return


# user_modify_product
# post: modify the target product according to the latest info
# implemented by lexie, 2021.11.23
# never been checked!
# no use for this function
@app.route('/usermodifyproduct', methods=['GET', 'POST', 'OPTIONS'])
def user_modify_product():
    info = json.loads(request.get_data())
    # directly return
    if request.method == 'GET':
        return

    # search the posted items from a specific user
    elif request.method == 'POST':
        dict1 = to_dict(Product.query.first())
        # search the target product based on the id
        target_product = Product.query.filter(and_(Product.product_id == info["product_id"],
                                                   Product.source_id == info["source_id"])).first()
        # modification
        target_product.product_name = info["product_name"]
        target_product.category_value = info["category_value"]
        target_product.price = info["price"]
        target_product.photo = info["photo"]
        target_product.description = info["description"]

        # a successful modification
        response_dict = to_dict(target_product)
        response_dict["result"] = "success"
        res = make_response(json.dumps(response_dict))
        res.headers["Access-Control-Allow-Origin"] = '*'
        return res

    # undefined behavior
    elif request.method == 'OPTIONS':
        print("product options error!")
        return


# delete_product
# post: delete the target product
@app.route('/delete_product', methods=['GET', 'POST', 'OPTIONS'])
def delete_product():
    info = json.loads(request.get_data())
    if request.method == 'GET':
        print("delete product get error")
        return

    elif request.method == 'POST':
        product_cnt = db.session.query(Product).filter(Product.product_id == info["product_id"]).count()
        if product_cnt == 0:
            user_dict = {}
            user_dict["state"] = False
            user_dict["result"] = "wrong id for product"
            res = make_response(json.dumps(user_dict))
            res.headers["Access-Control-Allow-Origin"] = '*'
            return res
        
        product_x = db.session.query(Product).filter(Product.product_id == info["product_id"]).first()
        # product_x.source_id = 0
        print("change successful")
        db.session.delete(product_x)
        db.session.commit()
        db.session.close()
        user_dict = {}
        user_dict["state"] = True
        user_dict["result"] = "delete successfully"
        res = make_response(json.dumps(user_dict))
        res.headers["Access-Control-Allow-Origin"] = '*'
        return res

    # undefined behavior
    elif request.method == 'OPTIONS':
        print("delete product options error!")
        return


# plain_search
# post: search the desired product by name
# not user-specific
# implemented by lexie, 2021.11.24
# no use for this function
@app.route('/plainsearch', methods=['GET', 'POST', 'OPTIONS'])
def plain_search():
    info = json.loads(request.get_data())
    # directly return
    if request.method == 'GET':
        return

    # search the posted items from a specific user
    elif request.method == 'POST':
        # all categories
        if info["strategy_0"] == 0:
            search_result = Product.query.filter(Product.product_name.in_([info["product_name"]])).all()

        # only want one category
        elif info["strategy_0"] == 1:
            search_result = Product.query.filter(and_(Product.product_name.in_([info["product_name"]]),
                                                      Product.category_value == info["category_value"])).all()

        # automatically present the product by id
        if info["strategy_1"] == 0:
            search_result_1 = search_result

        # sorted by price
        elif info["strategy_1"] == 1:
            search_result_1 = search_result
            search_result_1.sort(key=take_price)

        # sorted by category
        elif info["strategy_1"] == 2:
            search_result_1 = search_result
            search_result_1.sort(key=take_category)

        # change the type of list
        for i in range(len(search_result_1)):
            item_original = search_result_1[i]
            item_modify = to_dict(item_original)
            search_result_1[i] = item_modify

        res = make_response(json.dumps(search_result_1))
        res.headers["Access-Control-Allow-Origin"] = '*'
        return res

    # undefined behavior
    elif request.method == 'OPTIONS':
        print("product options error!")
        return


# wanted_info
# wanted: show the details of the product
# consult Cai for further improvements
# no use for this function
@app.route('/wantedinfo', methods=['GET', 'POST', 'OPTIONS'])
def wanted_info():
    info = json.loads(request.get_data())
    print("enter_wanted_info")
    print(info)

    # directly return
    if request.method == 'GET':
        return

    # search the posted items from a specific user
    elif request.method == 'POST':
        # dict1 = to_dict(Product.query.first())
        # search products based on the posted id
        # the result is a list
        # notice: use first as the search condition
        wanted_x = (Wanted.query.filter(Wanted.wanted_id == info["wanted_id"])).first()
        dict_result = to_dict(wanted_x)
        user_x = User.query.filter(User.id == wanted_x.source_id).first()

        # response to the front
        dict_result["seller_wechat"] = user_x.WeChat_id
        dict_result["email"] = user_x.email
        dict_result["result"] = "success"
        res = make_response(json.dumps(dict_result))
        res.headers["Access-Control-Allow-Origin"] = '*'
        return res

    # undefined behavior
    elif request.method == 'OPTIONS':
        print("product options error!")
        return

# product_info
# post: show the details of the product
@app.route('/product_info', methods=['GET', 'POST', 'OPTIONS'])
def product_info():
    info = json.loads(request.get_data())

    # directly return
    if request.method == 'GET':
        return

    # search the posted items from a specific user
    elif request.method == 'POST':
        # dict1 = to_dict(Product.query.first())
        # search products based on the posted id
        # the result is a list
        # notice: use first as the search condition
        product_cnt = Product.query.filter(Product.product_id == info["product_id"]).count()
        if (product_cnt == 0):
            user_dict = {}
            user_dict["state"] = False
            user_dict["result"] = "Wrong product id"
            res = make_response(json.dumps(user_dict))
            res.headers["Access-Control-Allow-Origin"] = '*'
            return res
        
        dict_result = to_dict((Product.query.filter(Product.product_id == info["product_id"])).first())
        basedir = os.path.abspath(os.path.dirname(__file__))
        # print(basedir)
        # path_photo_picture_folder = basedir + "/static/img/"
        # photo_picture_name = "2022-4-2919-516-10.png"
        print(dict_result)

       
        path = "\static\img\\2022-4-2919-516-10.png" 

        path_photo_picture_save = basedir + path
        # print(path_photo_picture_save)

        with open(path_photo_picture_save, 'r') as f:
            photo = f.read()
        
        dict_result["photo"] = photo
        print(type(photo))
        dict_result["result"] = "success"
        # print(dict_result)
        res = make_response(json.dumps(dict_result))
        res.headers["Access-Control-Allow-Origin"] = '*'
        return res

    # undefined behavior
    elif request.method == 'OPTIONS':
        print("product options error!")
        return


# login
# post: log in and send the status
@app.route('/login', methods=['GET', 'POST', 'OPTIONS'])
def login():
    info = json.loads(request.get_data())

    if request.method == 'GET':
        print("log in get error!")
        return

    # log in status
    elif request.method == 'POST':
        user_cnt = User.query.filter(User.email == info["email"]).count()
        if user_cnt == 0:
            # need modification
            result = {}
            result["state"] = False
            result["result"] = "failed: user name does not exist"
            res = make_response(json.dumps(result))
            res.headers["Accesss-Control-Allow-Origin"] = '*'
            return res
        else:
            user_search = to_dict(User.query.filter(User.email == info["email"]).first())

        # check the log in status
        if info["password"] != user_search["password"]:
            user_search["state"] = False
            user_search["result"] = "failed: wrong user name or password"
            res = make_response(json.dumps(user_search))
            res.headers["Access-Control-Allow-Origin"] = '*'
            return res

        # correctly log in
        user_search["state"] = True
        user_search["result"] = "log in successfully!"
        res = make_response(json.dumps(user_search))
        res.headers["Access-Control-Allow-Origin"] = '*'
        return res

    # undefined behavior
    elif request.method == 'OPTIONS':
        print("log in options error!")
        return


# register
# post: register a new account
@app.route('/register', methods=['GET', 'POST', 'OPTIONS'])
def register():
    info = json.loads(request.get_data())

    if request.method == 'GET':
        print("register get error!")
        return

    # register
    elif request.method == 'POST':
        user_cnt = User.query.filter(User.email == info["email"]).count()
        if user_cnt != 0:
            user_dict = {}
            user_dict["state"] = False
            user_dict["result"] = "Repeated registration!"
            res = make_response(json.dumps(user_dict))
            res.headers["Access-Control-Allow-Origin"] = '*'
            return res

        # create a new user account
        user_x = User(user_name = info["user_name"], password = info["password"], account = 0, identity = False, email = info["email"])
        db.session.add(user_x)
        db.session.commit()
        db.session.close()
        # response to the front
        user_dict = {}
        user_dict["state"] = True
        user_dict["result"] = "succeed in registration!"
        res = make_response(json.dumps(user_dict))
        res.headers["Access-Control-Allow-Origin"] = '*'
        return res

    # undefined behavior
    elif request.method == 'OPTIONS':
        print("log in options error!")
        return


# change_WeChat
# post: initialize the wechat id
# implemented by lexie, 2021.12.14
# no use for this function
@app.route('/changeWeChat', methods=['GET', 'POST', 'OPTIONS'])
def change_WeChat():
    info = json.loads(request.get_data())
    if request.method == 'GET':
        print("change WeChat get error!")
        return
    # register
    elif request.method == 'POST':
        user_x = db.session.query(User).filter(User.id == info["user_id"]).first()
        user_x.WeChat_id = info["WeChat_id"]
        db.session.add(user_x)
        db.session.commit()
        # response to the front
        user_dict = to_dict(user_x)
        db.session.close()
        user_dict["result"] = "success"
        res = make_response(json.dumps(user_dict))
        res.headers["Access-Control-Allow-Origin"] = '*'
        return res

    # undefined behavior
    elif request.method == 'OPTIONS':
        print("change Wechat options error!")
        return


# buy_product
# post: buy a certain product and set its state
# implemented by lexie, 2021.12.14
# TODO(scarlyw): check transaction
@app.route('/buy_product', methods=['GET', 'POST', 'OPTIONS'])
def buy_product():
    info = json.loads(request.get_data())

    if request.method == 'GET':
        print("buy product get error!")
        return

    # register
    elif request.method == 'POST':
        product_x = db.session.query(Product).filter(Product.product_id == info["product_id"]).first()
        buyer = db.session.query(User).filter(User.user_id == info["user_id"]).first()
        seller = db.session.query(User).filter(User.user_id == product_x.user_id).first()
        if product_x.state == False:
            user_dict = {}
            user_dict["state"] = False
            user_dict["result"] = "sold"
            res = make_response(json.dumps(user_dict))
            res.headers["Access-Control-Allow-Origin"] = '*'
            return res
        elif buyer.account < product_x.price:
            user_dict = {}
            user_dict["state"] = False
            user_dict["result"] = "outOfMoney"
            res = make_response(json.dumps(user_dict))
            res.headers["Access-Control-Allow-Origin"] = '*'
            return res

        history_x = History(user_provider_id = product_x.user_id,
                            user_purchaser_id = info["user_id"],
                            product_id = info["product_id"],
                            timestamp = datetime.now())

        buyer.account -= product_x.price
        seller.account += product_x.price
        product_x.state = False

        db.session.add_all([buyer, seller, product_x, history_x])
        db.session.commit()
        db.session.close()
        # db.session.close()

        # seller = User.query.filter(User.id == history_x.user_provider_id).first()
        # buyer = User.query.filter(User.id == history_x.user_purchaser_id).first()
        
        # sender = 'from@fairmart.com'
        # receivers = seller.email  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
        
        # content = "Dear user:\n" + "Your product " + product_x.product_name + " has been purchased by " + buyer.user_name + ",\n" + "Please contact the buyer via wechat or email,\n"  + "buyer wechat: " + buyer.WeChat_id + ", buyer email: " + buyer.email + "\n"

        # message = MIMEText(content, 'plain', 'utf-8')

        # message['From'] = Header("Fairmart", 'utf-8')   # 发送者
        # message['To'] =  Header(seller.user_name, 'utf-8')        # 接收者
 
        # subject = 'Fairmart message'
        # message['Subject'] = Header(subject, 'utf-8')

        # try:
        #     smtpObj = smtplib.SMTP('localhost')
        #     smtpObj.sendmail(sender, receivers, message.as_string())
        #     print ("邮件发送成功")
        # except smtplib.SMTPException:
        #     print ("Error: 无法发送邮件")

        # response to the front
        user_dict = {}
        user_dict["state"] = True
        user_dict["result"] = "You buy it successfully"
        res = make_response(json.dumps(user_dict))
        res.headers["Access-Control-Allow-Origin"] = '*'
        return res

    # undefined behavior
    elif request.method == 'OPTIONS':
        print("buy product options error!")
        return


# reset_pw
# post: retrieve the password of a certain account
# implemented by lexie, 2021.12.21
# no use for this function
@app.route('/resetpw', methods=['GET', 'POST', 'OPTIONS'])
def reset_pw():
    info = json.loads(request.get_data())
    if request.method == 'GET':
        print("reset password get error!")
        return
    # register
    elif request.method == 'POST':
        user_x = db.session.query(User).filter(User.email == info["email"]).first()
        user_x.password = info["new_pw"]
        db.session.add(user_x)
        db.session.commit()
        user_dict = to_dict(user_x)
        db.session.close()
        user_dict["result"] = "success"
        res = make_response(json.dumps(user_dict))
        res.headers["Access-Control-Allow-Origin"] = '*'
        return res

    # undefined behavior
    elif request.method == 'OPTIONS':
        print("reset password options error!")
        return

# change_contact_info
# post: change the other_contact_info
@app.route('/change_contact_info', methods=['GET', 'POST', 'OPTIONS'])
def change_contact_info():
    info = json.loads(request.get_data())
    if request.method == 'GET':
        print("reset password get error!")
        return
    # register
    elif request.method == 'POST':
        user_cnt = db.session.query(User).filter(User.user_id == info["user_id"]).count()
        if (user_cnt == 0):
            user_dict = {}
            user_dict["state"] = False
            user_dict["result"] = "Please log in first"
            res = make_response(json.dumps(user_dict))
            res.headers["Access-Control-Allow-Origin"] = '*'
            return res

        user_x = db.session.query(User).filter(User.user_id == info["user_id"]).first()
        user_x.other_contact_info = info["other_contact_info"]
        db.session.add(user_x)
        db.session.commit()
        db.session.close()
        user_dict = {}
        user_dict["state"] = True
        user_dict["result"] = "change information successfully"
        res = make_response(json.dumps(user_dict))
        res.headers["Access-Control-Allow-Origin"] = '*'
        return res

    # undefined behavior
    elif request.method == 'OPTIONS':
        print("reset password options error!")
        return


# add_favorite
# post: add a product to the favorite folder
@app.route('/add_favorite', methods=['GET', 'POST', 'OPTIONS'])
def add_favorite():
    info = json.loads(request.get_data())
    if request.method == 'GET':
        print("add favorite get error!")
        return

    # register
    elif request.method == 'POST':
        # product_x = Product.query.filter(Product.product_id == info["product_id"]).first()
        # correlation_x = Correlation(user_id=info["buyer_id"],
        #                             product_id=info["product_id"],
        #                             product_name=product_x.product_name,
        #                             category_value=product_x.category_value,
        #                             state=10,
        #                             price=product_x.price,
        #                             description=product_x.description,
        #                             source_id=product_x.source_id,
        #                             availability_state=product_x.availability_state)
        favorite_x = Favorites(user_id = info["user_id"], product_id = info["product_id"])
        db.session.add(favorite_x)
        db.session.commit()
        # response to the front
        db.session.close()
        user_dict = {}
        user_dict["state"] = True
        user_dict["result"] = "Mark successfully"
        res = make_response(json.dumps(user_dict))
        res.headers["Access-Control-Allow-Origin"] = '*'
        return res

    # undefined behavior
    elif request.method == 'OPTIONS':
        print("add favorite options error!")
        return


# my_favorites
# post: get all products that are favored
@app.route('/my_favorites', methods=['GET', 'POST', 'OPTIONS'])
def my_favorites():
    info = json.loads(request.get_data())
    if request.method == 'GET':
        return

    elif request.method == 'POST':
        # strategy_first = 0, all products
        # TODO(scarlyw) : 判定登录状态
        if info["user_id"] == 0:
            return 
        # only want one category_
        if info["strategy_0"] == 1:
            search_result = db.session.execute('select * from product where category_id = %d and product_id in \
                                                     (select favorites.product_id from favorites where user_id = %d)' 
                                                     % info["category_id"], info["user_id"])
        else:
            search_result = db.session.execute('select * from product where product_id in \
                                                     (select favorites.product_id from favorites where user_id = %d)' 
                                                     % info["user_id"])
        search_result = list(search_result)
        # different sorting strategies
        # automatically present the product by id
        if info["strategy_1"] == 0:
            search_result_1 = search_result

        # sorted by price
        elif info["strategy_1"] == 1:
            search_result_1 = search_result
            search_result_1.sort(key = take_price)

        # sorted by category
        elif info["strategy_1"] == 2:
            search_result_1 = search_result
            search_result_1.sort(key = take_category)

        # change the type of list
        for i in range(len(search_result_1)):
            item_original = search_result_1[i]
            item_modify = to_dict(item_original)
            basedir = os.path.abspath(os.path.dirname(__file__))
            path = "\static\img\\2022-4-2919-516-10.png"       
            path_photo_picture_save = basedir + path
            with open(path_photo_picture_save, 'r') as f:
                photo = f.read()
            item_modify["photo"] = photo
            search_result_1[i] = item_modify

        res = make_response(json.dumps(search_result_1))
        res.headers["Access-Control-Allow-Origin"] = '*'
        return res

    # undefined behavior
    elif request.method == 'OPTIONS':
        print("product options error!")
        return


# delete_favorite
# post: delete a certain product from the favorites folder
@app.route('/delete_favorite', methods=['GET', 'POST', 'OPTIONS'])
def delete_favorite():
    info = json.loads(request.get_data())
    if request.method == 'GET':
        print("delete favorite get error")
        return

    elif request.method == 'POST':
        favorite_cnt = Favorites.query.filter(and_(Favorites.user_id == info["user_id"],
                                                 Favorites.product_id == info["product_id"])).count()
        if (favorite_cnt == 0):
            user_dict = {}
            user_dict["state"] = False
            user_dict["result"] = "no result"
            res = make_response(json.dumps(user_dict))
            res.headers["Access-Control-Allow-Origin"] = '*'
            return res
        
        favorite_x = db.session.query(Favorites).filter(and_(Favorites.user_id == info["user_id"],
                                                 Favorites.product_id == info["product_id"])).first()
        user_dict = {}
        #something error
        db.session.delete(favorite_x)
        db.session.commit()
        db.session.close()
        user_dict["state"] = True
        user_dict["result"] = "delete successfully"
        res = make_response(json.dumps(user_dict))
        res.headers["Access-Control-Allow-Origin"] = '*'
        return res

    # undefined behavior
    elif request.method == 'OPTIONS':
        print("delete favorites options error!")
        return


# my_purchase
# post: get all products that have been purchased in the history table
@app.route('/my_purchase', methods=['GET', 'POST', 'OPTIONS'])
def my_purchase():
    info = json.loads(request.get_data())
    if request.method == 'GET':
        return

    elif request.method == 'POST':
        # strategy_first = 0, all products
        if info["user_id"] == 0:
            return 
        # only want one category_
        if info["strategy_0"] == 1:
            search_result = db.session.execute('select * from product where category_id = %d and product_id in \
                                                     (select history.product_id from history where user_purchaser_id = %d)' 
                                                     % info["category_id"], info["user_id"])
        else:
            search_result = db.session.execute('select * from product where product_id in \
                                                     (select history.product_id from history where user_purchaser_id = %d)' 
                                                     % info["user_id"])

        search_result = list(search_result)
        # different sorting strategies
        # automatically present the product by id
        if info["strategy_1"] == 0:
            search_result_1 = search_result

        # sorted by price
        elif info["strategy_1"] == 1:
            search_result_1 = search_result
            search_result_1.sort(key = take_price)

        # sorted by category
        elif info["strategy_1"] == 2:
            search_result_1 = search_result
            search_result_1.sort(key = take_category)

        # change the type of list
        for i in range(len(search_result_1)):
            item_original = search_result_1[i]
            item_modify = to_dict(item_original)
            basedir = os.path.abspath(os.path.dirname(__file__))
            path = "\static\img\\2022-4-2919-516-10.png"       
            path_photo_picture_save = basedir + path
            with open(path_photo_picture_save, 'r') as f:
                photo = f.read()
            item_modify["photo"] = photo
            search_result_1[i] = item_modify

        res = make_response(json.dumps(search_result_1))
        res.headers["Access-Control-Allow-Origin"] = '*'
        return res

    # undefined behavior
    elif request.method == 'OPTIONS':
        print("product options error!")
        return

# my_sold
# post: get all products that have been sold by this user
@app.route('/my_sold', methods=['GET', 'POST', 'OPTIONS'])
def my_sold():
    info = json.loads(request.get_data())
    if request.method == 'GET':
        return

    elif request.method == 'POST':
        # strategy_first = 0, all products
        if info["user_id"] == 0:
            return 
        # only want one category_
        if info["strategy_0"] == 1:
            search_result = db.session.execute('select * from product where category_id = %d and product_id in \
                                                     (select history.product_id from history where user_provider_id = %d)' 
                                                     % info["category_id"], info["user_id"])
        else:
            search_result = db.session.execute('select * from product where product_id in \
                                                     (select history.product_id from history where user_provider_id = %d)' 
                                                     % info["user_id"])
        search_result = list(search_result)
        # different sorting strategies
        # automatically present the product by id
        if info["strategy_1"] == 0:
            search_result_1 = search_result

        # sorted by price
        elif info["strategy_1"] == 1:
            search_result_1 = search_result
            search_result_1.sort(key = take_price)

        # sorted by category
        elif info["strategy_1"] == 2:
            search_result_1 = search_result
            search_result_1.sort(key = take_category)

        # change the type of list
        for i in range(len(search_result_1)):
            item_original = search_result_1[i]
            item_modify = to_dict(item_original)
            basedir = os.path.abspath(os.path.dirname(__file__))
            path = "\static\img\\2022-4-2919-516-10.png"       
            path_photo_picture_save = basedir + path
            with open(path_photo_picture_save, 'r') as f:
                photo = f.read()
            item_modify["photo"] = photo
            search_result_1[i] = item_modify

        res = make_response(json.dumps(search_result_1))
        res.headers["Access-Control-Allow-Origin"] = '*'
        return res

    # undefined behavior
    elif request.method == 'OPTIONS':
        print("product options error!")
        return

# get_seller_info
# post: get the information of the seller of this product
@app.route('/get_seller_info', methods=['GET', 'POST', 'OPTIONS'])
def get_seller_info():
    if request.method == 'GET' or request.method == 'OPTIONS':
        return

    info = json.loads(request.get_data())
    # TODO(scarlyw): 确认是否需要考虑商品错误
    product_x = Product.query.filter(Product.product_id == info["product_id"]).first()
    user_x = User.query.filter(User.user_id == product_x.user_id).first()
    user_dict = {}
    user_dict["email"] = user_x.email
    user_dict["other_connect_description"] = user_x.other_contact_info
    res = make_response(json.dumps(user_dict))
    res.headers["Access-Control-Allow-Origin"] = '*'
    return res

# get_user_info
# post: get the information of the user
@app.route('/get_user_info', methods=['GET', 'POST', 'OPTIONS'])
def get_user_info():
    if request.method == 'GET' or request.method == 'OPTIONS':
        return

    info = json.loads(request.get_data())
    user_cnt = User.query.filter(User.user_id == info["user_id"]).count()
    if (user_cnt == 0):
        user_dict = {}
        user_dict["state"] = False
        user_dict["result"] = "please log in first"
        res = make_response(json.dumps(user_dict))
        res.headers["Access-Control-Allow-Origin"] = '*'
        return res

    user_x = User.query.filter(User.user_id == info["user_id"]).first()
    user_dict = to_dict(user_x)
    user_dict.pop("password")
    user_dict["state"] = True
    user_dict["result"] = "success"
    res = make_response(json.dumps(user_dict))
    res.headers["Access-Control-Allow-Origin"] = '*'
    return res

# get_favorite_state
# post: get the state of this marked product
@app.route('/get_favorite_state', methods=['GET', 'POST', 'OPTIONS'])
def get_favorite_state():
    if request.method == 'GET' or request.method == 'OPTIONS':
        return

    info = json.loads(request.get_data())
    favorite_cnt = Favorites.query.filter(and_(Favorites.product_id == info["product_id"],
                                               Favorites.user_id == info["user_id"])).count()
    user_dict = {}
    user_dict["state"] = (favorite_cnt != 0)
    res = make_response(json.dumps(user_dict))
    res.headers["Access-Control-Allow-Origin"] = '*'
    return res

# deposit
# post: user deposit the money
@app.route('/deposit', methods=['GET', 'POST', 'OPTIONS'])
def deposit():
    if request.method == 'GET' or request.method == 'OPTIONS':
        return

    info = json.loads(request.get_data())
    user_cnt = db.session.query(User).filter(User.user_id == info["user_id"]).count()
    if (user_cnt == 0):
        user_dict = {}
        user_dict["state"] = False
        user_dict["result"] = "Please log in first"
        res = make_response(json.dumps(user_dict))
        res.headers["Access-Control-Allow-Origin"] = '*'
        return res

    user_x = db.session.query(User).filter(User.user_id == info["user_id"]).first()
    user_x.account += float(info["money"])
    db.session.add(user_x)
    db.session.commit()
    db.session.close()
    user_dict = {}
    user_dict["state"] = True
    user_dict["result"] = "deposit successfully"
    res = make_response(json.dumps(user_dict))
    res.headers["Access-Control-Allow-Origin"] = '*'
    return res

# get_user_state
# post: get the identity of the user
@app.route('/get_user_state', methods=['GET', 'POST', 'OPTIONS'])
def get_user_state():
    if request.method == 'GET' or request.method == 'OPTIONS':
        return

    info = json.loads(request.get_data())
    user_cnt = db.session.query(User).filter(User.user_id == info["user_id"]).count()
    if (user_cnt == 0):
        user_dict = {}
        user_dict["state"] = False
        user_dict["result"] = "Please log in first"
        res = make_response(json.dumps(user_dict))
        res.headers["Access-Control-Allow-Origin"] = '*'
        return res

    user_x = User.query.filter(User.user_id == info["user_id"]).first()
    user_dict = {}
    user_dict["state"] = user_x.identity
    res = make_response(json.dumps(user_dict))
    res.headers["Access-Control-Allow-Origin"] = '*'
    return res

# Email_exist
# post: check whether the email exists in the database
# no use for this function
@app.route('/Email_exist', methods=['GET', 'POST', 'OPTIONS'])
def Email_exist():
    info = json.loads(request.get_data())
    email_cnt = User.query.filter(User.email == info["email"]).count()
    if email_cnt != 0:
        user_x = User.query.filter(User.email == info["email"]).first()
        user_dict = to_dict(user_x)
        user_dict["result"] = "success"
        res = make_response(json.dumps(user_dict))
        res.headers["Access-Control-Allow-Origin"] = '*'
        return res
    else:
        user_dict = {}
        user_dict["result"] = "success"
        res = make_response(json.dumps(user_dict))
        res.headers["Access-Control-Allow-Origin"] = '*'
        return res



# initial function implemented for checking
@app.route('/')
def hello_world():
    return 'Hello world for dm_app_0 on our server.'


# the initialization of new tables
# not used in actual running process
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)
