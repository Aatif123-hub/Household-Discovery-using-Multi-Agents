from crewai import Task
from textwrap import dedent

class HouseholdMatcherTasks:
    def household_matcher_task(self,agent):
        return Task(description=dedent(f"""\
                    Identify records with different names but the same address.
                    Account for variations in address formatting (e.g., abbreviations, misspellings).
                    
                    Example:

                    "John Doe, 1701 Westpark Drive Apt 23",
                    "Mary Doe, 1701 Westpark Drive Apt 23",
                    These records form a household.

                    """),
                    agent=agent
        )