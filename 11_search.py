from AIDevs import AIDevsTasks, API_KEY, OPENAI_API_KEY
from langchain_openai import ChatOpenAI
import docker
from docker.models.containers import Container
import time

llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=OPENAI_API_KEY)
dev_task = AIDevsTasks(API_KEY, "whoami", debug=True)
docker_client = docker.from_env()

container: Container = docker_client.containers.run("qdrant/qdrant", detach=True)
time.sleep(5)
container.remove(force=True)
