# CartApp
Here I have created a simple CartAPI with user authentication and basic crud operations.

Main_URL:

**REGISTRATION::POST Method::Main_URL/register

  Input Body:
  
  { "username":"sample_username",
  
  "password":"sample_password"}
  
  The correct response will be in the form of::
  
  {"message":"Success",
  
   "token":"Random_JSON_Web_Token"}
   
   This token will be required for all the CRUD operations. So every method will require this JWT to be given as a BearerToken.
   
   This token expires in 15 mins so login may be required again if 15 mins pass.
   
**Login::POST Method::Main_URL/login

  Input Body:
  
  {"username":"sample_username",
  
  "password":"sample_password"}
  
  The correct response will be in the form of::
  
  {"message":"Success",
  
   "token":"Random_JSON_Web_Token"}
   
  If password or username is wrong it will show error.
  
**CreateCart::GET Method::Main_URL/createCart
   
  
 
 
 
   
   
