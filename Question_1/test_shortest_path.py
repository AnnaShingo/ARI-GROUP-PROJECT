from collections import deque

def shortest_path(source, target):
    if source == target:
        return []
    
    queue = deque([(source, [])])
    explored = {source}

    while queue:
        current_scientist, path = queue.popleft()
        
        # Get neighbors sorted by paper ID for deterministic behavior in tests
        neighbors = sorted(neighbors_for_person(current_scientist), key=lambda x: x[0])
        
        for paper_id, neighbor_id in neighbors:
            if neighbor_id == target:
                return path + [(paper_id, neighbor_id)]
            
            if neighbor_id not in explored:
                explored.add(neighbor_id)
                queue.append((neighbor_id, path + [(paper_id, neighbor_id)]))
    
    return None
