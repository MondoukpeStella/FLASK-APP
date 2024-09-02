import os
from flask import Flask, render_template, request
from Config.db import init_app, init_db, get_db
from Controllers.usersController import *   
from Controllers.articlesController import * 
   
app = Flask(__name__)

app.config.from_object(__name__) 

app.config.from_mapping(
    DATABASE = os.path.join(app.root_path, 'db.sqlite'),
    SECRET_KEY = os.urandom(22),
    USERNAME = 'admin',
    PASSWORD = 'default'
)

def query_db(query, args=(), action="get", one=False):
        if not os.path.exists('db.sqlite'):
            with app.app_context():
                init_db()
        cur = get_db().execute(query, args)
        if action == "get" :
            
            rv = cur.fetchall()
            cur.close()
            return (rv[0] if rv else None) if one else rv    

        elif action == "post":
            get_db().commit()
            rv = cur.lastrowid
            return rv  

init_app(app)
    
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST" :
        return create_user()  
    
@app.route('/login', methods=["GET", "POST"])
def login():   
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST" :
        return log_user()
    
@app.route('/users')
def index():
    return get_all_users()
        
@app.route('/user/<int:id>', methods=["GET","PUT","DELETE"])
def user(id):
    if request.method == "GET":
        if id == 0:
            return get_all_users()
        else :
            return read_user(id)
    elif request.method == "PUT":
        return update_user(id)
    elif request.method == "DELETE":
        return delete_user(id)
    
@app.route('/article',methods=["GET","POST"])
def create_article():
    if request.method == "GET":
        return render_template("articleform.html")
    elif request.method == "POST" :
        return store_article()

@app.route('/article/<int:article_id>',methods=["GET","PUT","DELETE"])
def show_article(article_id):
    if request.method == "GET":
        if article_id == 0:
            return get_all_articles()
        else :
            return read_article(article_id)
    elif request.method == "PUT":
        return update_article(article_id)
    elif request.method == "DELETE":
        return delete_article(article_id)

    
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000, debug=True)



  

    
    