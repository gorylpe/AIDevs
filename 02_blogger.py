from AIDevs import AIDevsTasks, API_KEY, OPENAI_API_KEY
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=OPENAI_API_KEY)
dev_task = AIDevsTasks(API_KEY, "blogger", debug=True)

task = dev_task.task()
# hint = dev_task.hint()

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Jesteś bloggerem który pisze wpisy na bloga o gotowaniu dla opornych na zadane tytuły.",
        ),
        ("user", "{input}"),
    ]
)
chain = prompt | llm

inputs = list(map(lambda x: {"input": x}, task["blog"]))
ans = chain.batch(inputs, config={"max_concurrency": 15})

answer = {"answer": [x.content for x in ans]}
print(answer)

result = dev_task.send_answer(answer)

assert result["code"] == 0
