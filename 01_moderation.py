from AIDevs import AIDevsTasks, API_KEY, OPENAI_API_KEY
from openai import OpenAI

openai_client = OpenAI(api_key=OPENAI_API_KEY)
dev_task = AIDevsTasks(API_KEY, "moderation", debug=True)

task = dev_task.task()
# hint = dev_task.hint()

inputs = task["input"]

moderation_response = openai_client.moderations.create(
    input=inputs, model="text-moderation-latest"
)
outputs = [int(x.flagged) for x in moderation_response.results]
print(outputs)

answer = {"answer": outputs}

result = dev_task.send_answer(answer)

assert result["code"] == 0
