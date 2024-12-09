import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_google_genai import ChatGoogleGenerativeAI
load_dotenv()

class LLM:
    def get_available_llm():
        return ['chatgpt','mistral','llama3.2','gemini']
    
    def get_llm(select_model):
        select_model = select_model
        if select_model == 'chatgpt':
          try:
            llm = ChatOpenAI(model = "gpt-4o",
                              max_tokens=4096,
                              temperature=0.2)
          except Exception as e:
            raise Exception(f"Cannot load chatgpt. Error:{e}")
        
        elif select_model == 'mistral':
           try:
              llm = ChatMistralAI(model = "mistral-large-latest",
                                  max_tokens=4096,
                                  temperature=0.2)
           except Exception as e:
              raise Exception(f"Cannot load mistral. Error:{e}")
           
        elif select_model == 'llama3.2':
           try:
              llm = ChatOpenAI(model="llama3.2",
                               base_url=os.getenv("BASE_URL"),
                               max_tokens=4096,
                               temperature=0.2)
           except Exception as e:
              raise Exception(f"Cannot load llama3.2. Error:{e}")
           
        elif select_model == 'gemini':
           try:
              llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash",
                          api_key = os.getenv("GOOGLE_API_KEY"),
                          max_tokens=4096,
                          temperature=0.2)
           except Exception as e:
              raise Exception(f"Cannot load gemini. Error:{e}")
              
        else:
           raise ValueError("Invalid Value. Select 'chatgpt','mistral' or 'llama3'.")
       
        return llm
              
        



        
        

