from constants import DEFAULT_GENERATE_OPTIONS as OPTIONS
import re


def read_generation_metadata(file_path=None):
    """
    Read the generation metadata from a file and return the start, count, and generated IDs.

    Args:
        file_path (str): The path to the metadata file.
    
    Returns:
        tuple: A tuple containing the start value, count, and a list of generated IDs found otherwise returns None if the file does not exist or is empty.

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
                    values[label] = match.group(2).strip() if label != "generated_ids" else match.group(2).strip().strip("[]")

        # print(f"Read metadata from {file_path}: {values}")
        start = int(values.get("start", OPTIONS.get("start", 0)))
        count = int(values.get("count", OPTIONS.get("count", 1)))
        generated_ids = [int(id) for id in values.get("generated_ids", "").split(", ") if id]

        # print(f"Read metadata from {file_path}: start={start}, count={count}, generated_ids={generated_ids}")
        return start, count, generated_ids
    except FileNotFoundError:
        return None
            

def write_generation_metadata(start=None, count=None, generated_ids=None, file_path=None):
    """
    Write the generation metadata to a file.

    Args:
        file_path (str): The path to the metadata file.
        start (int): The starting value of the ID sequence.
        count (int): The number of IDs generated.
        generated_ids (list): A list of generated IDs.
    
    """
    if start is None or count is None or generated_ids is None:
        raise ValueError("Start, count, and generated_ids must be provided")

    if file_path is None:
        file_path = OPTIONS.get("file", "generation_metadata.txt")

    if not isinstance(file_path, str) or not isinstance(start, int) or not isinstance(count, int) or not isinstance(generated_ids, list):
        raise ValueError("File must be a string, start and count must be integers, and generated_ids must be a list")

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(f"Start: {start}\n")
        file.write(f"Count: {count}\n")
        file.write(f"Generated_IDs: [{', '.join(map(str, generated_ids))}]\n")

def generate_id(start=OPTIONS.get("start", 1), count=OPTIONS.get("count", 1), generated_ids=None):
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
    
    if generated_ids is None:
        generated_ids = []
    
    # print(f"generated_ids: {generated_ids}")

    last_id = generated_ids[-1] if generated_ids else start - 1
    next_id = last_id + 1
    current_id = next_id

    # print(f"Generating {count} unique IDs starting from {next_id}...")
    while current_id < next_id + count:
        yield current_id
        current_id += 1

def main():
    file = OPTIONS.get("file", "generation_metadata.txt")
    start, count, generated_ids = read_generation_metadata(file_path=file) or (OPTIONS.get("start", 0), OPTIONS.get("count", 1), [])        

    generator = generate_id(start=start, count=6, generated_ids=generated_ids)
    output_ids = generated_ids + list(generator)
    write_generation_metadata(start=start, count=count, generated_ids=output_ids, file_path=file)

    return output_ids


gen1 = main()
gen2 = main()

print(f"First generation: {gen1}")
print(f"Second generation: {gen2}")