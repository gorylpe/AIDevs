from AIDevs import AIDevsTasks, API_KEY, OPENAI_API_KEY
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=OPENAI_API_KEY)
dev_task = AIDevsTasks(API_KEY, "functions", debug=True)

task = dev_task.task()

answer = {
    "answer": {
        "name": "addUser",
        "description": "Adds user to database",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Name of user"
                },
                "surname": {
                    "type": "string",
                    "description": "Surname of user"
                },
                "year": {
                    "type": "integer",
                    "description": "Year of birth of user"
                }
            }
        }
    }
}

result = dev_task.send_answer(answer)
