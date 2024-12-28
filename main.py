from http.client import HTTPException
from fastapi import FastAPI,Depends,status
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID, uuid4
import jwt
from datetime import datetime, timedelta

app = FastAPI()

class Task(BaseModel):
    id: Optional[UUID] = None
    title: str
    description: Optional[str] = None
    completed: bool = False

tasks = []

SECRET_KEY=  "XXX"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_token(data:dict, expires_delta:timedelta= None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow()+expires_delta
    else:
        expire = datetime.utcnow()+timedelta(minutes=15)
    to_encode.update({"exp":expire})
    encdoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encdoded_jwt

def verify_token(token:str = Depends(oauth2_scheme)):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username:str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401,detail="Invalid token")
        return username
    except jwt.PyJWTError:
        raise HTTPException(status_code=401,detail="invalid token")


@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Replace with your user authentication logic
    if form_data.username == "test" and form_data.password == "test":
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_token(
            data={"sub": form_data.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(status_code=400, detail="Incorrect username or password")

@app.post("/tasks/", response_model=Task) 
def create_task(task:Task,username:str = Depends(verify_token)):
    task.id = uuid4()
    tasks.append(task)
    return task

@app.get("/tasks/", response_model=List[Task])
def read_tasks(username:str=Depends(verify_token)):
    return tasks

# def read_tasks():
#     return tasks

# read_tasks = app.get("/tasks/", response_model = List[Task])(read_tasks)

@app.get("/tasks/{task_id}", response_model = Task)
def read_tasks(task_id: UUID,username:str=Depends(verify_token)):
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code = 404, detail="Task not found")

@app.put("/task/{task_id}", response_model = Task)
def update_task(task_id:UUID, task_update:Task, username:str=Depends(verify_token)):
    for idx, task in enumerate(tasks):
        if task.id == task_id:
            updated_task = task.copy(update=task_update.dict(exclude_unset=True))
            tasks[idx] = updated_task
            return updated_task
    raise HTTPException(statu_code=404, detail="not found")


@app.delete("/task/{task_id}", response_model=Task)
def delete_task(task_id: UUID, username:str=Depends(verify_token)):
    for idx, task in enumerate(tasks):
        if task.id == task_id:
            return tasks.pop(idx)

    raise HTTPException(status_code=404, detail="Task not found")


def read_tasks():
    return tasks

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)

      