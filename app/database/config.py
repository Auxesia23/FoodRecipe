import os
import motor.motor_asyncio
from dotenv import load_dotenv

load_dotenv()


client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGODB_URL"))
db = client.meal
meal_collection = db.get_collection("meals")
user_collection = db.get_collection("users")
favourites_collection = db.get_collection("favourites")
# meal_collection.create_index(
#     [("name", "text"), ("area", "text"), ("ingredients.name", "text")],
#     default_language="none",
# )

