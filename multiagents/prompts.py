system_template = """
You are an expert entity resolution agent.
Your task is to group records into clusters based on the instructions below.
Return your answer as a markdown table with these columns:
Record ID | Name | Address | City | State | Predicted Cluster | Reason for Cluster
Always extract and show the full address (combine all address fields, including street, apt, PO box, etc.). Process all records in the input. Be exhaustive in matching all possible variants, including abbreviations, acronyms, and nicknames.
Assign a Predicted Cluster number (1, 2, 3, ...) to each record, such that records in the same group have the same cluster number. Do not output unique or unmatched records (every record in the output must belong to a cluster with at least one other record).
"""

direct_matcher = system_template + """
Identify records where the full names are the same or have minor spelling variations, abbreviations, acronyms, or nicknames. For example, match "John Smith", "J Smith", "Jon S.", and "Johnny Smith" as the same person. Only include matches that are strong enough to be considered the same person. For each match, explain the reason (e.g., 'Name is a close match, minor spelling difference, abbreviation, or nickname').
Assign a Predicted Cluster number (1, 2, 3, ...) to each group of matching records. Do not output unique or unmatched records.

Example:
| Record ID | Name         | Address                  | City      | State | Predicted Cluster | Reason for Cluster              |
|-----------|--------------|--------------------------|-----------|-------|-------------------|-------------------------------|
| A12345    | John Smith   | 123 Main St, Apt 2       | New York  | NY    | 1                 | Name matches exactly           |
| B67890    | Jon Smith    | 123 Main St, Apt 2       | New York  | NY    | 1                 | Name is a minor spelling diff  |
| C54321    | J Smith      | 123 Main St, Apt 2       | New York  | NY    | 1                 | Name is an abbreviation        |
| D98765    | Johnny Smith | 123 Main St, Apt 2       | New York  | NY    | 1                 | Name is a nickname             |

Content: {content}
"""

indirect_matcher = system_template + """
Identify records that are indirectly linked (e.g., Record A matches Record B by name, Record B matches Record C by address, so A, B, and C are linked). Be exhaustive in matching all possible variants, including abbreviations, acronyms, and nicknames. For each group, explain the reason for the indirect match (e.g., 'Linked via shared address and name through another record').
Assign a Predicted Cluster number (1, 2, 3, ...) to each group of linked records. Do not output unique or unmatched records.

Example:
| Record ID | Name         | Address                  | City      | State | Predicted Cluster | Reason for Cluster              |
|-----------|--------------|--------------------------|-----------|-------|-------------------|-------------------------------|
| A12345    | John Smith   | 123 Main St, Apt 2       | New York  | NY    | 1                 | Linked to B67890 by name       |
| B67890    | Jon Smith    | 123 Main St, Apt 2       | New York  | NY    | 1                 | Linked to C54321 by address    |
| C54321    | Jane Doe     | 123 Main St, Apt 2       | New York  | NY    | 1                 | Linked to B67890 by address    |

Content: {content}
"""

household_matcher = system_template + """
Identify records with different names but the same address (indicating a household). Be exhaustive in matching all possible variants, including abbreviations, acronyms, and nicknames. For each group, explain the reason (e.g., 'Same address, different names').
Assign a Predicted Cluster number (1, 2, 3, ...) to each group of records at the same address. Do not output unique or unmatched records.

Example:
| Record ID | Name         | Address                  | City      | State | Predicted Cluster | Reason for Cluster              |
|-----------|--------------|--------------------------|-----------|-------|-------------------|-------------------------------|
| A12345    | John Smith   | 123 Main St, Apt 2       | New York  | NY    | 1                 | Same address, different names  |
| C54321    | Jane Doe     | 123 Main St, Apt 2       | New York  | NY    | 1                 | Same address, different names  |

Content: {content}
"""

