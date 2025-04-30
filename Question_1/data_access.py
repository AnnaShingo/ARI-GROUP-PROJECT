"""
Data Access Module - Handles loading and accessing scientist and collaboration data
from papers and authors CSV files
"""

import os
import csv
from collections import defaultdict

# Global data structures
scientists = {}  # id -> name
scientist_ids = {}  # name -> id (lowercased for case-insensitive lookup)
papers = {}  # paper_id -> title
paper_authors = defaultdict(list)  # paper_id -> list of scientist_ids
collaborations = {}  # scientist_id -> set of collaborator_ids


def load_data(data_dir):
    """
    Load scientists and derive collaborations data from CSV files
    
    Args:
        data_dir (str): Path to directory containing CSV files
    
    Returns:
        tuple: (success, message) where success is a boolean indicating if loading was successful
               and message is a string with details
    """
    global scientists, scientist_ids, papers, paper_authors, collaborations
    
    # Reset data structures
    scientists = {}
    scientist_ids = {}
    papers = {}
    paper_authors = defaultdict(list)
    collaborations = {}
    
    # Check if directory exists
    if not os.path.isdir(data_dir):
        return False, f"Directory '{data_dir}' does not exist"
    
    # Load scientists data
    scientists_file = os.path.join(data_dir, "scientists.csv")
    if not os.path.isfile(scientists_file):
        return False, f"Scientists file not found at '{scientists_file}'"
    
    try:
        with open(scientists_file, 'r', encoding='utf-8', errors='replace') as f:
            reader = csv.reader(f)
            header = next(reader, None)  # Skip header row
            
            # Check for both possible header formats: 'id' or 'scientist_id'
            if not header:
                return False, f"Empty header in scientists file"
            
            # Determine column indices based on available headers
            id_idx = -1
            name_idx = -1
            
            if 'id' in header:
                id_idx = header.index('id')
            elif 'scientist_id' in header:
                id_idx = header.index('scientist_id')
            
            if 'name' in header:
                name_idx = header.index('name')
            
            if id_idx == -1 or name_idx == -1:
                return False, f"Invalid header in scientists file: {header}. Need 'id' or 'scientist_id' and 'name' columns."
            
            for row in reader:
                if len(row) <= max(id_idx, name_idx):
                    continue  # Skip incomplete rows
                
                scientist_id = row[id_idx].strip()
                name = row[name_idx].strip()
                
                if scientist_id and name:
                    scientists[scientist_id] = name
                    scientist_ids[name.lower()] = scientist_id
    except Exception as e:
        return False, f"Error reading scientists file: {str(e)}"
    
    if not scientists:
        return False, "No scientists loaded. Check file format."
    
    # Load papers data
    papers_file = os.path.join(data_dir, "papers.csv")
    if not os.path.isfile(papers_file):
        return False, f"Papers file not found at '{papers_file}'"
    
    try:
        with open(papers_file, 'r', encoding='utf-8', errors='replace') as f:
            reader = csv.reader(f)
            header = next(reader, None)  # Skip header row
            
            paper_id_idx = -1
            title_idx = -1
            
            if 'paper_id' in header:
                paper_id_idx = header.index('paper_id')
            elif 'id' in header:
                paper_id_idx = header.index('id')
                
            if 'title' in header:
                title_idx = header.index('title')
            
            if paper_id_idx == -1:
                return False, f"Invalid header in papers file: {header}. Need 'paper_id' or 'id' column."
            
            for row in reader:
                if len(row) <= paper_id_idx:
                    continue
                
                paper_id = row[paper_id_idx].strip()
                title = row[title_idx].strip() if title_idx >= 0 and len(row) > title_idx else "Unknown Title"
                
                if paper_id:
                    papers[paper_id] = title
    except Exception as e:
        return False, f"Error reading papers file: {str(e)}"
    
    # Load author relationships
    authors_file = os.path.join(data_dir, "authors.csv")
    if not os.path.isfile(authors_file):
        return False, f"Authors file not found at '{authors_file}'"
    
    try:
        with open(authors_file, 'r', encoding='utf-8', errors='replace') as f:
            reader = csv.reader(f)
            header = next(reader, None)  # Skip header row
            
            scientist_id_idx = -1
            paper_id_idx = -1
            
            if 'scientist_id' in header:
                scientist_id_idx = header.index('scientist_id')
            
            if 'paper_id' in header:
                paper_id_idx = header.index('paper_id')
            
            if scientist_id_idx == -1 or paper_id_idx == -1:
                return False, f"Invalid header in authors file: {header}. Need 'scientist_id' and 'paper_id' columns."
            
            for row in reader:
                if len(row) <= max(scientist_id_idx, paper_id_idx):
                    continue
                
                scientist_id = row[scientist_id_idx].strip()
                paper_id = row[paper_id_idx].strip()
                
                if scientist_id in scientists and paper_id in papers:
                    paper_authors[paper_id].append(scientist_id)
    except Exception as e:
        return False, f"Error reading authors file: {str(e)}"
    
    # Build the collaboration network
    for paper_id, authors_list in paper_authors.items():
        if len(authors_list) < 2:
            continue  # Skip papers with only one author
        
        # For each pair of scientists who co-authored this paper
        for i in range(len(authors_list)):
            for j in range(i+1, len(authors_list)):
                sci1_id = authors_list[i]
                sci2_id = authors_list[j]
                
                # Add bidirectional collaborations
                if sci1_id not in collaborations:
                    collaborations[sci1_id] = set()
                if sci2_id not in collaborations:
                    collaborations[sci2_id] = set()
                
                collaborations[sci1_id].add(sci2_id)
                collaborations[sci2_id].add(sci1_id)
    
    return True, f"Successfully loaded {len(scientists)} scientists and derived collaborations"


def get_scientist_id(name):
    """Get scientist ID from name"""
    return scientist_ids.get(name.lower())


def get_scientist_name(scientist_id):
    """Get scientist name from ID"""
    return scientists.get(scientist_id)


def search_scientists(partial_name):
    """Search scientists by partial name"""
    partial_name = partial_name.lower()
    matches = []
    
    for name, sci_id in scientist_ids.items():
        if partial_name in name:
            matches.append((sci_id, scientists[sci_id]))
    
    return matches


def get_collaborators(scientist_id):
    """Get all collaborators of a scientist"""
    return collaborations.get(scientist_id, set())