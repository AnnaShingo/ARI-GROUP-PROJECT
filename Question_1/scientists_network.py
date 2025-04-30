"""
Scientists Network Module - Handles the graph operations and shortest path algorithms
"""

from collections import deque
from data_access import get_scientist_name, get_collaborators


def shortest_path(source_id, target_id):
    """
    Find the shortest path between two scientists
    
    Args:
        source_id (str): ID of the source scientist
        target_id (str): ID of the target scientist
    
    Returns:
        list or None: List of scientist IDs representing the path,
                      or None if no path exists
    """
    # Edge case: Same scientist
    if source_id == target_id:
        return [source_id]
    
    # Get collaborators of source and target for debugging
    source_collaborators = get_collaborators(source_id)
    target_collaborators = get_collaborators(target_id)
    
    # Check if either scientist has no collaborators
    if not source_collaborators:
        print(f"Warning: Source scientist has no collaborators in dataset")
    if not target_collaborators:
        print(f"Warning: Target scientist has no collaborators in dataset")
    
    # Direct connection check (optimization)
    if target_id in source_collaborators:
        return [source_id, target_id]
    
    # Use BFS to find shortest path
    visited = set([source_id])
    queue = deque([(source_id, [source_id])])
    
    visited_count = 1  # Counter for debugging
    
    while queue:
        current_id, path = queue.popleft()
        
        # Get all collaborators of the current scientist
        for collaborator_id in get_collaborators(current_id):
            if collaborator_id == target_id:
                # Found the target
                return path + [collaborator_id]
            
            if collaborator_id not in visited:
                visited.add(collaborator_id)
                visited_count += 1
                queue.append((collaborator_id, path + [collaborator_id]))
    
    # No path found - include debugging information
    print(f"Debug: Searched through {visited_count} scientists but found no path")
    return None


def print_path(path):
    """
    Print the path between scientists in a readable format
    
    Args:
        path (list): List of scientist IDs representing the path
    """
    if not path or len(path) == 0:
        print("Empty path provided.")
        return
    
    print("\nConnection Path:")
    print("-" * 40)
    
    for i, scientist_id in enumerate(path):
        name = get_scientist_name(scientist_id)
        print(f"{i+1}. {name}")
        
        # Print arrow between scientists
        if i < len(path) - 1:
            print("   ↓")
    
    print("-" * 40)
    if len(path) == 2:
        print(f"Direct collaboration between {get_scientist_name(path[0])} and {get_scientist_name(path[-1])}")
    else:
        print(f"Total: {len(path) - 1} degrees of separation")