from pydub import AudioSegment
from fastapi import UploadFile
import uuid
import os


async def convert_to_wav(file: UploadFile):
    file_name = f'{uuid.uuid4().hex}.wav'
    output_file = os.path.abspath(f"../var/www/html/uploads/{file_name}")

    convert = AudioSegment.from_file_using_temporary_files(file.file)
    convert.set_frame_rate(16000)
    convert.export(
        output_file,
        format="wav",
        bitrate="320k",
        parameters=[
            "-ac", "1",     # Set number of audio channel
            "-aq", "0"      # set audio quality
        ]
    )

    return file_name
