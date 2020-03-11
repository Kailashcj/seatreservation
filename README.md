# Restaurant Seat Reservation System:
A python, flask and mongodb based system for seat booking

![Image description] https://github.com/Kailashcj/seatreservation/blob/master/restaurant_check_availability.png

# Introduction:

This code uses a python flask app to perform seat booking for a single restautant.
A user of this app can perform following task using this code:

1. Check Seat availability for current and future dates for below table types in a restaurant
    - 2 seater
    - 4 seater
    - 6 seater

2. Web reservation of required seats for a given date and time based upon availability
3. Walk-in reservation of seats using the same web app
4. Reservation and customer data stored persistently in mongoDB database

# Requirements

Following version of binaries should be installed on a linux system or python virtualenvironment

- Flask==1.1.1
- pymongo==3.5.1
- Python3==3.6.8
- MongoDB shell version v4.2.3

# Assumptions

- A single non-chained restaurant with 42 seats
- App follows the table booking system
- 42 seats = 10 (2 seater table * 5 ), 20 (4 seater table * 5 ), 12 (6 seater table * 2)
- A 24 hour clock time for calculating time for reservation
- A sample time window between 08:00AM to 10:00AM. A booking slot is available every 30 minutes between this time window.
- Default booking time is 90 minutes per customer. This means a customer booking a slot for '0800' on table t1, would continue to use the table until '0930'. Thus this table t1 can be next booked at '0930'.

# Known Limitations

- Dummy customer id's is used in the code
- Seat cancellation and releasing the seat back to available pool is not implemented
- Claim seat feature, which releases the seat to available pool if a customer doesn't show-up within 30 minutes is not implemented
- releasing a reservation at the time of customer billing is not implemented. This feature would help to identify making seats available for walk-ins.
- Logic in the app.py can be ported into a python object based structure. This will help to scale the application to add more features
needed for a restaurant like, billing, food ordering etc. This can be discussed.

# Usage

1. Install listed requirements on a linux system
2. run mongo on a terminal by typing command $ mongo
3. run flask app on a terminal by typing command $ python3 app.py
4. Open a browser and run below url's:
    - Check Seat availability: http://127.0.0.1:5000/checkseatavailability?date=2020-03-15
    - Book Seat : http://127.0.0.1:5000/book?date=2020-03-14&time=1000&customer_id=y&num_people=2
5. You can modify the date, time and num_people values in above URL's
