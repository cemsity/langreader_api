from ..article import bp
from ..article.model import Article
from backend.app.extentions import db 
from flask import jsonify, request
from typing import List
from backend.app.blueprints import article
from backend.app.blueprints.user.model import User


@bp.route('/articles', methods=["GET"])
def get_list_of_articles():
    all_articles = Article.query.all()
    return jsonify(build_articles_response(all_articles))


@bp.route('/article/id/<id>', methods=["GET"])
def get_article_by_id(id:int):
    article: Article = Article.query.filter_by(id=id).first()
    if article:
        return jsonify(build_article_response(article))
    return f"Article id: {id} is not found", 404

@bp.route('/article/title/<title>')
def get_article_by_title(title:str):
    articles: Article = Article.query.filter_by(title=title).all()
    if len(articles) == 1:
        return jsonify(build_article_response(articles[0]))
    elif len(articles) > 1:
        return jsonify(build_articles_response(articles))
    else:
        return f"Article title:{title} is not found", 404

@bp.route("/article/new", methods=["POST"])
def create_article():
    req = request.get_json()
    user = User.query.filter_by(id=req["user"]).first()
    if user:
        article = Article(user=user, title=req["title"], text=req["text"])
        db.session.add(article)
        db.session.commit()
        return f"Article:{req['title']} successfully added", 200
    return f"User id: {req['user']} not found", 404

@bp.route("/article/update", methods=["PUT"])
def update_article():
    req = request.get_json()
    if "id" in req:
        article = Article.query.filter_by(id=req["id"]).first()
        if article:
            worked = article.update(**req)
            if worked:
                return f"Article id: {req['id']} has been updated", 200
            return f"Article id: {req['id']} has not been updated", 500
        return f"Article id: {req['id']} has not been found", 404
    return f'ID of Article required ', 400

@bp.route("/article/<id>", methods=["DELETE"])
def delete_article(id:int):
    art = Article.query.filter_by(id=id).one()
    if art:
        db.session.delete(art)
        db.session.commit()
        return f"Article ID: {id} has been deleted", 200
    return f"Article ID: {id} has not been found", 404

def build_article_response(article: Article):
        return {
            "id": article.id,
            'user_id': article.user_id,
            "title": article.title,
            "text" : article.text,
            "words": [{"id": w.id, "word": w.word, "level": w.level} for w in article.words]
        }

def build_articles_response(articles: List[Article]):
    out = dict(articles = [])
    out["articles"] = [{"id":art.id, "user_id":art.user_id, "title":art.title} for art in articles]
    return out 