from flask_app_mvc_webservices.model import *
from flask import render_template,request,session,url_for,redirect

@app.route('/login/',methods=['GET','POST'])
def login_user():
    msg=''
    if request.method=='POST':
        fuser=request.form['user']
        fpass=request.form['pass']
        login=Login.query.filter(Login.username==fuser,Login.password==fpass).first()
        if login:
            if login.username == 'admin' and login.password == 'admin123':
                session['userinfo'] = login.username
                return redirect(url_for('dashboard_page'))
            else:
                session['userinfo'] = login.username
                return redirect(url_for('hotel_booking'))
        msg = "Invalid Credentials"
    return render_template('login.html', resp=msg)

@app.route('/home/',methods=['GET'])
def dashboard_page():
    if 'userinfo' in session:
        return render_template('dashboard.html', user=session['userinfo'],
                               hotellist=Hotel.query.all(),hotel='',
                               acclist=Account.query.all(),account='',
                               roomlist=Room.query.all(),room='',
                               menulist=Menu.query.all(),menu='')
    return render_template('login.html', resp='')

@app.route('/logout/',methods=['GET'])
def logout():
    if 'userinfo' in session:
        session.pop('userinfo')
    return render_template('login.html', resp='')

@app.route('/hotel_booking/',methods=['GET'])
def hotel_booking():
    if 'userinfo' in session:
        return render_template('book_hotel.html',user=session['userinfo'],hotellist=Hotel.query.all())
    return render_template('login.html', resp='')

@app.route('/booked/<user>')
def room_booking(user):
    if 'userinfo' in session:
        return render_template('booking_room.html',user=user,)
    return render_template('login.html', resp='')



if __name__ == '__main__':
    app.run(debug=True)


