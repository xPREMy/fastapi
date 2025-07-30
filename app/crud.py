from fastapi import FastAPI , Response, status ,HTTPException
from fastapi.params import Body 
from pydantic import BaseModel
from typing import Optional
import random
app = FastAPI()
my_posts=[{"title":"khanak","discription":"idiot","id":1},{"title":"pankaj","dicription":"retila","id":2}]
def find_post(id):
    for p in my_posts:
        if p['id']== id:
            return p
        
def find_index(id):
    for i,p in enumerate(my_posts):
        if p['id']== id:
            return i
class posts(BaseModel):
    title : str
    discription: str 

@app.get("/")
def get_posts():
    return {"message": my_posts}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def posting(post : posts):
    post_dict= post.dict()
    post_dict['id']=random.randrange(4,8)
    my_posts.append(post_dict)
    
    return {"goodness": post}

@app.get("/posts/{id}")
def get_post(id : int,response:Response):
    post=find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"id:{id} not is  found")
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {"detail":f"{id} not found"}
    return post

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    i=find_index(id)
    if i == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"id:{id} not is  found")
    del my_posts[i]
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.post("/posts/{id}")
def update_post(id:int,post : posts):
    index = find_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"id:{id} not is  found")
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index]=post_dict
    return {"message": "success"}