# Mpendulo Khoza
# Group 2

import sqlite3
from flask import Flask
from flask_jwt import *
from flask_cors import CORS


class User(object):
    def __init__(self, id, email, password):
        self.id = id
        self.email = email
        self.password = password


# def authenticate(email, password):
#     user = customer_table.get(email, None)
#     if user and hmac.compare_digest(user.password.encode('utf-8'), password.encode('utf-8')):
#         return user


# def identity(payload):
#     user_id = payload['identity']
#     return userid_table.get(user_id, None)


class Items(object):
    def __init__(self, product_id, name, price, description, product_type):
        self.id = product_id
        self.name = name
        self.price = price
        self.description = description
        self.type = product_type


def customers():
    conn = sqlite3.connect('restaurant.db')
    print("Opened database successfully")

    conn.execute("CREATE TABLE IF NOT EXISTS tlbCustomers(CST_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                 "firstname TEXT NOT NULL,"
                 "lastname TEXT NOT NULL,"
                 "contact INT NOT NULL,"
                 "password TEXT NOT NULL,"
                 "username TEXT NOT NULL,"
                 "email TEXT NOT NULL)")
    print("Customer table created successfully")
    conn.close()


def reservation():
    with sqlite3.connect("restaurant.db") as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS tlbReservation(RES_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                     "CST_id INT NOT NULL,"
                     "Res_event TXT NOT NULL,"
                     "No_of_person INTEGER NOT NULL,"
                     "Res_date TXT NOT NULL,"
                     "image_url TXT NOT NULL)")
        print("Reservation table created successfully")


def cashier():
    with sqlite3.connect("restaurant.db") as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS tlbCashier(Cash_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                     "Employee_id INT NOT NULL,"
                     "Fullname TEXT NOT NULL,"
                     "Lastname TXT NOT NULL,"
                     "Address TXT NOT NULL,"
                     "Phone_no INTEGER NOT NULL,"
                     "image_url TXT NOT NULL)")
        print("Cashier table created successfully")


def payment():
    with sqlite3.connect("restaurant.db") as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS tlbPayment(Pay_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                     "CST_id INT NOT NULL,"
                     "Name_of_customer TEXT NOT NULL,"
                     "Name_of_cashier TXT NOT NULL,"
                     "total_amount TXT NOT NULL)")
        print("Payment table created successfully")


def employee():
    with sqlite3.connect("restaurant.db") as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS tlbEmployee(Employee_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                     "Employee_name TXT NOT NULL,"
                     "Employee_surname TEXT NOT NULL,"
                     "Position TXT NOT NULL,"
                     "Hire_date TXT NOT NULL,"
                     "Salary INTEGER NOT NULL,"
                     "image_url TXT NOT NULL)")
        print("Employee table created successfully")


def fetch_customers():
    with sqlite3.connect('restaurant.db') as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM tlbCustomers")
        customer = cursor.fetchall()

        new_customer = []
        for data in customer:
            new_customer.append(User(data[0], data[6], data[4]))
        return new_customer


customers()
reservation()
cashier()
payment()
employee()
user = fetch_customers()

customer_table = {u.email: u for u in user}
userid_table = {u.id: u for u in user}

app = Flask(__name__)
CORS(app)
app.debug = True
app.config['SECRETE_KEY'] = 'super-secret'


@app.route('/customer-registration', methods=["POST"])
def user_registration():
    response = {}

    if request.method == "POST":

        first_name = request.form['firstname']
        last_name = request.form['lastname']
        address = request.form['contact']
        email = request.form['username']
        username = request.form['password']
        password = request.form['email']

        with sqlite3.connect('restaurant.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Customers("
                           "firstname,"
                           "lastname,"
                           "contact,"
                           "username,"
                           "password,"
                           "email) VALUES(?, ?, ?, ?, ?, ?)",
                           (first_name, last_name, address, email, username, password))
            conn.commit()
            response["message"] = "Registration Inserted  Successfully "
            response["status_code"] = 200
        return response


@app.route('/book-reservation', methods=["POST"])
def book_reservation():
    response = {}

    if request.method == "POST":
        reservation_event = request.form['Res_event']
        no_of_person = request.form['No_of_person']
        reservation_date = request.form['Res_date']
        image = request.form['image_url']

        with sqlite3.connect("restaurant.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tblReservation("
                           "Res_event,"
                           "No_of_person,"
                           "Res_date,"
                           "image_url) VALUES (?, ?, ?, ?)", (reservation_event, no_of_person, reservation_date, image))
            conn.commit()
            response["status_code"] = 201
            response["description"] = "Reservation Booked successfully"
        return response


@app.route('/customer-profile/')
def view_profile():
    response = {}

    with sqlite3.connect("restaurant.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Customers ")

        response["status_code"] = 200
        response["description"] = "Profile fetched Successfully"
        response["data"] = cursor.fetchall()

    return jsonify(response)


