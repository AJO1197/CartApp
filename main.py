from flask import Flask
from flask import jsonify
from flask_restful import reqparse
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from connexion.apps.flask_app import FlaskJSONEncoder
from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import JWTManager
from flask_jwt_extended import (create_access_token, get_jwt_identity,jwt_required)

itemIds=["Apple","Banana","Orange","Mango"]

class CustomJSONEncoder(FlaskJSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)

        return super().default(o)

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/CartAPI"
app.config["DEBUG"] = True
app.json_encoder = CustomJSONEncoder
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'

parser = reqparse.RequestParser()
parser.add_argument('username', help = 'This field cannot be blank', required = True)
parser.add_argument('password', help = 'This field cannot be blank', required = True)

cartParser = reqparse.RequestParser()
cartParser.add_argument('cartId', help = 'This field cannot be blank', required = True)
cartParser.add_argument('itemId', help = 'This field cannot be blank', required = True)
cartParser.add_argument('Quantity', help = 'This field cannot be blank', required = True)

cartParser2 = reqparse.RequestParser()
cartParser2.add_argument('cartId', help = 'This field cannot be blank', required = True)


mongo=PyMongo(app)
jwt = JWTManager(app)

@app.route('/register', methods=['POST'])
def userRegistration():
    data = parser.parse_args()
    jsonify(data)
    if data.username=="" or data.password=="":
        return {"error":"Username or password cannot be blank"}
    try:
        user=mongo.db.users.find_one({"username":data.username})
        if user:
            raise Exception()
        
        data.password=sha256.hash(data.password)
        mongo.db.users.insert_one(data)
        refresh_token=create_access_token(identity=data['_id'])
        return {"Message":"Congratulations User created successfully!","token":refresh_token}
    except:
        return {"error":"Username already exists or MongoDB cannot be reached please wait!"}

@app.route('/login', methods=['POST'])
def userLogin():
    data=parser.parse_args()
    jsonify(data)
    
    try:
        user=mongo.db.users.find_one({"username":data.username})
        if not user:
            return {"User not Found"}
        if sha256.verify(data.password,user['password']):
            refresh_token=create_access_token(identity=user['_id'])
            return {"Message":"Successful Login","token":refresh_token}
        else:
            return {"Wrong password"}
    except:
        return {"error":"Database error try again after sometime"}
            
            
@app.route("/createCart", methods=["GET"])
@jwt_required()
def createCart():
    current_user = get_jwt_identity() 
    try:
        user=mongo.db.users.find_one({"_id":ObjectId(current_user)})
        if not user:
            return {"error":"Token Not Valid!"}
        cart={"Creator":current_user,"items":{}}
        mongo.db.carts.insert_one(cart)
        return cart
    except:
        return {"error":"Database error try again after sometime"}

@app.route("/addToCart", methods=["POST"])
@jwt_required()
def addToCart():
    current_user = get_jwt_identity()
    data=cartParser.parse_args()
    jsonify(data)
    Quantity=0
    try:
        Quantity=int(data["Quantity"])
        if(Quantity<0):
            raise Exception()
    except:
        return {"error":"Inputs not valid"}
    try:  
        if data.itemId not in itemIds:
            return {"error":"Not a valid Item"}
        
        cart=mongo.db.carts.find_one({"_id":ObjectId(data.cartId)})
        
        if not cart:
            return {"error":"Enter valid CartId"}
        
        if cart["Creator"]!=current_user:
            return {"error":"User Not Authorised to view Cart"}
        
        items=cart["items"]
        itemId=data["itemId"]
        
        if itemId in items.keys():
            present_quantity=items[itemId]
            items[itemId]=present_quantity+Quantity
        else:
            items[itemId]=Quantity
            
        filter = {"_id":ObjectId(data.cartId)}
        newVal = {"$set":{"items":items}}
        mongo.db.carts.update_one(filter,newVal)
        cart["items"]=newVal["$set"]["items"]
        return cart
    except:
        return {"error":"Database error try again after sometime"}        

@app.route("/removeFromCart", methods=["POST"])
@jwt_required()
def removeFromCart():
    current_user = get_jwt_identity()
    data=cartParser.parse_args()
    jsonify(data)
    Quantity=0
    try:
        Quantity=int(data["Quantity"])
        if(Quantity<0):
            raise Exception()
    except:
        return {"error":"Inputs not valid"}
    try:  
        if data.itemId not in itemIds:
            return {"error":"Not a valid Item"}
        
        cart=mongo.db.carts.find_one({"_id":ObjectId(data.cartId)})
        
        if not cart:
            return {"error":"Enter valid CartId"}
        
        if cart["Creator"]!=current_user:
            return {"error":"User Not Authorised to view Cart"}
        
        items=cart["items"]
        itemId=data["itemId"]
        
        if itemId in items.keys():
            present_quantity=items[itemId]
            new_quantity=present_quantity-Quantity
            if new_quantity<=0:
                del items[itemId]
            else:
                items[itemId]=new_quantity
                
        filter = {"_id":ObjectId(data.cartId)}
        newVal = {"$set":{"items":items}}
        mongo.db.carts.update_one(filter,newVal)
        cart["items"]=newVal["$set"]["items"]
        return cart
    except:
        return {"error":"Database error try again after sometime"}

@app.route("/getCart", methods=["POST"])
@jwt_required()
def getCart():
    current_user = get_jwt_identity()
    data=cartParser2.parse_args()
    jsonify(data)
    try:  
        
        cart=mongo.db.carts.find_one({"_id":ObjectId(data.cartId)})
        
        if not cart:
            return {"error":"Enter valid CartId"}
        
        if cart["Creator"]!=current_user:
            return {"error":"User Not Authorised to view Cart"}
        
        return cart
    except:
        return {"error":"Database error try again after sometime"}
    
@app.route("/getAllCarts", methods=["GET"])
@jwt_required()
def getAllCarts():
    current_user = get_jwt_identity()
    
    try:  
        
        cart=mongo.db.carts.find({"Creator":current_user})
        
        if not cart:
            return {"error":"Enter valid CartId"}

        agg=list(cart)
        return {"Carts":agg}
    except:
        return {"error":"Database error try again after sometime"}
    
@app.route("/deleteCart", methods=["POST"])
@jwt_required()
def deleteCart():
    current_user = get_jwt_identity()
    data=cartParser2.parse_args()
    jsonify(data)
    try:  
        
        cart=mongo.db.carts.find_one({"_id":ObjectId(data.cartId)})
        
        if not cart:
            return {"error":"Enter valid CartId"}
        
        if cart["Creator"]!=current_user:
            return {"error":"User Not Authorised to view Cart"}
        
        mongo.db.carts.remove({"_id":ObjectId(data.cartId)})
        return {"Message":"Successfully Deleted Cart"}
    except:
        return {"error":"Database error try again after sometime"}
    
app.run(debug=True, use_reloader=False)
