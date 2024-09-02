from Models.Model import Model
from flask import request, jsonify
from forms.articleForm import ArticleForm

def get_all_articles():
    return jsonify(Model.where("articles")),200

def store_article():
    data = request.get_json()
    title = data["title"]
    body = data["body"]
    user_id = data["userId"]
    validate_form = ArticleForm(title,body)
    
    validate_form.validate()
    if validate_form.is_valid():
        info = {"title":title,"body":body,"userId":user_id}
        id = Model.create("articles",info)
        return jsonify(Model.where("articles","id",id)),201
    else :
        return jsonify({"errors": validate_form.errors}),400
    
def read_article(id):
    info = Model.where("articles","id",id)
    if len(info)!=0:
        return jsonify(Model.where("articles","id",id)),200
    else:
        return jsonify({"errors":"Article not found"}),404
    
def update_article(id):
    data = request.get_json()
    new_title = data["title"]
    new_body = data["body"]
    user_id = data["userId"]
    
    validate_form = ArticleForm(new_title,new_body)
    
    if validate_form.is_valid():
        info = Model.where("articles","id",id)
        if len(info)!=0:
            if info["userId"] == user_id :
                Model.update("articles","title",id,new_title)
                Model.update("articles","body",id,new_body)
                return jsonify({"message":"Article updated successfully"}),200
            else :
                return jsonify({"errors":"You are not the owner of this article"}),401
        else :
            return jsonify({"errors":"Article not found"}),404
    else :
        return jsonify({"errors": validate_form.errors}),400
    
def delete_article(id):
    info = Model.where("articles","id",id)
    user_id = request.get_json()["userId"]
    if len(info)!=0:
        if info["userId"] == user_id :
            Model.delete("articles",id)
            return jsonify({"message":"Article deleted"}),200
        else :
            return jsonify({"errors":"You are not the owner of this article"}),401
    else :
        return jsonify({"errors":"Article not found"}),404