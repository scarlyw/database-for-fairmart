from os import name, stat_result
from unicodedata import category
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from init import db
import hashlib

app = Flask(__name__)

'''配置数据库'''
app.config['SECRET_KEY'] = 'hard to guess'#一个字符串，密码。也可以是其他如加密过的

#在此登录的是root用户，要填上密码如123456，MySQL默认端口是3306。并填上创建的数据库名如youcaihua
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/test_0'

#SQLALCHEMY_BINDS = {
 #   'product_0': 'mysql+pymysql://root:123456@127.0.0.1:3306/test_product_0',
  #  'user_0': 'mysql+pymysql://root:123456@127.0.0.1:3306/test_user_0',
   # 'history_0': 'mysql+pymysql://root:123456@127.0.0.1:3306/test_history_0',

#}
#app.config['SQLALCHEMY_BINDS'] = SQLALCHEMY_BINDS

#设置下方这行code后，在每次请求结束后会自动提交数据库中的变动

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


db = SQLAlchemy(app)#实例化数据库对象，它提供访问Flask-SQLAlchemy的所有功能

'''定义模型，建立关系'''
class Product(db.Model):
    #__bind_key__='product_0'
    __tablename__ = 'product'

    product_id = db.Column(db.Integer, primary_key = True)
    category_id = db.Column(db.Integer,db.ForeignKey("category.category_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    product_name = db.Column(db.String(256))
    price = db.Column(db.Float)
    # number is about to be included
    photo_path = db.Column(db.String(100))
    # add source id
    state = db.Column(db.Boolean)
    put_timestamp = db.Column(db.DateTime)
    product_description = db.Column(db.String(256))


    __table_args__ = {
        "mysql_charset" : "utf8"
    }

class Wanted(db.Model):
   # __bind_key__='product_0'
    __tablename__ = 'wanted'

    wanted_id = db.Column(db.Integer, primary_key = True)
    wanted_name = db.Column(db.String(64))
    category_value = db.Column(db.Integer)
    price = db.Column(db.Float)
    # number is about to be included
    # photo_path = db.Column(db.String(100))
    description = db.Column(db.String(500))
    # add source id
    source_id = db.Column(db.Integer)
    availability_state = db.Column(db.Integer)


    __table_args__ = {
        "mysql_charset" : "utf8"
    }

class User(db.Model):
   # __bind_key__ = 'user_0'
    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key = True)
    user_name = db.Column(db.String(64))
    password = db.Column(db.String(50))
    account = db.Column(db.Float)
    identity = db.Column(db.Boolean)
    # add email
    email = db.Column(db.String(100))
    other_contact_info = db.Column(db.String(100))

    __table_args__ = {
        "mysql_charset" : "utf8"
    }

class Correlation(db.Model):
    #__bind_key__='correlation_0'
    __tablename__ = 'correlation'

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)
    product_name = db.Column(db.String(64))
    category_value = db.Column(db.Integer)
    state = db.Column(db.Integer)
    # 0 represents nothing
    # 10 represents favorite
    price = db.Column(db.Float)
    description = db.Column(db.String(500))
    # add source id
    source_id = db.Column(db.Integer)
    availability_state = db.Column(db.Integer)

    __table_args__ = {
        "mysql_charset": "utf8"
    }

class History(db.Model):
   # __bind_key__ = 'history_0'
    __tablename__ = 'history'

    user_provider_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), primary_key = True)
    user_purchaser_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), primary_key = True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.product_id"), primary_key = True)
    timestamp = db.Column(db.DateTime)

    __table_args__ = {
        "mysql_charset": "utf8"
    }

class Category(db.Model):
    __tablename__ = 'category'

    category_id = db.Column(db.Integer, primary_key = True)
    category_name = db.Column(db.String(60))
    __table_args__ = {
        "mysql_charset" : "utf8"
    }

class Favorites(db.Model):
    __tablename__ = 'favorites'

    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), primary_key = True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.product_id"), primary_key = True)
    __table_args__ = {
        "mysql_charset" : "utf8"
    }

# class Role(db.Model):
#     __tablename__ = 'roles'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64), unique=True)
#     users = db.relationship('User', backref='role', lazy='dynamic')
#
#     def __repr__(self):
#         return '<Role %r>' % self.name
#
#
# class Users(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(64), unique=True, index=True)
#     role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
#
#     def __repr__(self):
#         return '<User %r>' % self.username


