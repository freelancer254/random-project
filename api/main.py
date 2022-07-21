import random
from datetime import datetime, timedelta
from enum import Enum
from typing import List
from fastapi import FastAPI, Body, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from mypackage import crud, schemas, dependency, auth

#Draw Type Enums
class DrawType(str, Enum):
	random_int = "Random Integer(s)"
	random_float = "Random Float"
	random_item = "1 Random Item From A List"
	random_items = "Random Items From A List"


app = FastAPI(title="A Random Project")

origins = [
	"*"
]

app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

#about the project
@app.get("/about", tags=["About"])
async def about():
	return {"data":{
		"about":"A random project is an open source project for verifiable randomness. All requested random values can be verified by the public. Use cases include lottery, giveaways, random games, etc. The source code is available on github: https://github.com/freelancer254 You can support the project too: https://www.buymeacoffee.com/freelancer254"
	}}

#redirect to the docs
@app.get("/", tags=["Docs"])
async def redirect_docs():
	return RedirectResponse("https://wby808.deta.dev/docs")

#login and get access token
@app.post("/token", response_model=schemas.Token, tags=["Login"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db = Depends(dependency.get_db)):
    user = auth.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user[0]["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
	

#create new user 
#User provides username, email and password
@app.post("/users/", tags=["Users"])
async def create_user(user: schemas.UserCreate, db = Depends(dependency.get_db)):
    #check if user exists
    if crud.get_user_by_username(db, username=user.username) or crud.get_user_by_email(db, email=user.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    return await crud.create_user(db=db, user=user)
   
'''Required if need to verify user email
#activate user
@app.get("/users/activate/{token}", tags=["Users"])
def activate_user(token: str, db = Depends(dependency.get_db)):
	user = auth.verify_activation_token(token, db)
	return {"data": f'Hello {user.get("username")}, your account has been activated'}
'''

#get user
@app.get("/users/{username}", tags=["Users"])
def get_user(username: str, db = Depends(dependency.get_db)):
    db_user = crud.get_user_by_username(db, username=username)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    user_draws = crud.get_user_draws(db, db_user[0]["username"] )
    return {"data":{"username":db_user[0].get("username"), "draws":user_draws}}

#get draws
@app.get("/draws/", tags=["Latest Draws"])
def get_latest_draws( db = Depends(dependency.get_db)):
    latest_draws = crud.get_latest_draws(db) 
    return latest_draws

#get draw using draw key/ID
@app.get("/draw/{draw_key}", tags=["Draws"])
def get_draw( key: str, db = Depends(dependency.get_db)):
    draw = crud.get_draw(db, key)
    if not draw:
        raise HTTPException(status_code=404, detail="Draw not found") 
    return draw

#Returns a random int between 0 and *sys.maxsize* - using first 16 base Deta base has a cap 
@app.get('/randomInt/',  tags = ["Random Integer"])
def get_random_int(numInt: int = 1, lower: int = 0, higher: int = 9223372036854, db = Depends(dependency.get_db),
	token: str = Depends(dependency.oauth2_scheme), user: schemas.User = Depends(dependency.get_current_user)):
	#check if lower > higher, then interchange
	if lower > higher:
		(lower, higher) = higher, lower

	#draw object 
	draw: dict = {
	"timestamp" : datetime.now().strftime("%d/%m/%Y/, %H:%M:%S GMT"),
	"description" : DrawType.random_int.value,
	"items" : [f"{numInt} Random Integer(s) between {lower} and {higher}"],
	"selected" : [random.randint(lower, higher) for i in range(numInt)],
	"username" : user[0].get("username")
	}
	created_draw = crud.create_user_draw(db, draw)
	return created_draw

#Returns a random float between 0 and 1
@app.get('/randomFloat/', tags = ["Random Float"])
def get_random_float(db = Depends(dependency.get_db), 
	token: str = Depends(dependency.oauth2_scheme), user: schemas.User = Depends(dependency.get_current_user)):

	#draw object 
	draw: dict = {
	"timestamp" : datetime.now().strftime("%d/%m/%Y/, %H:%M:%S GMT"),
	"description" : DrawType.random_float.value,
	"items" : ["Random Float Between 0 and 1"],
	"selected" : [random.random()],
	"username" : user[0]["username"]
	}
	created_draw = crud.create_user_draw(db, draw)
	return created_draw
	


#Returns a random item from a list of items
#List is passed as a request body
@app.put('/random/item/',  tags = ["Random Item From List"])
def get_random_item_from_list(items: List = Body(), db = Depends(dependency.get_db),
	token: str = Depends(dependency.oauth2_scheme), user = Depends(dependency.get_current_user)):
	#check if list is empty
	if not items:
		raise HTTPException(status_code=404, detail="List is empty")

	#draw object 
	draw: dict = {
	"timestamp" : datetime.now().strftime("%d/%m/%Y/, %H:%M:%S GMT"),
	"description" : DrawType.random_item.value,
	"items" : items,
	"selected" : [random.choice(items)],
	"username" : user[0]["username"]
	}
	created_draw = crud.create_user_draw(db, draw)
	return created_draw
	

#Returns a random set of items from a list of items
#List is passed as a request body
#Each item can only be selected once if list has no duplicates
@app.put('/random/items/{numItems}/', tags = ["Random Items From List"])
def get_random_items_from_list(numItems: int, items: List = Body(), db = Depends(dependency.get_db),
	token: str = Depends(dependency.oauth2_scheme), user: schemas.User = Depends(dependency.get_current_user)):
	#check if list is empty 
	if not items:
		raise HTTPException(status_code=404, detail="List is empty")
	#check if numItems > size of list
	if len(items) <= numItems:
		raise HTTPException(status_code=404, detail= f"List Not Big Enough For {numItems} random items")
		
	#draw object 
	draw: dict = {
	"timestamp" : datetime.now().strftime("%d/%m/%Y/, %H:%M:%S GMT"),
	"description" : DrawType.random_items.value,
	"items" : items,
	"selected" : random.sample(items, numItems),
	"username" : user[0]["username"]
	}
	created_draw = crud.create_user_draw(db, draw)
	return created_draw

