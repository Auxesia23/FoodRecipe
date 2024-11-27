from typing_extensions import Annotated
from typing import Optional
from pydantic import ConfigDict, BaseModel, Field, EmailStr
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




class UserModel(BaseModel) :
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    email : str = Field(...)
    password : str = Field(...)
    verified : bool = Field(default=False)
    created_at : Optional[str] = None
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example" : {
                "email" : "YourEmail@email.com",
                "password" : "YourSecretPassword"
            }
           
        }
    )
       

class UserResponseModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    email: EmailStr
    created_at: Optional[str] = None