#
#
'''进行数据库操作'''
if __name__ == '__main__':
    #删除旧表
    db.drop_all()
    db.create_all()#创建新表
    m = hashlib.md5()
    password_1 = "123456"
    password_1 = password_1.encode(encoding="utf-8")
    m.update(password_1)
    password_1 = m.hexdigest()

    m = hashlib.md5()
    password_2 = "123"
    password_2 = password_2.encode(encoding="utf-8")
    m.update(password_2)
    password_2 = m.hexdigest()

    m = hashlib.md5()
    password_3 = "111"
    password_3 = password_3.encode(encoding="utf-8")
    m.update(password_3)
    password_3 = m.hexdigest()

    user1 = User(user_id = 1, user_name = 'software engineering kills 01', password = password_1, email='1@163.com', account = 100.1, identity = False)
    user2 = User(user_id = 2, user_name = 'why ask2', password = password_2, email='2@gmail.com', account = 1000, identity = True )
    user3 = User(user_id = 3, user_name = 'test_2', password = password_3, email='Just_a_string', account = 100.15, identity = False)

    category1 = Category(category_id = 1, category_name = '二手书本')
    category2 = Category(category_id = 2, category_name = '数码产品')
    category3 = Category(category_id = 3, category_name = '票务转让')
    category4 = Category(category_id = 4, category_name = '二手衣物')
    category5 = Category(category_id = 5, category_name = '生活用品')
    category6 = Category(category_id = 6, category_name = '运动装备')
    category7 = Category(category_id = 7, category_name = '其他二手')
    # userx=User(user_id = 9, user_name = 'test_3', password='test', email='string', WeChat_id='userx_wechat')
    product1 = Product(product_id = 1, product_name='x0', price = 100.1, product_description='没人理解计算机系统', category_id=1, user_id = 2, state = True)
    product2 = Product(product_id = 2, product_name='x1', price = 50.1, product_description='操统话剧排练', category_id=1, user_id = 3, state = True)
    product3 = Product(product_id=3, product_name='x2', price=70.1, product_description='软件工程教材', category_id=1, user_id = 1, state = True)
    product4 = Product(product_id=4, product_name='x3', price=100000, product_description='信科大三本科生', category_id=2, user_id = 1, state = True)
    product5 = Product(product_id=5, product_name='x4', price=100010, product_description='信科大三一只猫', category_id=2, user_id = 2, state = True)

    product6 = Product(product_id=6, product_name='淑芬1', price=10.1, product_description='我就没学会过', category_id=2, user_id=3, state = True)
    product7 = Product(product_id=7, product_name='淑芬2', price=13.1, product_description='我就没学会过+1', category_id=1, user_id=3, state = True)
    product12 = Product(product_id=16, product_name='我和我的祖国', price=11.1, product_description='思修论文写作指导', category_id=1, user_id=2, state = True)
    #db.session.add_all([user1, user2, product1, product2])
    #db.session.add_all([product6, product7, product8])
    # history_0=History(user_purchaser_id=1, user_provider_id=2, product_id=1)
    db.session.add_all([user1, user2, user3])
    db.session.add_all([category1, category2, category3, category4, category5, category6, category7])
    db.session.commit()
    db.session.add_all([product1, product2, product3, product4, product5, product6, product7, product12])
    # db.session.add(product12)
    # db.session.add(userx)
    db.session.commit()
    wanted1 = Wanted(wanted_id = 1, wanted_name="April", price = 100.1, description="信科小姐姐", category_value=1)
    wanted2 = Wanted(wanted_id = 2, wanted_name="嘉然", price = 10, description="!!!!!! ", category_value=2)
    # user1 = User(id = 1, name='scarlyw', password = '123457')
    # user2 = User(id = 2, name='闫旭东', password = '123')
    # user3 = User(id = 3, name = '畅畅子yyds', password = '666666')
    #
    db.session.add_all([wanted1, wanted2])
    db.session.commit()
    # product1 = Product(id = 1, name = '数分三', price = 10.111, description = '好书一本哦，大家注意！！！')
    # product2 = Product(id = 2, name = 'test', price = 12334, description = 'test！！！')
    # #
    # correlation1 = Correlation(user_id = 1, product_id = 2, state = 0)
    # correlation2 = Correlation(user_id = 2, product_id = 1, state = 4)
    # #
    # # #在将对象写入数据库之前，先将其添加到会话中，数据库会话db.session和Flask session对象没有关系，数据库会话也称 事物 译作Database Transaction。
    # db.session.add_all([correlation1, correlation2])
    # #提交会话到数据库
    # db.session.commit()
    #
    # #修改roles名
    # user1.name = '刘雨薇yuweil'
    # db.session.add(user1)
    # db.session.commit()
    #
    # #删除数据库会话，从数据库中删除“Moderator”角色
    # #db.session.delete(mod_role)
    # #db.session.commit()#注意：删除 和插入、更新一样，都是在数据库会话提交后执行

    #查询
    print("debug")
    print(User.query.all())
