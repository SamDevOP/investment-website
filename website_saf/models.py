from app import db
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String())
    phone = db.Column(db.String())
    passcode = db.Column(db.String())
    referal_code = db.Column(db.String())
    def __init__(self, email, phone, passcode,referal_code):
        self.email = email
        self.phone = phone
        self.passcode = passcode
        self.referal_code =referal_code
    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id, 
            'email': self.email,
            'phone': self. phone,
            'passcode':self.passcode,
            'referal_code':self.referal_code
        }
