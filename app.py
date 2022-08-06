from sqlalchemy import true
from myflask import create_app 
 
if __name__=='__main__':
    napp=create_app()
    napp.run(debug=True)
    napp.run(host='0.0.0.0', port=80)