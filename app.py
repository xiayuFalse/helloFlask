import time

from flask import Flask, request, after_this_request, redirect, url_for, abort, json, make_response, Response
from flask.json import jsonify
import datetime

app = Flask(__name__)

# flask路由可多个url绑定同一视图函数，也可以进行参数的传递，或者设置参数传递时的默认值，
# 如果进行参数传递的时候，设置默认值，必须以下列写法

@app.route('/')
def index_page():
    return redirect(url_for('index'))

@app.route('/index', defaults={'name': 'xiayu'})
@app.route('/index/<name>')
def index(name):
    print((request.args).to_dict())
    return '<h1>Hello %s<h1>'%name

# 获取查询字符串
# immutablesMuitDict对象继承子werkzeug的MuitDict,支持一键多值，但是不可修改。
# MuitDict为一键多值类型，若获取其全部，可以使用get_list()方法，
@app.route('/args')
def query_str():
    str1 = request.args.get('name','nihao') # 通过查询字符串的键来获取值,第一个参数为需要获取的键，第二个参数为获取不到的默认值
    #dict1 = (request.args).to_dict() # werkzeug的immutableMuitDict对象，储存解析后的查询字符串，得到之后为immutableMUitDict类型的数据。
    # print(dict1)
    print(str1)
    return str1

# 根据请求方法的处理
@app.route('/request/', methods={'POST','GET'})
def request_method():
    print(request.endpoint) # 打印请求对象的端点值，即处理函数，此URl的端点值为request_method
    return '<h1>request</h1>'

# flask转换器
@app.route('/convert/<int(min):year>') # 此为flask中的转换器，可以把url的数据类型转换为所使用的转换器的数据类型，如果输入的数据类型转换错误，会触发404异常
@app.route('/convert/<any("hello","name"):year>') # 此为URL中的数据必须为any中的所列出的数据，否则就会404
def convert(year):
    return '<h1>This is your input: %s</h1>'% year

# 自定义flask转换器
# 集成wekzeug.routing中的base转换器
from werkzeug.routing import BaseConverter
class User_defindConverter(BaseConverter):
    '''
    可以通过重写父类init方法，实现使用转换器的时候可以传入规则
    def __init__(self, regex, url_map):
        super(User_defindConverter, self).__init__(url_map)
        regex=regex
    使用
        @app.route('/convert/<re('\d{9}')>')
    '''

    # 定义匹配规则
    regex = '1[34578][\d]{9}'
    # 此函数为正则匹配成功之后，进入视图函数处理之前进行调用
    def to_python(self, value):
        print('正则之后')
        return value
    # 反向解析传递函数时，首先url_for 传递给函数to_url,to_url函数对传入value值进行处理交给装饰器，然后重复to_python步骤。
    def to_url(self, value):
        # 调用父类的to_url方法，父类会使用url_quote()方法，对url进行编码，有效防止中文编码出现问题
        return BaseConverter.to_url(self,value)

# 对自定义的转换器进行注册，转换器的名称为user
app.url_map.converters['user']= User_defindConverter

# 使用自定义的转换器
@app.route('/user_defind/<user:phoneNum>')
def user_defind(phoneNum):
    return 'This is your telphonenum: %s'%phoneNum

#请求钩子的使用
# 在用户的第一次请求后执行的代码
@app.before_first_request
def do_first_something():
    print('this is first request')
# 在每一次的请求后执行的代码
@app.before_request
def do_something():
    print('this is every request')
# 如果没有未处理的异常，则在每次的请求结束后运行,需要接受一个响应类对象，并且返回同一个或者更后的响应对象
@app.after_request
def do_something_after(response):
    print('NO Exceptions and after request,')
    return response
# 即使有未处理的响应对象，也会在每次的请求后运行，但是如果发生异常，会把异常参数传入到注册的函数中
@app.teardown_request
def do_something_exception(e):
    print('Exception:',e)

#  在视图函数中内注册一个函数，会在这个请求的视图函数处理结束，进行处理，需要从flask中导入,
#  需要接受一个响应类对象，并且返回同一个或者更新后的响应类对象
@app.route('/after_this')
def after_request():
    language = request.cookies.get('language')
    if language == None:
        @after_this_request
        def set_language_cookie(response):
            print('after_this_request')
            response.set_cookie('language','chinese')
            return response
    return '<h1>response</h1>'


# 重定向
@app.route('/redirect')
def redirect_page():
    '''
    重定向的写法1：在return的后面可以加上状态码，如果为重定向，可以加一个字典，字典的键为'location‘，值为url
    重定向的写法2: 在return的后面可以加上状态码的后面可以加redirect重定向，其中可以写url，也可以通过反向解析实现
    如果使用redirect函数，默认的状态码时302，即临时重定向，也可以在，第二个参数/或者code关键字指定为永久重定向
    '''
    # return '<h1>redirect Page</h1>',302,{'location':'/index'}
    # return redirect('/index')
    return redirect(url_for('index'))

# abort函数
@app.route('/404')
def abort_page():
    '''
    假如你想手动返回错误响应，可以使用abort函数，参数为错误状态码，当使用abort的函数的时候，abort以下的代码将不会被执行
    :return:
    '''
    abort(403)
    return '<h1>Error Page</h1>'

# jsonify函数
@app.route('/jsonify')
def json_page():
    '''
    jsonify自动将传入的参数和数据进行序列化，转换为以json数据为主体的响应，并且自动的讲MIME设置为正确的类型
    :return:
    '''
    data = {
        'name':'xiayu'
    }
    response = make_response('Hello World')
    response.mimetype = 'text/html'
    print(response.headers)
    return jsonify(data)

# set_cookies函数
@app.route('/set_cookie/<name>')
def setCookie(name):
    cookie_max_age = datetime.datetime.today()+datetime.timedelta(hours=2)
    print(cookie_max_age)
    response = make_response('hello %s'%name)
    response.set_cookie(key='name', value = name, expires = cookie_max_age)
    return response