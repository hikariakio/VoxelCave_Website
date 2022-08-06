from pickle import NONE
from unicodedata import category, name
from flask import Blueprint, render_template, request, flash, session,redirect,url_for
from .models import ModelCategory, VoxelModel,ModelFormat,Order
from .forms import CheckoutForm

from . import db

# merrygo = Model(1,"Merry Go",3,16,"merrygo.png",50,["fbx","obj","max"],80,"This is a ship decription")
# pig = Model(2,"Pinky Piggy",2,2,"pig_card.png",30,["fbx"],0,"This is a pig decription")
# lawrence = Model(3,"QUT Lawrence",5,777,"qut_lawrence.png",999,["fbx","max"],0,"This is a pig decription")
# house = Model(4,"Choco House",4,5,"choco_house.png",10,["fbx","max","obj"],0,"This is a pig decription")

# modelList = [merrygo,pig,lawrence,house]

bp = Blueprint('main', __name__)

@bp.route('/',methods=['POST','GET'])
def index():
    sort = request.values.get('sort')
    discount = request.values.get('discountonly') 
 
    modelQuery = VoxelModel.query
    modelList, sort,discount = sortmodel(modelQuery,sort,discount)
        
    showText = 'Voxel Models'       
    catList = ModelCategory.query.order_by(ModelCategory.name).all()
    return render_template('index.html',models = modelList,category = catList,showText=showText,sortMode = sort,discountMode = discount)

# @bp.route('/#modellist')
# def indexToList(modelList,catList,showText):
#     return render_template('index.html',models = modelList,category = catList,showText=showText)

# @bp.route('/sc',methods=['POST','GET'])
# def category():
#     catKey =  request.values.get('searchCategory')  
#     cat= ModelCategory.query.filter_by(name = catKey).first()
#     if cat is None :
#         modelList =[]
#     else:
#         modelList = VoxelModel.query.filter_by(category = cat.id).all()
#     if len(modelList) == 0 :
#         showText = "No Result, try again!" 
#     else:
#         showText = "Showing  '{}'  Voxel Models".format(cat.name)
#     catList = ModelCategory.query.order_by(ModelCategory.name).all()
#     return render_template('index.html',models = modelList,category = catList,showText=showText)

# @bp.route('/search',methods=['POST','GET'])
# def search():
#     oriKey =  request.values.get('key')  
#     if(not oriKey):
#         return redirect(url_for('main.index'))
#     key = '%{}%'.format(oriKey)
#     modelList = VoxelModel.query.filter(VoxelModel.description.like(key)).all()

#     if len(modelList) == 0 :
#         showText = "No Result, try again!" 
#     else:
#         showText = "Showing '{}' related {} item(s)".format(oriKey,len(modelList))

#     catList = ModelCategory.query.order_by(ModelCategory.name).all()
#     return render_template('index.html',models = modelList,category = catList,showText=showText)

@bp.route('/filter',methods=['POST','GET'])
def filter():
    sort = request.values.get('sort') 
    discount = request.values.get('discountonly') 
    
    # searchccategory more prioritized
    catKey =  request.values.get('searchCategory') 
    
    if(catKey is not None):  
        cat= ModelCategory.query.filter_by(name = catKey).first()
        if cat is None :
            modelList =[]
        else:
            modelQuery = VoxelModel.query.filter_by(category = cat.id)
            modelList, sort ,discount= sortmodel(modelQuery,sort,discount)

        if len(modelList) == 0 :
            showText = "No Result, try again!" 
        else:
            showText = "Showing  '{}'  Voxel Models".format(cat.name)
        
    else:
        oriKey =  request.values.get('key')  
        if(not oriKey):
            return redirect(url_for('main.index',sort =sort))
        key = '%{}%'.format(oriKey)
        modelQuery = VoxelModel.query.filter(VoxelModel.description.like(key))
        modelList, sort ,discount= sortmodel(modelQuery,sort,discount)
       

        if len(modelList) == 0 :
            showText = "No Result, try again!" 
        else:
            showText = "Showing '{}' related {} item(s)".format(oriKey,len(modelList))

    catList = ModelCategory.query.order_by(ModelCategory.name).all()
    return render_template('index.html',models = modelList,category = catList,showText=showText,sortMode = sort,discountMode = discount)

