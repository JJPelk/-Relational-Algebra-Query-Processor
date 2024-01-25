import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from relation import Relation
from utils import parse_relation, parse_query

# Initialize CustomTkinter
ctk.set_appearance_mode("Dark")  
ctk.set_default_color_theme("dark-blue")  

# Function to execute relational algebra operations
def execute_query(relations, relation, operation, params):
    if operation == "select":
        return relation.select(params)
    elif operation == "project":
        return relation.project(params.split(", "))
    elif operation == "join":
        other_relation_name = params
        if other_relation_name in relations:
            return relation.join(relations[other_relation_name])
    elif operation == "union":
        if params in relations:
            return relation.union(relations[params])
    elif operation == "set_difference":
        if params in relations:
            return relation.set_difference(relations[params])
    elif operation == "intersection":
        if params in relations:
            return relation.intersection(relations[params])
    else:
        print(f"Debug: Available relations - {relations.keys()}")
        return "Operation not supported."

#Dynamic Table for user friendly relational tuple insertion/creation
class DynamicTable(ctk.CTkFrame):
    def __init__(self, parent=None, initial_rows=3, initial_columns=3):
        super().__init__(parent)
        self.header_row = []
        self.data_rows = []  # This will store row frames and their entries
        self.initial_rows = initial_rows
        self.initial_columns = initial_columns
        self.init_ui()

    def init_ui(self):
        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.pack(side=tk.TOP, fill=tk.X)
        self.data_frame = ctk.CTkFrame(self)
        self.data_frame.pack(side=tk.TOP, fill=tk.X)

        # Initialize with initial_columns columns
        for _ in range(self.initial_columns):
            self.addColumn()

        # Initialize with initial_rows rows
        for _ in range(self.initial_rows):
            self.addRow()
    def addRow(self):
        row_frame = ctk.CTkFrame(self.data_frame)
        row_frame.pack(side=tk.TOP, fill=tk.X)
        row = {'frame': row_frame, 'entries': []}
        for _ in self.header_row:
            entry = ctk.CTkEntry(row_frame, width=200, height=25)
            entry.pack(side=tk.LEFT, padx=1, pady=1)
            row['entries'].append(entry)
        self.data_rows.append(row)

    def addColumn(self):
        header_entry = ctk.CTkEntry(self.header_frame, width=200, height=25, fg_color="#343638", placeholder_text="Attribute")
        header_entry.pack(side=tk.LEFT, padx=1, pady=1)
        self.header_row.append(header_entry)

        for row in self.data_rows:
            entry = ctk.CTkEntry(row['frame'], width=200, height=25)
            entry.pack(side=tk.LEFT, padx=1, pady=1)
            row['entries'].append(entry)

    def removeColumn(self):
        if self.header_row:
            self.header_row[-1].destroy()
            self.header_row.pop()
            for row in self.data_rows:
                row['entries'][-1].destroy()
                row['entries'].pop()

    def removeRow(self):
        if self.data_rows:
            for widget in self.data_rows[-1]['entries']:
                widget.destroy()
            self.data_rows[-1]['frame'].destroy()
            self.data_rows.pop()

    def submit(self):
        # Collect headers
        headers = [entry.get() for entry in self.header_row]
        # Collect data, ensuring no trailing commas
        data = [[entry.get().strip() for entry in row['entries']] for row in self.data_rows]
        return headers, data

#Submit relation/query
def submit_relation():
    relation_name = relation_name_entry.get().strip()
    headers, data = table.submit()

    if relation_name and headers and all(headers) and all(all(row) for row in data):
        formatted_relation = f"{relation_name} ({', '.join(headers)}) = {{\n"
        formatted_relation += '\n'.join([', '.join(row) for row in data]) + "\n}"
        print(formatted_relation)  # For debugging, remove later
        relation_info = parse_relation(formatted_relation)

        if relation_info:
            relation_name, attributes, tuples = relation_info
            relations[relation_name] = Relation(relation_name, attributes, tuples)
            relation_result_textbox.configure(state=tk.NORMAL)
            relation_result_textbox.insert(tk.END, f"Relation '{relation_name}' added.\n\n")
            relation_result_textbox.configure(state=tk.DISABLED)
            relation_name_entry.delete(0, tk.END)
            print(f"Debug: Added relation - {relation_name}")
            print(f"Debug: Relations dictionary - {relations.keys()}")
        else:
            messagebox.showerror("Error", "Invalid relation format.")
    else:
        messagebox.showerror("Error", "Please enter a relation name, headers, and data.")

