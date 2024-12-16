from crewai import Task
from textwrap import dedent
from agents.direct_matcher import DirectMatchAgent

class DirectMatcherTasks:
    try:
     def direct_matcher_task():
        return Task(description=dedent(f"""\
                    Link records that directly match by name.

                    Identify records where the full names are the same or have minor spelling variations.
                    Consider abbreviations, nicknames, and common misspellings.
                    Account for case sensitivity and punctuation differences.  

                    Example:
                    Records A928147 and A972885 both have the name "FRANCINE J KEGLER" (with minor variations) and are thus a direct match.

                    """),
                    agent=DirectMatchAgent
        )
    except Exception as e:
       raise Exception(f"Cannnot execute Direct Matcher Task. Error:{e}") 