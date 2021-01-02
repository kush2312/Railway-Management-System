from train import db
from train.models import Admin, User, Passenger, Ticket, Train , Station, SeatStatus
from train import bcrypt

db.create_all()
hashed_pw = bcrypt.generate_password_hash("admin123").decode('utf-8')
admin = Admin(username='admin', email="admin@train.com", password=hashed_pw)
db.session.add(admin)
db.session.commit()