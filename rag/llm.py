import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from crewai import LLM
from langchain_mistralai import ChatMistralAI
from langchain_google_genai import ChatGoogleGenerativeAI
from litellm import completion
from langchain_deepseek import ChatDeepSeek
load_dotenv()

class LLM:
    @staticmethod
    def get_available_llm():
        return ['chatgpt','mistral','llama3.2','gemini','deepseek']
    
    @staticmethod
    def get_llm(select_model):
        select_model = select_model
        if select_model == 'chatgpt':
          try:
            llm = ChatOpenAI(model = "gpt-4o-mini",
                              max_tokens=4096,
                              temperature=0.2)
          except Exception as e:
            raise Exception(f"Cannot load chatgpt. Error:{e}")
        
        elif select_model == 'mistral':
           try:
              llm = ChatMistralAI(model = "mistral-large-latest",
                        api_key = os.getenv("MISTRAL_API_KEY"),
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
              llm = ChatGoogleGenerativeAI(model="gemini/gemini-1.5-flash",
                          api_key = os.getenv("GOOGLE_API_KEY"),
                          max_tokens=4096,
                          temperature=0.2)
           except Exception as e:
              raise Exception(f"Cannot load gemini. Error:{e}")
              
        elif select_model == 'deepseek':
           try:
              llm = ChatOpenAI(model="deepseek-r1:14b",
                                   base_url=os.getenv("BASE_URL"),
                                   max_tokens=4096,
                                   temperature=0.2)
           except Exception as e:
              raise Exception(f"Cannot load deepseek. Error:{e}")
              
        else:
           raise ValueError("Invalid Value. Select 'chatgpt','mistral' or 'llama3'.")
       
        return llm

# --- Top-level function for meta-agent feedback ---
def get_llm_feedback(prompt):
    """
    Calls the default LLM to get feedback for the meta-agent.
    You can customize this to use a specific LLM or pass in an LLM object if needed.
    """
    llm = ChatOpenAI(model = "o4-mini", max_tokens=1024, temperature=1)
    response = llm.invoke([{"role": "system", "content": prompt}])
    return response.content if hasattr(response, 'content') else str(response)
        



        
        

