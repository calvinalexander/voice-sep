import os


import torchaudio

from fastapi import Response
from io import BytesIO
import zipfile
from fastapi.responses import StreamingResponse


async def inference(file_name, model, num_speakers) -> str:
    zip_filename = "archive.zip"

    s = BytesIO()
    zf = zipfile.ZipFile(s, "w")

    # model = separator.from_hparams(
    #     source="speechbrain/sepformer-wsj02mix", savedir='pretrained_models/sepformer-wsj02mix')

    # stream_source = BytesIO()
    # for custom file, change path
    est_sources = model.separate_file(path=f"../var/www/html/uploads/{file_name}")

    if num_speakers == 2:
        torchaudio.save('audios/speakerA.wav',
                        est_sources[:, :, 0], 8000, format="wav")
        torchaudio.save('audios/speakerB.wav',
                        est_sources[:, :, 1], 8000, format="wav")

    if num_speakers == 3:
        torchaudio.save('audios/speakerA.wav',
                        est_sources[:, :, 0], 8000, format="wav")
        torchaudio.save('audios/speakerB.wav',
                        est_sources[:, :, 1], 8000, format="wav")
        torchaudio.save('audios/speakerC.wav',
                        est_sources[:, :, 2], 8000, format="wav")

    for i in os.listdir('audios'):
        zf.write("audios/"+i)

    zf.close()

    resp = Response(s.getvalue(), media_type="application/x-zip-compressed", headers={
        'Content-Disposition': f'attachment;filename={zip_filename}'
    })
    # torchaudio.save("source2hat.wav",
    #                 est_sources[:, :, 1].detach().cpu(), 8000)

    # zf = zipfile.ZipFile(stream_source, "w")
    # zf.write(est_sources[:, :, 0].detach().cpu())
    # zf.write(est_sources[:, :, 1].detach().cpu())

    # zf.close()

    # resp = StreamingResponse(stream_source.getvalue(),
    #  media_type = "audio/x-wav")

    return resp
