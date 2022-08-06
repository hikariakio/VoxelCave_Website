def AddCategoryToDB(_id,_name):
    return ModelCategory (id = _id ,name = _name)

def AddVoxelModelToDB(_id,_name,star,review,_price,discount,desc,img,cat):
    return VoxelModel(id = _id,name = _name,rating = star,reviewCount = review,price = _price,discountpercent = discount,description = desc,image = img,category = cat)

def AddFormatToDB(_name,_modelID):
    return ModelFormat (name = _name , model_id = _modelID)

from myflask.models import ModelCategory, VoxelModel, ModelFormat
from myflask import db,create_app

import os
os.remove("myflask/voxelcave.sqlite")

app = create_app()
ctx = app.app_context()
ctx.push()

db.create_all()

c1 = AddCategoryToDB(1,'People')
c2 = AddCategoryToDB(2,'House')
c3 = AddCategoryToDB(3,'Vehicle')
c4 = AddCategoryToDB(4,'Animal')

db.session.add(c1)
db.session.add(c2)
db.session.add(c3)
db.session.add(c4)


m1 = AddVoxelModelToDB(77401,'Pinky Piggy',2,2,30,0,'This is a pig','pig_card.png',4)
m2 = AddVoxelModelToDB(77501,'Merry Go',3,16,60,80,'This is a ship','merrygo.png',3)
m3 = AddVoxelModelToDB(77601,'QUT Lawrence',5,777,99,0,'This is Lawrence','qut_lawrence.png',1)
m4 = AddVoxelModelToDB(77701,'Choco House',4,5,60,50,'This is a house','choco_house.png',2)
m5 = AddVoxelModelToDB(77801,'Bin Duck',2,100,15,0,'This is a duck','duck_card.jpg',4)
m6 = AddVoxelModelToDB(77901,'Arvo Jet',4,10,75,10,'This is an aircraft','craft.jpg',3)
m7 = AddVoxelModelToDB(78001,'Shorty Witch',5,55,50,5,'This is a witch and her ghost family. Spooky! ','witch.JPG',1)

db.session.add(m1)
db.session.add(m2)
db.session.add(m3)
db.session.add(m4)
db.session.add(m5)
db.session.add(m6)
db.session.add(m7)

f1 = AddFormatToDB('obj',77401)
f2 = AddFormatToDB('fbx',77401)
f3 = AddFormatToDB('obj',77501)
f4 = AddFormatToDB('fbx',77501)
f5 = AddFormatToDB('max',77501)
f6 = AddFormatToDB('obj',77601)
f7 = AddFormatToDB('fbx',77701)
f8 = AddFormatToDB('fbx',77801)
f9 = AddFormatToDB('obj',77801)
f10 = AddFormatToDB('obj',77901)
f11 = AddFormatToDB('fbx',78001)

db.session.add(f1)
db.session.add(f2)
db.session.add(f3)
db.session.add(f4)
db.session.add(f5)
db.session.add(f6)
db.session.add(f7)
db.session.add(f8)
db.session.add(f9)
db.session.add(f10)
db.session.add(f11)

db.session.commit()
