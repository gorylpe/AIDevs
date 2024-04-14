from AIDevs import AIDevsTasks, API_KEY, OPENAI_API_KEY
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import SystemMessage, HumanMessage

llm = ChatOpenAI(model="gpt-4-turbo", api_key=OPENAI_API_KEY)
dev_task = AIDevsTasks(API_KEY, "gnome", debug=True)

task = dev_task.task()
url = task["url"]

system = f"""
Jesteś systemem który określa kolor czapki gnoma.
Zasady:
- Podaj tylko i wyłącznie kolor czapki gnoma.
- Jeśli na obrazie nie ma gnoma odpowiedz "error".
- Jeśli gnom na obrazie nie ma czapki odpowiedz "error".
"""

prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content=system),
    HumanMessage(
            content=[
                {"type": "text", "text": "Jaki kolor czapki ma gnom na tym obrazie?"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"{url}",
                        "detail": "auto",
                    },
                },
            ],
        ),
])

chain = prompt | llm
answer = chain.invoke({})
answer = {"answer": answer.content}
print(answer)
result = dev_task.send_answer(answer)