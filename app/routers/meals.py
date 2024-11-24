from bson import ObjectId
from fastapi import APIRouter,HTTPException, Response, status, File, UploadFile
from fastapi.responses import FileResponse
from pymongo import ReturnDocument

from pathlib import Path
import shutil

from ..database.models import MealModel, MealCollection, UpdateMealModel
from ..database.config import meal_collection

router = APIRouter(tags=["Meals"])

UPLOAD_DIR = Path("static/images")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post(
    "/meals/",
    response_description="Add new meal",
    response_model=MealModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_meal(meal: MealModel):
    """
    Insert a new m record.

    A unique `id` will be created and provided in the response.
    """

    new_meal = await meal_collection.insert_one(
        meal.model_dump(by_alias=True, exclude=["id"])
    )
    created_meal = await meal_collection.find_one(
        {"_id": new_meal.inserted_id}
    )
    return created_meal



@router.get(
    "/meals/",
    response_description="List all meals",
    response_model=MealCollection,
    response_model_by_alias=False,
)
async def list_meals():
    return MealCollection(meals=await meal_collection.find().to_list(1000))


@router.get(
    "/meals/{id}",
    response_description="Get a single student",
    response_model=MealModel,
    response_model_by_alias=False,
)
async def show_meals(id: str):
    """
    Get the record for a specific student, looked up by `id`.
    """
    if (
        meal := await meal_collection.find_one({"_id": ObjectId(id)})
    ) is not None:
        return meal

    raise HTTPException(status_code=404, detail=f"Meal {id} not found")


@router.put(
    "/meals/{id}",
    response_description="Update a student",
    response_model=MealModel,
    response_model_by_alias=False,
)
async def update_meal(id: str, meal: UpdateMealModel):
    """
    Update individual fields of an existing student record.

    Only the provided fields will be updated.
    Any missing or `null` fields will be ignored.
    """
    meal = {
        k: v for k, v in meal.model_dump(by_alias=True).items() if v is not None
    }

    if len(meal) >= 1:
        update_result = await meal_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": meal},
            return_document=ReturnDocument.AFTER,
        )
        if update_result is not None:
            return update_result
        else:
            raise HTTPException(status_code=404, detail=f"Meal {id} not found")

    # The update is empty, but we should still return the matching document:
    if (existing_meal := await meal_collection.find_one({"_id": id})) is not None:
        return existing_meal

    raise HTTPException(status_code=404, detail=f"Student {id} not found")


@router.delete("/meals/{id}", response_description="Delete a meal")
async def delete_meal(id: str):
    """
    Remove a single meal record from the database.
    """
    delete_result = await meal_collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Student {id} not found")



@router.put(
    "/meals/{id}/update-image",
    response_description="Update image URL of the meal",
)
async def update_image_url(id: str, file: UploadFile = File(...)):
    """
    Update the image URL for a specific meal.

    This will update the `imageUrl` field for the meal identified by `meal_id`.
    """

    # Cek apakah file yang diupload adalah gambar
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")

    file_path = UPLOAD_DIR / file.filename

    # Simpan file ke direktori
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Generate URL untuk gambar yang baru
    new_image_url = f"http://127.0.0.1:8000/static/images/{file.filename}"

    # Update meal di MongoDB
    update_result = await meal_collection.update_one(
        {"_id": ObjectId(id)},  # mencari meal berdasarkan ID
        {"$set": {"imageUrl": new_image_url}}  # update field `imageUrl`
    )

    if update_result.modified_count == 0:
        raise HTTPException(
            status_code=404, detail=f"Meal with ID {id} not found or imageUrl already up-to-date"
        )

    # Kembalikan URL baru atau data meal yang sudah diupdate
    

    return {"message": "Image URL updated successfully"}