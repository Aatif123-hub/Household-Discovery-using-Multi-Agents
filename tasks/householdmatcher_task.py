from crewai import Task
from textwrap import dedent
from agents.household_matcher import HouseholdMatchAgent

class HouseholdMatcherTasks:
    try:
     def household_matcher_task():
        return Task(description=dedent(f"""\
                    Identify records with different names but the same address.
                    Account for variations in address formatting (e.g., abbreviations, misspellings).
                    
                    Example:

                    "John Doe, 1701 Westpark Drive Apt 23",
                    "Mary Doe, 1701 Westpark Drive Apt 23",
                    These records form a household.

                    """),
                    agent=HouseholdMatchAgent
        )
    except Exception as e:
       raise Exception(f"Cannot execute Household Matcher Task. Error:{e}")