import os
from textwrap import dedent
from crewai import Agent
from rag.llm import LLM
class DirectMatchAgent:

    def __init__(self):
        self.llm = LLM

    def direct_match(self):
          return Agent(
            role = "Direct Match Specialist",
            goal = dedent("""\
                        Conduct research on the dataset and provide the direct match result in a tabular format.""" ),
            backstory = dedent("""\
                               As a Direct Matching Specialist in the field of entity resolution, 
                               you must provide the direct matches in a datset using multiple attributes
                               Identify records where the full names are the same or have minor spelling variations.
                               Consider abbreviations, nicknames, and common misspellings.
                               Account for case sensitivity and punctuation differences.
                               Example:

                               Records A928147 and A972885 both have the name "FRANCINE J KEGLER" (with minor variations) and are thus a direct match."""),
            
            allow_delegation=False,
            llm = self.llm,
            verbose=True
        )

    