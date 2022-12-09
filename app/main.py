from fastapi import FastAPI, Response, HTTPException, status, Depends
from schemas import Post
import uvicorn
from db import DB
from sqlalchemy.orm import Session
import models
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)
api = FastAPI()
db = DB()


@api.get("/")
def index():
    return {"message": "Hell"}

@api.get('/sqlalchemy')
def test_post(db: Session=Depends(get_db)):
    posts=db.query(models.Post).all()
    return dict(data=posts)



@api.get("/posts")
def get_posts(db: Session=Depends(get_db)):
    # conn = db.conn()
    # cur = conn.cursor()
    # cur.execute("""select * from posts;""")
    # posts = cur.fetchall()
    db: Session=Depends(get_db)
    posts=db.query(models.Post).all()
    return dict(posts=posts)


@api.get("/posts/{id}")
def get_posts_id(id: int):
    conn = db.conn()
    cur = conn.cursor()
    cur.execute("""select * from posts where id=%s;""", (str(id),))
    post = cur.fetchone()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} post not found"
        )
    return dict(post_details=post)


@api.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    conn = db.conn()
    cur = conn.cursor()
    cur.execute(
        """insert into 
        posts (title,content,published) 
        values (%s,%s,%s) returning *;""",
        (post.title, post.content, post.published),
    )
    new_post = cur.fetchone()
    conn.commit()
    return {"data": new_post}


@api.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    conn = db.conn()
    cur = conn.cursor()
    cur.execute("""delete from posts where id=%s returning *;""", (str(id),))
    deleted_post = cur.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"no post with id {id}"
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@api.put("/posts/{id}")
def update_post(id: int, post: Post):
    conn = db.conn()
    cur = conn.cursor()
    cur.execute(
        """update posts set title=%s,content=%s,published=%s where id =%s returning *;""",
        (post.title, post.content, post.published, str(id)),
    )
    updated_post = cur.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"no post with id {id}"
        )
    return {"data": updated_post}


if __name__ == "__main__":
    # connect_to_db()
    uvicorn.run("main:api", reload=True)