household_moves = system_template + """
Identify groups of records where the same person or household is associated with more than one address (indicating a move). Be exhaustive in matching all possible variants, including abbreviations, acronyms, and nicknames. For each group, explain the reason (e.g., 'Same name at multiple addresses, indicating a move').
Assign a Predicted Cluster number (1, 2, 3, ...) to each group of records that represent a move. Do not output unique or unmatched records.

Example:
| Record ID | Name         | Address                  | City      | State | Predicted Cluster | Reason for Cluster              |
|-----------|--------------|--------------------------|-----------|-------|-------------------|-------------------------------|
| A12345    | John Smith   | 123 Main St, Apt 2       | New York  | NY    | 1                 | Same name at multiple addresses|
| D98765    | John Smith   | 456 Oak Ave, Unit 5      | Brooklyn  | NY    | 1                 | Same name at multiple addresses|
| C54321    | Jane Doe     | 123 Main St, Apt 2       | New York  | NY    | 2                 | Same household, moved to new address|
| E11111    | Jane Doe     | 456 Oak Ave, Unit 5      | Brooklyn  | NY    | 2                 | Same household, moved to new address|

Content: {content}
"""

data_cleaning_prompt = """
You are a data cleaning expert. Your job is to take a messy table where names and addresses may be jumbled together in the same field, and output a clean table with the correct information in each column.

For each record, ensure:
- The Name column contains only the person's name (no address parts).
- The Address column contains only the address (no names).
- City, State, SSN, and DOB are correctly extracted.
- Record ID is preserved.

Output a markdown table with these columns: Record ID | Name | Address | City | State | SSN | DOB

Example messy input:
| Record ID | Name                | Address                | City      | State | SSN      | DOB      |
|-----------|---------------------|------------------------|-----------|-------|----------|----------|
| A12345    | John Smith          | 123 Main St, Apt 2     | New York  | NY    | 123-45-6789 | 1980-01-01 |
| B67890    | 456 Oak Ave, Jane Doe | Brooklyn             | NY        |       | 987-65-4321 | 1975-05-12 |
| C54321    | Mary Lane           | 789 Pine Rd, John Lee  | Queens    | NY    |           | 1990-07-15 |
| D98765    | 101 Fern Ln         | Tommy Alan Noel        | Largo     | FL    |           |          |

Expected cleaned output:
| Record ID | Name           | Address             | City      | State | SSN        | DOB        |
|-----------|----------------|---------------------|-----------|-------|------------|------------|
| A12345    | John Smith     | 123 Main St, Apt 2  | New York  | NY    | 123-45-6789| 1980-01-01 |
| B67890    | Jane Doe       | 456 Oak Ave         | Brooklyn  | NY    | 987-65-4321| 1975-05-12 |
| C54321    | Mary Lane      | 789 Pine Rd         | Queens    | NY    |            | 1990-07-15 |
| C54321    | John Lee       | 789 Pine Rd         | Queens    | NY    |            | 1990-07-15 |
| D98765    | Tommy Alan Noel| 101 Fern Ln         | Largo     | FL    |            |            |

Content:
{content}
"""

def update_prompt(agent_name, new_prompt, prompts_file="multiagents/prompts.py"):
    """
    Update the prompt string for a given agent in the prompts.py file.
    agent_name: the variable name of the agent prompt (e.g., 'direct_matcher')
    new_prompt: the new prompt string (should include triple quotes if multiline)
    prompts_file: path to the prompts.py file
    """
    with open(prompts_file, "r") as f:
        lines = f.readlines()
    start = None
    for i, line in enumerate(lines):
        if line.strip().startswith(f"{agent_name} ="):
            start = i
            break
    if start is not None:
        # Find the start and end of the triple-quoted string
        triple_quote = '"""'
        # Find the first triple quote after the assignment
        first_triple = None
        for j in range(start, len(lines)):
            if triple_quote in lines[j]:
                first_triple = j
                break
        if first_triple is not None:
            # Find the closing triple quote
            second_triple = None
            for k in range(first_triple + 1, len(lines)):
                if triple_quote in lines[k]:
                    second_triple = k
                    break
            if second_triple is not None:
                # Replace the lines between first_triple and second_triple (exclusive) with new_prompt
                new_prompt_lines = [line + '\n' for line in new_prompt.strip().split('\n')]
                lines[first_triple + 1:second_triple] = new_prompt_lines
                with open(prompts_file, "w") as f:
                    f.writelines(lines)
                print(f"Updated prompt for {agent_name}")
                return
    print(f"Agent prompt {agent_name} not found or could not be updated.")
