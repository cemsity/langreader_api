import datetime
import re 
from backend.app.blueprints.word.model import Word
from backend.app.extentions import db
from backend.app.models import Language, article_word_table
 

class Article(db.Model):    
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String, nullable=False)
    text = db.Column(db.Text(convert_unicode=True), nullable=False)
    language = db.Column(db.String, default="N/S")
    words = db.relationship(
        "Word", 
        secondary=article_word_table,
        back_populates="articles"
        )

    
    def __init__(self, title, text, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = title
        self.text = text
        word_set = Article.setify(text)
        self.make_words(word_set)



    
    @classmethod
    def setify(cls, string:str ) -> set: 
        raw_list = re.split(r"\W+", string)
        return set(map(lambda x: x.lower(), raw_list))
    
    def update(self, *args, **kwargs):
        if lang := kwargs.get('language'):
            self.language = lang
        if title := kwargs.get("title"):
            self.title = title
        if text := kwargs.get('text'):
            self.text = text
            word_set = self.setify(text)
            self.make_words(word_set)
        db.session.add(self)
        db.session.commit()
        return True
    
    def make_words(self, word_set):
        
        for word in word_set: 
            self.words.append(self.make_word(word))

    def make_word(self, word):
        return Word.new_word(user=self.user, word=word, lang=self.language)

    def __repr__(self):
        return f'<Artcle: {self.title}>'
    