def sortmodel(query,sorttag,discounttag):
    if(discounttag == 'true'):
        query = query.filter(VoxelModel.discountpercent > 0)
    else:
        discounttag='false'
    if(sorttag == 'lowprice'):
        sorttag = 'Low Price'
        modelList = query.order_by(VoxelModel.price * 0.01* (100 -VoxelModel.discountpercent)).all()
    elif(sorttag =='rating'):
        sorttag = 'Rating'
        modelList = query.order_by(VoxelModel.rating.desc(),VoxelModel.name).all()
    else:
        sorttag = 'Name'
        modelList = query.order_by(VoxelModel.name).all()
    
    return modelList,sorttag,discounttag


@bp.route('/model/<modelID>/<modelName>')
def detail(modelID ,modelName):   
    curModel = VoxelModel.query.filter_by(id = modelID).first()
    curCat = ModelCategory.query.filter_by(id = curModel.category).first()
    return render_template('detail.html',model = curModel,category = curCat)

@bp.route('/cart', methods=['POST','GET'])
def cart():   
    modelID =  request.values.get('modelID')  

    if 'order_id'in session.keys():
        order = Order.query.get(session['order_id'])
        # order will be None if order_id stale
    else:
        # there is no order
        order = None

    # create new order if needed
    if order is None:
        order = Order(status = False, firstname='', surname='', email='', phone='', totalcost=0)
        try:
            db.session.add(order)
            db.session.commit()
            session['order_id'] = order.id
        except:
            print('failed at creating a new order')
            order = None
    
    # calcultate totalprice
    totalprice = 0
    if order is not None:
        for model in order.models:
            totalprice = totalprice + (model.price * 0.01* (100-model.discountpercent))

    savedprice = 0
    if order is not None:
        for model in order.models:
            savedprice = savedprice + (model.price * 0.01* (model.discountpercent))

    # are we adding an item?
    if modelID is not None and order is not None:
        model = VoxelModel.query.get(modelID)
        if model not in order.models:
            try:
                order.models.append(model)
                db.session.commit()
            except:
                return 'There was an issue adding the item to your basket'
            return redirect(url_for('main.cart'))
        else:
            flash('item already in basket')
            return redirect(url_for('main.cart'))
    print(order)
    print(totalprice)
    print(savedprice)
    return render_template('cart.html',orderlist = order ,totalprice = totalprice, savedprice= savedprice)

@bp.route('/deleteitem', methods=['GET'])
def deletecartitem():
    modelID =  request.values.get('modelID')  

    if 'order_id' in session:
        order = Order.query.get_or_404(session['order_id'])
        model_to_del = VoxelModel.query.get(modelID)
        try:
            order.models.remove(model_to_del)
            db.session.commit()
            return redirect(url_for('main.cart'))
        except:
            return 'Problem deleting item from order'
    return redirect(url_for('main.cart'))

@bp.route('/deletecart')
def deletecart():
    if 'order_id' in session:
        del session['order_id']
        flash('All items deleted')
    return redirect(url_for('main.index'))


@bp.route('/checkout', methods=['POST','GET'])
def checkout():
    form = CheckoutForm() 
    totalcost = 0
    if 'order_id' in session:
        order = Order.query.get_or_404(session['order_id'])
        
        if(len(order.models) == 0):
            flash('Sorry! No item in the cart.')
            return redirect(url_for('main.index'))

        for model in order.models:
            totalcost = totalcost + (model.price * 0.01* (100-model.discountpercent))

        if form.validate_on_submit():
            order.status = True
            order.firstname = form.firstname.data
            order.surname = form.lastname.data
            order.email = form.email.data
            order.phone = form.phone.data

            totalcost = 0
            for model in order.models:
                totalcost = totalcost + (model.price * 0.01* (100-model.discountpercent))

            order.totalcost = totalcost

            try:
                db.session.commit()
                del session['order_id']
                flash('Thank you, {}. Your order has been recevied!'.format(form.firstname.data))
                return redirect(url_for('main.index'))
            except:
                return 'There was an issue completing your order'
    else:
        flash('Sorry! No Item in the cart.')
        return redirect(url_for('main.index'))

    return render_template('checkout.html', form = form,totalcost = totalcost)






def WithArgs(*list):
    for ele in list:
        print("{0} : {1} ".format(ele, request.args.get(ele)))  # only with GET

def WithValues(*list):
    for ele in list:
        print("{0} : {1} ".format(ele, request.values.get(ele)))  # GET/POST

def WithForms(*list):
    for ele in list:
        print("{0} : {1} ".format(ele, request.form.get(ele)))  # FORM/post 
