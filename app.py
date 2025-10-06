from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    
    # Конфигурация
    UPLOAD_FOLDER = 'uploads'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.secret_key = 'your-secret-key-here-change-this-in-production'
    
    # Регистрация blueprint'ов
    from routes.main import main_bp
    from routes.music import music_bp
    from routes.sup import sup_bp
    from routes.books import books_bp
    from routes.games import games_bp
    from routes.study import study_bp
    from routes.admin import admin_bp  # Упрощенное имя
    
    app.register_blueprint(main_bp)
    app.register_blueprint(music_bp)
    app.register_blueprint(sup_bp)
    app.register_blueprint(books_bp)
    app.register_blueprint(games_bp)
    app.register_blueprint(study_bp)
    app.register_blueprint(admin_bp)  # Регистрируем админ blueprint
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True, ssl_context=('fullchain.pem', 'privkey.pem'))
