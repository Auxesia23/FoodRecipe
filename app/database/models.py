from typing_extensions import Annotated
from typing import Optional
from pydantic import ConfigDict, BaseModel, Field
from pydantic.functional_validators import BeforeValidator

PyObjectId = Annotated[str, BeforeValidator(str)]

class Ingredient(BaseModel) :
    name : str = Field(...)
    measure : str = Field(...)

class MealModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    category : str = Field(...)
    area : str = Field(...)
    instructions : str = Field(...)
    youtubeUrl : str = Field(...)
    imageUrl : Optional[str] = None
    ingredients : list[Ingredient]
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "category": "chicken",
                "area": "Indonesia",
                "instructions": "Lorem ipsum dolor sit, amet consectetur adipisicing elit. Libero velit quis hic. Amet corporis atque, totam officia ullam animi facere temporibus tempore architecto fuga, ipsam quisquam dignissimos magnam sunt saepe!",
                "youtubeUrl": "https://youtube.com/videoexample",
                "ingredients" : [
                    {
                        "name": "Paha ayam",
                        "measure": "500 gram",
                    }
                ]
            }
        },
    )



class UpdateMealModel(BaseModel):
    """
    A set of optional updates to be made to a document in the database.
    """

    category : Optional[str] = None
    area : Optional[str] = None
    instructions : Optional[str] = None
    youtubeUrl : Optional[str] = None
    imageUrl : Optional[str] = None
    ingredients : Optional[list] = None
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "category": "chicken",
                "area": "Indonesia",
                "instructions": "Lorem ipsum dolor sit, amet consectetur adipisicing elit. Libero velit quis hic. Amet corporis atque, totam officia ullam animi facere temporibus tempore architecto fuga, ipsam quisquam dignissimos magnam sunt saepe!",
                "youtubeUrl": "https://youtube.com/videoexample",
                "imageUrl" : "htps://auxesia.com/image/Ayam",
                "ingredients" : [
                    {
                        "name": "Paha ayam",
                        "measure": "500 gram",
                    }
                ]
            }
        },
    )



class MealCollection(BaseModel):
    meals: list[MealModel]




from passlib.hash import bcrypt
class UserModel(BaseModel) :
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    username : str = Field(...)
    password : str = Field(...)
    created_at : Optional[str] = None
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example" : {
                "username" : "YourUsername",
                "password" : "YourSecretPassword"
            }
           
        }
    )
       

    def verify_password(self, password: str) -> bool:
        """Verify if provided password matches the hashed password."""
        return bcrypt.verify(password, self.password)

    @classmethod
    def from_mongo(cls, user_data: dict):
        """Helper method to transform MongoDB document into UserModel instance."""
        return cls(**user_data)

class UserResponseModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    username: str
    created_at: Optional[str] = None



