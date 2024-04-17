from AIDevs import AIDevsTasks, API_KEY, OPENAI_API_KEY, NGROK_AUTH_TOKEN
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain.schema.messages import AIMessage, HumanMessage
from fastapi import FastAPI
from pydantic import BaseModel
from contextlib import asynccontextmanager
import threading
import uvicorn
import ngrok

llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=OPENAI_API_KEY)
chain = llm | StrOutputParser()
dev_task = AIDevsTasks(API_KEY, "ownapipro", debug=True)


def run_test(url: str):
    print("Starting test")
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


messages = []


@app.post("/")
def answer(request: Request):
    question = request.question
    messages.append(HumanMessage(question))
    replyObj = llm.invoke(messages)
    reply = replyObj.content
    print(f"{question} - {reply}")
    messages.append(AIMessage(reply))
    return {"reply": reply}


if __name__ == "__main__":
    uvicorn.run(
        app=app,
        host="0.0.0.0",
        port=5000,
        reload=False,
    )
