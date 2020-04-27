from db import db


class AddressModel(db.Model):
    __tablename__ = 'addresses'

    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(80), nullable=False)
    city = db.Column(db.String(80), nullable=False)
    province = db.Column(db.String(80), nullable=False)
    line1 = db.Column(db.String(80), nullable=False)
    line2 = db.Column(db.String(80))
    latitude = db.Column(db.String(80))
    longitude = db.Column(db.String(80))
    user_phone_number = db.Column(db.String(80),nullable=False)
    address_phone_number = db.Column(db.String(80))

    def __init__(self, country, city, province, line1,line2,latitude,longitude,user_phone_number,address_phone_number):
        self.country = country
        self.city = city
        self.province = province
        self.line1 = line1
        self.line2 = line2
        self.latitude = latitude
        self.longitude = longitude
        self.user_phone_number = user_phone_number
        self.address_phone_number = address_phone_number

    def json(self):
        return {'id': self.id, 'country': self.country, 'province': self.province,
                'line1': self.line1, 'line2': self.line2,'latitude':self.latitude,'longitude':self.longitude,
                'user_phone_number':self.user_phone_number,'address_phone_number':self.address_phone_number}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod  #  using class name User
    def find_by_phone_number(cls, phone_number):  #  cls was self
        return cls.query.filter_by(user_phone_number=phone_number).all()

    @classmethod  #  using class name User
    def find_by_id(cls, _id):  #  cls was self
        return cls.query.filter_by(id=_id).first()