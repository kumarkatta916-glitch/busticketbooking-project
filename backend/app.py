from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import mysql.connector
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

CORS(app)

# =========================
# MYSQL CONNECTION
# =========================

db = mysql.connector.connect(

host=os.getenv("DB_HOST"),

user=os.getenv("DB_USER"),

password=os.getenv("DB_PASSWORD"),

database=os.getenv("DB_NAME")

)

cursor = db.cursor()

# =========================
# EMAIL CONFIGURATION
# =========================

sender_email = os.getenv("EMAIL_USER")

sender_password = os.getenv("EMAIL_PASSWORD")

# =========================
# OTP STORAGE
# =========================

otp_storage = {}

# =========================
# HOME API
# =========================

@app.route('/')

def home():

    return "Backend Running Successfully"

# =========================
# SEND OTP API
# =========================

@app.route('/send-otp', methods=['POST'])

def send_otp():

    data = request.json

    email = data['email']

    otp = str(random.randint(1000,9999))

    otp_storage[email] = otp

    try:

        msg = MIMEMultipart()

        msg['From'] = sender_email

        msg['To'] = email

        msg['Subject'] = "Bus Ticket Booking OTP"

        body = f"""

Hello User,

Your OTP is:

{otp}

Thank You
Bus Ticket Booking Team

"""

        msg.attach(MIMEText(body,'plain'))

        server = smtplib.SMTP("smtp.gmail.com",587)

        server.starttls()

        server.login(sender_email,sender_password)

        server.sendmail(

            sender_email,

            email,

            msg.as_string()

        )

        server.quit()

        return jsonify({

            "status":"success",

            "message":"OTP Sent Successfully"

        })

    except Exception as e:

        return jsonify({

            "status":"failed",

            "message":str(e)

        })

# =========================
# REGISTER API
# =========================

@app.route('/register', methods=['POST'])

def register():

    data = request.json

    full_name = data['full_name']

    username = data['username']

    email = data['email']

    phone = data['phone']

    country = data['country']

    state = data['state']

    password = data['password']

    otp = data['otp']

    # OTP CHECK

    if otp_storage.get(email) != otp:

        return jsonify({

            "status":"failed",

            "message":"Invalid OTP"

        })

    # USERNAME CHECK

    cursor.execute(

        "SELECT * FROM users WHERE username=%s",

        (username,)

    )

    existing_user = cursor.fetchone()

    if existing_user:

        return jsonify({

            "status":"failed",

            "message":"Username Already Exists"

        })

    # INSERT USER

    query = """

    INSERT INTO users

    (

    full_name,

    username,

    email,

    phone,

    country,

    state,

    password

    )

    VALUES (%s,%s,%s,%s,%s,%s,%s)

    """

    values = (

        full_name,

        username,

        email,

        phone,

        country,

        state,

        password

    )

    cursor.execute(query,values)

    db.commit()

    return jsonify({

        "status":"success",

        "message":"Registration Successful"

    })

# =========================
# LOGIN API
# =========================

@app.route('/login', methods=['POST'])

def login():

    data = request.json

    username = data['username']

    password = data['password']

    query = """

    SELECT * FROM users

    WHERE username=%s AND password=%s

    """

    values = (username,password)

    cursor.execute(query,values)

    user = cursor.fetchone()

    if user:

        return jsonify({

            "status":"success",

            "message":"Login Successful"

        })

    else:

        return jsonify({

            "status":"failed",

            "message":"Invalid Username or Password"

        })

# =========================
# BOOK TICKET API
# =========================

