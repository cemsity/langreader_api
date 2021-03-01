import datetime
from typing import List, Any
from sqlalchemy.sql.operators import exists

from backend.app.extentions import db
from backend.app.models import article_word_table
from backend.app.blueprints.user.model import User

class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    word = db.Column(db.String, nullable=False)
    level = db.Column(db.Integer, default=0)
    language = db.Column(db.String, default="N/S") #Posible enum mayby use pycountry Rember ath only languages in Spacy will be supported
    definition = db.Column(db.String)
    part_of_speach = db.Column(db.String)
    tags = db.Column(db.String)
    articles = db.relationship(
        "Article",
        secondary= article_word_table,
        back_populates="words"
    )

    __table_args__ = (db.UniqueConstraint(user_id, word, language,  name="_user_word_lang_uc"),)

    def __init__(self, user, word:str, language:str, definition=None, part_of_speach=None, *args, **kwargs ):
        super().__init__(*args, **kwargs)
        self.user= user
        self.word= str.lower(word)
        self.language = language
        self.definition = definition
        self.part_of_speach = part_of_speach
        

    def __repr__(self):
        return f'<Word: {self.word}>'
    
    
    @classmethod
    def new_word(cls, user:User, word:str, lang:str):
        res = cls.query.filter_by(user_id=user.id, word=word, language=lang).first()
        if res:
            return res
        return cls(user=user, word=word, language=lang)
    
    @classmethod
    def get_all(cls) -> List[Any]: #words is the datatype but I am not going to fix the typing python typing issue yet.
        return cls.query.all()

    def update(self, *args, **kwargs):
        if word := kwargs.get("word"):
            self.word = word
        if level := kwargs.get("level"):
            self.level = level
        if language:= kwargs.get("language"):
            self.language = language
        if definition := kwargs.get("definition"):
            self.definition = definition
        if pos := kwargs.get("pos"):
            self.part_of_speach = pos
        db.session.add(self)
        db.session.commit()
        return True
    
    def level_up(self):
        self.level += 1
        db.session.add(self)
        db.session.commit()
    
    def level_down(self):
        self.level -= 1
        db.session.add(self)
        db.session.commit()
    