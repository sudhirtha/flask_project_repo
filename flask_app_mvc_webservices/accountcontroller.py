from flask_app_mvc_webservices.configuration import db,app
from flask_app_mvc_webservices.model import*
from flask import render_template,request,session

@app.route('/account/',methods=['GET','POST'])
def save_update_account():
 if 'userinfo' in session:
    msg=''
    if request.method=='POST':
        accno=int(request.form['accno'])
        acctype = request.form['accty']
        accbal= request.form['accbal']
        dbacc=Account.query.filter_by(id=accno).first()
        if dbacc:
            dbacc.type=acctype
            dbacc.balance=accbal
            db.session.commit()
            msg='Account Updated Succesfully..!'
        else:
            dbacc=Account(id=accno,type=acctype,balance=accbal)
            db.session.add(dbacc)
            db.session.commit()
            msg='Account Created Succefully..!'

    return render_template('account.html',
                           reso=msg,user=session['userinfo'],
                           account=Account.get_dummy_account(),
                           acclist=Account.query.all(),
                           hotlist=Hotel.query.all(),
                           menulist=Menu.query.all(),
                           roomlist=Room.query.all()
                           )

 return render_template('login,html', resp='')



@app.route('/edit/<int:acid>')
def edit_account(acid):
    if 'userinfo' in session:
      return render_template('account.html',user=session['userinfo'],
                           account=Account.query.filter_by(id=acid).first(),
                           acclist=Account.query.all(),
                           hotlist=Hotel.query.all(),
                           menulist=Menu.query.all(),
                           roomlist=Room.query.all()
                         )
    return render_template('login.html',resp='')


@app.route('/delete/<int:acid>')
def delete_account(acid):
    if 'userinfo' in session:
        msg=''
        acc=Account.query.filter_by(id=acid).first()
        if acc:
            db.session.delete(acc)
            db.session.commit()
            msg='Account Delete Succesfully..!'
        return render_template('account.html',
                               resp=msg,user=session['userinfo'],
                               account=Account.get_dummy_account(),
                               acclist=Account.query.all(),
                               hotlist=Hotel.query.all(),
                               menulist=Menu.query.all(),
                               roomlist=Room.query.all()
                               )

    return render_template('login.html',resp='')


if __name__ == '__main__':
    app.run(debug=True)