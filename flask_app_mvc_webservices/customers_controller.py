from flask_app_mvc_webservices.model import *
from flask_app_mvc_webservices.hotelcontroller import remaining_accounts
from flask import render_template,request,redirect,url_for,session
from flask_app_mvc_webservices.logincontroller import hotel_booking
from flask_app_mvc_webservices.configuration import db,app

@app.route('/registration/',methods=['GET','POST'])
def register_customer():
    msg = ''
    if request.method == 'POST':
        custid = int(request.form['custid'])
        custname = request.form['custname']
        custadr = request.form['custadr']
        custcont = request.form['custcont']
        custmail = request.form['custmail']
        custaccno = request.form['custaccno']
        username = Login.query.filter_by(username=request.form['custname']).first()
        dbcust = Customer.query.filter_by(id=custid).first()
        if dbcust:
            dbcust.id = custid
            dbcust.name = custname
            dbcust.address = custadr
            dbcust.contact = custcont
            dbcust.email = custmail
            username.username = custname
            username.password = request.form['custpass']
            if custaccno:
                dbcust.accno = custaccno
            db.session.commit()
            msg = "Customer Data Updated Successfully..!"
            return redirect(url_for('hotel_booking'))

        else:
            dbcust = Customer(id=custid, name=custname, address=custadr, contact=custcont, email=custmail)
            dbcustomer = Login(username=request.form['custname'], password=request.form['custpass'])
            if username:
                msg = "Username Already Exit...!"
                return render_template('customer.html',
                                       resp=msg,
                                       cust=dbcust,
                                       acclist=remaining_accounts())
            if custaccno:
                dbcust.accno = custaccno
            db.session.add_all([dbcust,dbcustomer])
            db.session.commit()
            msg = "Registration Successfully...!"
            return render_template('login.html',resp=msg)

    return render_template('customer.html',
                           resp=msg,
                           cust=Customer.get_dummy_customer(),
                           acclist=remaining_accounts())

@app.route('/customer/edit/<user>')
def edit_customer_info(user):
    if 'userinfo' in session:
        cust = Customer.query.filter(Customer.name==user).first()
        if cust:
            return render_template('customer.html',
                                   resp='',
                                   cust=cust,
                                   acclist=remaining_accounts())
    return render_template('login.html', resp='')