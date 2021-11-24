import sqlite3
from flask import render_template, url_for, make_response, Flask, request
import csv
import os
import pandas as pd

app = Flask(__name__)

def read_txt(filename):
    #read the file
    myList = []
    with open(filename, "r") as data:
        for line in data:
            myList.append(tuple(line.strip().split(", ")))
    return myList[1:]

@app.route("/")
def index():
    if request.method == "GET":
        return render_template("base.html")

@app.route("/admin", methods=["GET", "POST"])
def admin():

    #go to admin page add products
    name = request.args.get("name")
    price = request.args.get("price")
    description = request.args.get("description")


    if name and price and description:
        sum = str(name) + "," + str(price) +  "," + str(description)
        appendFile = open('roster.csv', 'a')
        appendFile.write(sum)
        appendFile.write('\n')
        appendFile.close()

        # Adding data to database 
        with sqlite3.connect(f"roster.db") as conn:
            conn.execute(f"drop table if exists roster")
            data = pd.read_csv(f"roster.csv", header=None)
            data.to_sql(f"roster", conn)

            # Displaying data for admin
            cur = conn.cursor()
            cur.execute(f"select * from roster")
            if cur:
                emptyList = []
                for name in cur:
                    name = name[1:]
                    emptyList.append(name)
                return render_template("admin.html", name=emptyList)  
    else:
        return render_template("admin.html")

@app.route("/customer")
def costumer():
    # Connecting to the database file and select everything from the file
        with sqlite3.connect(f"roster.db") as conn:
                cur = conn.cursor()
                cur.execute(f"select * from roster")
                if cur:
                        emptyList = []
                        for name in cur:
                                name = name[1:]
                                emptyList.append(name)
                        if len(emptyList) == 0:
                                text = "No DATA!"
                                return render_template("customer.html", removed=text)
                        return render_template("customer.html", box=emptyList)
               

@app.route("/remove")
def delete():
        try:
                with sqlite3.connect(f"roster.db") as conn:
                        cur = conn.cursor()
                        cur.execute(f"delete from roster")
                        # delete item from database
                        os.remove("roster.csv") 
                        message = "You have successfully remove all items"
                        return render_template("base.html", myMessage=message)
        except FileNotFoundError:
                NoData = "There is no data in database"
                return render_template("base.html", myMessage=NoData)

@app.route("/cart")
def cart():
    return render_template("cart.html")