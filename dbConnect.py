from motor.motor_asyncio import AsyncIOMotorClient

uri = 'mongodb+srv://yoursram18:XH438QjA9mz6RiNU@cluster0.vwqhnrk.mongodb.net/'

client = AsyncIOMotorClient(uri)

database = client.CosmoCloud_Assignment

def get_db():   
    return database