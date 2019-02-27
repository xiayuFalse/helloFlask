from flask import Flask

app = Flask(__name__)

# flask路由可多个url绑定同一视图函数，也可以进行参数的传递，或者设置参数传递时的默认值，
# 如果进行参数传递的时候，设置默认值，必须以下列写法

@app.route('/index', defaults={'name': 'xiayu'})
@app.route('/index/<name>')
def index(name):
    return '<h1>Hello %s<h1>'%name