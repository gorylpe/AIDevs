from AIDevs import AIDevsTasks, API_KEY, OPENAI_API_KEY
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=OPENAI_API_KEY)
dev_task = AIDevsTasks(API_KEY, "liar", debug=True)

question = "What is capital of Poland?"
task = dev_task.task_with_data(data={"question": question})
# hint = dev_task.hint()
task_answer = task["answer"]

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            f'Oceniasz czy wiadomość poniżej jest odpowiedzią na pytanie "{question}". Zwróć NO jeśli nie i YES jeśli tak.',
        ),
        ("user", "{input}"),
    ]
)
chain = prompt | llm
chain_answer = chain.invoke(input=task_answer)

answer = {"answer": chain_answer.content}
print(answer)

result = dev_task.send_answer(answer)
