from AIDevs import AIDevsTasks, API_KEY, OPENAI_API_KEY
from openai import OpenAI
from os import path
import re
import urllib.request

openai_client = OpenAI(api_key=OPENAI_API_KEY)
dev_task = AIDevsTasks(API_KEY, "whisper", debug=True)

task = dev_task.task()
# hint = dev_task.hint()

filename = "whisper.mp3"
if not path.exists(filename):
    web_path = re.search("(?P<url>https?://[^\s]+)", task["msg"]).group("url")
    f = dev_task.get_file(web_path)
    with open(filename, "wb") as output:
        output.write(f)

file = open(filename, "rb")

transcription = openai_client.audio.transcriptions.create(
    model="whisper-1", file=file, response_format="text"
)
print(transcription)

result = transcription

answer = {"answer": result}

result = dev_task.send_answer(answer)
