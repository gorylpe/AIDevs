from AIDevs import AIDevsTasks, API_KEY, OPENAI_API_KEY
from langchain_openai import ChatOpenAI
from flask import Flask, request
from flask_cloudflared import _run_cloudflared
import threading
import time

llm = ChatOpenAI(model="gpt-4-turbo", api_key=OPENAI_API_KEY)
dev_task = AIDevsTasks(API_KEY, "ownapi", debug=True)

task = dev_task.task()


def run_test():
    tunnel_url = _run_cloudflared(port=5000, metrics_port=8100)
    time.sleep(2)
    print(tunnel_url)
    answer = {"answer": tunnel_url}
    result = dev_task.send_answer(answer)
    exit()


threading.Thread(target=run_test).start()

app = Flask(__name__)
app.debug = False


@app.route("/", methods=["GET", "POST"])
def answer():
    question = request.json["question"]
    reply = llm.invoke(question)
    print(f"{question} - {reply.content}")
    return {"reply": reply.content}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
