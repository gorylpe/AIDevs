from AIDevs import AIDevsTasks, API_KEY, OPENAI_API_KEY
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate

import requests

llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=OPENAI_API_KEY)
dev_task = AIDevsTasks(API_KEY, "scraper", debug=True)

task = dev_task.task()
url = task["input"]
question = task["question"]

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

success = False
while not success:
    try:
        out = requests.get(url, headers=headers, timeout=60)
        if out.status_code == 200:
            success = True
        else:
            print(out.status_code)
    except Exception as e:
        print(e)

prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            "Odpowiadasz tylko na podstawie podanego kontekstu.\n"
            'W przypadku gdy kontekst nie zawiera odpowiedniej informacji odpowiedz "Nie wiem.".\n'
            "Kontekst:\n"
            "###\n"
            "{context}\n"
            "###\n"
        ),
        ("user", "Odpowiedź musi być w języku polskim i mieć maksymalnie 200 znaków. Pytanie: {input}. Odpowiedź w języku polskim:"),
    ]
)
chain = prompt | llm
chain_answer = chain.invoke({"input": question, "context": out.content})

print(chain_answer.content)

# Tłumaczenie jako oddzielny prompt może być

answer = {"answer": chain_answer.content}

result = dev_task.send_answer(answer)
