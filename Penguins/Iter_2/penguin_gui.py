import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import csv
import matplotlib.pyplot as plt
import os
print("Current folder:", os.getcwd())
print("Files here:", os.listdir('.'))

# Import your logic functions
# (Make sure penguin_logic.py is in the same folder!)
from penguin_logic import (
    headers, numeric_indices, 
    filter_data, describe_data, unique_data, sort_data, 
    augment_data, scatter_data, hist_data, boxplot_data, 
    load_file_content, PenguinError, generate_penguin_ascii, get_random_fact
)

# --- 1. Setup Main Window ---
root = tk.Tk()
root.title("Penguin Data Manager 🐧")
root.geometry("600x600")

data = []  # This variable will hold our loaded penguin data

# --- 2. Define the Helper Functions ---

def log(message):
    """Helper to write to the scrolling text area."""
    log_area.config(state='normal')
    log_area.insert(tk.END, message + "\n")
    log_area.see(tk.END)
    log_area.config(state='disabled')

def update_inputs(event=None):
    """Updates the labels and input boxes based on the selected command."""
    cmd = cmd_var.get()

    # Default: Show everything with generic names
    arg2_entry.grid()
    arg2_label.grid()
    arg1_label.config(text="Arg 1:")
    arg2_label.config(text="Arg 2:")
    arg1_entry.delete(0, tk.END)
    arg2_entry.delete(0, tk.END)
    # Customize based on command
    if cmd == 'load':
        arg1_label.config(text="Filename:")
        arg2_entry.grid_remove()  # Hide 2nd box
        arg2_label.grid_remove()  # Hide 2nd label
    elif cmd == 'filter':
        arg1_label.config(text="Column:")
        arg2_label.config(text="Value:")
    elif cmd == 'sort':
        arg1_label.config(text="Column:")
        arg2_label.config(text="Order (asc/desc):")
    elif cmd == 'augment':
        arg1_label.config(text="Percentage:")
        arg2_label.config(text="Option (duplicate/create):")
    elif cmd == 'scatter':
        arg1_label.config(text="X Column:")
        arg2_label.config(text="Y Column:")
    elif cmd in ('fact', 'art'):
        arg1_entry.grid_remove()  # Hide box 1
        arg1_label.grid_remove()  # Hide label 1
        arg2_entry.grid_remove()  # Hide box 2
        arg2_label.grid_remove()  # Hide label 2``

