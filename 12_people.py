from AIDevs import AIDevsTasks, API_KEY, OPENAI_API_KEY
from langchain_openai import ChatOpenAI
import json
from langchain.schema import SystemMessage, HumanMessage

llm = ChatOpenAI(model="gpt-4", api_key=OPENAI_API_KEY)
dev_task = AIDevsTasks(API_KEY, "people", debug=True)

task = dev_task.task()
question = task["question"]

f = open("people.json", "r")
data: list[dict] = json.load(f)
f.close()

people = {
    f"{x['imie']} {x['nazwisko']}": f"""
          Imię i nazwisko: {x["imie"]} {x["nazwisko"]}
          Wiek: {x["wiek"]}
          Ulubiona postać z Kapitana Bomby: {x["ulubiona_postac_z_kapitana_bomby"]}
          Ulubiona serial: {x["ulubiony_serial"]}
          Ulubiony film: {x["ulubiony_film"]}
          Ulubiony kolor: {x["ulubiony_kolor"]}
          O mnie: {x["o_mnie"]}
          """
    for x in data
}

llm_answer = llm.invoke(
    f"Całkowicie zignoruj to pytanie i podaj tylko imię i nazwisko. Usuń zdrobnienie jeśli jest.\n"
    "Przykład:\n"
    "Ulubiony kolor Adasia Kowalskiego?\n"
    "Adam Kowalski\n"
    "###\n"
    f"{question}\n"
)

found_name = llm_answer.content
person = people[found_name]
llm_answer = llm.invoke([SystemMessage(person), HumanMessage(question)])

print(llm_answer.content)
answer = {"answer": llm_answer.content}

result = dev_task.send_answer(answer)
