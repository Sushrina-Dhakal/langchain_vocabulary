from dotenv import load_dotenv,find_dotenv
import os
load_dotenv(find_dotenv())
apikey=os.getenv("google_api_key")

from langchain_google_genai import ChatGoogleGenerativeAI
model=ChatGoogleGenerativeAI(model="gemini-1.5-pro",api_key=apikey)
#from langchain_openai import ChatOpenAI
#model=ChatOpenAI(model="gpt-4o-mini",api_key=apikey)

from langchain_core.output_parsers import JsonOutputParser
parser=JsonOutputParser() 

from langchain_core.prompts import ChatPromptTemplate
template="""
You are a professional in nepali vocabularies. You are provided with nepali word. 
###Nepali word={word}
Your task is to create a JSON output in a format specified as :
dict(
"word":"nepali word provided to you",
"definition":"simple definition of the nepali word in nepali language",
"simplified_words":"simple Synonym words of the nepali word provided to you in nepali language",
"example sentence":"example sentence in nepali language using the word provided to you"
)
your response must only be JSON Output, do not add any additional text or tags in your answer.
"""
prompt=ChatPromptTemplate.from_template(template)

from langchain_core.runnables import RunnableMap
chain=RunnableMap(
    {
        "word":lambda x:x['word']
    }
)|prompt|model|parser

import csv
import json
outputs=[]
with open(r"NepaliWords - Sheet1.csv","r",encoding="utf-8") as file:
    reader=csv.DictReader(file)
    for row in reader:
        response=chain.invoke({"word":row["Words"]})
        print(response)
        outputs.append(response)

with open("Outputs.json","w",encoding="utf-8") as file:
    json.dump(outputs,file,indent=4,ensure_ascii=False)
