from crewai import Task
from textwrap import dedent
from agents.householdmoves_matcher import HouseholdMovesAgent

class HouseholdMovesTasks:
    try:
     def household_moves_task():
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
                    agent=HouseholdMovesAgent
        )
    except Exception as e:
       raise Exception(f"Cannot execute Household Moves Task. Eroor:{e}")
