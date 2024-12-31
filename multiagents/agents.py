import os
from textwrap import dedent
from crewai import Agent
from rag.llm import LLM

class ER_AGENTS:
    def direct_match():
        return Agent(
            role = "Direct Record Matcher",
            goal = dedent("""\
                        Conduct research on the dataset and provide the direct match result in a tabular format.""" ),
            backstory = dedent("""\
                               As a Direct Matcher in the field of record linkage, 
                               you must provide the direct matches in a datset using multiple attributes
                               Identify records where the full names are the same or have minor spelling variations.
                               Consider abbreviations, nicknames, and common misspellings.
                               Account for case sensitivity and punctuation differences."""),
            
            allow_delegation=False,
            llm = LLM,
            verbose=True
        )
    def indirect_match():
          return Agent(
            role = "Indirect Record Matcher",
            goal = dedent("""\
                        Conduct research on the dataset and provide the indirect match result in a tabular format.""" ),
            backstory = dedent("""\
                               As an Indirect Matcher in the field of entity resolution, 
                               you must provide the indirect matches in a datset using multiple attributes
                               Identify records where the full names are the same or have minor spelling variations.
                               Consider abbreviations, nicknames, and common misspellings.
                               Account for case sensitivity and punctuation differences."""),
            
            allow_delegation=False,
            llm = LLM,
            verbose=True
        )
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
    