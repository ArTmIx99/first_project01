from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class User(BaseModel):
    id:int
    username:str
    email:str


class UserCreate(BaseModel):
    username:str
    email:str


users: list[User] = [
    User(id=1, username="alice", email="alice@example.com"),
    User(id=2, username="bob", email="bob@example.com"),
    User(id=3, username="charlie", email="charlie@example.com"),
]

@app.get("/users", response_model=list[User])
def get_user():
    return users

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    for user in users:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

@app.post("/user_create",response_model=User, status_code=201)
def user_create(data:UserCreate):
    new_id = max(u.id for u in users) + 1 if users else 1
    new_user = User(id=new_id, username=data.username, email=data.email)
    users.append(new_user)
    return new_user

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)