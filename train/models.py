from train import db, user_login_manager
from flask_login import UserMixin

@user_login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class Admin(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)

	def __repr__(self):
		return f"Admin('{self.username}', '{self.email}')"

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)
	passengers = db.relationship('Passenger', backref='booker', lazy=True)

	def __repr__(self):
		return f"User('{self.username}', '{self.email}')"

class Passenger(db.Model):
	pass_id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(20),nullable=False)
	age = db.Column(db.Integer,nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
	source = db.Column(db.String(20),nullable=False)
	destination = db.Column(db.String(20),nullable=False)
	tier = db.Column(db.String(20),nullable=False)
	date = db.Column(db.String(20),nullable=False)
	train_no = db.Column(db.String(20),nullable=False)
	ticket = db.relationship('Ticket',backref='passenger',lazy=True,uselist=False)  #uselist=False implies one-to-one relationship
	def __repr__(self):
		return f"Passenger('{self.pass_id}','{self.name}','{self.age}','{self.user_id}')"

class Ticket(db.Model):
	pnr_number = db.Column(db.String(10),primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
	destination = db.Column(db.String(20),nullable=False)
	source = db.Column(db.String(20),nullable=False)
	journey_date = db.Column(db.String(20),nullable=False)
	seat_no = db.Column(db.Integer,nullable=False)
	pass_id = db.Column(db.Integer,db.ForeignKey('passenger.pass_id'),nullable=False)
	train_no = db.Column(db.Integer,db.ForeignKey('train.train_no'),nullable=False)
	tier = db.Column(db.String(20),nullable=False)
	fare = db.Column(db.String(20),nullable=False)
	def __repr__(self):
		return f"Ticket('{self.pnr_number}', '{self.source}', '{self.destination}', '{self.journey_date}', '{self.train_no}', '{self.seat_no}', '{self.pass_id}','{self.fare}')"

class Train(db.Model):
	train_no = db.Column(db.Integer,primary_key=True)
	train_name = db.Column(db.String(30),unique=True,nullable=False)
	source = db.Column(db.String(20),nullable=False)
	destination = db.Column(db.String(20),nullable=False)
	monday = db.Column(db.Integer,nullable=False,default=0)
	tuesday = db.Column(db.Integer,nullable=False,default=0)
	wednesday = db.Column(db.Integer,nullable=False,default=0)
	thursday = db.Column(db.Integer,nullable=False,default=0)
	friday = db.Column(db.Integer,nullable=False,default=0)
	saturday = db.Column(db.Integer,nullable=False,default=0)
	sunday = db.Column(db.Integer,nullable=False,default=0)
	ac_first_class_coaches = db.Column(db.Integer,nullable=False)
	ac_two_tier_coaches = db.Column(db.Integer,nullable=False)
	ac_three_tier_coaches = db.Column(db.Integer,nullable=False)
	sleeper_class_coaches = db.Column(db.Integer,nullable=False)
	ac_first_class_available_seats = db.Column(db.Integer,nullable=False)
	ac_two_tier_available_seats = db.Column(db.Integer,nullable=False)
	ac_three_tier_available_seats = db.Column(db.Integer,nullable=False)
	sleeper_class_available_seats = db.Column(db.Integer,nullable=False)
	ac_first_class_fare = db.Column(db.Integer,nullable=False)
	ac_two_tier_fare = db.Column(db.Integer,nullable=False)
	ac_three_tier_fare = db.Column(db.Integer,nullable=False)
	sleeper_class_fare = db.Column(db.Integer,nullable=False)
	departure = db.Column(db.String(10),nullable=False)
	arrival = db.Column(db.String(10),nullable=False)
	total = db.Column(db.String(10),nullable=False)

	def __repr__(self):
		return f"Train('{self.train_no}', '{self.train_name}')"

class SeatStatus(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	train_no = db.Column(db.Integer, nullable=False)
	seat_no = db.Column(db.Integer, nullable=False)
	pass_id = db.Column(db.Integer, nullable=False, default=0)
	seat_type = db.Column(db.String(20), nullable=False)
	def __repr__(self):
		return f"Ticket('{self.id}', '{self.train_no}', '{self.seat_no}',  '{self.pass_id}')"


class Station(db.Model):
	station_id = db.Column(db.Integer,primary_key=True)
	station_name = db.Column(db.String(20),nullable=False,unique=True)
	# train_source = db.relationship('Train',backref='starting_trains',lazy=True)
	# train_destination = db.relationship('Train',backref='ending_trains',lazy=True)

	def __repr__(self):
		return f"Station('{self.station_id}', '{self.station_name}')"

