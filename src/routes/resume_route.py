from fastapi import APIRouter, UploadFile, File, HTTPException

from services.resume_workflow import convert_pdf, image_to_json
router = APIRouter(prefix='/extra')

@router.post("/resume-upload")
async def get_resume(file: UploadFile = File(...)):
    if not file.filename.lower().endswith('pdf'):
        raise HTTPException(status_code=400,detail="Invalid file, only supports PDF")

    try:
        images = convert_pdf(file)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to convert PDF to IMG")

    try:
        json_list = image_to_json(images)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Failed to convert IMG to JSON")

    #fetch jobs & perform matching
    job_list = []

    return job_list

