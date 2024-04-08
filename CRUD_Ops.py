from fastapi import APIRouter,HTTPException
from starlette.responses import JSONResponse
from models import Student
import dbConnect
from bson.objectid import ObjectId
from typing import Optional

router = APIRouter()


@router.post('/students')
async def addStudents(req:Student):
    try:
        db = dbConnect.database
        student_Collection = db.Students
        student = {}
        user_req=req.dict()
        
        student['name']=user_req['name']
        student['age']=user_req['age']
        
        Address={}
        Address['city']=user_req['address']['city']
        Address['country']=user_req['address']['country']
        student['address'] = Address
        
        result = await student_Collection.insert_one(student)
        
        content = str(result.inserted_id)
        status_code = 201  
        return JSONResponse(content=content, status_code=status_code)

    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))



@router.get('/students')
async def getStudents(country:str=None,age:int=None):
    try:
        db = dbConnect.database
        student_Collection = db.Students
        
        
        query = {}
        if country :
            query["address.country"] = country
        
        if age is not None:
            query["age"] = {"$gte":age}
            
        result = student_Collection.find(query)
        
        studentList = []
        
        async for doc in result:
            temp_variable = {}
            temp_variable['name']=doc['name']
            temp_variable['age']=doc['age']
            studentList.append(temp_variable)
        

        status_code = 200
        return JSONResponse(content=studentList,status_code=status_code)
    
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))


@router.get('/students/{id}')
async def getStudentsByID(id:str):
    try:
        db = dbConnect.get_db()
        coll = db["Students"]
        
        oid = ObjectId(id)
        
        projection = {"_id": 0}
        result = await coll.find_one({"_id":oid},projection)
        
        status_code = 200
        return JSONResponse(content=result,status_code=status_code)
    
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))


@router.patch('/students/{id}')
async def getStudents(id:str,update_req:dict):
    try:
        db = dbConnect.get_db()
        coll = db["Students"]
        
        
        oid = ObjectId(id)
        
        projection = {"_id": 0}
        oldRecord = await coll.find_one({"_id":oid},projection)
        
        updatedStudent = oldRecord
        
        if 'name' in update_req:
            updatedStudent["name"]=update_req["name"]
            
        if 'age' in update_req:
            updatedStudent["age"]=update_req["age"]
        
        if 'address' in update_req:
            if 'city' in update_req["address"]:
                updatedStudent["address"]["city"]=update_req["address"]["city"]
                
            if 'country' in update_req["address"]:
                updatedStudent["address"]["country"]=update_req["address"]["country"]
        
        
        result = await coll.update_one({"_id":oid},{"$set":updatedStudent})
        
        content = {"message": "Record Updated"}
        status_code = 204
        return JSONResponse(content=content, status_code=status_code)

    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))


@router.delete('/students/{id}')
async def deleteStudent(id:str):
    try:
        db = dbConnect.get_db()
        coll = db["Students"]
        oid = ObjectId(id)

        result = await coll.delete_one({"_id":oid})
        if result.deleted_count == 0:
            return("NOt found!")

        content = {"message": "Document deleted successfully"}
        status_code = 200
        return JSONResponse(content=content, status_code=status_code)
    
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))