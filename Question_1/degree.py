import csv
import sys
from collections import deque

# Maps names to a set of corresponding scientist_ids
name_to_ids = {}

# Maps each scientist_id to another dictionary with values for the scientist's
# name and the set of all the papers they authored
scientist_data = {}

# Maps each paper_id to another dictionary with values for that paper's
# title, year of publication, and the set of all the paper's authors
paper_data = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load scientists
    with open(f"{directory}/scientists.csv", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            scientist_id = row["scientist_id"]
            name = row["name"]
            
            # Map each name to a set of corresponding scientist_ids
            if name not in name_to_ids:
                name_to_ids[name] = {scientist_id}
            else:
                name_to_ids[name].add(scientist_id)
                
            # Map scientist_id to name and initialize set of papers
            scientist_data[scientist_id] = {
                "name": name,
                "papers": set()
            }
    
    # Load papers
    with open(f"{directory}/papers.csv", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            paper_id = row["paper_id"]
            
            # Map papers to data and initialize set of authors
            paper_data[paper_id] = {
                "title": row["title"],
                "year": row["year"],
                "authors": set()
            }
    
    # Load author relationships
    with open(f"{directory}/authors.csv", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            scientist_id = row["scientist_id"]
            paper_id = row["paper_id"]
            
            # Add paper to scientist's papers set
            if scientist_id in scientist_data:
                scientist_data[scientist_id]["papers"].add(paper_id)
            
            # Add scientist to paper's authors set
            if paper_id in paper_data:
                paper_data[paper_id]["authors"].add(scientist_id)


def get_scientist_id(name):
    """
    Returns the ID for the scientist with the given name.
    If multiple scientists have this name, returns one of their IDs.
    """
    scientist_ids = name_to_ids.get(name)
    if scientist_ids:
        return next(iter(scientist_ids))
    return None


def neighbors_for_person(scientist_id):
    """
    Returns (paper_id, scientist_id) pairs for all scientists 
    who co-authored a paper with the given scientist.
    """
    neighbors = set()
    
    # For each paper authored by the scientist
    for paper_id in scientist_data[scientist_id]["papers"]:
        # For each author of that paper (excluding the scientist themselves)
        for author_id in paper_data[paper_id]["authors"]:
            if author_id != scientist_id:
                neighbors.add((paper_id, author_id))
    
    return neighbors


def shortest_path(source, target):
    """
    Returns the shortest list of (paper_id, scientist_id) pairs
    that connect the source to the target.
    
    If no path is found, returns None.
    """
    # Return immediately if source and target are the same
    if source == target:
        return []
    
    # Initialize a queue for BFS
    queue = deque([(source, [])])
    
    # Keep track of explored scientists
    explored = {source}
    
    # BFS
    while queue:
        # Get the next scientist and path to reach them
        current_scientist, path = queue.popleft()
        
        # Get all neighbors (co-authors)
        for paper_id, neighbor_id in neighbors_for_person(current_scientist):
            # Check if we've reached the target
            if neighbor_id == target:
                # Return the path including this last step
                return path + [(paper_id, neighbor_id)]
            
            # If neighbor hasn't been explored, add to queue
            if neighbor_id not in explored:
                explored.add(neighbor_id)
                queue.append((neighbor_id, path + [(paper_id, neighbor_id)]))
    
    # No path found
    return None


def print_path(path):
    """
    Prints the path from source to target in the required format.
    """
    if not path:
        print("No connection found.")
        return
    
    print(f"{len(path)} degrees of separation.")
    
    for i, (paper_id, scientist_id) in enumerate(path, 1):
        # Get the paper information
        paper = paper_data[paper_id]
        # Get the current scientist
        current_scientist = scientist_data[scientist_id]["name"]
        
        # For the first connection, we need to get the previous scientist
        # from our search which isn't stored in the path
        if i == 1:
            # Find a scientist who co-authored this paper but isn't our target
            co_author = None
            for author_id in paper["authors"]:
                if author_id != scientist_id:
                    co_author = scientist_data[author_id]["name"]
                    break
                    
            print(f"{i}: {co_author} and {current_scientist} co-authored \"{paper['title']}\"")
        else:
            # Get the previous scientist from the previous path item
            previous_scientist_id = path[i-2][1]
            previous_scientist = scientist_data[previous_scientist_id]["name"]
            
            print(f"{i}: {previous_scientist} and {current_scientist} co-authored \"{paper['title']}\"")


def main():
    if len(sys.argv) != 3:
        sys.exit("Usage: python degrees.py directory")
    
    directory = sys.argv[1] if len(sys.argv) > 1 else "."
    
    # Load data from files
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")
    
    # Get source scientist name
    source_name = input("Name: ")
    source_id = get_scientist_id(source_name)
    if source_id is None:
        sys.exit(f"Scientist '{source_name}' not found.")
        
    # Get target scientist name
    target_name = input("Name: ")
    target_id = get_scientist_id(target_name)
    if target_id is None:
        sys.exit(f"Scientist '{target_name}' not found.")
        
    # Find shortest path
    path = shortest_path(source_id, target_id)
    
    # Print the path
    print_path(path)


if __name__ == "__main__":
    main()