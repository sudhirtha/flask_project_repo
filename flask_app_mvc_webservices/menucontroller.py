from flask_app_mvc_webservices.model import *
from flask import render_template,request,session


@app.route('/menu/',methods=['GET','POST'])
def save_update_menu():
  if 'userinfo' in session:
    msg=''
    if request.method=='POST':
            mid=int(request.form['mid'])
            name = request.form['mname']
            price=float(request.form['mprice'])
            menuhotels = request.form.getlist('menuhotels')
            dbmenu=Menu.query.filter_by(id=mid).first()
            if dbmenu:

                dbmenu.name=name
                dbmenu.price=price
                if menuhotels:
                    hotellist = []
                    for hotel in menuhotels:
                        hotellist.append(Hotel.query.filter_by(id=hotel).first())
                    dbmenu.href = hotellist
                db.session.commit()
                msg='Menu Updated Succesfully..!'
            else:
                dbmenu=Menu(name=name,price=price)
                hotellist = []
                if menuhotels:
                    for hotel in menuhotels:
                        hotellist.append(Hotel.query.filter_by(id=hotel).first())
                    dbmenu.href.extend(hotellist)
                db.session.add(dbmenu)
                db.session.commit()
                msg='Menu Created Succesfully..!'
    return  render_template('menu.html',
                            resp=msg,hotellist = Hotel.query.all(),
                            menu=Menu.get_dummy_menu(),
                            menulist=Menu.query.all(),
                            hotlist=Hotel.query.all(),
                            roomlist=Room.query.all(),
                            accountlist=Account.query.all())
  return render_template('login.html',resp='')

@app.route('/menu/edit/<int:mid>')
def edit_menu(mid):
 if 'userinfo' in session:
    return render_template('menu.html',hotellist = Hotel.query.all(),
                           menu=Menu.query.filter_by(id=mid).first(),
                           menulist=Menu.query.all(),
                           hotlist=Hotel.query.all(),
                           roomlist=Room.query.all(),
                           accountlist=Account.query.all())
 return render_template('login.html',resp='')



@app.route('/menu/delete/<int:mid>')
def delete_menu(mid):
 if 'userinfo' in session:
    msg=''
    menu=Menu.query.filter_by(id=mid).first()
    if menu:
        db.session.delete(menu)
        db.session.commit()
        msg='Menu Deleted Succesfully..!'
    return render_template('menu.html',
                           resp=msg,hotellist = Hotel.query.all(),
                           menu=Menu.get_dummy_menu(),
                           menulist=Menu.query.all(),
                           hotlist=Hotel.query.all(),
                           roomlist=Room.query.all(),
                           accountlist=Account.query.all()
                           )
 return render_template('login.html',resp='')


if __name__ == '__main__':
    app.run(debug=True)