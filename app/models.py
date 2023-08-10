from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from datetime import datetime

""" class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    name = db.Column(db.String(128))
    surname = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    picture = db.Column(db.LargeBinary)
    profile = db.relationship('Profile', back_populates='user', uselist=False)

    def __repr__(self):
        return f'<User id: {self.id}, username: {self.username}, email: {self.email}>'
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    surname = db.Column(db.String(100))
    citizenship = db.Column(db.String(100))
    date_of_birth = db.Column(db.Date)
    date_of_registration = db.Column(db.Date)
    identity_card_number = db.Column(db.String(50))
    date_of_expiry = db.Column(db.Date)
    residence = db.Column(db.String(200))
    issued_by = db.Column(db.String(200))
    oib = db.Column(db.String(20))

    # Relationship with User model
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    user = db.relationship('User', back_populates='profile')

    def __repr__(self):
        return f"Profile({self.name}, {self.surname})"
    
class Reception(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    entry_date = db.Column(db.Date, nullable=False)
    entry_time = db.Column(db.Time, nullable=False)
    
    # Dodajemo relationship za povezivanje sa modelom Profile
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'), nullable=False)
    profile = db.relationship('Profile', backref='receptions')

    def __repr__(self):
        return f"<Reception {self.id}>"
     """
""" class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    name = db.Column(db.String(128))
    surname = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    picture = db.Column(db.LargeBinary)
    citizenship = db.Column(db.String(100))
    date_of_birth = db.Column(db.Date)
    date_of_registration = db.Column(db.Date)
    identity_card_number = db.Column(db.String(50))
    date_of_expiry = db.Column(db.Date)
    residence = db.Column(db.String(200))
    issued_by = db.Column(db.String(200))
    oib = db.Column(db.String(20))
    def __repr__(self):
        return f'<User id: {self.id}, username: {self.username}, email: {self.email}>'
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password) """

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    surname = db.Column(db.String(128))
    picture = db.Column(db.LargeBinary)
    sex = db.Column(db.String(10), nullable=True)
    country = db.Column(db.String(100), nullable=True)
    citizenship = db.Column(db.String(100), nullable=True) 
    date_of_birth = db.Column(db.Date)
    date_of_registration = db.Column(db.Date)
    identity_card_number = db.Column(db.String(50))
    date_of_expiry = db.Column(db.Date)
    residence = db.Column(db.String(200))
    issued_by = db.Column(db.String(200))
    oib = db.Column(db.String(20))
    front_document = db.Column(db.LargeBinary)
    back_document = db.Column(db.LargeBinary)

    def __repr__(self):
        return f'<User id: {self.id}>'
    

class Reception(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    entry_date = db.Column(db.Date, nullable=False)
    entry_time = db.Column(db.Time, nullable=False)
    
    user = db.relationship('User', backref='receptions')

    def __repr__(self):
        return f"<Reception {self.id}>"
    
    
@login.user_loader
def load_user(id):
    return User.query.get(int(id))