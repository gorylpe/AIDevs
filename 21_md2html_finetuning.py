from AIDevs import OPENAI_API_KEY
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(model="gpt-4-turbo", api_key=OPENAI_API_KEY)

system = """
To generate artificial data with structure {"messages":[{"role":"system","content":"MD2HTML"},{"role":"user","content":"(markdown)"},{"role":"assistant","content":"(html)"}]}, we need to follow these rules:
- Always strictly follow the JSON structure described above with special care and attention.
- Convert markdown to html.
- Markdown example should be at least 3 lines.
- For bold always use following syntax <span class="bold">text</span>
- Always return multiple lines of JSONL data.
- Fit each example in single line.

Example:
Genarate 2 examples of artificial data. Generate 1 example with conversion of single markdown element. 
{"messages":[{"role":"system","content":"MD2HTML"},{"role":"user","content":"## Templating example\n1. Template **first**\n2.Template second"},{"role":"assistant","content":"<h2>Templating example</h2>\n<ol>\n<li>Template <span class=\"bold\">first</span></li>\n<li>Template second</li>\n</ol>"}]}
{"messages":[{"role":"system","content":"MD2HTML"},{"role":"user","content":"[AI Devs 3.0](https://aidevs.pl) _nowy_ *kurs*"},{"role":"assistant","content":"<a href="https://aidevs.pl">AI Devs 3.0</a> <u>nowy</u> <em>kurs</em>"}]}
{"messages":[{"role":"system","content":"MD2HTML"},{"role":"user","content":"_underline_"},{"role":"assistant","content":"<u>underline</u>"}]}
"""
prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(system),
        HumanMessage(
            "Generate 20 examples of artificial data. Example text should be about Fortnite. Generate 10 examples with conversion of single markdown element."
        ),
    ]
)
output_parser = StrOutputParser()

chain = prompt | llm | output_parser
output = chain.invoke({})
print(output)
