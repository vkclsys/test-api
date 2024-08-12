from fastapi import FastAPI,Response, status ,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["https://www.google.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Post(BaseModel):
    title : str
    content : str
    published: bool =True
    rating : Optional[int] =None


my_post = [
            { 
                "title":"title of post 1",
                "content":"content of post 1 ",
                "id":1
            },

            {
                "title":"title of post 2",
                "content":"content of post 2 ",
                "id":2
            }
        ]

def find_post(id):
    for p in my_post:
        if p["id"] == id :
            return p
        

def find_index_post(id):
    for i,p in enumerate(my_post):
        if p['id'] == id :
            return i


@app.get("/")
def root():
    return {"message": "Hello World test"}


@app.get("/posts")
def get_posts():
    return {"data": my_post}


@app.post("/posts_0")
def create_posts(body: dict = Body (...) ):
    print(body)
    return {"new_post ": f"Title - {body['title']}with Content - {body['content']}"}


@app.post("/posts_1",status_code=status.HTTP_201_CREATED)
def create_posts(post : Post):
    print(post)
    # print(post.published)
    # print(post.rating)
    # print(post.dict())

    post_dict = post.dict()
    post_dict["id"] = randrange(0,1000000)


    my_post.append(post_dict)

    return {"data ": post_dict}


@app.get("/posts/latest")
def get_latest_post():
    post = my_post[len(my_post)-1]
    return{"post_latest_detail":post}


@app.get("/posts/{id}")
def get_post(id:int , response:Response):
    post = find_post(id)

    if not post:

        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message" : f"{id} NOT Found"}

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"{id} NOT Found")

    return{"post_detail":post}

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int ):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND ,  detail= f"post with id:{id} does not exist")

    my_post.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id:int , post:Post):

    # print(post)
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND ,  detail= f"post with id:{id} does not exist")
    
    post_dict = post.dict()

    post_dict['id'] = id

    my_post[index]= post_dict

    # return {"message": "updated post"}
    return Response(status_code=status.HTTP_205_RESET_CONTENT)