from AIDevs import AIDevsTasks, API_KEY, OPENAI_API_KEY
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(model="text-embedding-ada-002", api_key=OPENAI_API_KEY)
dev_task = AIDevsTasks(API_KEY, "embedding", debug=True)

task = dev_task.task()
# hint = dev_task.hint()

result = embeddings.embed_query("Hawaiian pizza")

answer = {"answer": result}

result = dev_task.send_answer(answer)
