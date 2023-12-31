from flask import render_template, Blueprint, request, url_for, session, redirect, flash, jsonify
import sqlite3
from static.python.paths import files as file, routes as route


account = Blueprint('account', __name__)

############################# Account Create #############################

@account.route(route['account']['create'], methods=['GET', 'POST'])
def accountCreate():
    if "bid" in session:
        try:
            conn = sqlite3.connect(file['db'])
            cursor = conn.cursor()
            rows = cursor.execute(
                "SELECT cid FROM customer ORDER BY cid ASC").fetchall()
            cids = [row[0] for row in rows]
        except:
            print("DB Error")
        finally:
            conn.close()

        if request.method == "POST":
            print(request.form)
            cid = int(request.form['custId'])
            atype = request.form['accttype']
            name1 = request.form['name1']
            name2 = request.form['name2']
            relation1 = request.form['relation1']
            relation2 = request.form['relation2']
            add1 = request.form['add1']
            add2 = request.form['add2']
            aadharno1 = request.form['aadharno1']
            aadharno2 = request.form['aadharno2']
            contactno1 = request.form['contactno1']
            contactno2 = request.form['contactno2']

            custData = (cid, atype)
            suretyData = (name1, name2, relation1, relation2, add1, add2,
                          aadharno1, aadharno2, contactno1, contactno2)
            colCustData = "cid, atype, "
            colSuretyData = ", name1, name2, relation1, relation2, add1, add2, aadharno1, aadharno2, contactno1, contactno2"
            famount=0
            sign="+"
            saidQuery=""
            if atype == "01":
                siamount = request.form['siamount']
                spurpose = request.form['spurpose']
                sir = request.form['sir']
                famount = siamount

                acctData = (siamount, spurpose, sir)
                colAcctData = "balance, purpose, interestrate"
            elif atype == "02":
                lamount = request.form['lamount']
                lpurpose = request.form['lpurpose']
                lrt = request.form['lrepaymenttenure']
                lri = request.form['lrepaymentir']
                ltramount = int(request.form['ltramount'].split(" ")[0])
                liamount = int(request.form['linterestamount'].split(" ")[0])
                lmi = request.form['lmi']

                if lamount == "01":
                    balance = "-25000"
                    amount = "25000"
                elif lamount == "02":
                    balance = "-50000"
                    amount = "50000"
                elif lamount == "03":
                    balance = "-100000"
                    amount = "100000"
                famount = amount
                acctData = (balance, amount, lpurpose, lrt,
                            lri, ltramount, liamount, lmi)
                colAcctData = "balance, amount, purpose, term, interestrate, finalamount, interestamount, monthlyinstallment"

                saidQuery = "SELECT aid FROM account WHERE cid={} and atype='01' ORDER BY aid ASC".format(cid)
                print(saidQuery)
            elif atype == "03": 
                fdamount = request.form['fdamount']
                fdpurpose = request.form['fdpurpose']
                fdterm = request.form['fdterm']
                fdir = request.form['fdir']
                fdmamount = int(request.form['fdmamount'].split(" ")[0])
                fdiamount = int(request.form['fdinterestamount'].split(" ")[0])

                if fdamount == "01":
                    amount = "10000"
                elif fdamount == "02":
                    amount = "25000"
                elif fdamount == "03":
                    amount = "50000"
                elif fdamount == "04":
                    amount = "75000"
                elif fdamount == "05":
                    amount = "100000"
                famount = amount
                acctData = (amount, fdpurpose, fdterm,
                            fdir, fdmamount, fdiamount)
                colAcctData = "amount, purpose, term, interestrate, finalamount, interestamount"
                
            elif atype == "04":
                rdamount = request.form['rdamount']
                rdpurpose = request.form['rdpurpose']
                rdterm = request.form['rdterm']
                rdir = request.form['rdir']
                rdmamount = int(request.form['rdmamount'].split(" ")[0])
                rdiamount = int(request.form['rdinterestamount'].split(" ")[0])
                rdmi = request.form['rdmi']

                if rdamount == "01":
                    balance = "-10000"
                    amount = "10000"
                elif rdamount == "02":
                    balance = "-25000"
                    amount = "25000"
                elif rdamount == "03":
                    balance = "-50000"
                    amount = "50000"
                elif rdamount == "04":
                    balance = "-75000"
                    amount = "75000"
                elif rdamount == "05":
                    balance = "-100000"
                    amount = "100000"
                famount = amount
                acctData = (balance, amount, rdpurpose, rdterm,
                            rdir, rdmamount, rdiamount, rdmi)
                colAcctData = "balance, amount, purpose, term, interestrate, finalamount, interestamount, monthlyinstallment"

            cols = colCustData+colAcctData+colSuretyData
            data = custData+acctData+suretyData

            acctQuery = "INSERT INTO account ({}) VALUES {}".format(cols, data)
            print("INSERT QUERY: {}".format(acctQuery))
            try:
                conn = sqlite3.connect(file['db'])
                cursor = conn.cursor()
                cursor.execute(acctQuery)
                conn.commit()
                
                if atype == "01":
                    if(famount!="0"):
                        aid = cursor.lastrowid
                        transactionQuery =  """ INSERT INTO transactions (aid, cid, atype, ttype, amount, description)
                                                VALUES ('{}', '{}', '{}', '{}', '{}', '{}')
                                            """.format(aid, cid, atype, '01', famount, 'Initial Deposit')
                        bankQuery = """ UPDATE bank 
                                    SET balance = CAST((CAST(balance AS INTEGER) {} {}) AS TEXT)
                                    WHERE id='101'""".format(sign, famount)
                    
                        cursor.execute(transactionQuery)
                        cursor.execute(bankQuery)
                        conn.commit()
                    flash('Saving Account Created', 'success')
                elif atype == "02":
                    flash('Loan Account Created', 'success')
                    said = cursor.execute(saidQuery).fetchall()[0][0]
                    print(said)
                    squery = """ UPDATE account
                        SET balance = CAST((CAST(balance AS INTEGER) + {}) AS TEXT)
                        WHERE aid={}
                    """.format(famount, said)
                    cursor.execute(squery)
                    conn.commit()
                    
                    sign="-"
                elif atype == "03":
                    flash('FD Account Created', 'success')
                elif atype == "04":
                    flash('RD Account Created', 'success')

                
                
                    
            except Exception as e:
                print(e)
            finally:
                conn.close()

            return redirect(url_for("home.home_home"))
        else:
            return render_template(file['account']['create'], cids=cids)
    else:
        return redirect(url_for('auth.login'))

