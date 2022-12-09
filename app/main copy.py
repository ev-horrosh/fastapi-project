from fastapi import FastAPI, Depends
import uvicorn

from typing import Optional
from starlette.templating import Jinja2Templates
from starlette.requests import Request

from schemas import User

api = FastAPI()
templates = Jinja2Templates("templates")


@api.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# @api.get("/user/")
# def user_info(user: User = Depends()):

#     return f"{user.first_name}"


data = {"first_name": "John", "last_name": "Doe", "age": 32, "sex": "m"}
# user = User({"first_name": "John", "last_name": "Doe", "age": 32, "sex": "m"})
# print(user)

if __name__ == "__main__":
    uvicorn.run(api)
