# project/models.py
"""

"""

import datetime

from project import db, bcrypt


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)

    def __init__(self, email, password, confirmed,
                 admin=False, confirmed_on=None):
        self.email = email
        self.password = bcrypt.generate_password_hash(password)
        self.registered_on = datetime.datetime.now()
        self.admin = admin
        self.confirmed = confirmed
        self.confirmed_on = confirmed_on

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<email {}'.format(self.email)


class Tracking(db.Model):

    __tablename__ = "tracking"

    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    post_ID = db.Column(db.Integer, nullable=False)
    user_ID = db.Column(db.Integer, nullable=False)
    ip = db.Column(db.Integer, nullable=False)
    
    def __init__(self, post_ID, user_ID, ip):
        self.post_ID = post_ID
        self.ip = ip
        self.user_ID = user_ID
        
    def get_id(self):
        return self.id


class Points(db.Model):
    __tablename__ = "points"

    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    user_ID = db.Column(db.Integer, nullable=False)
    post_ID = db.Column(db.Integer, nullable=False)
    earned_points = db.Column(db.Integer, default = 0)
    
    def __init__(self, user_ID, post_ID, earned_points):
        self.user_ID = user_ID
        self.post_ID = post_ID
        self.earned_points = earned_points
        
        
    def get_id(self):
        return self.id

class Posts(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    post_title = db.Column(db.String, nullable=False) 
    post_link = db.Column(db.String, unique=True, nullable=False)
    post_image = db.Column(db.String, default='')
    post_description = db.Column(db.String,default='')
    post_code = db.Column(db.String, unique=True, nullable=False)
    post_category = db.Column(db.String,default='')
    post_type = db.Column(db.String,default='article')
    

    def __init__(self, post_title, post_link, post_image, post_description, post_category, post_code):
        self.post_title = post_title
        self.post_link = post_link
        self.post_image = post_image
        self.post_description = post_description
        self.post_category = post_category
        self.post_code = post_code
        
    def get_id(self):
        return self.id

