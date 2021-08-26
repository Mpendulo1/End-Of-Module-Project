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
                     "name_of_person TXT NOT NULL,"
                     "Res_event TXT NOT NULL,"
                     "No_of_person INTEGER NOT NULL,"
                     "Res_date TXT NOT NULL,"
                     "image_url TXT NOT NULL,"
                     "CONSTRAINT fk_customer FOREIGN KEY (name_of_person) REFERENCES user(CST_id))")
        print("Reservation table created successfully")


def cashier():
    with sqlite3.connect("restaurant.db") as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS tlbCashier(Cash_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                     "Fullname TEXT NOT NULL,"
                     "Lastname TXT NOT NULL,"
                     "Address TXT NOT NULL,"
                     "Phone_no INTEGER NOT NULL,"
                     "image_url TXT NOT NULL,"
                     "CONSTRAINT fk_employee FOREIGN KEY (Fullname) REFERENCES user(Employee_id))")
        print("Cashier table created successfully")


def payment():
    with sqlite3.connect("restaurant.db") as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS tlbPayment(Pay_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                     "Name_of_customer TEXT NOT NULL,"
                     "Name_of_cashier TXT NOT NULL,"
                     "total_amount TXT NOT NULL,"
                     "CONSTRAINT fk_customer FOREIGN KEY (Name_of_customer) REFERENCES user(CST_id),"
                     "CONSTRAINT fk_customer FOREIGN KEY (Name_of_cashier) REFERENCES user(Cash_id))")
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

