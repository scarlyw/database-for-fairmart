### 前后端功能对应

以前端用户每一次点击为一个功能

| 前端功能                             | 描述                                             | Sql                                                          | 后端API name | 后端API参数                        |
| ------------------------------------ | ------------------------------------------------ | ------------------------------------------------------------ | ------------ | ---------------------------------- |
| 打开网页                             | 展示初始页面，显示商品等信息                     | select<br />1. category(name)<br />2. product(name) where state=onsale |              | x                                  |
| 用户点击注册                         | 进入注册界面                                     | x                                                            | x            | x                                  |
| 用户在注册界面输入信息并点击确认注册 | 尝试注册，注册成功返回个人页面；失败提示错误信息 | insert(user_id,user_name,password,email)                     |              | user_name, password,email          |
| 用户输入信息并点击登录               | 尝试登录，登录成功返回个人页面；失败提示请注册   | select *(except password) from user where email=input and password=input |              | email,password                     |
| 用户点击商品                         | 进入商品页面，显示商品信息                       | select * from product where product_id = input               |              | product_id                         |
| 用户在商品页面点击购买               | 购买商品                                         | transaction:<br />1. buyer_money -= price<br />2. seller_money += price<br />2. state = sold<br /> |              | user_id, product_id                |
| 用户在商品页面点击获得联系方式       | 提供卖家联系方式                                 | select email, other connect description from user where user_id = owner_id |              | product_id                         |
| 用户在商品页面点击收藏               | 收藏商品                                         | insert collect(user_id,product_id)                           |              | user_id,product_id                 |
| 商品页面显示是否收藏                 | 判断是否收藏                                     | select * from collect where user_id = input and product_id = input |              | user_id,product_id                 |
| 用户在已收藏的商品页面点击取消收藏   | 取消某个商品的收藏                               | delete collect(user_id, product_id)                          |              | user_id,product_id                 |
| 点击购买记录，显示购买记录           | 跳转到购买记录页面                               | select product info from product where history.product_id = product.id and buyer = input |              | user_id                            |
| 点击售出记录，显示售出记录           | 跳转到售出记录页面                               | select product info from product where history.product_id = product.id and seller = input |              | user_id                            |
| 用户充值                             | 点击充值按钮并充值                               | money += input                                               |              | user_id, money                     |
| 商品检索                             | 输入商品名关键字并点击搜索                       | product_name like "\*input\*" from product                   |              | keyword                            |
| 管理员界面                           | 判断是否为管理员，显示删除按钮等                 | select state from user where user_id = input                 |              | user_id                            |
| 管理员删除商品                       | 删除商品                                         | delect product(product_id) if user is administrator          |              | user_id, product_id                |
| 商品排序                             | 对当前显示的商品排序                             | order by id/name, category                                   |              |                                    |
| 用户点击个人页面                     | 进入个人页面                                     | select *(except password) from user where user_id = input    |              | user_id                            |
| 修改Other contact description        | 点击修改并输入新内容                             | update(user_id, input)                                       |              | user_id, other_contact_description |
|                                      |                                                  |                                                              |              |                                    |
|                                      |                                                  |                                                              |              |                                    |
|                                      |                                                  |                                                              |              |                                    |
|                                      |                                                  |                                                              |              |                                    |
|                                      |                                                  |                                                              |              |                                    |
|                                      |                                                  |                                                              |              |                                    |
|                                      |                                                  |                                                              |              |                                    |
|                                      |                                                  |                                                              |              |                                    |
|                                      |                                                  |                                                              |              |                                    |
|                                      |                                                  |                                                              |              |                                    |
|                                      |                                                  |                                                              |              |                                    |
|                                      |                                                  |                                                              |              |                                    |
|                                      |                                                  |                                                              |              |                                    |
|                                      |                                                  |                                                              |              |                                    |

