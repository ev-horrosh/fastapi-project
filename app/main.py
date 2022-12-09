from fastapi import FastAPI, Response, HTTPException, status

# from fastapi.params import
from schemas import Post
from random import randrange

import uvicorn

api = FastAPI()

my_posts = [
    dict(title="title of post 1", content="c1", id=1),
    dict(title="title of post 2", content="c2", id=2),
]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i


@api.get("/")
def index():
    return {"message": "Hell"}


@api.get("/posts")
def get_posts():
    return dict(posts=my_posts)


@api.get("/posts/{id}")
def get_posts_id(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} post not found"
        )
    return dict(posts_details=post)


@api.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_data = post.dict()
    post_data["id"] = randrange(0, 1000000)
    my_posts.append(post_data)
    return dict(posts=post_data)


@api.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"no post with id {id}"
        )
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@api.put('/posts/{id}')
def update_post(id:int,post: Post):
    index=find_index_post(id)
    if index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"no post with id {id}"
        )
    post_dict=post.dict()
    post_dict['id']=id
    my_posts[index]=post_dict
    return {'data':post_dict}
    
    
    


if __name__ == "__main__":
    uvicorn.run("main:api", reload=True)
