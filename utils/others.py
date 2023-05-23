import os
import io

from typing import Any
from pydub import AudioSegment

from logs_info import logger
from utils.models import SoundsDb


async def convertor_wave_to_mp3(file: bytes, sound_data: SoundsDb) -> int:
    try:
        recording = AudioSegment.from_file(io.BytesIO(file), format="wave")
        folder_path = f'static/sounds/{sound_data.user_id}'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        recording.export(f'{folder_path}/{sound_data.sound_uuid}.mp3', format='mp3')  # for export
        sound_id = await sound_data.post_sound_to_db()
        return sound_id
    except Exception:
        logger.error(f"convertor_wave_to_mp3 has error", exc_info=True)


async def get_ids_from_path(path_value: str) -> Any:
    try:
        ids = path_value.split("?")[1:][0].split("&")
        ids_tuple = (int(ids[0][6:]), int(ids[1][8:]))
        return ids_tuple
    except Exception:
        logger.error(f"get_ids_from_path has error", exc_info=True)
        return None
