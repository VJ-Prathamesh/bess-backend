from fastapi import APIRouter

from .schemas import LoadProfileRequest

from .service import (
    calculate_load_profile,
    get_load_summary
)


router = APIRouter()



@router.post("/")
def create_load_profile(
    data: LoadProfileRequest
):

    result = calculate_load_profile(data)


    return {

        "message":
        "Load profile calculated successfully",

        "summary":
        result

    }




@router.get("/summary")
def load_summary():

    return get_load_summary()