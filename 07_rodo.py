from AIDevs import AIDevsTasks, API_KEY, OPENAI_API_KEY
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=OPENAI_API_KEY)
dev_task = AIDevsTasks(API_KEY, "rodo", debug=True)

task = dev_task.task()

result = """
Zasady:
- Za wrażliwe informacje uważaj: imię, nazwisko, zawód i miasto.
- Zastąp wszystkie imiona i nazwiska symbolem zastępczym %imie% %nazwisko%.
- Miasta należy zastąpić symbolem zastępczym %miasto%, pozostawiając nazwy krajów bez zmian.
- Użyj symbolu zastępczego %zawod% dla zawodu i innych informacji związanych z pracą.

Opowiedz mi o sobie ściśle przestrzegając zasad.
"""

answer = {"answer": result}

result = dev_task.send_answer(answer)