############################# Account Search #############################


@account.route(route['account']['search'], methods=["GET", "POST"])
def accountSearch():
    if "bid" in session:
        if request.method == "POST":
            data = request.get_json()
            fields = data['fields']
            searchby = data['searchby']
            if fields == "all":
                if (searchby == "01"):
                    query = "SELECT * FROM account ORDER BY aid ASC"
                elif (searchby == "02"):
                    aid = data['value']
                    query = "SELECT * FROM account WHERE aid={}".format(
                        int(aid))
            elif fields == "aid":
                if (searchby == "02"):
                    aid = data['value']
                    query = "SELECT aid FROM account WHERE aid={}".format(
                        int(aid))
            elif fields == "aid-atype-dt":
                if (searchby == "02"):
                    cid = data['value']
                    query = "SELECT aid, atype, createdt FROM account WHERE cid={}".format(
                        int(cid))
            print(query)

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
            return render_template(file['account']['search'])

    else:
        return redirect(url_for('auth.login'))

############################# Account Info #############################


@account.route(route['account']['info'], methods=['GET', 'POST'])
def accountInfo():
    if "bid" in session:
        aid = request.args.get('aid')
        if aid:
            return render_template(file['account']['info'], aid=aid)
        else:
            return redirect(url_for('account.accountSearch'))
    else:
        return redirect(url_for('auth.login'))
