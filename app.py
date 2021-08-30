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


def vehicles():
    with sqlite3.connect("restaurant.db") as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS tlbVehicles(VHC_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                     "name TXT NOT NULL,"
                     "brand TXT NOT NULL,"
                     "type INTEGER NOT NULL,"
                     "price TXT NOT NULL,"
                     "year TXT NOT NULL,"
                     "description TXT NOT NULL,"
                     "transition TXT NOT NULL,"
                     "image TXT NOT NULL,"
                     "CONSTRAINT fk_customer FOREIGN KEY (name) REFERENCES user(CST_id))")
        print("Reservation table created successfully")


def sales():
    with sqlite3.connect("restaurant.db") as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS tlbSales(Sale_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                     "sale_date TEXT NOT NULL,"
                     "payment_info TXT NOT NULL,"
                     "CONSTRAINT fk_vehicles FOREIGN KEY (payment_info) REFERENCES tlbVehicles(VHC_id),"
                     "CONSTRAINT fk_employee FOREIGN KEY (sale_date) REFERENCES tlbCustomers(CST_id))")
        print("Cashier table created successfully")


def insurance_type():
    with sqlite3.connect("restaurant.db") as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS tlbInsurance_type(INS_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                     "insurance_period TEXT NOT NULL,"
                     "amount TXT NOT NULL,"
                     "insurance_condition TXT NOT NULL)")
        print("Payment table created successfully")


def insurance_provider():
    with sqlite3.connect("restaurant.db") as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS tlbInsurance_provider(Insure_prov_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                     "address TXT NOT NULL,"
                     "phone TEXT NOT NULL,"
                     "website TXT NOT NULL,"
                     "special_condition TXT NOT NULL,"
                     "licence TXT NOT NULL)")
        print("Employee table created successfully")

def registered_insurance():
    with sqlite3.connect("restaurant.db") as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS tlbRegisteredInsurance(Reg_insurance_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                     "start_date TXT NOT NULL,"
                     "end_date TEXT NOT NULL,"
                     "payment_information TXT NOT NULL,"
                     "special_features TXT NOT NULL,"
                     "CONSTRAINT fk_vehicles FOREIGN KEY (payment_information) REFERENCES tlbVehicles(VHC_id),"
                     "CONSTRAINT fk_vehicles FOREIGN KEY (payment_information) REFERENCES tlbVehicles(Insure_prov_id),"
                     "CONSTRAINT fk_vehicles FOREIGN KEY (payment_information) REFERENCES tlbVehicles(Sale_id),"
                     "CONSTRAINT fk_vehicles FOREIGN KEY (payment_information) REFERENCES tlbVehicles(INS_id),"
                     "CONSTRAINT fk_vehicles FOREIGN KEY (payment_information) REFERENCES tlbVehicles(CST_id))")
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
vehicles()
sales()
registered_insurance()
insurance_provider()
insurance_type()
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


