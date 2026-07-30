from fastapi import APIRouter


from .schemas import DesignAssistRequest


from .service import (

    calculate_design_assist,

    get_design_summary

)



router = APIRouter()



@router.post("/")
def create_design_assist(
        data: DesignAssistRequest
):

    result = calculate_design_assist(data)


    return {

        "message":
        "Design analysis completed",

        "summary":
        result

    }




@router.get("/summary")
def design_summary():

    return get_design_summary()