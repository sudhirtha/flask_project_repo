from flask_app_mvc_webservices.model import *
from flask import render_template,request,session


def remaining_accounts():
    acclist = Account.query.all()
    accl = []
    for acc in acclist:
        if not acc.hotelref and not acc.custref:
            accl.append(acc)
    return accl

@app.route('/hotel/',methods=['GET','POST'])
def save_update_hotel():
 if 'userinfo' in session:
    msg=''
    if request.method=='POST':
            hid=int(request.form['hid'])
            name = request.form['hname']
            address= request.form['haddress']
            contact= int(request.form['hcontact'])
            website= request.form['hwebsite']
            dbhotel=Hotel.query.filter_by(id=hid).first()
            if dbhotel:
                dbhotel.id = hid
                dbhotel.name=name
                dbhotel.address=address
                dbhotel.contact=contact
                dbhotel.website=website
                hotelaccno = request.form['hotelaccno']
                if hotelaccno:
                    dbhotel.accno = hotelaccno
                db.session.commit()
                msg='Hotel Updated Succesfully..!'
            else:
                dbhotel=Hotel(id=hid,name=name,address=address,contact=contact,website=website)
                hotelaccno = request.form['hotelaccno']
                if hotelaccno:
                    dbhotel.accno = hotelaccno
                db.session.add(dbhotel)
                db.session.commit()
                msg='Hotel Created Succesfully..!'
    return  render_template('hotel.html',
                            resp=msg,
                            hotel=Hotel.get_dummy_hotel(),
                            hotellist=Hotel.query.all(),
                            acclist1= remaining_accounts(),
                            accountlist=Account.query.all(),
                            roolist=Room.query.all(),
                            menulist=Menu.query.all())
 return render_template('login.html',resp='')

@app.route('/hotel/edit/<int:hid>')
def edit_hotel(hid):
  if 'userinfo' in session:
    hotel = Hotel.query.filter_by(id=hid).first()
    return render_template('hotel.html',
                           hotel=hotel,
                           hotellist=Hotel.query.all(),
                           acclist = remaining_accounts(),
                           accountlist=Account.query.all(),
                           roolist=Room.query.all(),
                           menulist=Menu.query.all())

  return render_template('login.html',resp='')


@app.route('/hotel/delete/<int:hid>')
def delete_hotel(hid):
  if 'userinfo' in session:
    msg=''
    hotel=Hotel.query.filter_by(id=hid).first()
    if hotel:
        db.session.delete(hotel)
        db.session.commit()
        msg='Hotel Deleted Succesfully..!'
    return render_template('hotel.html',
                           resp=msg,
                           hotel=Hotel.get_dummy_hotel(),
                           hotellist=Hotel.query.all(),
                           acclist=remaining_accounts(),
                           accountlist=Account.query.all(),
                           roolist=Room.query.all(),
                           menulist=Menu.query.all())
  return render_template('login.html',resp='')


if __name__ == '__main__':
    app.run(debug=True)


