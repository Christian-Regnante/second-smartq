from flask import Flask
from flask_migrate import Migrate
from config import Config
from app.models import db

migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Register blueprints
    from app.routes import client, staff, admin, super_admin
    
    app.register_blueprint(client.bp)
    app.register_blueprint(staff.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(super_admin.bp)

    # Home route
    @app.route('/')
    def index():
        return '''
        <html>
        <head>
            <title>SmartQ - Queue Management System</title>
            <style>
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    margin: 0;
                    padding: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    min-height: 100vh;
                }
                .container {
                    background: white;
                    padding: 3rem;
                    border-radius: 20px;
                    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                    text-align: center;
                    max-width: 600px;
                }
                h1 {
                    color: #667eea;
                    margin-bottom: 0.5rem;
                    font-size: 2.5rem;
                }
                .subtitle {
                    color: #666;
                    margin-bottom: 2rem;
                    font-size: 1.1rem;
                }
                .links {
                    display: flex;
                    flex-direction: column;
                    gap: 1rem;
                }
                a {
                    display: block;
                    padding: 1rem 2rem;
                    background: #667eea;
                    color: white;
                    text-decoration: none;
                    border-radius: 10px;
                    font-size: 1.1rem;
                    transition: all 0.3s ease;
                }
                a:hover {
                    background: #764ba2;
                    transform: translateY(-2px);
                    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
                }
                .version {
                    margin-top: 2rem;
                    color: #999;
                    font-size: 0.9rem;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🎯 SmartQ</h1>
                <p class="subtitle">Modern Queue Management for Rwanda</p>
                <div class="links">
                    <a href="/client">📱 Client Kiosk</a>
                    <a href="/staff/login">👨‍💼 Staff Dashboard</a>
                    <a href="/admin/login">⚙️ Admin Panel</a>
                    <a href="/super-admin/login">⚙️ Super Admin Panel</a>
                </div>
                <p class="version">Version 1.0.0 MVP</p>
            </div>
        </body>
        </html>
        '''
    
    # Create tables
    with app.app_context():
        db.create_all()
        create_initial_data()
    
    return app

def create_initial_data():
    """Create initial super admin if database is empty"""
    from app.models import User
    
    # Check if super admin exists
    super_admin = User.query.filter_by(role='super_admin').first()
    if not super_admin:
        admin = User(
            username='superadmin',
            role='super_admin'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("✅ Initial super admin created: username='superadmin'/ password='admin123'")