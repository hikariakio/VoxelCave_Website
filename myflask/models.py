from . import db

class VoxelModel(db.Model):
    __tablename__='voxelmodels'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True ,nullable = False)
    rating = db.Column (db.Integer)
    reviewCount = db.Column (db.Integer)
    price = db.Column (db.Float)
    discountpercent = db.Column (db.Integer)
    description = db.Column(db.String(500), nullable=False)
    image = db.Column(db.String(60), nullable=False, default = 'noimg.png')
    formatList = db.relationship('ModelFormat', backref='VoxelModel', cascade="all, delete-orphan")
    category = db.Column(db.String(32),db.ForeignKey('categories.id'),nullable = False)

    def __repr__(self):
        str = "Id: {}, Name: {}, Description: {}, Image: {}\n" 
        str =str.format( self.id, self.name,self.description,self.image)
        return str



class ModelFormat(db.Model):
    __tablename__='formats'
    name = db.Column(db.String(3),nullable=False,primary_key=True)
    model_id = db.Column(db.Integer, db.ForeignKey('voxelmodels.id'),primary_key=True)
    link = db.Column(db.String(50), nullable=False ,default = 'noimg.png')
    
    def __repr__(self):
        str = "Name: {}, For ModelID: {}" 
        str =str.format( self.name,self.model_id )
        return str

class ModelCategory(db.Model):
    __tablename__='categories'
    id= db.Column(db.Integer,nullable= False,primary_key = True)
    name = db.Column(db.String(32),nullable=False)
    modelList = db.relationship('VoxelModel', backref='ModelCategory', cascade="all, delete-orphan")

    def __repr__(self):
        str = "Name: {}" 
        str =str.format( self.name)
        return str

orderdetails = db.Table('orderdetails', 
    db.Column('order_id', db.Integer,db.ForeignKey('orders.id'), nullable=False),
    db.Column('model_id',db.Integer,db.ForeignKey('voxelmodels.id'),nullable=False),
    db.PrimaryKeyConstraint('order_id', 'model_id') )

class Order(db.Model):
    __tablename__='orders'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Boolean, default=False)
    firstname = db.Column(db.String(64))
    surname = db.Column(db.String(64))
    email = db.Column(db.String(128))
    phone = db.Column(db.String(32))
    totalcost = db.Column(db.Float)
    models = db.relationship("VoxelModel", secondary=orderdetails, backref="orders")
    
    def __repr__(self):
        str = "id: {}, Status: {}, Firstname: {}, Surname: {}, Email: {}, Phone: {}, models: {}, Total Cost: {}\n" 
        str =str.format( self.id, self.status,self.firstname,self.surname, self.email, self.phone, self.models, self.totalcost)
        return str
