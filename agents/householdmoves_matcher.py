from textwrap import dedent
from crewai import Agent
from rag.llm import LLM

class HouseholdMovesAgent:
    try:
     def household_moves():
          return Agent(
            role = "Household Moves Specialist",
            goal = dedent("""\
                        Conduct research on the dataset and provide the Household Moves result in a tabular format.""" ),
            backstory = dedent("""\
                               As a Household Moves Specialist in the field of entity resolution, 
                               you must provide the Household Moves in a datset using multiple attributes
                               Consider abbreviations, nicknames, and common misspellings.
                               Account for case sensitivity and punctuation differences."""),
            
            allow_delegation=False,
            llm = LLM,
            verbose=True
        )
    except Exception as e:
       raise Exception(f"Cannot execute Household Moves Agent. Error:{e}")
