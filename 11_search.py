from AIDevs import AIDevsTasks, API_KEY, OPENAI_API_KEY
from langchain_openai import ChatOpenAI
import docker
from docker.models.containers import Container
from qdrant_client import QdrantClient
import json
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate

llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=OPENAI_API_KEY)
dev_task = AIDevsTasks(API_KEY, "search", debug=True)
docker_client = docker.from_env()

port = 6333
container: Container = None
try:
    container = docker_client.containers.run(
        "qdrant/qdrant", detach=True, name="11_search", ports={f"{port}/tcp": port}
    )
except Exception as e:
    print("Container already created")

qdrant_client = QdrantClient(host="localhost", port=port)

f = open("archiwum_aidevs.json", "r")
data: list[dict] = json.load(f)
f.close()

inserted_data_count = qdrant_client.count("docs")
if inserted_data_count.count < len(data):
    qdrant_client.delete_collection("docs")

    docs = []
    metadata = []
    ids = []
    for i, d in enumerate(data):
        docs.append(d["info"])
        metadata.append({"title": d["title"], "url": d["url"], "date": d["date"]})
        ids.append(i)

    # Use FastEmbed for embeddings now
    qdrant_client.add("docs", documents=docs, metadata=metadata, ids=ids)
else:
    print("Data already uploaded")

task = dev_task.task()
question = task["question"]

search_result = qdrant_client.query("docs", question, limit=5)

answer = {"answer": search_result[0].metadata["url"]}

result = dev_task.send_answer(answer)

# todo dodatkowe rzeczy które też mogą być podobne z tematów, LLM który sprawdza który najbardziej
#
# documents = "\n".join([f"{i}. {x.document}" for (i, x) in enumerate(search_result)])
# print(documents)

# prompt = ChatPromptTemplate.from_messages(
#     [
#         SystemMessagePromptTemplate.from_template(
#             "Odpowiadasz tylko na podstawie podanej listy tematów.\n"
#             'W przypadku gdy lista nie zawiera odpowiedniej informacji odpowiedz "Nie wiem".\n'
#             "Lista tematów:\n"
#             "{context}\n"
#         ),
#         (
#             "user",
#             'Podaj tylko numer tematu który jest najbardziej związany z pytaniem "{input}".',
#         ),
#     ]
# )
# chain = prompt | llm
# chain_answer = chain.invoke({"input": question, "context": documents})
# print(chain_answer.content)
