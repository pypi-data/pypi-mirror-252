import logging

import bentoml
import gradio as gr
import numpy as np
from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI

from llmchatbot.controller.chatter import Chatter
from llmchatbot.controller.translator import (
    Speech2TextTranslator,
    Text2SpeechTranslator,
)
from llmchatbot.model.finetune.model_loader import (
    T5_MODEL,
    T5_PROCESSOR,
    T5_VOCODER,
    WHISPER_MODEL,
    WHISPER_PROCESSOR,
)
from llmchatbot.view.viewer import ChatbotViewer

dotenv_file = find_dotenv("envs/.env")
load_dotenv(dotenv_file)

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger()


speech2text_translator = bentoml.Runner(
    runnable_class=Speech2TextTranslator,
    name="speech2text",
    models=[WHISPER_PROCESSOR, WHISPER_MODEL],
)
text2speech_translator = bentoml.Runner(
    runnable_class=Text2SpeechTranslator,
    name="text2speech",
    models=[T5_PROCESSOR, T5_MODEL, T5_VOCODER],
)

svc = bentoml.Service(
    name="llmchatbot",
    runners=[
        speech2text_translator,
        text2speech_translator,
    ],
)


@svc.api(input=bentoml.io.NumpyNdarray(), output=bentoml.io.Text())
def generate_text(speech: np.ndarray) -> str:
    text = speech2text_translator.translate.run(speech)
    return text


@svc.api(input=bentoml.io.Text(), output=bentoml.io.NumpyNdarray())
def generate_speech(text: str) -> np.ndarray:
    return text2speech_translator.translate.run(text)


chatter = Chatter(generate_speech, generate_text, WHISPER_PROCESSOR, LOGGER)
app = FastAPI()
viewer = ChatbotViewer(chatter)
app = gr.mount_gradio_app(app, viewer.get_view(), path="/llmchatbot")
svc.mount_asgi_app(app, "/")
