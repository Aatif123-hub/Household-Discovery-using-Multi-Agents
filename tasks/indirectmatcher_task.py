from crewai import Task
from textwrap import dedent
from agents.indirect_matcher import IndirectMatchAgent

class IndirectMatcherTasks:
    try:
     def indirect_matcher_task():
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
                    agent=IndirectMatchAgent
        )
    except Exception as e:
       raise Exception(f"Cannot execute Indirect Matcher Task. Error:{e}")