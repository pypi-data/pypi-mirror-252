import torch
from .whisper_sinhala import (whisper_sinhala)
from faster_whisper import WhisperModel

def transcribe(file, language, model_size):
    res = ""
    if language == "sin" or language == "Sin":
        res = whisper_sinhala(file)
        return res
    elif model_size == "tiny" or model_size == "small" or model_size == "medium" or model_size == "large" or model_size == "large-v1" or model_size == "large-v2" or model_size == "large-v3":

        if torch.cuda.is_available():
            # run on GPU with INT8
            model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")
        else:
            # run on CPU with INT8
            model = WhisperModel(model_size, device="cpu", compute_type="int8")

        if language in model.supported_languages:
            segments, info = model.transcribe(file, language=language, beam_size=1)

            for segment in segments:
                res += segment.text + " "
                return res
        else:
            Exception("Language code not supported.\nThese are the supported languages:\n", model.supported_languages)
    else:
        raise Exception("only 'tiny', 'small', 'medium', 'large', 'large-v1', 'large-v2', 'large-v3' models are available.")

