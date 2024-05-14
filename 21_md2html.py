from AIDevs import AIDevsTasks, API_KEY, OPENAI_API_KEY
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(
    model="ft:gpt-3.5-turbo-0125:personal:aidevs3:9FLiI9QQ",
    api_key=OPENAI_API_KEY,
)
dev_task = AIDevsTasks(API_KEY, "md2html", debug=True)

task = dev_task.task()
input = task["input"]

system = "MD2HTML"
prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(system),
        HumanMessage(input),
    ]
)
output_parser = StrOutputParser()

chain = prompt | llm | output_parser
output = chain.invoke({})

print(output)
answer = {"answer": output}
result = dev_task.send_answer(answer)
