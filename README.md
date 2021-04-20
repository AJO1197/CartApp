# CartApp
Here I have created a simple CartAPI with user authentication and basic crud operations.

Main_URL:

itemIds=("Apple","Banana","Orange","Mango")

**REGISTRATION::POST Method::Main_URL/register**

  Input Body:
  
  { "username":"sample_username",
  
   "password":"sample_password"}
  
  The correct response will be in the form of::
  
  {"message":"Success",
  
   "token":"Random_JSON_Web_Token"}
   
   This token will be required for all the CRUD operations. So every method will require this JWT to be given as a BearerToken.
   
   This token expires in 15 mins so login may be required again if 15 mins pass.
   
**Login::POST Method::Main_URL/login**

  Input Body:
  
  {"username":"sample_username",
  
   "password":"sample_password"}
  
  The correct response will be in the form of::
  
  {"message":"Success",
  
   "token":"Random_JSON_Web_Token"}
   
  If password or username is wrong it will show error.
  
**CreateCart::GET Method::Main_URL/createCart**

  The Token helps in authentication of the user. No need of any other parameters as input.
  
  The correct response will be in the form of:
  
  {"_id":"MongoDB ObjectId",
  
   "Creator":"ObjectId of Creator",
   
   "items":"Dictionary of items with their quantity"}
   
   User needs to save this MogoDB object ID of the cart to be able to perform updation and deletion of items later in the cart.
   
**AddToCart::POST Method::Main_URL/addToCart**

  Input Body:
  
  {"cartId":"Cart Object ID from prev"
  
  "itemId":"Currently for test only 4 items are Available",
  
   "Quantity":"integer"}
   
   The correct response will be same as CreateCart with updated items.
   
**RemoveFromCart::POST Method::Main_URL/removeFromCart**

  Input Body:
  
  {"cartId":"Cart Object ID from prev"
  
  "itemId":"Currently for test only 4 items are Available",
  
   "Quantity":"integer"}
   
   The correct response will be same as CreateCart with updated items.

   
**GetCart::POST Method::Main_URL/getCart**
  
  Input Body:
  
  {"cartId":"Cart Object ID from prev"}
  
  The correct response will be same as CreateCart with the specific cart being asked for being returned.
  
**GetAllCarts::GET Method::Main_URL/getAllCarts**
  
  The correct response will be a JSON object with "Carts" as key and a list of carts as value.
  
**DeleteCart::POST Method::Main_URL/deleteCart**
  
  Input Body:
  
  {"cartId":"Cart Object ID from prev"}
  
  The correct response will be a success message.
 
   
   