def submit_query():
    query_text = query_entry.get()
    if query_text:
        operation, relation_name, params = parse_query(query_text)
        if operation and relation_name in relations:
            result = execute_query(relations, relations[relation_name], operation, params)
            result_textbox.configure(state=tk.NORMAL)
            result_textbox.insert(tk.END, f"Query Result:\n{result}\n\n")
            result_textbox.configure(state=tk.DISABLED)
        else:
            messagebox.showerror("Error", "Invalid operation or relation not found.")
        query_entry.delete(0, tk.END)

# Initialize CustomTkinter
ctk.set_appearance_mode("Dark")  # Other options: "Light", "System"
ctk.set_default_color_theme("dark-blue")  # Other options: "blue", "green", etc.

# Create a modern-looking tkinter application window
root = ctk.CTk()
root.title("Relational Algebra Processor")


relations = {}

# Relation name entry
relation_name_label = ctk.CTkLabel(root, text="Enter Relation Name:")
relation_name_label.pack(pady=(10, 0))

relation_name_entry = ctk.CTkEntry(root, width=400, placeholder_text="Relation Name")
relation_name_entry.pack(pady=(0, 10))

# Dynamic Table for Relations
table = DynamicTable(root)
table.pack(pady=(0, 10))

# Buttons for table manipulation
button_frame = ctk.CTkFrame(root)
button_frame.pack(pady=(0, 10))

add_row_button = ctk.CTkButton(button_frame, text="Add Row", command=table.addRow)
add_row_button.pack(side="left", padx=5)

add_column_button = ctk.CTkButton(button_frame, text="Add Column", command=table.addColumn)
add_column_button.pack(side="left", padx=5)

remove_row_button = ctk.CTkButton(button_frame, text="Remove Row", command=table.removeRow)
remove_row_button.pack(side="left", padx=5)

remove_column_button = ctk.CTkButton(button_frame, text="Remove Column", command=table.removeColumn)
remove_column_button.pack(side="left", padx=5)

submit_button = ctk.CTkButton(button_frame, text="Submit Relation", command=submit_relation)
submit_button.pack(side="left", padx=5)

# Custom scrollbar and text box for displaying relation results
relation_result_display = ctk.CTkFrame(root)
relation_result_display.pack(fill="x", pady=(0, 10))

relation_result_textbox = ctk.CTkTextbox(relation_result_display)
relation_result_textbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

relation_result_scrollbar = ctk.CTkScrollbar(relation_result_display, command=relation_result_textbox.yview)
relation_result_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

relation_result_textbox.configure(yscrollcommand=relation_result_scrollbar.set)

# Query input section should be packed after the relation result display
query_label = ctk.CTkLabel(root, text="Enter Query:")
query_label.pack()

query_entry = ctk.CTkEntry(root, width=400, placeholder_text="Query")
query_entry.pack(pady=(0, 10))

submit_query_button = ctk.CTkButton(root, text="Submit Query", command=submit_query)
submit_query_button.pack(pady=(0, 10))

# Custom scrollbar and text box for displaying query results
# This part seems to be for the query results, and should be at the bottom.
result_display = ctk.CTkFrame(root)
result_display.pack(fill="x", pady=(0, 10))

result_textbox = ctk.CTkTextbox(result_display)
result_textbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

result_scrollbar = ctk.CTkScrollbar(result_display, command=result_textbox.yview)
result_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

result_textbox.configure(yscrollcommand=result_scrollbar.set)

# Start the Tkinter event loop
root.mainloop()