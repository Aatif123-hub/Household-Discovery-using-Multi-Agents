from textwrap import dedent
from crewai import Agent
from rag.llm import LLM

class HouseholdMovesAgent:

    def __init__(self):
        self.llm = LLM

    def household_moves(self):
          return Agent(
            role = "Household Moves Specialist",
            goal = dedent("""\
                        Conduct research on the dataset and provide the Household Moves result in a tabular format.""" ),
            backstory = dedent("""\
                               As a Household Moves Specialist in the field of entity resolution, 
                               you must provide the Household Moves in a datset using multiple attributes
                               Identify records where the full names are the same or have minor spelling variations.
                               Consider abbreviations, nicknames, and common misspellings.
                               Account for case sensitivity and punctuation differences."""),
            
            allow_delegation=False,
            llm = self.llm,
            verbose=True
        )
