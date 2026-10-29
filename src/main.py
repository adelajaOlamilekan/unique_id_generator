from constants import DEFAULT_GENERATE_OPTIONS as OPTIONS
import re


def read_generation_metadata(file_path=None):
    """
    Read the generation metadata from a file and return the start, count, and generated IDs.

    Args:
        file_path (str): The path to the metadata file.
    
    Returns:
        tuple: A tuple containing the start value, count, and the last generated ID found otherwise returns None if the file does not exist or is empty.

    """
    if file_path is None:
        file_path = OPTIONS.get("file", "generation_metadata.txt")

    if not isinstance(file_path, str):
        raise ValueError("File must be a string")
    
    try:
        values = {}
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            for line in content.splitlines():
                match = re.search(OPTIONS.get("regex_pattern"), line) 
                # print(f"line: {line}, match: {match}")       
                if match:
                    label = match.group(1).strip().lower()
                    values[label] = match.group(2).strip()

        # print(f"Read metadata from {file_path}: {values}")
        start = int(values.get("start", OPTIONS.get("start", 0)))
        count = int(values.get("count", OPTIONS.get("count", 1)))
        last_generated_id = int(values.get("last_id", "").split(", ")[-1]) if values.get("last_id", "") else None

        # print(f"Read metadata from {file_path}: start={start}, count={count}, last_generated_id={last_generated_id}")
        return start, count, last_generated_id
    except FileNotFoundError:
        return None
            

def write_generation_metadata(start=None, count=None, last_generated_id=None, file_path=None):
    """
    Write the generation metadata to a file.

    Args:
        file_path (str): The path to the metadata file.
        start (int): The starting value of the ID sequence.
        count (int): The number of IDs generated.
        last_generated_id (int): The last generated ID.

    """
    if start is None or count is None or last_generated_id is None:
        raise ValueError("Start, count, and last_generated_id must be provided")

    if file_path is None:
        file_path = OPTIONS.get("file", "generation_metadata.txt")

    if not isinstance(file_path, str) or not isinstance(start, int) or not isinstance(count, int) or not isinstance(last_generated_id, int):
        raise ValueError("File must be a string, start and count must be integers, and last_generated_id must be an integer")

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(f"Start: {start}\n")
        file.write(f"Count: {count}\n")
        file.write(f"Last_ID: {last_generated_id}\n")

def generate_id(start=OPTIONS.get("start", 1), count=OPTIONS.get("count", 1), last_generated_id=None):
    """
    Generate a unique ID starting from a given start value.

    Args:
        start (int, optional):  The starting value of the ID sequence. Defaults to 1.
        count (int, optional):  The number of IDs to be generated. If None, the genrator will produce just one ID and stop.
    
    Yields:
        int: A unique ID in the sequence.
    
    """

    #Validate input parameters
    if not isinstance(start, int) or not isinstance(count, int):
        raise ValueError("Start, count must be integers and file must be a string")
    
    if last_generated_id is None:
        last_generated_id = start - 1

    # print(f"last_generated_id: {last_generated_id}")

    next_id = last_generated_id + 1
    current_id = next_id

    # print(f"Generating {count} unique IDs starting from {next_id}...")
    while current_id < next_id + count:
        yield current_id
        current_id += 1

def main():
    file = OPTIONS.get("file", "generation_metadata.txt")
    start, count, last_generated_id = read_generation_metadata(file_path=file) or (OPTIONS.get("start", 0), OPTIONS.get("count", 1), None)        

    generator = generate_id(start=start, count=6, last_generated_id=last_generated_id)
    output_ids = list(generator)
    write_generation_metadata(start=start, count=count, last_generated_id=output_ids[-1] if output_ids else None, file_path=file)

    return output_ids


gen1 = main()
gen2 = main()

print(f"First generation: {gen1}")
print(f"Second generation: {gen2}")