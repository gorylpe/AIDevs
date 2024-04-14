from AIDevs import AIDevsTasks, API_KEY, OPENAI_API_KEY
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from langchain.prompts import HumanMessagePromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import requests

llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=OPENAI_API_KEY)
dev_task = AIDevsTasks(API_KEY, "knowledge", debug=True)

task = dev_task.task()
question = task["question"]

system = """
To describe a user message as JSON with this structure {"action": "currency|population|knowledge", "details": "(details)"}, we need to follow these rules:
- Always strictly follow the JSON structure described above with special care and attention.
- If user message is about currency, set details to currency code.
- If user message is about population, set details to country name in English.
- In other cases set details as answer using your knowledge and answer in Polish.
- Always return JSON and nothing else.

Examples:
- Jaki jest kurs franka szwajcarskiego?
- {"action": "currency", "details": "chf"}
- Ile osób mieszka w Polsce?
- {"action": "population", "details": "poland"}
- Ile jest planet w Układzie Słonecznym?
- {"action": "knowledge", "details": "Osiem."}
"""
prompt = ChatPromptTemplate.from_messages([
    SystemMessage(system),
    HumanMessagePromptTemplate.from_template("{question}")
])

output_parser = JsonOutputParser()

chain = prompt | llm | output_parser
action_json = chain.invoke({"question": question})
print(action_json)

action = action_json["action"]
details = action_json["details"]

answer = ""
if action == "knowledge":
    answer = details
if action == "currency":
    answer = requests.get(f"https://api.nbp.pl/api/exchangerates/rates/a/{details}?format=json").json()
    answer = answer["rates"][0]
    answer = f"{answer['mid']}"
if action == "population":
    answer = requests.get(f"https://restcountries.com/v3.1/name/{details}").json()
    answer = answer[0]
    answer = f"{answer['population']}"
# """
#     'database #1': 'Currency http://api.nbp.pl/en.html (use table A)',
# 'database #2': 'Knowledge about countries https://restcountries.com/ - field '
#             "'population'"
# """

print(answer)
answer = {"answer": answer}
result = dev_task.send_answer(answer)