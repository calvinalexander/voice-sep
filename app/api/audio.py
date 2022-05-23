from fastapi import APIRouter, UploadFile, Response, status, File
from pydantic import BaseModel
from app.model.audio import InferInResponse
from app.service.convert_to_wav import convert_to_wav
from app.service.inference import inference
from speechbrain.pretrained import SepformerSeparation as separator


# belum ubah2 ini
router = APIRouter()
model_2speakers = separator.from_hparams(
    source="speechbrain/sepformer-wsj02mix", savedir='pretrained_models/sepformer-wsj02mix')
model_3speakers = separator.from_hparams(
    source="speechbrain/sepformer-wsj03mix", savedir='pretrained_models/sepformer-wsj03mix')


@router.post("/infer", response_model=InferInResponse, response_model_exclude_none=True)
async def endpoint_infer(response: Response,  num_speakers: int, file: UploadFile = None) -> InferInResponse:
    if num_speakers == 2:
        model = model_2speakers
    elif num_speakers == 3:
        model = model_3speakers
    # No files were uploaded
    if num_speakers < 2 and num_speakers > 3:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return InferInResponse.parse_obj({
            "status": 400,
            "message": "Currently model available for two or three speakers"
        })

    if file is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return InferInResponse.parse_obj({
            "status": 400,
            "message": "No files were uploaded"
        })

    # Invalid file extension
    elif file.content_type.split("/")[0] != "audio":
        response.status_code = status.HTTP_400_BAD_REQUEST
        return InferInResponse.parse_obj({
            "status": 400,
            "message": "Invalid file extension",
            "data": {
                "file": file.filename,
                "fileType": file.content_type
            }
        })

    # Convert to wav
    file_name = await convert_to_wav(file)

    try:
        return await inference(file_name, model, num_speakers)

    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return InferInResponse.parse_obj({
            "status": 400,
            "message": str(e),
            "data": {
                "file": file.filename,
                "fileType": file.content_type
            }
        })
