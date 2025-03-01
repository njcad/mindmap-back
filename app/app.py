# from flask import Flask
# from flask_cors import CORS
# from routes.session_routes import session_bp
# from routes.question_routes import question_bp
# from routes.main_routes import main_bp
# from models.session import SessionManager

# app = Flask(__name__)
# session_manager = SessionManager()

# CORS(app, 
#      origins=["http://localhost:5173", "http://127.0.0.1:3000", "http://10.27.128.109:5173"],  # Specify your frontend origin
#      methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
#      allow_headers=["Content-Type", "Authorization"],
#      supports_credentials=True)

# CORS(app, 
#      resources={r"/api/*": {  # Apply to all /api/ routes
#          "origins": ["http://localhost:5173", "http://127.0.0.1:3000"],
#          "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
#          "allow_headers": ["Content-Type", "Authorization"],
#          "supports_credentials": True
#      }},
#      expose_headers=["Content-Range", "X-Content-Range"]
# )

# Register blueprints
# app.register_blueprint(main_bp)
# app.register_blueprint(session_bp, url_prefix='/api/session')
# app.register_blueprint(question_bp, url_prefix='/api/questions')

# # Pass session_manager to blueprints
# session_bp.session_manager = session_manager
# question_bp.session_manager = session_manager

# if __name__ == '__main__':
#     app.run(debug=True)
