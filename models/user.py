from db import db


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    phone_number = db.Column(db.String(80), unique=True, nullable=False)
    authorized_store_id = db.Column(db.Integer)
    role = db.Column(db.String(80), nullable=False)

    def __init__(self, name, password, phone_number, authorized_store_id, role):
        self.name = name
        self.password = password
        self.phone_number = phone_number
        self.authorized_store_id = None
        self.role = role

    def json(self):
        return {'id': self.id, 'name': self.name, 'phone_number': self.phone_number,
                'authorized_store_id': self.authorized_store_id, 'role': self.role}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod  #  using class name User
    def find_by_name(cls, name):  #  cls was self
        return cls.query.filter_by(name=name).first()

    @classmethod  #  using class name User
    def find_by_id(cls, _id):  #  cls was self
        return cls.query.filter_by(id=_id).first()

    @classmethod  #  using class name User
    def find_by_phone_number(cls, phone_number):  #  cls was self
        return cls.query.filter_by(phone_number=phone_number).first()
