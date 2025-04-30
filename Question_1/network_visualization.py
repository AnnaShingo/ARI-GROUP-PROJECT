"""
Network Visualization - Frontend interface for visualizing the scientist network
and finding shortest paths between scientists.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
from scientists_network import shortest_path
from data_access import get_all_scientists, get_path_info, get_scientist_name, get_paper_title, load_data, get_name_to_id

class ScientistNetworkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Scientists Network")
        self.root.geometry("800x600")
        
        # Main menu
        menubar = tk.Menu(root)
        root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Load Data...", command=self.load_data_dialog)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.quit)
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Status label for data loading
        self.data_status_var = tk.StringVar(value="No data loaded. Please load data from CSV files.")
        data_status_label = ttk.Label(main_frame, textvariable=self.data_status_var, font=("Arial", 10))
        data_status_label.pack(fill=tk.X, pady=5)
        
        # Load data button
        load_button = ttk.Button(main_frame, text="Load Data", command=self.load_data_dialog)
        load_button.pack(pady=5)
        
        # Create source and target selection frame
        self.selection_frame = ttk.LabelFrame(main_frame, text="Find Shortest Path", padding="10")
        self.selection_frame.pack(fill=tk.X, pady=10)
        self.selection_frame.pack_forget()  # Hide until data is loaded
        
        # Source scientist selection
        ttk.Label(self.selection_frame, text="Source Scientist:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.source_var = tk.StringVar()
        self.source_combo = ttk.Combobox(self.selection_frame, textvariable=self.source_var, width=30)
        self.source_combo.grid(row=0, column=1, padx=5, pady=5)
        
        # Target scientist selection
        ttk.Label(self.selection_frame, text="Target Scientist:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.target_var = tk.StringVar()
        self.target_combo = ttk.Combobox(self.selection_frame, textvariable=self.target_var, width=30)
        self.target_combo.grid(row=1, column=1, padx=5, pady=5)
        
        # Find path button
        find_button = ttk.Button(self.selection_frame, text="Find Path", command=self.find_path)
        find_button.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Results frame
        self.results_frame = ttk.LabelFrame(main_frame, text="Path Results", padding="10")
        self.results_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        self.results_frame.pack_forget()  # Hide until data is loaded
        
        # Results treeview
        columns = ("step", "from_scientist", "paper", "to_scientist")
        self.tree = ttk.Treeview(self.results_frame, columns=columns, show="headings")
        
        # Define headings
        self.tree.heading("step", text="Step")
        self.tree.heading("from_scientist", text="From Scientist")
        self.tree.heading("paper", text="Via Paper")
        self.tree.heading("to_scientist", text="To Scientist")
        
        # Define column widths
        self.tree.column("step", width=50, anchor=tk.CENTER)
        self.tree.column("from_scientist", width=150)
        self.tree.column("paper", width=300)
        self.tree.column("to_scientist", width=150)
        
        # Add treeview to frame with scrollbar
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(self.results_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Status label
        self.status_var = tk.StringVar()
        status_label = ttk.Label(main_frame, textvariable=self.status_var, font=("Arial", 10, "italic"))
        status_label.pack(fill=tk.X, pady=5)
        
        # Initialize scientists data
        self.scientists = {}
        self.name_to_id = {}
        
    def load_data_dialog(self):
        """Open dialog to select directory containing CSV files"""
        directory = filedialog.askdirectory(
            title="Select Directory with CSV Files",
            mustexist=True
        )
        
        if directory:
            self.load_data(directory)
    
    def load_data(self, directory):
        """Load data from CSV files in the specified directory"""
        try:
            # Check if the required files exist
            required_files = ["scientists.csv", "papers.csv", "authors.csv"]
            for file in required_files:
                if not os.path.isfile(os.path.join(directory, file)):
                    messagebox.showerror("Error", f"Missing required file: {file}")
                    return False
            
            # Load the data
            success = load_data(directory)
            
            if success:
                # Get updated scientists data
                self.scientists = get_all_scientists()
                self.name_to_id = get_name_to_id()
                
                # Update comboboxes with scientist names
                scientist_names = list(self.scientists.values())
                scientist_names.sort()  # Sort names alphabetically
                self.source_combo['values'] = scientist_names
                self.target_combo['values'] = scientist_names
                
                # Update status
                self.data_status_var.set(f"Loaded data from {directory}")
                
                # Show selection and results frames
                self.selection_frame.pack(fill=tk.X, pady=10, after=self.data_status_var.master)
                self.results_frame.pack(fill=tk.BOTH, expand=True, pady=10)
                
                # Clear any previous results
                for item in self.tree.get_children():
                    self.tree.delete(item)
                
                self.status_var.set(f"Loaded {len(self.scientists)} scientists")
                return True
            else:
                messagebox.showerror("Error", f"Failed to load data from {directory}")
                return False
        except Exception as e:
            messagebox.showerror("Error", f"Error loading data: {str(e)}")
            return False
            
    def find_path(self):
        """Find and display the shortest path between selected scientists"""
        source_name = self.source_var.get()
        target_name = self.target_var.get()
        
        # Clear previous results
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Validate selections
        if not source_name or not target_name:
            messagebox.showerror("Error", "Please select both source and target scientists")
            return
            
        # Find source and target IDs using the name-to-ID mapping
        source_id = None
        target_id = None
        
        for name, id in self.name_to_id.items():
            if name == source_name:
                source_id = id
            if name == target_name:
                target_id = id
        
        if not source_id or not target_id:
            messagebox.showerror("Error", "Could not find scientist IDs")
            return
            
        # Find shortest path
        path = shortest_path(source_id, target_id)
        
        if path is None:
            self.status_var.set(f"No path found between {source_name} and {target_name}")
            return
            
        if len(path) == 0:
            self.status_var.set(f"Source and target are the same scientist: {source_name}")
            return
            
        # Get detailed path information
        path_info = get_path_info(path)
        
        # Display path
        current_scientist = source_id
        current_scientist_name = source_name
        
        for i, step in enumerate(path_info):
            paper_title = step["paper_title"]