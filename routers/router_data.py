import uuid

from fastapi import APIRouter, UploadFile, Body, File
from starlette.responses import JSONResponse, FileResponse

from data_env import main_url
from logs_info import logger
from utils.models import InputData, UsersDb, UserInfo, SoundInfo, InputSound, SoundsDb, GetUuidSound
from utils.others import convertor_wave_to_mp3, get_ids_from_path

router = APIRouter(
    prefix="/data",
    tags=['data']
)


@router.post("/user", status_code=200, response_model=UserInfo)
async def save_user(input_data: InputData):
    try:
        user_id, user_uuid = await UsersDb.post_user_to_db(input_data.user_name)
    except Exception:
        logger.error(f"save_user has error", exc_info=True)
    return {"user_id": user_id, "user_uuid": user_uuid}


@router.post("/sound", status_code=200, response_model=SoundInfo)
async def convert_and_save_sound(info_data: InputSound = Body(...),
                                 file: UploadFile = File(...)
                                 ):
    try:
        sound_uuid: str = str(uuid.uuid1())
        sound_data = SoundsDb(info_data.user_id, info_data.user_uuid, sound_uuid)
        check_result = await sound_data.check_id_and_uuid()
        if check_result is not None:
            sound_id = await convertor_wave_to_mp3(file.file.read(), sound_data)
            path_url = f"{main_url}/record?id=id_{sound_id}&user=id_{info_data.user_id}"
            return {"sound_url": path_url}
        else:
            logger.info("The given user does not exist")
            return JSONResponse(status_code=404,
                                content={"detail": "The given user does not exist"})
    except Exception:
        logger.error("convert_and_save_sound has error", exc_info=True)


@router.get("/download", status_code=200)
async def download_file(path_value: str):
    ids_tuple = await get_ids_from_path(path_value)
    if ids_tuple is None:
        logger.info("The request is incorrect")
        return JSONResponse(status_code=400,
                            content={"detail": "The request is incorrect"})
    else:
        sound_uuid = await GetUuidSound.check_sound_uuid(ids_tuple[0], ids_tuple[1])
        if sound_uuid is None:
            logger.info("The sound does not exist")
            return JSONResponse(status_code=404,
                                content={"detail": "The sound does not exist"})
        else:
            headers = {'Content-Disposition': f'attachment; filename="{ids_tuple[1]}"'}
            return FileResponse(path=f'static/sounds/{ids_tuple[1]}/{sound_uuid}.mp3', headers=headers,
                                media_type='audio/mp3')
