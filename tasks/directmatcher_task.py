from crewai import Task
from textwrap import dedent

class DirectMatcherTasks:
    def direct_matcher_task(self,agent):
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