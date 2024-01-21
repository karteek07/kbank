from flask import render_template, Blueprint, request, redirect, url_for, jsonify, session, flash
import sqlite3
from static.python.paths import files as file, routes as route


customer = Blueprint('customer', __name__)


############################# Customer Create #############################
@customer.route(route['customer']['create'], methods=['GET', 'POST'])
def customerCreate():
    if "bid" in session:
        if request.method == "POST":
            title = request.form['title']
            fname = request.form['fname']
            lname = request.form['lname']
            dob = request.form['dob']
            gender = request.form['gender']
            maritalstatus = request.form['maritalstatus']
            annualincome = request.form['annualincome']
            fathername = request.form['fathername']
            mothername = request.form['mothername']

            add1 = request.form['add1']
            add2 = request.form['add2']
            add3 = request.form['add3']
            state = request.form['state']
            district = request.form['district']
            city = request.form['city']
            pincode = request.form['pincode']

            aadharno = request.form['aadharno']
            panno = request.form['panno']

            primaryno = request.form['primaryno']
            secondaryno = request.form['secondaryno']
            email = request.form['email']

            name1 = request.form['name1']
            name2 = request.form['name2']
            relation1 = request.form['relation1']
            relation2 = request.form['relation2']
            nadd1 = request.form['nadd1']
            nadd2 = request.form['nadd2']
            aadharno1 = request.form['aadharno1']
            aadharno2 = request.form['aadharno2']
            contactno1 = request.form['contactno1']
            contactno2 = request.form['contactno2']

            data = (title, fname, lname, dob, gender, maritalstatus, annualincome, fathername, mothername,
                    add1, add2, add3, state, district, city, pincode,
                    aadharno, panno,
                    primaryno, secondaryno, email)

            try:
                conn = sqlite3.connect(file['db'])
                cursor = conn.cursor()
                cursor.execute("""  INSERT INTO customer (
                                title, fname, lname, dob, gender, maritalstatus, annualincome, fathername, mothername, 
                                add1, add2, add3, state, district, city, pincode, 
                                aadharno, panno, 
                                primaryno, secondaryno, email) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 
                                ?, ?, ?, ?, ?, ?, ?,
                                ?, ?,
                                ?, ?, ?)    """, data)
                conn.commit()
                flash('Customer Created', 'success')

                cid = cursor.lastrowid
                acctData = (cid, '01', '01', 'Savings', '0', name1, name2, relation1, relation2, nadd1, nadd2, aadharno1, aadharno2, contactno1, contactno2)
                acctQuery = """ INSERT INTO account (cid, atype, interestrate, purpose, balance, 
                                name1, name2, relation1, relation2, add1, add2, aadharno1, aadharno2, contactno1, contactno2)
                                VALUES {}""".format(acctData)
                print(acctQuery)
                cursor.execute(acctQuery)
                conn.commit()
            except:
                print("Connection Failed")
            finally:
                conn.close()

            return render_template(file['home'])

        else:
            return render_template(file['customer']['create'])
    else:
        return redirect(url_for('auth.login'))


############################# Customer Search #############################
@customer.route(route['customer']['search'], methods=['GET', 'POST'])
def customerSearch():
    if "bid" in session:
        if request.method == "POST":
            data = request.get_json()
            print("Data: ", data)
            fields = data['fields']
            if fields == "all":
                searchby = data['searchby']
                value = data['value']
                values = {'searchby': searchby, 'value': value}

                if searchby != "01":
                    if searchby == "02":
                        col = "cid"
                        value = int(value)
                    elif searchby == "03":
                        col = "fname"
                    elif searchby == "04":
                        col = "lname"
                    elif searchby == "05":
                        col = "aadharno"
                    elif searchby == "06":
                        col = "panno"

                    query = "SELECT * FROM customer WHERE {}='{}'".format(
                        col, value)
                elif searchby == "01":
                    query = "SELECT * FROM customer"

            elif fields == "fullname":
                field = data['value']
                queries = []
                for cid in field:
                    query = "SELECT title, fname, lname FROM customer WHERE cid = {}".format(
                        cid)
                    queries.append(query)
                query = " UNION ALL ".join(queries)
                values = 0

            print("The Query for Customer Search is: "+query)
            try:
                conn = sqlite3.connect(file['db'])
                cursor = conn.cursor()
                row = cursor.execute(query).fetchall()

                data = {'values': values, 'results': row}
            except:
                print("DB Error")
            finally:
                conn.close()

            return jsonify(data)

        else:
            return render_template(file['customer']['search'])
    else:
        return redirect(url_for('auth.login'))

############################# Customer Info #############################


@customer.route(route['customer']['info'], methods=['GET', 'POST'])
def customerInfo():
    if "bid" in session:
        cid = request.args.get('cid')
        if cid:
            return render_template(file['customer']['info'], cid=cid)
        else:
            return redirect(url_for('customer.customerSearch'))
    else:
        return redirect(url_for('auth.login'))


############################# Customer Short Info #############################
@customer.route(route['customer']['shortInfo'], methods=['POST'])
def customerShortInfo():
    if request.method == "POST":
        data = request.get_json()
        cust_id = data['cust_id']
        try:
            conn = sqlite3.connect(file['db'])
            cursor = conn.cursor()
            row = cursor.execute(
                "SELECT * FROM customer WHERE cid={}".format(int(cust_id))).fetchall()
            if (len(row) > 0):
                row = row[0]
                values = {
                    "present": 1,
                    "cid": row[0],
                    "ctype": row[1],
                    "title": row[2],
                    "fname": row[3],
                    "lname": row[4],
                    "dob": row[5],
                    "gender": row[6],
                    "maritalstatus": row[7],
                    "annualincome": row[8],
                    "fathername": row[9],
                    "mothername": row[10],
                    "add1": row[11],
                    "add2": row[12],
                    "add3": row[13],
                    "state": row[14],
                    "district": row[15],
                    "city": row[16],
                    "pincode": row[17],
                    "aadharno": row[18],
                    "panno": row[19],
                    "primaryno": row[20],
                    "secondaryno": row[21],
                    "email": row[22],
                }
            elif (len(row) == 0):
                values = {
                    "present": 0
                }

        except:
            print("DB Error")
        finally:
            conn.close()

        return jsonify(values)
