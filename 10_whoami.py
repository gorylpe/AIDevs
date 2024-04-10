from AIDevs import AIDevsTasks, API_KEY, OPENAI_API_KEY
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=OPENAI_API_KEY)
dev_task = AIDevsTasks(API_KEY, "whoami", debug=True)
answer = None
tries = 0

hints = []
while answer == None and tries < 10:
    tries += 1

    task = dev_task.task()
    hint = task["hint"]
    hints.append(hint)
    hints_str = "\n".join([f"- {x}." for x in hints])
    print(hints_str)

    query = f"""
    Na podstawie podanych niżej wskazówek zgadnij co to za osoba.
    
    Wskazówki:
    {hints_str}

    Bądź bardzo dokładny i ścisły. Możesz jedynie odpowiedzieć "Imię nazwisko" gdy jesteś absolutnie pewien odpowiedzi i "NIE" gdy nie jesteś pewny.
    """

    result = llm.invoke(query)
    print(result.content)
    if "NIE" not in result.content:
        answer = result.content


answer = {"answer": answer}
query = dev_task.send_answer(answer)
