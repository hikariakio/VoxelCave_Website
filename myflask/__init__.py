#import flask - from the package import a module
from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

db=SQLAlchemy()
app=Flask(__name__)  # this is the name of the module/package that is calling this app

#create a function that creates a web application
# a web server will run this web application
def create_app():
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.debug = True
    app.secret_key='mysecretkeybutstupid'
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///voxelcave.sqlite'
    app.config['SESSION_COOKIE_SECURE'] = False
    app.config['BOOTSTRAP_SERVE_LOCAL'] = True
    app.static_folder = 'static'
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    
    db.init_app(app)
    bootstrap = Bootstrap(app)

    #add the Blueprint
    from . import views
    app.register_blueprint(views.bp)
   
    return app

@app.errorhandler(404) 
# inbuilt function which takes error as parameter 
def not_found(e): 
    return render_template("404.html")

@app.errorhandler(500)
def internal_error(e):
    return render_template("500.html")