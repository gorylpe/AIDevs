from AIDevs import AIDevsTasks, API_KEY, OPENAI_API_KEY
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4", api_key=OPENAI_API_KEY)
dev_task = AIDevsTasks(API_KEY, "knowledge", debug=True)

task = dev_task.task()
question = task["question"]

# """
#     'database #1': 'Currency http://api.nbp.pl/en.html (use table A)',
# 'database #2': 'Knowledge about countries https://restcountries.com/ - field '
#             "'population'"
# """
