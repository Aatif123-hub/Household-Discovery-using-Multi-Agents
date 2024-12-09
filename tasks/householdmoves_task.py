from crewai import Task
from textwrap import dedent

class HouseholdMovesTasks:
    def household_moves_task(self,agent):
        return Task(description=dedent(f"""\
                    Find instances where a household has moved to a new address.
                    
                    Identify groups of records where the same individuals (by name) are associated with more than one address.
                    Ensure that the names match despite minor variations.
                    Account for address changes indicating a move.
                                       
                    Example:

                    Old Address:
                    "John Doe, 1701 Westpark Drive Apt 110"
                    "Mary Doe, 1701 Westpark Drive Apt 110"
                    
                    New Address:
                    "John Doe, 1710 Westpark Drive Apt 321"
                    "Mary Doe, 1710 Westpark Drive Apt 321"
                    
                    All four records together represent a household move.             

                    """),
                    agent=agent
        )