import export
from flask import Flask, render_template, request, jsonify
import subprocess as sp
from pymongo import MongoClient
from mongopass import mongopass
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

client = MongoClient(mongopass)
db = client.restaurant2
collectionOfTables = db.tables
collectionOfBookings = db.bookings


# Muestro todas las mesas
@app.route('/', methods=['GET'])
def hello_world():  # put application's code here
    documents = collectionOfBookings.find()
    tables = list(documents)
    for table in tables:
        print(table)
    return render_template("index.html", bookings=tables)


@app.route('/bookrestaurant', methods=['POST'])
def booking():
    print("COMIENZO FUNCION")
    fname = request.json.get("fname")
    sname = request.json.get("sname")
    smoking = request.json.get("smoking")
    phone = request.json.get("phone")
    str_diners = request.json.get("diners")
    diners = int(str_diners)
    location = request.json.get("location")
    date = request.json.get("date")
    time = request.json.get("time")
    datetime = request.json.get("datetime")

    email = request.json.get("email")

    # Busco si hay mesas con un número de comensales mesas con un número de comensales mayor
    # o igual que el que pide el usuario en esa localización

    queryTable = {
        "location": location,
        "diners": {
            "$gte": diners
        }
    }

    resulttable = collectionOfTables.find_one(queryTable)
    num_table = int(resulttable["number"])

    insert = {
        "1name": fname,
        "2name": sname,
        "phone": phone,
        "customer": email,
        "diners": diners,
        "datetime": datetime,
        "location": location,
        "smoking": smoking,
        "table": num_table
    }

    # Insert the document into the collection
    inserted_id = collectionOfBookings.insert_one(insert).inserted_id
    # Print the inserted document's ID
    print("Inserted document ID:", inserted_id)

    # si inserted_id distinto de null devuelvo 200
    if not inserted_id:
        response = jsonify({"message": "Failed"})
        response.status_code = 500  # Set the status code explicitly
    else:
        response = jsonify({"message": "Success"})
        response.status_code = 200  # Set the status code explicitly

    return response


if __name__ == '__main__':
    """
    from flask_cors import CORS
    import ssl

    context = ssl.SSLContext()
    context.load_cert_chain("/home/mariajesus/certificados/conversational_ugr_es.pem",
                            "/home/mariajesus/certificados/conversational_ugr_es.key")
    CORS(app)
    app.run(host='0.0.0.0', port=5050, ssl_context=context, debug=False)
    """

    app.run()

