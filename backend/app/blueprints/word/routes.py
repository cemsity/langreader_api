from ..word import bp
from ..word.model import Word
from backend.app.extentions import db 
from flask import jsonify, request
from typing import List
from backend.app.blueprints import word
from backend.app.blueprints.user.model import User
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

@bp.route("/words")
def get_all_words():
    words = Word.get_all()
    return jsonify(build_words_response(words))

@bp.route('/words/language/<lang>')
def get_words_by_language(lang:str):
    words = Word.query.filter_by(language=lang).all()
    if words:
        return jsonify(build_words_response(words))
    return f"Words with Language: {lang} were not found", 404

@bp.route("/words/pos/<pos>")
def get_words_by_pos(pos:str):
    words = Word.query.filter_by(part_of_speach=pos).all()
    if words:
        return jsonify(build_words_response(words))
    return f"Words with pos: {pos} were not found", 404

@bp.route("/words/user/<id>")
def get_words_by_user(id: int):
    words = Word.query.filter_by(user_id=id).all()
    if words:
        return jsonify(build_words_response(words))
    return f"Words with User_ID: {id} were not found", 404

@bp.route("/word/create", methods=["POST"])
def create_word():
    req = request.get_json()
    try:
        user = User.query.filter_by(id=req["user_id"]).one()
        word = Word(user=user,
                    word=req["word"],
                    language=req["language"],
                    definition=req.get("definition"),
                    part_of_speach= req.get("pos"))
        db.session.add(word)
        db.session.commit()
        return f"Word: {word} was created", 200
    except NoResultFound as nrf:
        return f'User not Found {nrf}', 404
    except ValueError as ve:
        return f'Improper Request: {ve}', 400
    except Exception as e:
        return f"Exception: {e}", 500

@bp.route('/word/id/<id>')
def get_word_by_id(id:int):
    try:
        word = Word.query.filter_by(id=id).one()
    except NoResultFound as nrf:
        return f"Word id: {id} has not been found", 404
    return build_word_response(word)
    

@bp.route('/word/update', methods=["PUT"])
def update_word():
    req = request.get_json()
    try:
        word = Word.query.filter_by(id=req["id"]).one()
    except NoResultFound as nrf:
        return f"Word id: {id} has not been found", 404
    worked = word.update(**req)
    if worked:
        return f"Word id: {id} has been updated", 200
    return f"Word id: {id} has not been updated", 500

@bp.route('/word/levelup/<id>', methods=["POST"])
def level_up_word(id:int):
    try:
        word = Word.query.filter_by(id=id).one()
    except NoResultFound as nrf:
        return f"Word id: {id} has not been found", 404
    word.level_up()
    return jsonify(build_word_response(word))


@bp.route('/word/leveldown/<id>', methods=["POST"])
def level_down_word(id:int):
    try:
        word = Word.query.filter_by(id=id).one()
    except NoResultFound as nrf:
        return f"Word id: {id} has not been found", 404
    word.level_down()
    return jsonify(build_word_response(word))
    # return f"Word: {word.word} has leveled down" , 200

@bp.route('/word/<id>', methods=["DELETE"])
def delete_word(id:int):
    try:
        word = Word.query.filter_by(id=id).one()
    except NoResultFound as nrf:
        return f"Word id: {id} has not been found", 404
    db.session.delete(word)
    db.session.commit()
    return f'Word Id: {id} has been deleted', 200


def build_words_response(words):
    return dict(words=[build_word_response(w) for w in words])

def build_word_response(word):
    return dict(id=word.id,
                word=word.word,
                level=word.level,
                language=word.language)