from flask import render_template, Blueprint, request, url_for, session, redirect, jsonify, flash
import sqlite3
from static.python.paths import files as file, routes as route

transaction = Blueprint('transaction', __name__)

############################# Transaction Home #############################


@transaction.route(route['transaction']['transaction'], methods=['GET', 'POST'])
def transaction_home():
    if "bid" in session:
        if request.method == "POST":
            data = request.get_json()
            print(data)
            cid = data['cid']
            aid = data['aid']
            aid2 = data['aid2']
            atype = data['atype']
            ttype = data['ttype']
            amount = int(data['amount'])
            description = data['description']

            sign = ""
            result = ""

            transactionQuery = """  INSERT INTO transactions (aid, cid, atype, ttype, amount, description)
                                    VALUES ('{}', '{}', '{}', '{}', '{}', '{}')
                                """.format(aid, cid, atype, ttype, amount, description)


            if ttype == "01":
                query = """ UPDATE account
                            SET balance = CAST((CAST(balance AS INTEGER) + {}) AS TEXT)
                            WHERE aid={}
                        """.format(amount, aid)
                sign = '+'
            elif ttype == "02":
                query = """ UPDATE account 
                            SET balance = CAST((CAST(balance AS INTEGER) - {}) AS TEXT)
                            WHERE aid={} AND CAST(balance AS INTEGER) - {} >= 0
                        """.format(amount, aid, amount)
                sign = '-'
            elif ttype == "03":
                query = """ UPDATE account
                            SET balance = CAST((CAST(balance AS INTEGER) + {}) AS TEXT)
                            WHERE aid={};
                            UPDATE account
                            SET balance = CAST((CAST(balance AS INTEGER) - {}) AS TEXT)
                            WHERE aid={} AND CAST(balance AS INTEGER) - {} >= 0;
                        """.format(amount, aid2, amount, aid, amount)
                transactionQuery = """ INSERT INTO transactions (aid, aid2, cid, atype, ttype, amount, description)
                                        VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}')
                                    """.format(aid, aid2, cid, atype, ttype, amount, description)

            bankQuery = """ UPDATE bank 
                            SET balance = CAST((CAST(balance AS INTEGER) {} {}) AS TEXT)
                            WHERE id='101'""".format(sign, amount)
            print(query)
            print(transactionQuery)
            print(bankQuery)

            try:
                conn = sqlite3.connect(file['db'])
                cursor = conn.cursor()
                cursor.executescript(query)

                if ttype == "01":
                    cursor.execute(transactionQuery)
                    cursor.execute(bankQuery)
                    conn.commit()
                    result = "success"

                elif ttype == "02":
                    if cursor.rowcount == 0:
                        print("Account has no money")
                        result = "failure"
                    else:
                        cursor.execute(transactionQuery)
                        cursor.execute(bankQuery)
                        conn.commit()
                        result = "success"
                elif ttype == "03":
                    if cursor.rowcount == 0:
                        print("Account has no money")
                        result = "failure"
                    else:
                        cursor.execute(transactionQuery)
                        conn.commit()
                        result = "success"

                if result == "success":
                    pass

            except Exception as e:
                print(e)
            finally:
                conn.close()

            print(result)
            return jsonify({'result': result})
        else:
            return render_template(file['transaction'])
    else:
        return redirect(url_for('auth.login'))

############################# Transaction Search #############################


@transaction.route(route['transaction']['search'], methods=['GET', 'POST'])
def transactionSearch():
    if "bid" in session:
        if request.method == "POST":
            data = request.get_json()
            print("Data: ", data)
            aid = data['aid']
            query = """ SELECT ttype, aid2, amount, description, dt 
                        FROM transactions 
                        WHERE aid={}
                        ORDER BY tid ASC
                    """.format(int(aid))

            print("The Query for Transaction Search is: "+query)
            try:
                conn = sqlite3.connect(file['db'])
                cursor = conn.cursor()
                row = cursor.execute(query).fetchall()

                data = {'results': row}
            except:
                print("DB Error")
            finally:
                conn.close()

            return jsonify(data)
    else:
        return redirect(url_for('auth.login'))
