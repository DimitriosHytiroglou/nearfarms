from flask import render_template, redirect, request, session
from app import app, model
from .forms import   NewUserForm, LoginForm, TripForm
from .model import *
from app.encryption.HashingHandler import *

# Root app routing
@app.route('/')
def index():
    if 'username' in session:
        username = session['username']
        return render_template('home.html')
    else:
        return redirect('/login')

# App routing for USER LOGOUT
@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('password', None)
    return redirect('/')

# App routing for USER LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    loginForm = LoginForm()
    
    wrong = 'none'

    if loginForm.validate_on_submit():
        
        u = loginForm.username.data
        p = loginForm.password.data

        collection = chooseCollection('users')
        userPass = getUserPass(collection, u)

        if userPass != []:
            if checkPass(userPass,p):
                session['username'] = u
                session['password'] = userPass
                return redirect('/trips')
            else:
                wrong = 'block'
                return render_template('login.html', loginForm=loginForm, wrong=wrong)
        else:
                wrong = 'block'
                return render_template('login.html', loginForm=loginForm, wrong=wrong)

    return render_template('login.html', loginForm=loginForm, wrong=wrong)


# App routing to CREATE USER
@app.route('/create_newUser', methods=['GET', 'POST'])
def create_newUser():
    
    wrong = 'none'

    newUserForm = NewUserForm()
    if newUserForm.validate_on_submit():
        first_name = newUserForm.first_name.data
        last_name = newUserForm.last_name.data
        email = newUserForm.email.data
        username = newUserForm.username.data
        password = newUserForm.password.data

        collection = chooseCollection('users')
        userPass = getUserPass(collection, username)

        if userPass == []:
            # Password Hashing
            password = hashPass(password)

            collection = chooseCollection('users')
            insertUser(collection, email, username, password, first_name, last_name)

            session['username'] = username
            session['password'] = password

            return redirect('/trips')

        else:
            wrong = 'block'
            return render_template('register.html', newUserForm=newUserForm, wrong=wrong)

    return render_template('register.html', newUserForm=newUserForm, wrong=wrong)

# App routing to CREATE TRIP
@app.route('/create_trip', methods=['GET', 'POST'])
def create_trip():
    tripForm = TripForm()
    
    collection = chooseCollection('users')
    friends = findUsers(collection)

    boomlist = []
    friendChoices = []
    for friend in friends:
        row = {}
        row['first_name'] = friend['First']
        row['last_name'] = friend['Last']
        
        boomlist.append(row)  
        
    if tripForm.validate_on_submit():
        trip_title = tripForm.trip_title.data
        trip_destination = tripForm.trip_destination.data
        trip_friend = tripForm.trip_friend.data

        participants = [session['username'],trip_friend]
        collection = chooseCollection('trips')
        insertTrip(collection, trip_title, trip_destination, participants)

        return redirect('/trips')
    return render_template('trip.html', tripForm=tripForm, friends=boomlist, user=session['username'])

# App routing to DISPLAY TRIPS
@app.route('/trips')
def trips():
    collection = chooseCollection('users')    
    fullName = getUserFullName(collection, session['username'])

    collection = chooseCollection('trips')    
    tripsFullName = findTripsFullName(collection, fullName)

    trips = findTrips(collection, session['username'])

    boomlist = []

    if trips.count() is not 0:
    
        boomlist = []

        for trip in trips:
            row = {}
            row['trip_title'] = trip['Title']
            row['trip_destination'] = trip['Destination']

            boomlist.append(row)

    if tripsFullName.count() is not 0:
    
        if boomlist is not []:

            for trip in tripsFullName:
                row = {}
                row['trip_title'] = trip['Title']
                row['trip_destination'] = trip['Destination']
        
                boomlist.append(row)    
        else:
            boomlist = []
            for trip in tripsFullName:
                row = {}
                row['trip_title'] = trip['Title']
                row['trip_destination'] = trip['Destination']
        
                boomlist.append(row) 

    return render_template('home.html',trips=boomlist, user=session['username'])

# App routing to REMOVE TRIP FROM DATABASE
@app.route('/tripsrem/<value>', methods=['GET', 'POST'])
def tripsrem(value):

    collection = chooseCollection('trips')

    removeTrip(collection,value)

    collection = chooseCollection('users')    
    fullName = getUserFullName(collection, session['username'])

    collection = chooseCollection('trips')    
    tripsFullName = findTripsFullName(collection, fullName)

    trips = findTrips(collection, session['username'])
       
    boomlist = []

    if trips.count() is not 0:
    
        boomlist = []

        for trip in trips:
            row = {}
            row['trip_title'] = trip['Title']
            row['trip_destination'] = trip['Destination']
        
            boomlist.append(row)    

    if tripsFullName.count() is not 0:
    
        if boomlist is not []:

            for trip in tripsFullName:
                row = {}
                row['trip_title'] = trip['Title']
                row['trip_destination'] = trip['Destination']
        
                boomlist.append(row)    
        else:
            boomlist = []
            for trip in tripsFullName:
                row = {}
                row['trip_title'] = trip['Title']
                row['trip_destination'] = trip['Destination']
        
                boomlist.append(row)  

    return render_template('home.html',trips=boomlist, user=session['username'])

# App routing to add friends in the app
# IS NOT USED IN THIS IMPLEMENTATION
@app.route('/friends')
def friends():    
    collection = chooseCollection('users')
    friends = findUsers(collection)

    boomlist = []

    for friend in friends:
        row = {}
        row['first_name'] = friend['First']
        row['last_name'] = friend['Last']
        
        boomlist.append(row)        


    return render_template('friends.html', friends=boomlist, session=session)
