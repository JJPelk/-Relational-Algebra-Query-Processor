# utils.py
import re

def parse_relation(text):
    match = re.match(r"(\w+)\s*\(([\w\s,]+)\)\s*=\s*\{(.+)\}", text, re.DOTALL)
    if match:
        relation_name = match.group(1).strip()
        attributes = [attr.strip() for attr in match.group(2).split(',')]
        tuples = []

        for item in match.group(3).split('\n'):
            if item.strip():
                tuple_values = item.strip().split(', ')
                tuple_values = [int(val) if val.isdigit() else val for val in tuple_values]
                tuples.append(tuple(tuple_values))

        return relation_name, attributes, tuples
    return None

def parse_query(query):
    print(f"Debug: Received query - {query}")  # Print the received query

    # First, check for the format "select condition(relation_name)"
    # where condition can include comparison operators like <, >, =, <=, >=, !=
    select_match = re.match(r"select\s+([\w\s!<>=]+)\((\w+)\)", query)
    if select_match:
        operation = "select"
        params = select_match.group(1).strip()
        relation_name = select_match.group(2).strip()

        print(f"Debug: Parsed operation - {operation}")
        print(f"Debug: Parsed relation name - {relation_name}")
        print(f"Debug: Parsed params - {params}")

        return operation, relation_name, params

    # Then check for the format "operation(relation_name, params)"
    match = re.match(r"(\w+)\((\w+),\s*(.+)\)", query)
    if match:
        operation = match.group(1).strip()
        relation_name = match.group(2).strip()
        params = match.group(3).strip()

        print(f"Debug: Parsed operation - {operation}")
        print(f"Debug: Parsed relation name - {relation_name}")
        print(f"Debug: Parsed params - {params}")

        return operation, relation_name, params

    # Finally, check for the format "operation params(relation_name)"
    match = re.match(r"(\w+)\s+(.+)\((\w+)\)", query)
    if match:
        operation = match.group(1).strip()
        params = match.group(2).strip()
        relation_name = match.group(3).strip()

        print(f"Debug: Parsed operation - {operation}")
        print(f"Debug: Parsed relation name - {relation_name}")
        print(f"Debug: Parsed params - {params}")

        return operation, relation_name, params

    # Print a message if the query does not match the expected format
    print("Debug: Query does not match expected format.")
    return None, None, None