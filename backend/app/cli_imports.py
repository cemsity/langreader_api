from backend.app.app import create_app, db 


from backend.app.models import article_word_table
from backend.app.blueprints.user.model import User
from backend.app.blueprints.article.model import Article
from backend.app.blueprints.word.model import Word

app = create_app()



@app.shell_context_processor
def make_shell_context() -> dict:
    return {
        "db": db, 
        "User": User,
        "Article": Article,
        "Word": Word,
        "article_word_table":article_word_table
    }