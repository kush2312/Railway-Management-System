from train import app, db, bcrypt
from flask import render_template, url_for, flash, redirect, request, session, make_response
from train.models import Admin, User, Train, Passenger, SeatStatus, Ticket
from train.forms import AddTrain, UpdateTrain, RegistrationForm, LoginForm, AdminLoginForm ,CancelBookingForm ,BookTicket , UpdateAccountForm
from flask_login import login_user, current_user, logout_user, login_required
import datetime
from datetime import time
import pdfkit

adminLog = 0    #To check if admin is logged in or not
config = pdfkit.configuration(wkhtmltopdf='/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')

def is_time_between(begin_time, end_time, check_time=None):
    # If check time is not given, default to current UTC time
    check_time = check_time or datetime.utcnow().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time

@app.route('/')
@app.route('/home')
def home():
	return render_template('index.html',admin=adminLog)

@app.route('/book_ticket',methods=['GET','POST'])
@login_required
def bookTicket():
	
	if session["adminLog"] == 1:
		session["adminLog"] = 0
	form =BookTicket()
	if request.method=='POST':
		session["source"] = (form.source.data).source
		session["destination"]=(form.destination.data).destination
		session["date"]=form.date.data
		print(type(session["date"]))
		print(session["date"])
		session["tier"]=form.tier.data
		print(session["source"],type(session["tier"]))
		print("Hello")
		print(session["tier"])
		if(session["date"]< datetime.date.today()):
			flash('Please select a proper date', 'danger')
			return redirect(url_for('bookTicket'))
		else:
			return redirect(url_for('availableTrain'))
	else:
		return render_template('book_ticket.html', title= "Book Ticket", form=form,admin = session["adminLog"])


@app.route('/book_ticket/available_train',methods=['GET','POST'])
@login_required
def availableTrain():
	if session["adminLog"] == 1:
		session["adminLog"] = 0
	arr = session['date'].split(',')
	print(arr[1][13:])
	ans=arr[0]
	week = {'monday':'Mon','tuesday':'Tue','wednesday':'Wed','thursday':'Thu','friday':'Fri','saturday':'Sat','sunday':'Sun'}
	train_class = {'1A':'ac_first_class_available_seats','2A':'ac_two_tier_available_seats','3A':'ac_three_tier_available_seats','Sl':'sleeper_class_available_seats'}
	selected_trains = [train for train in Train.query.filter_by(source = session["source"], destination=session["destination"])]
	if request.method=='POST':
		session["train_no"] = request.form['select_train']
		return redirect(url_for('addPassenger'))		
	
	return render_template('available_trains.html', selected_trains=selected_trains,source = session['source'],destination=session['destination'],ans=ans,week=week,train_class=train_class,tier = session['tier'])


@app.route('/book_ticket/add_passengers', methods=['GET','POST'])
@login_required
def addPassenger():
	if session["adminLog"] == 1:
		session["adminLog"] = 0
	if request.method == "POST":
		if 'passengers' in request.form:
			session["passengers"] = int(request.form["passengers"])
			return render_template('add_passengers.html',title="Add Passengers",passengers=session["passengers"],admin = session["adminLog"],loaded=True)
		elif 'addp' in request.form:		
			form = request.form	
			print(session['source'],session['destination'])
			for i in range(session['passengers']):
				passenger = Passenger(name =form[f"name{i+1}"], age= form[f"age{i+1}"], user_id=current_user.id,source=session['source'],destination=session['destination'],tier=session['tier'],train_no=session['train_no'],date=session['date'])
				seat = SeatStatus.query.filter_by(train_no = session['train_no'],  pass_id=0, seat_type=session['tier']).first()
				seat_no = seat.seat_no
				print(seat_no)
				pnr_no = int(session['train_no'])*10000 + int(seat_no)			
				db.session.add(passenger)
				db.session.commit()
				seat.pass_id= passenger.pass_id	
				train = Train.query.filter_by(train_no = session['train_no']).first()
				passenger_class = {'1A': train.ac_first_class_fare,'2A':train.ac_two_tier_fare,'3A':train.ac_three_tier_fare,'Sl':train.sleeper_class_fare}
				print(session["date"],type(session["date"]))
				journey_date = session['date'].split(',')[1][:13] + train.departure + " IST"
				ticket = Ticket(pnr_number = pnr_no,user_id=current_user.id, source=session['source'], destination=session['destination'], journey_date=journey_date, seat_no=seat_no, pass_id=passenger.pass_id, train_no=session['train_no'], tier=session['tier'],fare = str(passenger_class[session['tier']]))
				db.session.add(ticket)
				if session["tier"]=="1A":
					train.ac_first_class_available_seats = train.ac_first_class_available_seats-1
					print(train.ac_first_class_available_seats)
				elif session["tier"]=="2A":
					train.ac_two_tier_available_seats = train.ac_two_tier_available_seats-1
					print(train.ac_two_tier_available_seats)
				elif session["tier"]=="3A":
					train.ac_three_tier_available_seats = train.ac_three_tier_available_seats-1
					print(train.ac_three_tier_available_seats)
				elif session["tier"]=="Sl":
					train.sleeper_class_available_seats = train.sleeper_class_available_seats-1
					print(train.sleeper_class_available_seats)
			db.session.commit()
			flash('Ticket has been booked successfully', 'info')
			return redirect(url_for('myBookings'))
	return render_template('add_passengers.html',title="Add Passengers",passengers=0,admin = session["adminLog"],loaded=False)


