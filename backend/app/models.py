from datetime import datetime
from .extentions import db
from enum import Enum, unique

article_word_table = db.Table("article_words",
    db.Column("article_id", db.Integer, db.ForeignKey("article.id"), primary_key=True),
    db.Column("word_id", db.Integer, db.ForeignKey("word.id"), primary_key=True)
)
@unique
class Language(Enum):
    FRENCH = "FR"
    ENGLISH = "EN"
    SPANISH = "ES"
    