def menu():
    pass

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
            cursor.execute("INSERT INTO tlbCustomers("
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
        person = request.form['name_of_person']
        reservation_event = request.form['Res_event']
        no_of_person = request.form['No_of_person']
        reservation_date = request.form['Res_date']
        image = request.form['image_url']

        with sqlite3.connect("restaurant.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tlbReservation("
                           "name_of_person,"
                           "Res_event,"
                           "No_of_person,"
                           "Res_date,"
                           "image_url) VALUES (?, ?, ?, ?,?)", (person, reservation_event, no_of_person, reservation_date, image))
            conn.commit()
            response["status_code"] = 201
            response["description"] = "Reservation Booked successfully"
        return response


@app.route('/cashier-profile', methods=["POST"])
def cashier_profile():
    response = {}
    
    if request.method == "POST":
        # employee_id = request.form['Employee_id']
        fullname = request.form['Fullname']
        lastname = request.form['Lastname']
        address = request.form['Address']
        phone_no = request.form['Phone_no']
        image = request.form["image_url"]
        
        with sqlite3.connect('restaurant.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tlbCashier("
                           "Fullname,"
                           "Lastname,"
                           "Address,"
                           "image_url,"
                           "Phone_no) VALUES(?, ?, ?, ?,?)", (fullname, lastname, address, phone_no, image))
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
# --------------Viewing My Information ------------------


@app.route('/customer-profile/', methods=['GET'])
def view_profile():
    response = {}

    with sqlite3.connect("restaurant.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tlbCustomers ")

        response["status_code"] = 200
        response["description"] = "Profile fetched Successfully"
        response["data"] = cursor.fetchall()

    return jsonify(response)


@app.route("/view-reservation/", methods=['GET'])
def view_reservation():
    response = {}

    with sqlite3.connect("restaurant.db") as conn:
        cursor = conn.cursor()
        cursor.row_factory = sqlite3.Row
        cursor.execute("SELECT * FROM tlbReservation")
        results = cursor.fetchall()
        reserve = []

        for i in results:
            reserve.append({x: i[x] for x in i.keys()})
        response["status_code"] = 200
        response["data"] = tuple(reserve)
        response["description"] = "Displaying Reservation Successfully"
    return jsonify(response)


@app.route("/view-cashier", methods=['GET', "POST"])
def view_cashier():
    response = {}

    with sqlite3.connect("restaurant.db") as conn:
        cursor = conn.cursor()
        cursor.row_factory = sqlite3.Row
        cursor.execute("SELECT * FROM tlbCashier")
        results = cursor.fetchall()
        cash = []

        for i in results:
            cash.append({x: i[x] for x in i.keys()})
        response["status_code"] = 200
        response["data"] = tuple(cash)
        response["description"] = "Displaying Cashier Successfully"
    return jsonify(response)


@app.route("/view-payment", methods=["GET"])
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


@app.route("/view-employee", methods=['GET'])
def view_employee():
    response = {}

    with sqlite3.connect("restaurant.db") as conn:
        cursor = conn.cursor()
        cursor.row_factory = sqlite3.Row
        cursor.execute("SELECT * FROM tlbEmployee")
        results = cursor.fetchall()
        employ = []

        for i in results:
            employ.append({x: i[x] for x in i.keys()})
        response["status_code"] = 200
        response["data"] = tuple(employ)
        response["description"] = "Displaying Employee Successfully"
    return jsonify(response)

# ------------------------- Removing/Deleting my Information------------------------------


@app.route('/delete-customer/<int:customer_id>')
def remove_customer(customer_id):
    response = {}
    with sqlite3.connect("restaurant.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tlbCustomers WHERE id=?" + str(customer_id))
        conn.commit()
        response['status_code'] = 200
        response['message'] = "Customer Removed Successfully"

    return response


@app.route("/delete-reservation/<int:reservation_id>")
def remove_reservation(reservation_id):
    response = {}

    with sqlite3.connect("restaurant.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tlbReservation WHERE id=?" + str(reservation_id))
        conn.commit()
        response['status_code'] = 200
        response['message'] = "Reservation Cancelled Successfully"

    return response


@app.route("/delete-payment", methods=["POST"])
def remove_payment(payment_id):
    response = {}

    with sqlite3.connect("restaurant.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tlbPayment WHERE id=?" + str(payment_id))
        conn.commit()
        response['status_code'] = 200
        response['message'] = "Payment Cancelled Successfully"

    return response


@app.route("/delete-cashier/<int:cashier_id>", methods=["POST"])
def remove_cashier(cashier_id):
    response = {}

    with sqlite3.connect("restaurant.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tlbCashier WHERE id=?" + str(cashier_id))
        conn.commit()
        response['status_code'] = 200
        response['message'] = "Cashier Removed Successfully"

    return response


@app.route("/delete-employee/<int:employee_id>", methods=["POST"])
def remove_employee(employee_id):
    response = {}

    with sqlite3.connect("restaurant.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tlbEmployee WHERE id=?" + str(employee_id))
        conn.commit()
        response['status_code'] = 200
        response['message'] = "Employee Removed Successfully"

    return response

# -----------------------------Updating/Editing my Information----------------------------------------


@app.route('/update-customer/<int:customer_id>/', methods=["PUT"])
def update_customer(customer_id):
    response = {}
    if request.method == "PUT":
        with sqlite3.connect("restaurant.db") as conn:
            cursor = conn.cursor()
            incoming_data = dict(request.json)
            put_data = {}

            if incoming_data.get("firstname") is not None:
                put_data["firstname"] = incoming_data.get("firstname")
                with sqlite3.connect("restaurant.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE tlbCustomers SET firstname=? WHERE CST_id=?", (put_data["firstname"], customer_id))
                    conn.commit()
                    response['message'] = "Updating Customer Details Successful"
                    response['status_code'] = 200
                return response

            if incoming_data.get("lastname") is not None:
                put_data["lastname"] = incoming_data.get("lastname")
                with sqlite3.connect("restaurant.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE ltbCustomers SET lastname=? WHERE CST_id=?", (put_data["lastname"], customer_id))
                    conn.commit()
                    response['message'] = "Updating Customer Last Name successfully"
                    response['status_code'] = 200

            if incoming_data.get("contact") is not None:
                put_data["contact"] = incoming_data.get("contact")
                with sqlite3.connect("restaurant.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE tlbCustomers SET contact=? WHERE CST_id=?", (put_data["contact"], customer_id))
                    conn.commit()
                    response['message'] = "Updating Customer Contact successfully"
                    response['status_code'] = 200

            if incoming_data.get('password') is not None:
                put_data['password'] = incoming_data.get('password')
                with sqlite3.connect('restaurant.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute('UPDATE tlbCustomers password=? WHERE CST_id=?', (put_data['password'], customer_id))
                    conn.commit()
                    response['message'] = "Updating Password Successfully"
                    return response

            if incoming_data.get('email') is not None:
                put_data['email'] = incoming_data.get('email')
                with sqlite3.connect('restaurant.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute('UPDATE tlbCustomers email=? WHERE CST_id=?', (put_data['email'], customer_id))
                    conn.commit()
                    response['message'] = "Updating Email Successfully"
                    return response


@app.route("/update-reservation/<int:reservation_id>", methods=["PUT"])
def update_reservation(reservation_id):
    response = {}
    if request.method == "PUT":
        with sqlite3.connect("restaurant.db") as conn:
            cursor = conn.cursor()
            incoming_data = dict(request.json)
            put_data = {}

            if incoming_data.get("Res_event") is not None:
                put_data["Res_event"] = incoming_data.get("Res_event")
                with sqlite3.connect("restaurant.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE tlbReservation SET Res_event=? WHERE RES_id=?", (put_data["Res_event"], reservation_id))
                    conn.commit()
                    response['message'] = "Updating Customer Reservation Event Successful"
                    response['status_code'] = 200
                return response

            if incoming_data.get("No_of_person") is not None:
                put_data["No_of_person"] = incoming_data.get("No_of_person")
                with sqlite3.connect("restaurant.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE ltbReservation SET No_of_person=? WHERE RES_id=?", (put_data["No_of_person"], reservation_id))
                    conn.commit()
                    response['message'] = "Updating Customer Reservation successfully"
                    response['status_code'] = 200

            if incoming_data.get("Res_date") is not None:
                put_data["Res_date"] = incoming_data.get("Res_date")
                with sqlite3.connect("restaurant.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE tlbReservation SET Res_date=? WHERE RES_id=?", (put_data["Res_date"], reservation_id))
                    conn.commit()
                    response['message'] = "Updating Customer Reservation Date successfully"
                    response['status_code'] = 200

            if incoming_data.get('image') is not None:
                put_data['image'] = incoming_data.get('image')
                with sqlite3.connect('restaurant.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute('UPDATE tlbReservation image=? WHERE RES_id=?', (put_data['image'], reservation_id))
                    conn.commit()
                    response['message'] = "Updating Reservation Image Successfully"
                    return response


@app.route("/update-payment<int:payment_id>")
def update_payment(payment_id):
    response = {}
    if request.method == "PUT":
        with sqlite3.connect("restaurant.db") as conn:
            cursor = conn.cursor()
            incoming_data = dict(request.json)
            put_data = {}

            if incoming_data.get("Name_of_customer") is not None:
                put_data["Name_of_customer"] = incoming_data.get("Name_of_customer")
                with sqlite3.connect("restaurant.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE tlbPayment SET Name_of_customer=? WHERE Pay_id=?", (put_data["Name_of_customer"], payment_id))
                    conn.commit()
                    response['message'] = "Updating Customer Name Successful"
                    response['status_code'] = 200
                return response

            if incoming_data.get("Name_of_cashier") is not None:
                put_data["Name_of_cashier"] = incoming_data.get("Name_of_cashier")
                with sqlite3.connect("restaurant.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE ltbPayment SET Name_of_cashier=? WHERE Pay_id=?", (put_data["Name_of_cashier"], payment_id))
                    conn.commit()
                    response['message'] = "Updating Customer Payment successfully"
                    response['status_code'] = 200

            if incoming_data.get("Res_date") is not None:
                put_data["Res_date"] = incoming_data.get("Res_date")
                with sqlite3.connect("restaurant.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE tlbPayment SET Res_date=? WHERE Pay_id=?", (put_data["Res_date"], payment_id))
                    conn.commit()
                    response['message'] = "Updating Customer Payment Date successfully"
                    response['status_code'] = 200
            #
            # if incoming_data.get('image') is not None:
            #     put_data['image'] = incoming_data.get('image')
            #     with sqlite3.connect('restaurant.db') as conn:
            #         cursor = conn.cursor()
            #         cursor.execute('UPDATE tlbPayment image=? WHERE Pay_id=?', (put_data['image'], payment_id))
            #         conn.commit()
            #         response['message'] = "Updating Payment Image Successfully"
            #         return response


if __name__ == '__main__':
    app.run(debug=True)