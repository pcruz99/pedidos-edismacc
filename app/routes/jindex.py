from flask import Blueprint, url_for, redirect

index = Blueprint('index', __name__)

@index.route('/', methods=['GET'])
def Index():
    return redirect(url_for('auth.login'))