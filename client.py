from flask import Flask, render_template, redirect, url_for, session, flash, request, jsonify
import requests
from forms.registerform import RegisterForm
from forms.loginform import LoginForm
from forms.articleForm import ArticleForm
from forms.updateform import UpdateForm
import os

client = Flask(__name__)

client.config.from_mapping(
    SECRET_KEY = os.urandom(22)
)

@client.route('/',methods=["GET"])
def index():
    response = requests.get("http://localhost:5000/article/0")
    articles = response.json()
    return render_template("home.html",articles=articles)

@client.route('/signup',methods=["GET","POST"])
def sign_up():
    if request.method == "GET":
        return render_template('register.html')
    elif request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        password_conf = request.form.get("confirm-password")
        
        validate_form = RegisterForm(username,email,password,password_conf)
        validate_form.validate()
        
        if validate_form.is_valid():
            data = {
                    "username":username,
                    "email":email,
                    "password":password,
                    "confirm-password":password_conf
                }
            response = requests.post(headers={"Accept":"application/json", "Content-Type": "application/json"},
                                     url="http://localhost:5000/register",
                                     json=data)
            if response.status_code == 201 :
                return redirect(url_for("sign_in"))
            else :
                errors = response.json()["errors"]
                return render_template("register.html",errors=errors)
        else :
            errors = validate_form.errors
            return render_template("register.html",errors=errors)

@client.route('/signin',methods=["GET","POST"])
def sign_in():
    if request.method == "GET":
        return render_template('login.html')
    elif request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        validate_form = LoginForm(email,password)
        validate_form.validate()
        
        if validate_form.is_valid():
            data = {"email":email,
                    "password":password}
            response = requests.post(
                                    headers={"Accept":"application/json", "Content-Type": "application/json"},
                                    url="http://localhost:5000/login",
                                    json=data)
            if response.status_code == 200 :
                user = response.json()["user"]
                session.clear()
                session["id"] = user["_id"]
                session["username"] = user["username"]
                session["email"] = user["email"]
                return redirect(url_for("index"))
            else :
                errors = response.json()["errors"]
                return render_template("login.html",errors=errors)
        else :
            errors = validate_form.errors
            return render_template("login.html",errors=errors)
    
@client.route('/logout',methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for('sign_in'))

@client.route('/user',methods=["GET", "POST"])
def user():
    if request.method == "GET":
        id = session["id"]
        user = requests.get(f"http://localhost:5000/user/{id}")
        session["username"] = user.json()["username"]
        session["email"] = user.json()["email"]
        return render_template("user.html")
    elif request.method == "POST" :
        username = request.form.get("username")
        email = request.form.get("email")
        
        validate_form = UpdateForm(username,email)
        validate_form.validate()
        if validate_form.is_valid():
            data = {"username":username,
                    "email":email}
            id = session["id"]
            response = requests.put(headers={"Accept":"application/json", "Content-Type": "application/json"},
                                        url=f"http://localhost:5000/user/{id}",
                                        json=data)
            if response.status_code == 200 :
                return redirect(url_for("user"))
            else :
                errors = response.json()["errors"]
                return render_template("user.html",errors=errors)
        else :
            errors = validate_form.errors
            return render_template("user.html",errors=errors)
    
@client.route('/user/delete',methods=["POST"])
def delete_user():
    id = session["id"]
    response = requests.delete(f"http://localhost:5000/user/{id}")
    flash("User was successfully deleted!")
    return redirect(url_for("index"))

@client.route('/article/create',methods=["GET","POST"])
def create_article():
    if request.method == "GET":
        return render_template('articleform.html')
    elif request.method == "POST":
        title = request.form.get("title")
        body = request.form.get("body")
        
        validate_form = ArticleForm(title,body)
        validate_form.validate()
        
        if validate_form.is_valid():
            user_id = session["id"]
            
            data = {"title":title,
                    "body":body,
                    "userId":user_id}
            
            response = requests.post(headers={"Accept":"application/json", "Content-Type": "application/json"},
                                            url="http://localhost:5000/article",
                                            json=data)
            if response.status_code == 201:
                flash("Article was successfully created")
                return redirect(url_for("index"))
            else :
                errors = response.json()["errors"]
                return render_template("articleform.html",errors=errors)
        else :
            errors = validate_form.errors
            return render_template("articleform.html",errors=errors)
            

@client.route('/article/<int:article_id>')
def article(article_id):
    response = requests.get(f"http://localhost:5000/article/{article_id}")
    if response.status_code == 200:
        article = response.json()
        return render_template("article.html",article=article)
    else :
        return "404 Article not found"
    
@client.route('/article/delete/<int:id>',methods=["POST"])
def delete_article(id):
    user_id = session["id"]
    response = requests.delete(headers={"Accept":"application/json", "Content-Type": "application/json"},
                                url=f"http://localhost:5000/article/{id}",
                                json={"userId":user_id})
    if response.status_code == 200:
        flash("Article was successfully deleted")
        return redirect(url_for("index"))
        
@client.route('/article/edit/<int:article_id>')
def edit_article(id, methods=["GET","POST"]):
    if request.method == "GET":
        return render_template('articleform.html')
    pass     

if __name__ == '__main__':
    client.run(host='0.0.0.0', port=3000, debug=True)