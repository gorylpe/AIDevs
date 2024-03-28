from AIDevs import AIDevsTasks, API_KEY, OPENAI_API_KEY
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.prompts import SystemMessagePromptTemplate

llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=OPENAI_API_KEY)
dev_task = AIDevsTasks(API_KEY, "inprompt", debug=True)

task = dev_task.task()
# hint = dev_task.hint()
task_input: list[str] = task["input"]
task_question = task["question"]

ans1 = llm.invoke(
    f'Jak ma na imię osoba wspomniana w pytaniu "{task_question}"? Zwróć tylko imię w mianowniku.'
)
name = ans1.content
print(name)

input_filtered = [x for x in task_input if name in x]
print(input_filtered)

facts = "\n".join(f"- {i}" for i in input_filtered)

prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            "Masz listę faktów na temat różnych osób i możesz odpowiadać tylko i wyłącznie na podstawie tych faktów.\n"
            'W przypadku gdy te fakty nie zawierają informacji odpowiedz "Nie wiem.".\n'
            "Fakty:\n"
            "{facts}"
        ),
        ("user", "{input}"),
    ]
)
chain = prompt | llm
chain_answer = chain.invoke({"input": task_question, "facts": facts})

answer = {"answer": chain_answer.content}
print(answer)

result = dev_task.send_answer(answer)
