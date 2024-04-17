from AIDevs import AIDevsTasks, API_KEY, OPENAI_API_KEY
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import SystemMessage, HumanMessage
import requests

llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=OPENAI_API_KEY)
dev_task = AIDevsTasks(API_KEY, "meme", debug=True)

task = dev_task.task()
image = task["image"]
text = task["text"]

RENDERFORM_APIKEY = "placeholder todo"

headers = {
    "X-API-KEY": RENDERFORM_APIKEY,
    "Content-Type": "application/json",
}
response = requests.post(
    "https://get.renderform.io/api/v2/render",
    headers=headers,
    json={
        "template": "heavy-frogs-dig-well-1437",
        "data": {
            "title.text": text,
            "image.src": image,
        },
    },
)

response_json = response.json()
print(response_json)
answer: str = response_json["href"]
print(answer)
answer = {"answer": answer}
result = dev_task.send_answer(answer)
