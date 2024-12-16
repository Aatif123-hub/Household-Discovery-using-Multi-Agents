from textwrap import dedent
from crewai import Agent
from rag.llm import LLM

class HouseholdMatchAgent:
    try:
     def household_match():
          return Agent(
            role = "Household Match Specialist",
            goal = dedent("""\
                        Conduct research on the dataset and provide the Household match result in a tabular format.""" ),
            backstory = dedent("""\
                               As a Household Matching Specialist in the field of entity resolution, 
                               you must provide the Household Matches in a datset using multiple attributes
                               Identify records where the full names are the same or have minor spelling variations.
                               Consider abbreviations, nicknames, and common misspellings.
                               Account for case sensitivity and punctuation differences."""),
            
            allow_delegation=False,
            llm = LLM,
            verbose=True
        )
    except Exception as e:
       raise Exception(f"Cannot execute Household Matcher Agent. Error:{e}")