from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()

class Organization(db.Model):
    __tablename__ = 'organizations'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200))
    contact = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    admins = db.relationship('User', backref='organization', lazy=True, 
                            foreign_keys='User.organization_id')
    services = db.relationship('Service', backref='organization', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'contact': self.contact,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # super_admin, admin, staff
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    service = db.relationship('Service', backref='staff_members', foreign_keys=[service_id])
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'role': self.role,
            'organization_id': self.organization_id,
            'service_id': self.service_id
        }

class Service(db.Model):
    __tablename__ = 'services'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)
    counter_number = db.Column(db.String(20))
    avg_service_time = db.Column(db.Integer, default=10)  # minutes
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    queue_items = db.relationship('QueueItem', backref='service', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'organization_id': self.organization_id,
            'counter_number': self.counter_number,
            'avg_service_time': self.avg_service_time,
            'is_active': self.is_active
        }

class QueueItem(db.Model):
    __tablename__ = 'queue_items'
    
    id = db.Column(db.Integer, primary_key=True)
    queue_number = db.Column(db.String(20), nullable=False, index=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    status = db.Column(db.String(20), default='waiting')  # waiting, serving, done, skipped
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    called_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    
    def to_dict(self):
        return {
            'id': self.id,
            'queue_number': self.queue_number,
            'service_id': self.service_id,
            'phone_number': self.phone_number,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'called_at': self.called_at.isoformat() if self.called_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }