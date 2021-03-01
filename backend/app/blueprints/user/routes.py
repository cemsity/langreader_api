from flask import (
    Blueprint, 
    redirect,
    request
)

user = Blueprint('user', __name__)

@user.route("/login", methods=["POST"])
def login():
    """# TODO IMPLEMENT """
    
    pass

@user.route('/signup')
def signup():
    """# TODO IMPLEMENT """
    pass
