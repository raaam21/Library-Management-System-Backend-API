from fastapi import FastAPI
import CRUD_Ops

app = FastAPI()

@app.head('/')
@app.get('/')
def root():
    return ('Cosmo Cloud Assignment !')

app.include_router(CRUD_Ops.router)