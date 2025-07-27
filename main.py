import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
import csv
from data.database import setup_database, add_project, add_supply, add_tool 
from data.database import get_all_projects, get_supplies_for_project, get_tools_for_project
from data.database import update_supply, update_tool, delete_supply_by_id, delete_supply_by_id

class ProjectPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Project Planner")
        self.root.geometry("800x800")

        self.tools = []
        self.supplies = []

        # creating the frames
        self.tools_frame = tk.LabelFrame(root, text="Tools Needed")
        self.tools_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.tools_listbox = tk.Listbox(self.tools_frame, width=40)
        self.tools_listbox.pack(fill="both", expand=True)

        self.supplies_frame = tk.LabelFrame(root, text="Supplies Needed")
        self.supplies_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")


        self.supplies_listbox = tk.Listbox(self.supplies_frame, width=40)
        self.supplies_listbox.pack(fill="both", expand=True)

        # buttons
        tool_buttons_frame = tk.Frame(root)
        tool_buttons_frame.grid(row=1, column=0, padx=10, pady=5)
        
        tk.Button(tool_buttons_frame, text="Add Tool", command=self.add_tool).pack(fill="x", pady=2)
        tk.Button(tool_buttons_frame, text="Edit Tool", command=self.edit_tool).pack(fill="x", pady=2)
        tk.Button(tool_buttons_frame, text="Delete Tool", command=self.edit_tool).pack(fill="x", pady=2)
        
        supply_buttons_frame = tk.Frame(root)
        supply_buttons_frame.grid(row=1, column=1, padx=10, pady=5)

        tk.Button(supply_buttons_frame, text="Add Supply", command=self.add_supply).pack(fill="x", pady=2)
        tk.Button(supply_buttons_frame, text="Edit Supply", command=self.edit_supply).pack(fill="x", pady=2)
        tk.Button(supply_buttons_frame, text="Delete Supply", command=self.delete_supply).pack(fill="x", pady=2)

        # action buttons (new project + export)
        action_frame = tk.Frame(root)
        action_frame.grid(row=1, column=0, columnspan=2, pady=10)

        tk.Button(action_frame, text="New Project", command=self.new_project).pack(side="left", padx=10)
        tk.Button(action_frame, text="Export to CSV", command=self.export_project_to_csv).pack(side="left", padx=10)



        # allow resizing
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=0)

        # Project selection UI
        self.project_select_frame = tk.Frame(root)
        self.project_select_frame.grid(row=2, column=0, columnspan=2, pady=10)

        tk.Label(self.project_select_frame, text="Load Existing Project:").pack(side="left")

        self.project_var = tk.StringVar()
        self.project_dropdown = tk.OptionMenu(self.project_select_frame, self.project_var, "")
        self.project_dropdown.pack(side="left")

        tk.Button(self.project_select_frame, text="Load", command=self.load_project).pack(side="left")


        self.refresh_project_dropdown()


    def add_tool(self):
        tool = simpledialog.askstring("Add tool", "Enter tool name")
        if tool:
            tool_id = None
            if self.current_project_id:
                tool_id = add_tool(self.current_project_id, tool)

            tool_entry = {"id": tool_id, "name": tool}
            self.tools.append(tool_entry)
            self.tools_listbox.insert(tk.END, tool)

    def edit_tool(self):
        selected = self.tools_listbox.curselection()
        if not selected:
            messagebox.showwarning("No selection", "Please select a tool to edit.")
            return
        
        index = selected[0]
        current_name = self.tools[index]

        new_name = simpledialog.askstring("Edit Tool", "Enter a new tool name.")
        if not new_name:
            return
        
        self.tools[index] = new_name
        self.tools_listbox.delete(index)
        self.tools_listbox.insert(index, new_name)

        if self.current_project_id and tool["id"]:
            update_tool(tool["id"], new_name)

    def delete_tool(self):
        selected = self.tools_listbox.curselection()
        if not selected:
            messagebox.showwarning("No selection", "Please select a tool to delete.")
            return

        index = selected[0]
        tool = self.tools[index]

        if messagebox.askyesno("Confirm", f"Delete tool '{tool['name']}'?"):
            if self.current_project_id and tool["id"]:
                delete_tool_by_id(tool["id"])

        # update the display
        self.tools.pop(index)
        self.tools_listbox.delete(index)

    
    def add_supply(self):
        supply_name = simpledialog.askstring("Add supply", "Enter supply name")
        if not supply_name:
            return
        
        quantity = simpledialog.askstring("Quantity", "Enter quantity")
        if not quantity:
            return

        ssupply_entry = {"id": None, "name": supply_name, "quantity": quantity}

        if self.current_project_id:
            supply_id = add_supply(self.current_project_id, supply_name, quantity)
            supply_entry["id"] = supply_id

        self.supplies.append(supply_entry)
        self.supplies_listbox.insert(tk.END, f"{supply_name} - {quantity}")

    def delete_supply(self):
        selected = self.supplies_listbox.curselection()
        if not selected:
            messagebox.showwarning("No selection", "Please select a supply to delete.")
            return
        
        index = selected[0]
        supply = self.supplies[index]

        if messagebox.askyesno("Confirm", f"Delete supply '{supply['name']}'?"):
            if self.current_project_id and supply["id"]:
                delete_supply_by_id(supply["id"])

            self.supplies.pop(index)
            self.supplies_listbox.delete(index)
    
    def edit_supply(self):
        selected = self.supplies_listbox.curselection()
        if not selected:
            messagebox.showwarning("No selection", "Please select a supply to edit.")
            return

        index = selected[0]
        supply = self.supplies[index]

        new_name = simpledialog.askstring("Edit Supply", "Enter new name:", initialvalue=supply["name"])
        if not new_name:
            return
        new_quantity = simpledialog.askstring("Edit Quantity", "Enter new quantity:", initialvalue=supply["quantity"])
        if not new_quantity:
            return

        supply["name"] = new_name
        supply["quantity"] = new_quantity

        self.supplies_listbox.delete(index)
        self.supplies_listbox.insert(index, f"{new_name} - {new_quantity}")

        if self.current_project_id and supply["id"]:
            update_supply(supply["id"], new_name, new_quantity)



    def new_project(self):
        name = simpledialog.askstring("New Project", "Enter project name.")
        if not name:
            return
    
        try:
            self.current_project_id = add_project(name)
            self.current_project_name = name
        
            self.tools.clear()
            self.supplies.clear()
            self.tools_listbox.delete(0, tk.END)
            self.supplies_listbox.delete(0, tk.END)

            messagebox.showinfo("Success", f"Project '{name}' created.")

            # add tools and then supplies
            while True:
                tool = simpledialog.askstring("Tool", "Enter a tool or leave blank if done.")
                if not tool:
                    break
                self.tools.append(tool)
                self.tools_listbox.insert(tk.END, tool)
                add_tool(self.current_project_id, tool)

            while True:
                supply_name = simpledialog.askstring("Supply", "Enter a supply or leave blank if done.")
                if not supply_name:
                    break
                quantity = simpledialog.askstring("Quantity", f"Enter the quantity of {supply_name}.")
                if quantity is None:
                    continue

                if quantity.strip() == "":
                    quantity = "N/A"

                supply_entry = {"name": supply_name, "quantity": quantity}
                self.supplies.append(supply_entry)
                self.supplies_listbox.insert(tk.END, f"{supply_name} - {quantity}")
                add_supply(self.current_project_id, supply_name, quantity)

            messagebox.showinfo("Success", f"Project '{name}' created with {len(self.tools)} tools and {len(self.supplies)} supplies.")
            # adds new project to the drop down
            self.refresh_project_dropdown()

        except Exception as e:
            messagebox.showerror("Error", f"Could not create project: {e}.")


    def refresh_project_dropdown(self):
        self.project_var.set("")
        self.project_dropdown["menu"].delete(0, "end")

        self.projects = get_all_projects()
        self.project_name_to_id = {}

        for project_id, name in self.projects:
            self.project_dropdown["menu"].add_command(
                label=name,
                command=lambda n=name: self.project_var.set(n)
            )
            self.project_name_to_id[name] = project_id

    def load_project(self):
        name = self.project_var.get()
        if not name:
            messagebox.showwarning("No selection", "Please select a project to load.")

        project_id = self.project_name_to_id.get(name)
        if not project_id:
            messagebox.showerror("Error", "Selected project could not be loaded.")
            return
        
        self.current_project_id = project_id
        self.current_project_name = name

        # clear the existing lists
        self.tools.clear()
        self.supplies.clear()
        self.tools_listbox.delete(0, tk.END)
        self.supplies_listbox.delete(0, tk.END)

        # load from the DB
        self.tools = get_tools_for_project(project_id)
        for tool in self.tools:
            self.tools_listbox.insert(tk.END, tool["name"])

        self.supplies = get_supplies_for_project(project_id)
        for supply in self.supplies:
            display = f"{supply['name']} - {supply['quantity']}"
            self.supplies_listbox.insert(tk.END, display)

        messagebox.showinfo("Loaded", f"Project '{name}' loaded.")

    def export_project_to_csv(self):
        if not hasattr(self, "current_project_name"):
            messagebox.showwarning("No Project", "Please load or create a project.")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            initialfile=f"{self.current_project_name}.csv"
        )

        if not file_path:
            return
        
        try:
            with open(file_path, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Project", "Type", "Name", "Quantity"])

                for tool in self.tools:
                    # needs "" because 1 fewer column than supplies
                    writer.writerow([self.current_project_name, "Tool", tool["name"], ""])
            
                for supply in self.supplies:
                    writer.writerow([self.current_project_name, "Supply", supply["name"], supply["quantity"]])
            messagebox.showinfo("Exported", f"Project exported to:\n{file_path}")

        except Exception as e:
            messagebox.showerror("Export Error", f"Couldn't export CSV: {e}")


if __name__ == "__main__":
    setup_database()
    root = tk.Tk()
    app = ProjectPlanner(root)
    root.mainloop()