from crewai import Task
from textwrap import dedent

class ER_TASKS:
    def direct_matcher_task(agent):
        return Task(description=dedent(f"""\
                    Link records that directly match by name.

                    Identify records where the full names are the same or have minor spelling variations.
                    Consider abbreviations, nicknames, and common misspellings.
                    Account for case sensitivity and punctuation differences.  

                    Example:
                    Records A928147 and A972885 both have the name "FRANCINE J KEGLER" (with minor variations) and are thus a direct match.

                    """),
                    agent=agent
        )
    def indirect_matcher_task(agent):
        return Task(description=dedent(f"""\
                    Perform indirect matching of records connected through an intermediary.

                    Identify records where one record matches two others via different attributes (e.g., name and address).
                    Record A matches Record B by name.
                    Record A matches Record C by address.
                    Therefore, Records A, B, and C are indirectly linked.  

                    Example:

                    Record 1: "John Doe, 1701 Westpark Drive Apt 110"
                    Record 2: "J D, 1701 Westpark Drive Apt 110" (matches Record 1 by address)
                    Record 3: "John Doe, 1710 Westpark Drive Apt 41" (matches Record 1 by name)
                    Records 1, 2, and 3 are indirectly matched.

                    """),
                    agent=agent
        )
    def household_matcher_task(agent):
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
    def household_moves_task(agent):
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