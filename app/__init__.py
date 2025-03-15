from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

# Initialize SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize SQLAlchemy with the app
    db.init_app(app)

    # Import models here to avoid circular imports
    from app.models import Role, User
    app.config['SECRET_KEY'] = 'your-secret-key-here'
    # Create tables if they don't exist
    with app.app_context():
        db.create_all()
        print("Tables created successfully!")

        # Create sample data if the database is empty
        if not Role.query.first():  # Check if the database is empty
            create_sample_data()

    # Register blueprints
    from app.routes.manager import manager_bp
    from app.routes.staff import staff_bp
    from app.routes.supplier import supplier_bp
    from app.routes.auth import auth_bp

    app.register_blueprint(manager_bp)
    app.register_blueprint(staff_bp)
    app.register_blueprint(supplier_bp)
    app.register_blueprint(auth_bp)

    return app

def create_sample_data():
    # Import models here to avoid circular imports
    from app.models import Role, User

    try:
        # Create sample roles
        manager_role = Role(role_name='manager')
        staff_role = Role(role_name='staff')
        supplier_role = Role(role_name='supplier')

        db.session.add(manager_role)
        db.session.add(staff_role)
        db.session.add(supplier_role)
        db.session.commit()

        # Create sample users with hashed passwords
        manager_user = User(
            username='manager1',
            password_hash='password1',  # Use a proper password hashing library
            role=manager_role.role_id
        )
        staff_user = User(
            username='staff1',
            password_hash='password2',  # Use a proper password hashing library
            role=staff_role.role_id
        )
        supplier_user = User(
            username='supplier1',
            password_hash='password3',  # Use a proper password hashing library
            role=supplier_role.role_id
        )

        db.session.add(manager_user)
        db.session.add(staff_user)
        db.session.add(supplier_user)
        db.session.commit()

        print("Sample data created successfully!")
    except Exception as e:
        db.session.rollback()
        print(f"Error creating sample data: {e}")