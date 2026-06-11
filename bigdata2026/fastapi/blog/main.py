from blog.schema.response import PostResponse, MessageResponse
from typing import List
from blog.schema.request import PostCreate, PostUpdate
from fastapi import FastAPI, status, HTTPException

app = FastAPI(title='Blog REST API')

db_posts = []
next_id = 1
# 전체 데이터 조회
@app.get(
    '/posts',
    response_model=list[PostResponse],
    status_code=status.HTTP_200_OK       
)
def get_all_posts():
    return db_posts
# 단일 게시물 조회
@app.get(
    '/posts/{post_id}',
    response_model=PostResponse,
)
def get_post(post_id: int):
    for post in db_posts:
        if post['id'] == post_id:
            return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='게시글을 찾을 수 없습니다')
# 게시글 생성
@app.post(
    '/posts',
    response_model=PostResponse,
    status_code=status.HTTP_201_CREATED
)
def create_post(payload: PostCreate):
    global next_id
    new_post = {
        'id': next_id,
        'title':payload.title,
        'content':payload.content,
    }
    db_posts.append(new_post)
    next_id += 1
    return new_post
# 게시글 수정
@app.patch(
    '/posts/{post_id}',
    response_model=PostResponse,
    status_code=status.HTTP_200_OK
)
def update_post(post_id:int, payload:PostUpdate):
    for post in db_posts:
        if post['id'] == post_id:
            post['title'] = payload.title
            post['content'] = payload.content
            return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='수정한 게시글은 존재하지 않습니다.')

# 게시글 삭제    
@app.delete(
    '/posts/{post_id}',
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_post(post_id: int):
    for post in db_posts:
        if post['id'] == post_id:
            db_posts.remove(post)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='삭제할 게시글은 존재하지 않습니다.')
