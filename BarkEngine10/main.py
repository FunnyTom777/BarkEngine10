import os
import json
import zipfile
import shutil
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

MODS_FOLDER = "mods"
DETAILS_FILE = "details.json"

class ModMaker(tk.Toplevel):
    def __init__(self, parent, barkengine_versions):
        super().__init__(parent)
        self.title("Mod Maker")
        self.geometry("400x400")
        self.parent = parent

        self.selected_files = []

        tk.Label(self, text="Mod Name:").pack(anchor="w", padx=10, pady=(10,0))
        self.mod_name_entry = tk.Entry(self)
        self.mod_name_entry.pack(fill="x", padx=10)

        tk.Label(self, text="Mod Author:").pack(anchor="w", padx=10, pady=(10,0))
        self.mod_author_entry = tk.Entry(self)
        self.mod_author_entry.pack(fill="x", padx=10)

        tk.Label(self, text="BarkEngine Version:").pack(anchor="w", padx=10, pady=(10,0))
        self.version_var = tk.StringVar(value=barkengine_versions[0])
        self.version_dropdown = ttk.Combobox(self, values=barkengine_versions, state="readonly", textvariable=self.version_var)
        self.version_dropdown.pack(fill="x", padx=10)

        tk.Label(self, text="Additional files (max 10):").pack(anchor="w", padx=10, pady=(10,0))
        self.files_listbox = tk.Listbox(self, height=6)
        self.files_listbox.pack(fill="both", padx=10, pady=(0,5), expand=True)

        add_file_btn = tk.Button(self, text="Add Files", command=self.add_files)
        add_file_btn.pack(padx=10)

        build_btn = tk.Button(self, text="Build Mod", command=self.build_mod)
        build_btn.pack(pady=15)

    def add_files(self):
        files = filedialog.askopenfilenames(title="Select up to 10 files")
        for f in files:
            if len(self.selected_files) < 10 and f not in self.selected_files:
                self.selected_files.append(f)
                self.files_listbox.insert(tk.END, os.path.basename(f))
            if len(self.selected_files) >= 10:
                messagebox.showinfo("Limit reached", "You can only add up to 10 additional files.")
                break

    def build_mod(self):
        mod_name = self.mod_name_entry.get().strip()
        mod_author = self.mod_author_entry.get().strip()
        version = self.version_var.get()

        if not mod_name:
            messagebox.showerror("Error", "Mod name is required.")
            return

        info_json = {
            "mod name": mod_name,
            "mod author": mod_author if mod_author else "Unknown",
            "BarkEngine version": version
        }

        mod_zip_path = os.path.join(MODS_FOLDER, f"{mod_name}.zip")

        try:
            with zipfile.ZipFile(mod_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Write info.json
                zipf.writestr("info.json", json.dumps(info_json, indent=4))
                # Add additional files
                for file_path in self.selected_files:
                    arcname = os.path.basename(file_path)
                    zipf.write(file_path, arcname)
            messagebox.showinfo("Success", f"Mod '{mod_name}' built and saved to mods folder!")
            self.parent.load_mods()
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to build mod: {e}")


class BarkModsApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("BarkMods Manager")
        self.geometry("700x450")

        self.current_version = self.load_barkengine_version()

        version_label = ttk.Label(self, text=f"BarkEngine Version: {self.current_version}")
        version_label.pack(pady=5)

        self.mod_list = ttk.Treeview(self, columns=("Name", "Author", "Mod Version", "Status"), show='headings')
        self.mod_list.heading("Name", text="Mod Name")
        self.mod_list.heading("Author", text="Author")
        self.mod_list.heading("Mod Version", text="BarkEngine Version")
        self.mod_list.heading("Status", text="Status")
        self.mod_list.pack(fill=tk.BOTH, expand=True, padx=10)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        remove_btn = tk.Button(btn_frame, text="Remove Selected Mod", command=self.remove_selected_mod)
        remove_btn.grid(row=0, column=0, padx=5)

        modmaker_btn = tk.Button(btn_frame, text="Open Mod Maker", command=self.open_mod_maker)
        modmaker_btn.grid(row=0, column=1, padx=5)

        # Enable drag and drop on the main window for mod installation
        self.setup_drag_and_drop()

        self.load_mods()

    def load_barkengine_version(self):
        if os.path.exists(DETAILS_FILE):
            try:
                with open(DETAILS_FILE, "r") as f:
                    data = json.load(f)
                    return data.get("barkengine_version", "Unknown")
            except Exception:
                return "Unknown"
        else:
            return "Unknown"

    def load_mods(self):
        # Clear existing
        for item in self.mod_list.get_children():
            self.mod_list.delete(item)

        if not os.path.exists(MODS_FOLDER):
            os.makedirs(MODS_FOLDER)

        mods = [f for f in os.listdir(MODS_FOLDER) if f.endswith(".zip")]
        for mod_file in mods:
            mod_path = os.path.join(MODS_FOLDER, mod_file)
            try:
                with zipfile.ZipFile(mod_path, 'r') as zip_ref:
                    if "info.json" in zip_ref.namelist():
                        with zip_ref.open("info.json") as info_file:
                            info_data = json.load(info_file)
                            name = info_data.get("mod name", "Unknown")
                            author = info_data.get("mod author", "Unknown")
                            mod_version = info_data.get("BarkEngine version", "Unknown")

                            if mod_version != self.current_version:
                                status = f"Version Mismatch! Expected {self.current_version}"
                            else:
                                status = "OK"
                    else:
                        name = mod_file
                        author = "-"
                        mod_version = "-"
                        status = "Incomplete/Corrupted (no info.json)"
            except Exception as e:
                name = mod_file
                author = "-"
                mod_version = "-"
                status = f"Error: {e}"

            self.mod_list.insert("", "end", values=(name, author, mod_version, status))

    def remove_selected_mod(self):
        selected = self.mod_list.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a mod to remove.")
            return

        confirm = messagebox.askyesno("Confirm Removal", "Are you sure you want to remove the selected mod(s)?")
        if not confirm:
            return

        for item in selected:
            mod_name = self.mod_list.item(item, "values")[0]
            # Mod file is mod_name.zip
            mod_path = os.path.join(MODS_FOLDER, f"{mod_name}.zip")
            if os.path.exists(mod_path):
                try:
                    os.remove(mod_path)
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to remove mod file: {e}")
            self.mod_list.delete(item)

    def open_mod_maker(self):
        versions = [self.current_version] if self.current_version != "Unknown" else ["0.1-alpha"]
        ModMaker(self, versions)

    def setup_drag_and_drop(self):
        # Tkinter native drag-and-drop support is limited.
        # On Windows, you can use the 'tkdnd' package.
        # Here we provide a simple workaround with a hidden file dialog triggered on drop
        # Or instruct user to drag files onto a button to add mods.
        # For full drag & drop support, external libs are needed.
        # We'll simulate drag & drop with a "Add Mods" button for now.

        add_mod_btn = tk.Button(self, text="Add Mods (Drag and Drop Not Supported, Click to Add)", command=self.add_mods)
        add_mod_btn.pack(pady=5)

    def add_mods(self):
        files = filedialog.askopenfilenames(title="Select mod .zip files", filetypes=[("ZIP files", "*.zip")])
        for file_path in files:
            try:
                dest_path = os.path.join(MODS_FOLDER, os.path.basename(file_path))
                shutil.copy(file_path, dest_path)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add mod: {e}")
        self.load_mods()


if __name__ == "__main__":
    if not os.path.exists(MODS_FOLDER):
        os.makedirs(MODS_FOLDER)
    app = BarkModsApp()
    app.mainloop()
