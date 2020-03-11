'''
This file has python code for
reserving seats in a restaurant.

'''
from flask import Flask
from flask import request
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

app = Flask(__name__)

# mongodb connection
client = MongoClient('mongodb://127.0.0.1:27017')
try:
    client.admin.command('ismaster')
    print('MongoDB connection: Success')
except ConnectionFailure as cf:
    print('MongoDB connection: failed', cf)

'''
- A total of 12 tables in the restaurant. 2 seaters : 5, 4 seaters; 5, 6 seaters: 2
- sample slots for seat reservation.
- booking defaults to 90 minutes. 
- next slot is available after 90 minutes on the same table
- Follows a 24 hour clock and 10:00AM is last booking available in the sample below
'''

tables = ['t1', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 't9', 't10', 't11', 't12']
all_slots = ['0800', '0830', '0900', '0930', '1000']
tslots = {
    '0800': ['0800', '0830', '0900'],
    '0830': ['0830', '0900', '0930'],
    '0900': ['0900', '0930', '1000'],
    '0930': ['0930', '1000'],
    '1000': ['1000']
}

@app.route('/checkseatavailability')
def check_availability():
    date = request.args.get('date')
    available = {2: {}, 4 :{}, 6: {}}
    current_bookings = {}
    db = client['seats'] # handle for 'seats' db
    query_result = db['bookings'].find({'date': date})
    for results in query_result:
        if results['table'] not in current_bookings:
            current_bookings[results['table']] = results['slots']
    
    for t in tables:
        if t not in current_bookings: # if tables are empty. show all slots
            if int(t[1:]) <= 5:
                available[2][t] = all_slots
            elif int(t[1:]) <=10:
                available[4][t] = all_slots
            elif int(t[1:]) <= 12:
                available[6][t] = all_slots
        else:
            for k in current_bookings: # for blocked tables, check possible available slots
                temp = []
                for time in current_bookings[k]:
                    temp.append(time)
                sublist = list(set(all_slots) - set(temp))
                if len(sublist) >= 3:
                    for s in tslots:
                         if set(tslots[s]) >= set(sublist):
                             if int(k[1:]) <= 5:
                                 available[2][k] = s
                             elif int(k[1:]) <= 10:
                                 available[4][k] = s
                             elif int(k[1:]) <= 12:
                                 available[6][k] = s
    return available

#tables availabile for 2, 4 and 6 seats
def get_possible_tables(num_people):
    if num_people <= 2:
        return ['t1', 't2', 't3', 't4', 't5']
    elif num_people <= 4:
        return ['t6', 't7', 't8', 't9', 't10']
    elif num_people <= 6:
        return ['t11', 't12']
    else:
        return []

def is_booking_possible(table_detail, time):
    if 'slots' not in table_detail: # slots are empty
        return True
    slots = table_detail['slots']
    booking_slots = tslots[time]
    for booking_slot in booking_slots:
        if booking_slot in slots:
            return False
    return True

def do_booking(table_detail, time, customer_id):
    if 'slots' not in table_detail:
        table_detail['slots'] = {}
    slots = table_detail['slots']
    booking_slots = tslots[time]
    for booking_slot in booking_slots:
        slots[booking_slot] = customer_id
    
@app.route('/')
def welcome():
    return "Welcome to Seat Reservation System!"

@app.route('/book')
def book():
    date = request.args.get('date')
    time = request.args.get('time')
    customer_id = request.args.get('customer_id')
    num_people = int(request.args.get('num_people'))

    possible_tables = get_possible_tables(num_people)
    db = client['seats'] # handle for 'seats' db

    booking_done = False
    for possible_table in possible_tables:
        query_result = db['bookings'].find({'date': date, 'table': possible_table})
        table_detail = {}
        for result in query_result:
            table_detail = result

        # if table is empty
        if not table_detail:
            table_detail = {'date': date, 'table': possible_table}
            do_booking(table_detail, time, customer_id)
            db['bookings'].insert(table_detail)
            booking_done = True
            break
        else:
            possible = is_booking_possible(table_detail, time)
            if possible:
                do_booking(table_detail, time, customer_id)
                db['bookings'].update({'date': date, 'table': possible_table}, table_detail)
                booking_done = True
                break
    if booking_done:
        return "Booking done"
    else:
        return "Booking not possible"

if __name__ == '__main__':
    app.run()
