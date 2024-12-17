from bson import ObjectId
from fastapi import APIRouter, HTTPException, status

from app.database.models import MealAdminCollection, UserCollection, UserAdmin, UpdateUserPrivilage, MealAdmin, UpdateMealStatus
from app.dependencies import CurrentSuperUser
from app.database.config import user_collection, meal_collection
router = APIRouter(tags=["Admin"], prefix="/admin")


@router.get("/users", response_model=UserCollection)
async def users_list(user : CurrentSuperUser):
    return UserCollection(users=await user_collection.find().to_list(1000))

@router.get("/users/{id}", response_model=UserAdmin)
async def get_user(user : CurrentSuperUser, id : str) :

    # Validasi ObjectId
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Invalid user ID"
        )

    user_obj = await user_collection.find_one({"_id" : ObjectId(id)})
    if not user_obj :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {id} not found"
        )
    return user_obj


@router.patch("/users/{id}", response_model=UserAdmin)
async def update_user_privileges(
    id: str, 
    updates: UpdateUserPrivilage, 
    user: CurrentSuperUser  # Pastikan hanya admin yang bisa mengakses
):
    """
    Update user privileges such as 'superuser' or 'active' status.
    """
    # Validasi ObjectId
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Invalid user ID"
        )

    # Cari user berdasarkan ID
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )

    # Filter atribut yang akan diupdate
    update_data = updates.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="No updates provided"
        )

    # Update user di database
    update_result = await user_collection.update_one(
        {"_id": ObjectId(id)}, 
        {"$set": update_data}
    )

    if update_result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Failed to update user"
        )

    # Kembalikan data user yang diperbarui
    updated_user = await user_collection.find_one({"_id": ObjectId(id)})
    return updated_user




@router.get(
    "/meals",
    response_description="List pending meals",
    response_model=MealAdminCollection,
    response_model_by_alias=False,
)
async def list_meals(user : CurrentSuperUser):
    meals = await meal_collection.find({ "verification_status" : "pending"}).to_list()
    return MealAdminCollection(meals=meals)




@router.patch("/meals{id}",response_description="Updated Meal",response_model=MealAdmin)
async def update_meal_status(id: str, updates: UpdateMealStatus, user: CurrentSuperUser ):
    # Validasi ObjectId
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Invalid user ID"
        )

    # Cari meal berdasarkan ID
    meal = await meal_collection.find_one({"_id": ObjectId(id)})
    if not meal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )

    # Filter atribut yang akan diupdate
    update_data = updates.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="No updates provided"
        )

    # Update user di database
    update_result = await meal_collection.update_one(
        {"_id": ObjectId(id)}, 
        {"$set": update_data}
    )

    if update_result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Failed to update user"
        )

    # Kembalikan data user yang diperbarui
    updated_meal = await meal_collection.find_one({"_id": ObjectId(id)})
    return updated_meal