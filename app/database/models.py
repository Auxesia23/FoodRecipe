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
    name : str = Field(...)
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
                "name" : "Ayam Goreng",
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

class MealAdmin(MealModel) :
    author : EmailStr
    verification_status: str = Field("pending", enum=["pending", "approved", "rejected"])
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "name" : "Ayam Goreng",
                "category": "chicken",
                "area": "Indonesia",
                "instructions": "Lorem ipsum dolor sit, amet consectetur adipisicing elit. Libero velit quis hic. Amet corporis atque, totam officia ullam animi facere temporibus tempore architecto fuga, ipsam quisquam dignissimos magnam sunt saepe!",
                "youtubeUrl": "https://youtube.com/videoexample",
                "ingredients" : [
                    {
                        "name": "Paha ayam",
                        "measure": "500 gram",
                    }
                ],
                "author" : "user@email.com",
                "verification_status" : "approved"
            }
        },
    )

class MealAdminCollection(BaseModel):
    meals : list[MealAdmin]


class UpdateMealModel(BaseModel):
    """
    A set of optional updates to be made to a document in the database.
    """

    name : Optional[str] = None
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
                "name" : "Ayam goreng",
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

class UpdateMealStatus(BaseModel):
    verification_status: str = Field("pending", enum=["pending", "approved", "rejected"])


class MealCollection(BaseModel):
    meals: list[MealModel]




class UserModel(BaseModel) :
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    email : str = Field(...)
    password : Optional[str] = Field(...)
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example" : {
                "email" : "YourEmail@email.com",
                "password" : "YourSecretPassword",
            }
           
        }
    )

class UserAdmin(UserModel):
    superuser : bool 
    verified : bool 
    active : bool 
    created_at : str

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example" : {
                "email" : "YourEmail@email.com",
                "password" : "YourSecretPassword",
                "superuser" : False,
                "active" : False,
                "created_at" : "2024-12-01T08:36:18.248618"
            }
           
        }
    )

       

class UserResponseModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    email: EmailStr

class UserCollection(BaseModel) :
    users : list[UserAdmin]

class UpdateUserPrivilage(BaseModel):
    superuser : Optional[bool] = None
    active : Optional[bool] = None
    model_config = ConfigDict(
        json_schema_extra={
            "example" : {
                "superuser" : True,
                "active" : True
            }
        }
    )