@app.route('/cashier-profile', methods=["POST"])
def cashier_profile():
    response = {}
    
    if request.method == "POST":
        employee_id = request.form['Employee_id']
        fullname = request.form['Fullname']
        lastname = request.form['Lastname']
        address = request.form['Address']
        phone_no = request.form['Phone_no']
        
        with sqlite3.connect('restaurant.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tlbCashier("
                           "Employee_id,"
                           "Fullname,"
                           "Lastname,"
                           "Address,"
                           "Phone_no) VALUES(?, ?, ?, ?)", (employee_id, fullname, lastname, address, phone_no))
            conn.commit()
            response["status_code"] = 201
            response["description"] = "Cashier Added successfully"
        return response


@app.route('/payment-details', methods=["POST"])
def payment_slip():
    response = {}

    if request.method == "POST":
        cashier_id = request.form['CST_id']
        name_of_customer = request.form['Name_of_customer']
        name_of_cashier = request.form['Name_of_cashier']
        total_amount = request.form['total_amount']

        with sqlite3.connect('restaurant.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tlbPayment("
                           "CST_id,"
                           "Name_of_customer,"
                           "Name_of_cashier,"
                           "total_amount) VALUES(?, ?, ?, ?)", (cashier_id, name_of_cashier, name_of_customer, total_amount))
            conn.commit()
            response["status_code"] = 201
            response["description"] = "Cashier Added successfully"
        return response


@app.route('/employee-profile', methods=["POST"])
def employee():
    response = {}

    if request.method == "POST":
        employee_name = request.form['Employee_name']
        employee_surname = request.form['Employee_surname']
        position = request.form['Position']
        hire_date = request.form['Hire_date']
        salary = request.form['Salary']
        image_url = request.form['image_url']

        with sqlite3.connect('restaurant.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tlbPayment("
                            "Employee_name,"
                            "Employee_surname,"
                            "Position,"
                            "Hire_date,"
                            "Salary,"
                            "image_url) VALUES(?, ?, ?, ?, ?, ?)",
                            (employee_name, employee_surname, position, hire_date, salary, image_url))
            conn.commit()
            response["status_code"] = 201
            response["description"] = "Employee Added successfully"
        return response


@app.route("/view-payment", methods=["POST"])
def view_payslip():
    response = {}

    with sqlite3.connect("restaurant.db") as conn:
        cursor = conn.cursor()
        cursor.row_factory = sqlite3.Row
        cursor.execute("SELECT * FROM tlbPayments")
        results = cursor.fetchall()
        pay = []

        for i in results:
            pay.append({x: i[x] for x in i.keys()})
        response["status_code"] = 200
        response["data"] = tuple(pay)
        response["description"] = "Displaying Payments Successfully"
    return jsonify(response)


# @app.route('/delete-car/<int:vehicle_id>')
# def remove_vehicle(vehicle_id):
#     response = {}
#     with sqlite3.connect("dealership.db") as conn:
#         cursor = conn.cursor()
#         cursor.execute("DELETE FROM Car_dealership WHERE id=" + str(vehicle_id))
#         conn.commit()
#         response['status_code'] = 200
#         response['message'] = "Vehicle deleted Successfully"
#
#     return response
#
#
# @app.route('/edit-car/<int:vehicle_id>/', methods=["PUT"])
# def edit_car(vehicle_id):
#     response = {}
#     if request.method == "PUT":
#         with sqlite3.connect("dealership.db") as conn:
#             incoming_data = dict(request.json)
#
#             put_data = {}
#             if incoming_data.get("name") is not None:
#                 put_data["name"] = incoming_data.get("name")
#                 with sqlite3.connect("dealership.db") as conn:
#                     cursor = conn.cursor()
#                     cursor.execute("UPDATE Car_dealership SET name=? WHERE id=?", (put_data["name"], vehicle_id))
#                     conn.commit()
#                     response['message'] = "Updating successful"
#                     response['status_code'] = 200
#                 return response
#
#             if incoming_data.get("brand") is not None:
#                 put_data["brand"] = incoming_data.get("brand")
#                 with sqlite3.connect("dealership.db") as conn:
#                     cursor = conn.cursor()
#                     cursor.execute("UPDATE Car_dealership SET brand=? WHERE id=?", (put_data["brand"], vehicle_id))
#                     conn.commit()
#                     response['message'] = "Updating  successfully"
#                     response['status_code'] = 200
#
#             if incoming_data.get("price") is not None:
#                 put_data["price"] = incoming_data.get("price")
#                 with sqlite3.connect("dealership.db") as conn:
#                     cursor = conn.cursor()
#                     cursor.execute("UPDATE Car_dealership SET price=? WHERE id=?", (put_data["price"], vehicle_id))
#                     conn.commit()
#                     response['message'] = "Updating  successfully"
#                     response['status_code'] = 200
#
#             if incoming_data.get('year') is not None:
#                 put_data['year'] = incoming_data.get('year')
#                 with sqlite3.connect('dealership.db') as conn:
#                     cursor = conn.cursor()
#                     cursor.execute('UPDATE Car_dealership SET year=? WHERE id=?', (put_data['year'], vehicle_id))
#                     conn.commit()
#                     response['message'] = "Updating Successfully"
#                     return response
#
#
if __name__ == '__main__':
    app.run(debug=True)