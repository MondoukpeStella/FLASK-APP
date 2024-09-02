from Config.db import get_db, init_db
import os
from flask import current_app
from werkzeug.security import generate_password_hash

def query_db(query, args=(), action="get", one=False):
        if not os.path.exists('db.sqlite'):
            with current_app.app_context():
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

class Model :
    
    def create(table,data):
        if table == "users":
            username,email,password = data["username"],data["email"],data["password"]
            password_hashed = generate_password_hash(password)
            id = query_db("INSERT INTO users (username,email,password) VALUES(?,?,?)",args=(username,email,password_hashed),action="post")
            return id
        elif table == "articles":
            title,body,user_id = data["title"],data["body"],data["userId"]
            id = query_db("INSERT INTO articles (title,body,creationDate,userId) VALUES(?,?,DATE(),?)",args=(title,body,user_id),action="post")
            return id
    
    def where(table,field=None,input=None):
        result = []
        datas = []
        if table == "users":
            if field and input :
                datas = []
                response = query_db(f"SELECT * FROM users WHERE {field} = ?",args=(input,))
                if len(response) !=0:
                    for user in response :
                        for info in user : 
                            datas.append(info) 
                    return {"_id":datas[0],"username":datas[1],"email":datas[2],"password":datas[3]}
                else:
                    return []
            else :
                response = query_db("SELECT * FROM users")
                for user in response :
                    for info in user :
                        datas.append(info)
                for i in range(0,len(datas),4) :
                    id = datas[i]
                    username = datas[i+1]
                    email = datas[i+2]
                    result.append({"_id":id,"username":username,"email":email})
                return result
        elif table == "articles":
            if field and input :
                response = query_db(f"SELECT * FROM articles WHERE {field} = ?",args=(input,))
                if len(response) !=0:
                    for user in response :
                        for info in user : 
                            datas.append(info) 
                    return {"_id":datas[0],"title":datas[1],"body":datas[2],"creationDate":datas[3],"userId":datas[4]}
                else:
                    return []
            else :
                
                response = query_db("SELECT * FROM articles")
                for article in response :
                    for info in article :
                        datas.append(info)
                for i in range(0,len(datas),5) :
                    id = datas[i]
                    title = datas[i+1]
                    body = datas[i+2]
                    creation_date = datas[i+3]
                    user_id = datas[i+4]
                    result.append({"_id":id,"title":title,"body":body,'creationDate':creation_date,'userId':user_id})
                return result
        
    def update(table,field,id,value):
        if table == "users":
            query_db(f"UPDATE users SET {field} = ? WHERE id = ?", args=(value,id,), action="post")
        elif table == "articles":
            query_db(f"UPDATE articles SET {field} = ? WHERE id = ?", args=(value,id,), action="post")

    def delete(table,id):
        if table == "users":
            query_db("DELETE FROM users WHERE id = ?",args=(id,),action="post")
        elif table == "articles":
            query_db("DELETE FROM articles WHERE id = ?",args=(id,),action="post")
        