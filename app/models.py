from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


# Create many-to-many mapping from groups to users using a helper table.
groups = db.Table(
    'groups',
    db.Column("group_id", db.Integer, db.ForeignKey("group.id"), primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),    
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    words = db.relationship("Slang", backref="author", lazy="dynamic")
    groups = db.relationship(
        "Group", 
        secondary=groups, 
        lazy="subquery",
        backref=db.backref("groups", lazy=True),
        overlaps="users, groups",
    )

    def __repr__(self):
        return f"<User {self.username}>"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Slang(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(56))
    meaning = db.Column(db.String(280))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return f"<Word {self.word}>"


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True)
    users = db.relationship(
        "User", 
        secondary=groups, 
        lazy="subquery",
        backref=db.backref("users", lazy=True),
        overlaps="groups, users",
    )


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