@app.route('/create-vehicles', methods=['POST'])
def create_vehicles():
    response = {}

    if request.method == "POST":

        name = request.form['name']
        brand = request.form['brand']
        type = request.form['type']
        price = request.form['price']
        year = request.form['year']
        description = request.form['description']
        transition = request.form['transtion']
        image = request.form['image']
        with sqlite3.connect('restaurant.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tlbVehicles("
                           "name,"
                           "brand,"
                           "type,"
                           "price,"
                           "year,"
                           "description,"
                           "transition,"
                           "image) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                           (name, brand, type, price, year, description, transition, image))
            conn.commit()
            response["message"] = "Registration Vehicles  Successfully "
            response["status_code"] = 200
        return response


@app.route('/create-sales', methods=['POST'])
def create_sales():
    response = {}

    if request.method == "POST":
        sales_date = request.form['sales_date']
        payment_info = request.form['payment_info']

        with sqlite3.connect('restaurant.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tlbSales("
                           "sales_date,"
                           "payment_info) VALUES(?, ?)",
                           (sales_date, payment_info))
            conn.commit()
            response["message"] = "Registration sales  Successfully "
            response["status_code"] = 200
        return response


@app.route('/create-insurance-type', methods=['POST'])
def insurance_type():
    response = {}

    if request.method == "POST":
        period = request.form['insurance_period']
        amount = request.form['amount']
        condition = request.form['insurance_condition']

        with sqlite3.connect('restaurant.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tlbInsurance_type("
                           "insurance_period,"
                           "amount,"
                           "insurance_condition) VALUES(?, ?, ?)",
                           (period, amount, condition))
            conn.commit()
            response["message"] = "Registration Insurance Type  Successfully "
            response["status_code"] = 200
        return response


@app.route('/create-insurance-provider', methods=['POST'])
def insurance_provider():
    response = {}

    if request.method == "POST":
        address = request.form['address']
        phone = request.form['phone']
        website = request.form['website']
        special_conditions = request.form['special_condition']
        licence = request.form['licence']

        with sqlite3.connect('restaurant.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tlbInsurance_provider("
                           "address,"
                           "phone,"
                           "website,"
                           "special_condition,"
                           "licence) VALUES(?, ?, ?, ?, ?)",
                           (address, phone, website, special_conditions, licence))
            conn.commit()
            response["message"] = "Registration Insurance Provider  Successfully "
            response["status_code"] = 200
        return response


@app.route('/cerate-registerd-insurance', methods=['POST'])
def registered_insurance():
    response = {}

    if request.method == "POST":
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        payment_info = request.form['payment_information']
        special_features = request.form['special_features']

        with sqlite3.connect('restaurant.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tlbRegisteredInsurance("
                           "sales_date,"
                           "payment_info) VALUES(?, ?, ?, ?)",
                           (start_date, payment_info, end_date, special_features))
            conn.commit()
            response["message"] = "Registration Insurances  Successfully "
            response["status_code"] = 200
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


@app.route('/view-vehicles', methods=['GET'])
def view_vehicles():
    response = {}

    with sqlite3.connect("restaurant.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tlbVehicles ")

        response["status_code"] = 200
        response["description"] = "Profile fetched Successfully"
        response["data"] = cursor.fetchall()

    return jsonify(response)


@app.route('/view-sales', methods=['GET'])
def view_sales():
    response = {}

    with sqlite3.connect("restaurant.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tlbSales")

        response["status_code"] = 200
        response["description"] = "Profile fetched Successfully"
        response["data"] = cursor.fetchall()

    return jsonify(response)


@app.route('/insurance-type')
def view_insurance_type():
    response = {}

    with sqlite3.connect("restaurant.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tlbInsurance_type ")

        response["status_code"] = 200
        response["description"] = "Profile fetched Successfully"
        response["data"] = cursor.fetchall()


@app.route('/insurance-provider', methods=['GET'])
def view_insurance_provider():
    response = {}

    with sqlite3.connect("restaurant.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tlbInsurance_provider ")

        response["status_code"] = 200
        response["description"] = "Profile fetched Successfully"
        response["data"] = cursor.fetchall()


@app.route('/registered-insurance', methods=['GET'])
def view_registered_insurance():
    response = {}

    with sqlite3.connect("restaurant.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tlbRegisteredInsurance ")

        response["status_code"] = 200
        response["description"] = "Profile fetched Successfully"
        response["data"] = cursor.fetchall()

# ------------------------- Removing/Deleting my Information------------------------------


@app.route('/delete-customer/<int:customer_id>', methods=['POST'])
def remove_customer(customer_id):
    response = {}
    with sqlite3.connect("restaurant.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tlbCustomers WHERE CST_id=" + str(customer_id))
        conn.commit()
        response['status_code'] = 200
        response['message'] = "Customer Removed Successfully"

    return response

@app.route('/delete-vehicle/<int:vehicle_id>', methods=['POST'])
def remove_vehicle(vehicle_id):
    response = {}
    with sqlite3.connect("restaurant.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tlbVehicles WHERE VHC_id=" + str(vehicle_id))
        conn.commit()
        response['status_code'] = 200
        response['message'] = "Vehicle Removed Successfully"

    return response


@app.route('/delete-sales/<int:sales_id>', methods=['POST'])
def remove_sales(sales_id):
    response = {}
    with sqlite3.connect("restaurant.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tlbSales WHERE Sale_id=" + str(sales_id))
        conn.commit()
        response['status_code'] = 200
        response['message'] = "Customer Removed Successfully"

    return response


@app.route('/delete-insurance-type/<int:ins_type_id>')
def remove_insurance_type(ins_type_id):
    response = {}
    with sqlite3.connect("restaurant.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tlbInsurance_type WHERE INS_id=" + str(ins_type_id))
        conn.commit()
        response['status_code'] = 200
        response['message'] = "Insurance Type Removed Successfully"
    return response


@app.route('/delete-insurance-provider/<int:ins_pro_id>', methods=['POST'])
def remove_insurance_provider(ins_pro_id):
    response = {}
    with sqlite3.connect("restaurant.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tlbInsurance_provider WHERE Insure_prov_id=" + str(ins_pro_id))
        conn.commit()
        response['status_code'] = 200
        response['message'] = "Insurance Provider Removed Successfully"

    return response


@app.route('/delete-registered-insurance/<int:reg_ins_id>', methods=['POST'])
def remove_registerd_insurance(reg_ins_id):
    response = {}
    with sqlite3.connect("restaurant.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tlbRegisteredInsurance WHERE Reg_insurance_id=" + str(reg_ins_id))
        conn.commit()
        response['status_code'] = 200
        response['message'] = "Registered Insurance Removed Successfully"

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
                    cursor.execute("UPDATE tlbCustomers SET firstname=? WHERE CST_id=", (put_data["firstname"], customer_id))
                    conn.commit()
                    response['message'] = "Updating Customer Details Successful"
                    response['status_code'] = 200
                return response

            if incoming_data.get("lastname") is not None:
                put_data["lastname"] = incoming_data.get("lastname")
                with sqlite3.connect("restaurant.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE ltbCustomers SET lastname=? WHERE CST_id=", (put_data["lastname"], customer_id))
                    conn.commit()
                    response['message'] = "Updating Customer Last Name successfully"
                    response['status_code'] = 200

            if incoming_data.get("contact") is not None:
                put_data["contact"] = incoming_data.get("contact")
                with sqlite3.connect("restaurant.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE tlbCustomers SET contact=? WHERE CST_id=", (put_data["contact"], customer_id))
                    conn.commit()
                    response['message'] = "Updating Customer Contact successfully"
                    response['status_code'] = 200

            if incoming_data.get('password') is not None:
                put_data['password'] = incoming_data.get('password')
                with sqlite3.connect('restaurant.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute('UPDATE tlbCustomers password=? WHERE CST_id=', (put_data['password'], customer_id))
                    conn.commit()
                    response['message'] = "Updating Password Successfully"
                    return response

            if incoming_data.get('email') is not None:
                put_data['email'] = incoming_data.get('email')
                with sqlite3.connect('restaurant.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute('UPDATE tlbCustomers email=? WHERE CST_id=', (put_data['email'], customer_id))
                    conn.commit()
                    response['message'] = "Updating Email Successfully"
                    return response


if __name__ == '__main__':
    app.run(debug=True)