@app.route('/book', methods=['POST'])
def book_ticket():

    data = request.json

    username = data['username']
    email = data['email']
    mobile = data['mobile']

    from_place = data['from_place']
    to_place = data['to_place']
    journey_date = data['journey_date']

    bus_type = data['bus_type']
    travels_name = data['travels_name']

    base_price = data['base_price']
    gst = data['gst']
    state_tax = data['state_tax']
    toll_fee = data['toll_fee']
    total_price = data['total_price']

    payment_status = data['payment_status']

    passengers = data['passengers']

    booking_id = "BUS" + str(random.randint(10000,99999))

    # =========================
    # SAVE BOOKING
    # =========================

    booking_query = """
    INSERT INTO bookings
    (
    booking_id,
    username,
    email,
    mobile,
    from_place,
    to_place,
    journey_date,
    bus_type,
    travels_name,
    ticket_count,
    base_price,
    gst,
    state_tax,
    toll_fee,
    total_price,
    payment_status
    )
    VALUES
    (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    booking_values = (
        booking_id,
        username,
        email,
        mobile,
        from_place,
        to_place,
        journey_date,
        bus_type,
        travels_name,
        len(passengers),
        base_price,
        gst,
        state_tax,
        toll_fee,
        total_price,
        payment_status
    )

    cursor.execute(
        booking_query,
        booking_values
    )

    # =========================
    # SAVE PASSENGERS
    # =========================

    for passenger in passengers:

        passenger_query = """
        INSERT INTO passengers
        (
        booking_id,
        passenger_name,
        age,
        gender,
        seat_number
        )
        VALUES
        (%s,%s,%s,%s,%s)
        """

        passenger_values = (

            booking_id,

            passenger['passenger_name'],

            passenger['age'],

            passenger['gender'],

            passenger['seat_number']

        )

        cursor.execute(
            passenger_query,
            passenger_values
        )

    db.commit()

    # =========================
    # SEND EMAIL
    # =========================

    try:

        passenger_details = ""

        for passenger in passengers:

            passenger_details += f"""

Passenger Name : {passenger['passenger_name']}
Age            : {passenger['age']}
Gender         : {passenger['gender']}
Seat Number    : {passenger['seat_number']}

"""

        msg = MIMEMultipart()

        msg['From'] = sender_email
        msg['To'] = email
        msg['Subject'] = "Bus Ticket Confirmation"

        body = f"""

Bus Ticket Booked Successfully

Booking ID : {booking_id}

Username : {username}

Mobile : {mobile}

From : {from_place}

To : {to_place}

Journey Date : {journey_date}

Bus Type : {bus_type}

Travels Name : {travels_name}

Base Price : ₹ {base_price}

GST : ₹ {gst}

State Tax : ₹ {state_tax}

Toll Fee : ₹ {toll_fee}

Total Amount : ₹ {total_price}

Payment Status : {payment_status}

Passenger Details:

{passenger_details}

Thank You
Bus Ticket Booking Team

"""

        msg.attach(
            MIMEText(body,'plain')
        )

        server = smtplib.SMTP(
            "smtp.gmail.com",
            587
        )

        server.starttls()

        server.login(
            sender_email,
            sender_password
        )

        server.sendmail(
            sender_email,
            email,
            msg.as_string()
        )

        server.quit()

    except Exception as e:

        print(e)

    return jsonify({

        "status":"success",

        "booking_id":booking_id,

        "message":"Ticket Booked Successfully"

    })

# =========================
# VIEW BOOKINGS API
# =========================

@app.route('/view-bookings', methods=['GET'])

def view_bookings():

    cursor.execute(

        "SELECT * FROM bookings"

    )

    bookings = cursor.fetchall()

    result = []

    for booking in bookings:

        result.append({

            "id": booking[0],

            "booking_id": booking[1],

            "username": booking[2],

            "passenger_name": booking[3],

            "age": booking[4],

            "gender": booking[5],

            "from_place": booking[6],

            "to_place": booking[7],

            "bus_type": booking[8],

            "travels_name": booking[9],

            "seat_number": booking[10],

            "journey_date": booking[11],

            "payment_status": booking[12]

        })

    return jsonify(result)

# =========================
# RUN FLASK APP
# =========================

if __name__ == '__main__':

    app.run(

        host='0.0.0.0',

        port=5000,

        debug=True

    )
