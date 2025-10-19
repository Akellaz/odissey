from flask import Flask

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
    from routes.study import study_bp
    from routes.admin import admin_bp
    
    # Новый blueprint для ассистента
    from assistant.routes import assistant_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(music_bp)
    app.register_blueprint(sup_bp)
    app.register_blueprint(books_bp)
    app.register_blueprint(study_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(assistant_bp)  # Регистрируем ассистент
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True, ssl_context=('fullchain.pem', 'privkey.pem'))
