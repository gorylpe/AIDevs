from AIDevs import AIDevsTasks, API_KEY, OPENAI_API_KEY, NGROK_AUTH_TOKEN, SERP_APIKEY
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from langchain.schema import SystemMessage, HumanMessage
from fastapi import FastAPI
from pydantic import BaseModel
from contextlib import asynccontextmanager
import threading
import uvicorn
import ngrok
from serpapi import GoogleSearch

llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=OPENAI_API_KEY)
chain = llm | JsonOutputParser()
dev_task = AIDevsTasks(API_KEY, "google", debug=True)


def run_test(url: str):
    task = dev_task.task()
    answer = {"answer": url}
    result = dev_task.send_answer(answer)


@asynccontextmanager
async def lifespan(app: FastAPI):
    listener = await ngrok.forward(5000, authtoken=NGROK_AUTH_TOKEN)
    url = listener.url()
    threading.Thread(target=run_test, args=[url]).start()
    yield


app = FastAPI(lifespan=lifespan)


class Request(BaseModel):
    question: str


system = SystemMessage(
    content="""
To describe a user message as JSON with this structure {"action": "url|knowledge", "details": "(details)"}, we need to follow these rules:
- Always strictly follow the JSON structure described above with special care and attention.
- For message about searching information in internet use action "url" with "details" what to query search engine.
- In other cases set details as answer using your knowledge and answer in Polish.
- Always return JSON and nothing else.

Examples:
- Szukam strony z ogłoszeniami o pracę w firmie Comarch, pomożesz?
- {"action": "url", "details": "Comarch ogłoszenia o pracę"}
- Ile osób mieszka w Polsce?
- {"action": "knowledge", "details": "Około 38 milionów"}
"""
)


@app.post("/")
def answer(request: Request):
    question = request.question
    human = HumanMessage(content=question)
    action_json = chain.invoke([system, human])
    print(f"{question} - {action_json}")
    action = action_json["action"]
    details = action_json["details"]

    answer = ""
    if action == "knowledge":
        answer = details
    elif action == "url":
        search = GoogleSearch(
            {
                "q": details,
                "location": "Warsaw,Poland",
                "api_key": SERP_APIKEY,
            }
        )
        result = search.get_dict()
        answer = result["organic_results"][0]["link"]
    print(f"{question} - {action_json} - {answer}")
    return {"reply": answer}


if __name__ == "__main__":
    uvicorn.run(
        app=app,
        host="0.0.0.0",
        port=5000,
        reload=False,
    )