@app.route('/train_status')
@login_required
def trainStatus():
	
	if session["adminLog"] == 1:
		session["adminLog"] = 0
	current_date = datetime.datetime.now()
	current_time = current_date.strftime("%H:%M:%S")
	day = current_date.strftime("%A").lower()
	trains=list()
	final_list = list()
	if day == 'monday':
		trains = Train.query.filter_by(monday=1)
	elif day == 'tuesday':
		trains = Train.query.filter_by(tuesday=1)
	elif day == 'wednesday':
		trains = Train.query.filter_by(wednesday=1)
	elif day == 'thursday':
		trains = Train.query.filter_by(thursday=1)
	elif day == 'friday':
		trains = Train.query.filter_by(friday=1)
	elif day == 'saturday':
		trains = Train.query.filter_by(saturday=1)
	elif day == 'sunday':
		trains = Train.query.filter_by(sunday=1)
	for train in trains:
		if is_time_between(train.departure,train.arrival,str(current_time)):
			final_list.append((train,1))
		else:
			final_list.append((train,0))
	return render_template('train_status.html',title= "Train Status",admin = session["adminLog"],trains=final_list)

@app.route('/my_bookings', methods=['GET', 'POST'])
@login_required
def myBookings():
	
	if session["adminLog"] == 1:
		session["adminLog"] = 0
	my_bookings = [ticket for ticket in reversed(Ticket.query.filter_by(user_id = current_user.id).all())]
	return render_template('my_bookings.html',title= "My Bookings",my_bookings=my_bookings)

@app.route("/ticket/<string:pnr>")
def ticket(pnr):
	ticket = Ticket.query.get(pnr)
	passenger = ticket.passenger
	return render_template('ticket.html',ticket=ticket,passenger=passenger)

@app.route("/ticket/<string:pnr>/download")
def download(pnr):
	ticket = Ticket.query.get(pnr)
	rendered = render_template('pdf_template.html',ticket = ticket,passenger = ticket.passenger)
	pdf = pdfkit.from_string(rendered,False,configuration=config)
	response = make_response(pdf)
	response.headers['Content-type'] = 'application/pdf'
	response.headers['Content-Disposition'] = 'inline; filename='+str(pnr)+'.pdf'
	return response

@app.route("/ticket/<string:pnr>/cancel", methods=['POST'])
@login_required
def cancelTicket(pnr):
	ticket = Ticket.query.get(pnr)
	passenger = ticket.passenger
	seat = SeatStatus.query.filter_by(pass_id=passenger.pass_id).first()
	seat.pass_id=0
	train = Train.query.filter_by(train_no = ticket.train_no).first()
	if ticket.tier=="1A":
		train.ac_first_class_available_seats = train.ac_first_class_available_seats+1
		print(train.ac_first_class_available_seats)
	elif ticket.tier=="2A":
		train.ac_two_tier_available_seats = train.ac_two_tier_available_seats+1
		print(train.ac_two_tier_available_seats)
	elif ticket.tier=="3A":
		train.ac_three_tier_available_seats = train.ac_three_tier_available_seats+1
		print(train.ac_three_tier_available_seats)
	elif ticket.tier=="Sl":
		train.sleeper_class_available_seats = train.sleeper_class_available_seats+1
		print(train.sleeper_class_available_seats)
	db.session.delete(ticket)		
	db.session.delete(passenger)
	db.session.commit()
	flash('Ticket has been cancelled', 'info')
	return redirect(url_for('myBookings'))

