# This file holds the main routes for the application and also the homepage functionality.

from flask import Blueprint, render_template
from flask_login import login_required, current_user

bp = Blueprint('main', __name__)

@bp.route('/')

@bp.route('/index')

# This makes sure the user is logged in to access the homepage
@login_required
def index():
    return render_template('index.html', title='Home', user=current_user)
