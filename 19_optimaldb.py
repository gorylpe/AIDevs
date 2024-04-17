from AIDevs import AIDevsTasks, API_KEY, OPENAI_API_KEY
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.schema import SystemMessage
import json

llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=OPENAI_API_KEY)
dev_task = AIDevsTasks(API_KEY, "optimaldb", debug=True)

task = dev_task.task()

f = open("3friends.json", "r")
data: dict = json.load(f)
f.close()

system = f"""
You are persons database optimizer. Take a deep breath and analyze all informations about given persons. 
Then try to optimize text about them to get shorter description.
Rules:
- Result description should have all informations about person. Important to not skip any.
- Preserve all specific informations like favourite name of puzzles or movies.
- Remove all duplicate informations.
- Group similar informations in one sentence.
- Result in English in list format.

Example:
###
Piotr:
Lubi film "Gwiezdne wojny" i ogólnie chodzić do kina.
Lubi serial "Dr House"

Piotr:
Likes "Star Wars" and "Dr House" and visit cinema. 
"""

prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content=system),
        HumanMessagePromptTemplate.from_template("{name}:\n{informations}"),
    ]
)

inputs = list(
    map(lambda kv: {"name": kv[0], "informations": "\n- ".join(kv[1])}, data.items())
)
# del inputs[-2:]
# print(inputs)

chain = prompt | llm
answer = chain.batch(inputs, config={"max_concurrency": 3})
answer = {"answer": "\n\n".join([x.content for x in answer])}
print(answer)
result = dev_task.send_answer(answer)
