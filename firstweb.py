#encoding: utf-8

from flask import Flask,render_template,request,redirect,url_for,session,g
import config
from decorators import login_required
#获取数据库的结构
from models import User,Question,Answer
from sqlalchemy import or_

#获取控制数据库的方法
from exts import db


app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)




@app.route('/')
def index():
    context = {
        'questions': Question.query.order_by('-create_time').all()
    }
    return render_template('index.html',**context)


@app.route('/register/',methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        #判断手机号码是不是已经存在
        user = User.query.filter(User.telephone == telephone).first()
        if user:
            return u'该手机已经被注册了，请换个手机吧。'
        else:
            #判断密码是不是一样
            if password1 != password2:
                return u"两次密码输入不一样哦"
            else:
                user = User(telephone=telephone,username=username,password=password2)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))

@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        user = User.query.filter(User.telephone == telephone).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            #如果你想在31天内不需要登录，
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return u'手机号码或者密码错误'

@app.route('/logout/')
def logout():
    session.pop('user_id')
    return redirect(url_for('login'))



@app.route('/question/',methods=['GET','POST'])
@login_required
def question():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('contect')
        question = Question(title=title,content=content)
        question.author = g.user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))


@app.route('/detail/<question_id>')
def detail(question_id):
    questions_model = Question.query.filter(Question.id == question_id).first()

    return render_template('detail.html',question = questions_model)

@app.route('/add_answer/',methods=['POST'])
@login_required
def add_answer():
    content = request.form.get('answer_content')
    question_id = request.form.get('question_id')

    answer = Answer(content=content)
    answer.author = g.user
    question = Question.query.filter(Question.id == question_id).first()
    answer.question = question
    db.session.add(answer)
    db.session.commit()
    return redirect(url_for('detail',question_id=question_id))

@app.route('/search/')
def search():
    q = request.args.get('q')
    questions = Question.query.filter(or_(Question.title.contains(q),Question.content.contains(q))).order_by('-create_time')
    return render_template('index.html',questions=questions)

@app.before_request
def my_before_request():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            g.user = user



@app.context_processor
#没搞清这个干嘛的，好像是在每个页面显示自己的用户名
def my_context_processor():
    if hasattr(g,"user"):
            return {'user':g.user}
    return {}

if __name__ == '__main__':
    app.run()
