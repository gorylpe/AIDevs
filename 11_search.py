from AIDevs import AIDevsTasks, API_KEY, OPENAI_API_KEY
from langchain_openai import ChatOpenAI
import docker
from docker.models.containers import Container
from qdrant_client import QdrantClient
import json

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
