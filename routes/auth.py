from flask import render_template, Blueprint, request, session, redirect, url_for, jsonify, render_template_string, flash
from static.python.paths import files as file, routes as route
import sqlite3

auth = Blueprint('auth', __name__)


############################# Base #############################
@auth.route(route['base'], methods=['GET', 'POST'])
def base():
    if "bid" in session:
        return render_template(file['base'])
    else:
        return redirect(url_for('auth.login'))


############################# Login #############################
@auth.route(route['login'], methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        banker_id = int(request.form['bid'])
        banker_pass = request.form['bpass']

        try:
            conn = sqlite3.connect(file['db'])
            cursor = conn.cursor()
            row = cursor.execute(
                "SELECT * FROM banker WHERE bid={}".format(int(banker_id))).fetchall()
            if (len(row) != 0):
                row = row[0]
                bid = row[0]
                bpass = row[1]
                btype = row[2]
                bfname = row[3]
                blname = row[4]

                if (banker_id == bid and banker_pass == bpass):
                    data = {
                        'bid': bid,
                        'btype': btype,
                        'bfname': bfname,
                        'blname': blname
                    }
                    flash("Logged In", "success")
                    session["bid"] = banker_id
                    session["data"] = data
                    return redirect(url_for('home.home_home'))
                else:
                    flash("Banker ID or Password is wrong", "danger")
                    return redirect(url_for('auth.login'))
            else:
                flash("Banker ID or Password is wrong", "danger")
                return redirect(url_for('auth.login'))
        except:
            print("DB Error")
    else:
        if "bid" in session:
            return redirect(url_for('home.home_home'))
        else:
            return render_template(file['login'])

############################# Logout #############################
@auth.route(route['logout'])
def logout():
    session.clear()
    flash("You have logged out", "success")
    return redirect(url_for('auth.login'))
