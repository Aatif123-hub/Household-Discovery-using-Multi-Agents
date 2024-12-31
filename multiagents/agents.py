import os
from textwrap import dedent
from crewai import Agent
from rag.llm import LLM

class ER_AGENTS:
    def __init__(self, select_model):
        self.select_model = select_model

    def direct_match(self):
        return Agent(
            role="Direct Record Linkage Specialist",
            goal=dedent("""\
                        Link records that directly match by name and provide results in a tabular format."""),
            backstory=dedent("""\
                               As a Direct Record Linker, you must identify and link records with identical 
                               or nearly identical full names, accounting for minor spelling variations, 
                               abbreviations, nicknames, case sensitivity, and punctuation differences."""),
            allow_delegation=False,
            llm=LLM.get_llm(self.select_model),
            verbose=True
        )

    def indirect_match(self):
        return Agent(
            role="Indirect Record Linking Specialist",
            goal=dedent("""\
                    Link records that are connected through an intermediary and provide results in a tabular format"""),
            backstory=dedent("""\
                               As an Indirect Record Linker, you must identify records that are indirectly 
                               connected through an intermediary attribute, such as matching one record by 
                               name and another by address, thereby linking all associated records."""),
            allow_delegation=False,
            llm=LLM.get_llm(self.select_model),
            verbose=True
        )

    def household_match(self):
        return Agent(
            role="Household Identification Specialist",
            goal=dedent("""\
                    Find records that form a household and provide results in a tabular format."""),
            backstory=dedent("""\
                               As a Household Identification Specialist, you must detect groups of records 
                               that represent individuals residing at the same address, indicating 
                               a household, despite variations in name and address formatting."""),
            allow_delegation=False,
            llm=LLM.get_llm(self.select_model),
            verbose=True
        )

    def household_moves(self):
        return Agent(
            role="Relocation Tracking Specialist",
            goal=dedent("""\
                    Find instances where a household has moved to a new address and provide results in a tabular format."""),
            backstory=dedent("""\
                               As a Relocation Tracking Specialist, you must identify instances 
                               where a household has moved to a new address by detecting groups 
                               of records where the same individuals (by name) are associated 
                               with more than one address, accounting for minor name variations and address changes."""),
            allow_delegation=False,
            llm=LLM.get_llm(self.select_model),
            verbose=True
        )