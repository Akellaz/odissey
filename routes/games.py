from flask import Blueprint, render_template

games_bp = Blueprint('games', __name__)

@games_bp.route('/game')
def game():
    return render_template('g.html')

@games_bp.route('/game.js')
def game_js():
    return render_template('game.js')
