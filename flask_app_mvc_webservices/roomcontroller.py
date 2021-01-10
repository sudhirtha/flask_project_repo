from flask_app_mvc_webservices.model import *
from flask_app_mvc_webservices.configuration import app,db
from flask import request,render_template,session


@app.route('/room/',methods=['GET','POST'])
def save_or_update_rooms():
    if 'userinfo' in session:
        msg  = ''
        if request.method == 'POST':
            rid = int(request.form['rid'])
            type = request.form['rtype']
            charge = request.form['rcharge']
            status = request.form['rstatus']
            hotelids = request.form.getlist('hotelid')
            dbroom = Room.query.filter_by(id=rid).first()
            if dbroom:
                dbroom.type = type
                dbroom.charge = charge
                dbroom.status = status
                hotellist = []
                for hotel in hotelids:
                    hotellist.append(Hotel.query.filter_by(id=hotel).first())
                dbroom.rhotelref = hotellist
                db.session.commit()
                msg = "Room Info Updated Successfully..!"
            else:
                dbroom = Room(id=rid,type=type,charge=charge,status=status)
                hotellist = []
                for hotel in hotelids:
                    hotellist.append(Hotel.query.filter_by(id=hotel).first())
                dbroom.rhotelref.extend(hotellist)
                db.session.add(dbroom)
                db.session.commit()
                msg = "Room Info Created Successfully...!"

        return render_template('room.html',
                               resp = msg,
                               hotellist=Hotel.query.all(),
                               room = Room.get_dummy_room(),
                               roomlist =Room.query.all(),
                               hotlist=Hotel.query.all(),
                               menulist=Menu.query.all(),
                               accountlist=Account.query.all()
                               )

    return render_template('login.html',resp='')

@app.route('/room/edit/<int:rid>')
def edit_Room_info(rid):
    if 'userinfo' in session:
        return render_template('room.html',
                               resp='',hotellist=Hotel.query.all(),
                               room=Room.query.filter_by(id=rid).first(),
                               roomlist=Room.query.all(),
                               hotlist=Hotel.query.all(),
                               menulist=Menu.query.all(),
                               accountlist=Account.query.all()
                               )
    return render_template('login.html',resp='')




@app.route('/room/delete/<int:rid>')
def delete_Room_info(rid):
    if 'userinfo' in session:
        msg = ''
        room = Room.query.filter_by(id=rid).first()
        if room:
            db.session.delete(room)
            db.session.commit()
            msg = "Room Removed Successfully..!"
        return render_template('room.html',hotellist=Hotel.query.all(),
                               resp=msg,
                               room=Room.get_dummy_room(),
                               roomlist=Room.query.all(),
                               hotlist = Hotel.query.all(),
                               menulist = Menu.query.all(),
                               accountlist = Account.query.all()
                               )
    return render_template('login.html',resp='')

FLAG = True

@app.route('/room/<val>',methods=['GET'])
def toggle_room_type(val):
    if 'userinfo' in session:
        global FLAG
        allrooms = Room.query.all()
        if FLAG:
            if val == 'rid':
                allrooms.sort(key=lambda room : room.id,reverse =True)
            elif val == 'rtype':
                allrooms.sort(key=lambda room : room.type)
            elif val == 'rcharge':
                allrooms.sort(key=lambda room: room.charge)
            elif val == 'rstatus':
                allrooms.sort(key=lambda room: room.status)
            FLAG = False
        else:
            FLAG = True
        return render_template('room.html',
                               resp='',user=session['userinfo'],
                               room=allrooms,
                               roomlist=allrooms)

    return render_template('login.html',resp='')
if __name__ == '__main__':
    app.run(debug=True)