@app.route('/fare', methods=['GET', 'POST'])
@login_required
def fare():
		trains = Train.query.all()
		if len(trains) > 0:
			return render_template('fare.html',title= "Fare Chart",trains= trains,admin = session["adminLog"])
		else:
			return "no trains found"
	

@app.route('/account' , methods=['GET', 'POST'])
@login_required
def account():
	
	if session["adminLog"] == 1:
		session["adminLog"] = 0
	form = UpdateAccountForm()
	if form.validate_on_submit():
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash('Your account has been updated!', 'success')
		return redirect(url_for('account'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	return render_template('account.html' , title = "Account" , admin = session["adminLog"] , form = form)

@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		session["adminLog"] = 0
		return redirect(url_for('home'))
	form =RegistrationForm()
	if form.validate_on_submit():
		hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
		db.session.add(user)
		db.session.commit()
		flash('Your account has been created', 'success')
		session["adminLog"] = 0
		return redirect(url_for('login'))
	return render_template('register.html', title= "Register", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		session["adminLog"] = 0
		return redirect(url_for('home'))
	form =LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			if next_page:
				session["adminLog"] = 0
				return redirect(next_page)
			else:
				session["adminLog"] = 0
				return redirect(url_for('home'))
		else:
			flash('Login Unsuccessful! Please check email & Password', 'danger')
	return render_template('login.html', title= "Login", form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('home'))

@app.route('/about_us', methods=['GET', 'POST'])
def aboutUs():
	return render_template('about_us.html')


@app.route('/add_train',methods=['GET', 'POST'])
def addTrain():
	if session["adminLog"] == 1:
		form = AddTrain()
		if form.validate_on_submit():
			print("Yes")
			days=['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
			for day in days:
				if form[day].data:
					form[day].data = 1
				else:
					form[day].data = 0
			train = Train(train_no = form.trainID.data,train_name = form.trainName.data,
						source= form.starting.data,destination = form.ending.data,
						monday=form.monday.data,tuesday=form.tuesday.data,wednesday=form.wednesday.data,thursday=form.thursday.data,
						friday=form.friday.data,saturday=form.saturday.data,sunday=form.sunday.data,ac_first_class_coaches=form.acFirstClassCoaches.data,
						ac_two_tier_coaches=form.acTwoTierCoaches.data,ac_three_tier_coaches=form.acThreeTierCoaches.data,sleeper_class_coaches=form.sleeperClassCoaches.data,
						ac_first_class_available_seats=24*int(form.acFirstClassCoaches.data),
						ac_two_tier_available_seats=54*int(form.acTwoTierCoaches.data), ac_three_tier_available_seats=64*int(form.acThreeTierCoaches.data),
						sleeper_class_available_seats=72*int(form.sleeperClassCoaches.data),
						ac_first_class_fare=form.acFirstClassFare.data,ac_two_tier_fare=form.acTwoTierFare.data,ac_three_tier_fare=form.acThreeTierFare.data,
						sleeper_class_fare=form.sleeperClassFare.data,departure = str(form.departure.data),arrival = str(form.arrival.data) , total = str(form.tot_time.data))
			db.session.add(train)
			print("Train read Success")
			ac1_seats = 24*int(form.acFirstClassCoaches.data)
			for i in range(ac1_seats):
				print("Inside Loop")
				seat = SeatStatus(train_no = form.trainID.data, seat_no = 1000+i+1, seat_type="1A")
				db.session.add(seat)

			ac2_seats = 54*int(form.acTwoTierCoaches.data)
			for i in range(ac2_seats):
				seat = SeatStatus(train_no = form.trainID.data, seat_no = 2000+i+1, seat_type="2A")
				db.session.add(seat)
			
			ac3_seats = 64*int(form.acThreeTierCoaches.data)
			for i in range(ac3_seats):
				seat = SeatStatus(train_no = form.trainID.data, seat_no = 3000+i+1, seat_type="3A")
				db.session.add(seat)
			
			sleep_seats = 72*int(form.sleeperClassCoaches.data)
			for i in range(sleep_seats):
				seat = SeatStatus(train_no = form.trainID.data, seat_no = 4000+i+1, seat_type="Sl")
				db.session.add(seat)

			db.session.commit()

			flash('Your train has been added', 'success')
			return redirect(url_for('view'))
		return render_template('add_train.html',title="Add Train",form = form,admin = session["adminLog"])
	else:
		if current_user.is_authenticated:
			return redirect(url_for('home'))
		else:
			flash('Please log in to access this page.', 'info')
			return redirect(url_for('adminLogin'))
		

@app.route('/update_train',methods=['GET', 'POST'])
def update():
	if session["adminLog"] == 1:
		form = UpdateTrain()
		train = ""
		return render_template('update_train.html',title="Update Train",form = form,train=train,admin = session["adminLog"])
	else:
		if current_user.is_authenticated:
			return redirect(url_for('home'))
		else:
			flash('Please log in to access this page.', 'info')
			return redirect(url_for('adminLogin'))
	

train = ""

@app.route('/update_train/<loaded>',methods=['GET', 'POST'])
def updateTrain(loaded):
	if session["adminLog"] ==1:
		global train
		form = UpdateTrain()
		try:
			global train
			train_no = request.form["train_no"]
			train = Train.query.filter_by(train_no=train_no).first()
			print(train_no)
		except:
			if form.validate_on_submit():
				db.session.delete(train)
				db.session.commit()
				train = Train(train_no = form.trainID.data,train_name = form.trainName.data,
						source= form.starting.data,destination = form.ending.data,
						monday=form.monday.data,tuesday=form.tuesday.data,wednesday=form.wednesday.data,thursday=form.thursday.data,
						friday=form.friday.data,saturday=form.saturday.data,sunday=form.sunday.data,ac_first_class_coaches=form.acFirstClassCoaches.data,
						ac_two_tier_coaches=form.acTwoTierCoaches.data,ac_three_tier_coaches=form.acThreeTierCoaches.data,sleeper_class_coaches=form.sleeperClassCoaches.data,
						ac_first_class_available_seats=24*int(form.acFirstClassCoaches.data),
						ac_two_tier_available_seats=54*int(form.acTwoTierCoaches.data), ac_three_tier_available_seats=64*int(form.acThreeTierCoaches.data),
						sleeper_class_available_seats=72*int(form.sleeperClassCoaches.data),
						ac_first_class_fare=form.acFirstClassFare.data,ac_two_tier_fare=form.acTwoTierFare.data,ac_three_tier_fare=form.acThreeTierFare.data,
						sleeper_class_fare=form.sleeperClassFare.data,arrival=str(form.arrival.data),departure=str(form.departure.data),total=str(form.total.data))
				db.session.add(train)
				db.session.commit()
				flash('Your train has been updated', 'success')
				return redirect(url_for('view'))
		return render_template('update_train.html',title="Update Train",loaded=loaded, form = form, train=train,admin = session["adminLog"])
	else:
		if current_user.is_authenticated:
			return redirect(url_for('home'))
		else:
			flash('Please log in to access this page.', 'info')
			return redirect(url_for('adminLogin'))


@app.route('/view')
def view():
	if session["adminLog"] == 1:
		trains = Train.query.all()
		if len(trains) > 0:
			return render_template('view_train.html',title= "View Trains",trains= trains,admin = session["adminLog"])
		else:
			return "no trains found"
	else:
		if current_user.is_authenticated:
			return redirect(url_for('home'))
		else:
			flash('Please log in to access this page.', 'info')
			return redirect(url_for('adminLogin'))
	

@app.route('/admin_login', methods=['GET', 'POST'])
def adminLogin():
	if current_user.is_authenticated:
		flash('Please log out from the user first', 'info')
		return redirect(url_for('adminLogin'))
	form =LoginForm()
	if form.validate_on_submit():
		admin = Admin.query.filter_by(email=form.email.data).first()
		if admin and bcrypt.check_password_hash(admin.password, form.password.data):
			next_page = request.args.get('next')
			
			session["adminLog"] = 1	
			global adminLog
			adminLog=1			#admin is logged in
			if next_page:
				return redirect(next_page)
			else:
				return redirect(url_for('home'))
		else:
			flash('Login Unsuccessful! Please check email & Password', 'danger')
	return render_template('admin_login.html', title= "Admin Login", form=form)

@app.route('/admin_logout')
def adminLogout():
	session["adminLog"] = 0
	global adminLog
	adminLog=0
	return redirect(url_for('home'))
