from AIDevs import AIDevsTasks, API_KEY, OPENAI_API_KEY
from langchain_openai import ChatOpenAI
from langchain.prompts import HumanMessagePromptTemplate, ChatPromptTemplate
from langchain.schema import SystemMessage
from langchain_core.output_parsers import JsonOutputParser
from datetime import datetime, timedelta
from pytz import timezone

llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=OPENAI_API_KEY)
dev_task = AIDevsTasks(API_KEY, "tools", debug=True)

task = dev_task.task()
question = task["question"]

today = datetime.now(timezone('Europe/Warsaw'))
tomorrow = today + timedelta(1)

system = f"""
To describe a user message as JSON with this structure {{"tool": "ToDo|Calendar", "desc": "(description)", "date(only with Calendar)": "(yyyy-MM-dd)"}}, we need to follow these rules:
- Always strictly follow the JSON structure described above with special care and attention.
- Task without specified date treat with tool ToDo. Important! Remove "date" field from JSON.
- Task with specified date treat with tool Calendar. Set date to the time this task has to be done.
- Today is {today.strftime('%Y-%m-%d')}
- Always return JSON and nothing else.

Examples:
- Jutro mam spotkanie z Marianem
- {{"tool": "Calendar", "desc": "Spotkanie z Marianem", "date":"{tomorrow.strftime('%Y-%m-%d')}"}}
- Przypomnij mi, że mam kupić mleko
- {{"tool": "ToDo", "desc": "Kup mleko"}}
"""

print(system)

prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content=system),
    HumanMessagePromptTemplate.from_template("{question}")
])

output_parser = JsonOutputParser()
chain = prompt | llm | output_parser
answer = chain.invoke({"question": question})


answer = {"answer": answer}
print(answer)
result = dev_task.send_answer(answer)