def execute_command():
    """Gets inputs and runs the appropriate logic function."""
    global data # We need to modify the global 'data' variable
    
    cmd = cmd_var.get()
    arg1 = arg1_entry.get().strip()
    arg2 = arg2_entry.get().strip()
    
    # Build the command list: ['filter', 'species', 'Adelie']
    command_list = [cmd]
    if arg1: command_list.append(arg1)
    if arg2: command_list.append(arg2)

    try:
        if cmd == 'load':
            if not arg1:
                messagebox.showerror("Error", "Please enter a filename!")
                return
            data = load_file_content(arg1)
            log(f"✅ Loaded {len(data)} penguins from {arg1}")

        elif cmd == 'filter':
            result = filter_data(command_list, data)
            log(f"🔍 Found {len(result)} matches.")
            for row in result[:5]:
                log(str(row))

        elif cmd == 'describe':
            res = describe_data(command_list, data)
            if res:
                log(f"📊 Stats for {arg1}: Min={res[0]}, Max={res[1]}, Avg={res[2]:.2f}")

        elif cmd == 'unique':
            res = unique_data(command_list, data)
            log(f"🔢 Unique values for {arg1}:")
            for k, v in res.items():
                log(f"   {k}: {v}")

        elif cmd == 'sort':
            sorted_data, elapsed = sort_data(command_list, data)
            data = sorted_data
            log(f"⚡ Sorted by {arg1} in {elapsed:.4f}s")

        elif cmd == 'augment':
            new_data, count, action = augment_data(command_list, data)
            data = new_data
            log(f"🧬 {action.title()}d {count} new penguins.")
            # Save the augmented file
            with open('augmented_data.csv', 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(list(headers.keys()))
                writer.writerows(data)
            log("   Saved to augmented_data.csv")

        elif cmd == 'scatter':
            x, y = scatter_data(command_list, data)
            plt.figure(figsize=(6, 4))
            plt.scatter(x, y, color='darkorange')
            plt.xlabel(arg1)
            plt.ylabel(arg2)
            plt.title(f"{arg1} vs {arg2}")
            plt.grid(True)
            plt.show()
            log(f"📈 Scatter plot created.")

        elif cmd == 'hist':
            vals, bins = hist_data(command_list, data)
            plt.figure(figsize=(6, 4))
            plt.hist(vals, bins=bins, color='teal', edgecolor='black')
            plt.title(f"Histogram of {arg1}")
            plt.show()
            log(f"📊 Histogram created.")

        elif cmd == 'boxplot':
            groups = boxplot_data(command_list, data)
            plt.figure(figsize=(6, 4))
            plt.boxplot(groups.values(), tick_labels=groups.keys())
            plt.title(f"{arg2} by {arg1}")
            plt.show()
            log(f"📦 Boxplot created.")
        
        elif cmd == 'fact':
            fact = get_random_fact()
            log(f"💡 DID YOU KNOW? {fact}")

        elif cmd == 'art':
            art = generate_penguin_ascii()
            log("🐧 Penguin ASCII Art:\n" + art)

    except PenguinError as e:
        messagebox.showerror("Penguin Error", str(e))
        log(f"❌ Error: {e}")
    except Exception as e:
        messagebox.showerror("System Error", f"Unexpected error: {e}")
        log(f"❌ Unexpected Error: {e}")

# --- 3. Build the GUI Layout ---

# Container for Controls
control_frame = ttk.LabelFrame(root, text="Command Center", padding="10")
control_frame.pack(fill="x", padx=10, pady=5)

# Dropdown
ttk.Label(control_frame, text="Operation:").grid(row=0, column=0, padx=5, pady=5)
cmd_var = tk.StringVar()
cmd_combo = ttk.Combobox(control_frame, textvariable=cmd_var, state="readonly")
cmd_combo['values'] = [
    "load", "filter", "describe", "unique", "sort", 
    "augment", "scatter", "hist", "boxplot",
    "fact", "art"
]
cmd_combo.grid(row=0, column=1, padx=5, pady=5)
cmd_combo.current(0)
# BINDING: This connects the dropdown to the function!
cmd_combo.bind("<<ComboboxSelected>>", update_inputs)

# Argument 1 (Saved to variable arg1_label)
arg1_label = ttk.Label(control_frame, text="Arg 1:")
arg1_label.grid(row=1, column=0, padx=5, pady=5)
arg1_entry = ttk.Entry(control_frame, width=20)
arg1_entry.grid(row=1, column=1, padx=5, pady=5)

# Argument 2 (Saved to variable arg2_label)
arg2_label = ttk.Label(control_frame, text="Arg 2:")
arg2_label.grid(row=2, column=0, padx=5, pady=5)
arg2_entry = ttk.Entry(control_frame, width=20)
arg2_entry.grid(row=2, column=1, padx=5, pady=5)

# Run Button
run_btn = ttk.Button(control_frame, text="Execute Command", command=execute_command)
run_btn.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")

# Output Log
output_frame = ttk.LabelFrame(root, text="Output Log", padding="10")
output_frame.pack(fill="both", expand=True, padx=10, pady=5)
log_area = scrolledtext.ScrolledText(output_frame, height=10, state='disabled')
log_area.pack(fill="both", expand=True)

# Initialize the labels correctly for the first item
update_inputs()

# --- 4. Start the App ---
root.mainloop()