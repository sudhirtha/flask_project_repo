from flask_app_mvc_webservices.configuration import db,app

class GenericModel(db.Model):
    __abstract__ = True
    created = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated = db.Column(db.DateTime, default=db.func.current_timestamp(),onupdate=db.func.current_timestamp())
    active = db.Column('active', db.String(10),default='Yes')

menu_hotel = db.Table('menu_hotel',
    db.Column('menu_id',db.ForeignKey('menu.menu_id')),
    db.Column('hotel_id',db.ForeignKey('hotel.hotel_id'))
)
class Menu(GenericModel):
    id = db.Column('menu_id', db.Integer(), primary_key=True)
    name = db.Column('menu_name', db.String(40),)
    price = db.Column('menu_price', db.Float())
    href = db.relationship('Hotel',secondary=menu_hotel, backref=db.backref("menuref", lazy=True))

    @staticmethod
    def get_dummy_menu():
       return Menu(id=0,name='',price=0.0)

room_hotel = db.Table('room_hotel',
                      db.Column('room_id',db.ForeignKey('room.room_id'),unique=False),
                      db.Column('hotel_id',db.ForeignKey('hotel.hotel_id'),unique=False)
                      )

class Hotel(GenericModel):
    id = db.Column('hotel_id',db.Integer(),primary_key=True)
    name = db.Column('hotel_name',db.String(40),unique=True)
    address = db.Column('hotel_address',db.String(40))
    contact = db.Column('hotel_contact',db.Integer())
    website = db.Column('hotel_website', db.String(40))
    accno = db.Column("acc_id", db.ForeignKey("account.acc_no"), unique=False, nullable=True)
    #menuref = db.relationship("Menu",secondary='menu_hotel',backref=db.backref("hotelref1",uselist=True))
    roomref = db.relationship("Room", secondary=room_hotel, backref=db.backref("rhotelref", uselist=True))
    orderref = db.relationship("Mainorder", lazy=True, backref="ohotelref", uselist=True)

    @staticmethod
    def get_dummy_hotel():
        return Hotel(id=0, name='', address='', contact=0,website='')

class Room(GenericModel):
    id = db.Column('room_id', db.Integer(), primary_key=True)
    type = db.Column('room_type', db.String(40),)
    charge = db.Column('room_charge',db.Float())
    status = db.Column('room_status',db.String(30))


    @staticmethod
    def get_dummy_room():
       return Room(id=0,type='',charge=0.0,status='')

class Account(GenericModel):
    id = db.Column('acc_no', db.Integer(), primary_key=True)
    type = db.Column('acc_type', db.String(40))
    balance = db.Column('acc_bal', db.Float())
    hotelref = db.relationship(Hotel,lazy=True,backref="haccref",uselist=True)
    custref = db.relationship("Customer",lazy=True,backref="caccref",uselist=True)

    @staticmethod
    def get_dummy_account():
       return Account(id=0,type='',balance=0.0)


class Customer(GenericModel):
    id = db.Column('cust_id', db.Integer(), primary_key=True)
    name = db.Column('cust_name', db.String(40), unique=True)
    address = db.Column('cust_address', db.String(40),)
    contact = db.Column('cust_contact',db.BigInteger())
    email = db.Column('cust_email',db.String(40))
    accno = db.Column("acc_id", db.ForeignKey("account.acc_no"), unique=False, nullable=True)
    orderref = db.relationship("Mainorder",lazy=True,backref="custref",uselist=True)

    @staticmethod
    def get_dummy_customer():
       return Customer(id=0,name='',address='',contact='',email='')

class ProcessedOrder(GenericModel):
    pid = db.Column('pr_order_id', db.Integer(), primary_key=True)
    orderId = db.Column("order_id",db.ForeignKey("mainorder.order_id"),unique=False)
    menuid =  db.Column("menus",db.ForeignKey("menu.menu_id"),unique=False,nullable=True)
    roomid = db.Column("room",db.ForeignKey("room.room_id"),unique=False,nullable=True)
    finalprice = db.Column('menu_price', db.Float())
    qty = db.Column('menu_qty', db.Integer())

class Mainorder(GenericModel):
    id = db.Column('order_id', db.Integer(), primary_key=True)
    csid = db.Column('cust_id', db.ForeignKey("customer.cust_id"),nullable=False,unique=False)
    htid = db.Column('hotel_id', db.ForeignKey("hotel.hotel_id"),nullable=False,unique=False)
    billamount = db.Column('total_bill', db.Float())


class Login(GenericModel):
    username=db.Column('username',db.String(50),primary_key=True)
    password=db.Column('password',db.String(50))




if __name__ == '__main__':
    # db.drop_all()
    db.create_all()

    # login=Login(username='sudhir',password='sudhir123')
    # db.session.add(login)
    # db.session.commit()
    #db.drop_all()

