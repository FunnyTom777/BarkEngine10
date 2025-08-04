import os
import json
import zipfile
import shutil
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import tempfile
import traceback
from lupa import LuaRuntime

MODS_FOLDER = "mods"
DETAILS_FILE = "details.json"
LUA_ENTRY_FILE = "mod.lua"

# Setup Lua
lua = LuaRuntime(unpack_returned_tuples=True)
root_window = None

def set_root_window(window):
    global root_window
    root_window = window

# Lua-callable Python functions
def open_window(title):
    print(f"[Lua] open_window('{title}')")
    if root_window is None:
        print("⚠️ root window not set")
        return
    w = tk.Toplevel(root_window)
    w.title(title)
    tk.Label(w, text=f"Hello from Lua mod: {title}").pack()

# Extra Python functions Lua mods can use
def print_debug(msg):
    print(f"[MOD DEBUG] {msg}")

def alert(title, message):
    if root_window:
        messagebox.showinfo(title, message)
    else:
        print(f"[ALERT] {title}: {message}")

def get_mod_name():
    return current_mod_name or "Unknown Mod"

def ask_file():
    if root_window:
        return filedialog.askopenfilename()
    return ""

def save_file(contents):
    if root_window:
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(contents)
            return path
    return ""

def run_python(code):
    try:
        exec(code)
    except Exception as e:
        print(f"Python exec error: {e}")

# Register to Lua
lua.globals()["open_window"] = open_window
lua.globals()["print_debug"] = print_debug
lua.globals()["alert"] = alert
lua.globals()["get_mod_name"] = get_mod_name
lua.globals()["ask_file"] = ask_file
lua.globals()["save_file"] = save_file
lua.globals()["run_python"] = run_python  # ⚠️ Be careful with this!

def run_lua_mods(app_instance, mod_folder=MODS_FOLDER):
    global root_window
    root_window = app_instance
    print("🔍 Scanning for Lua mods...")

    if not os.path.exists(mod_folder):
        os.makedirs(mod_folder)

    for filename in os.listdir(mod_folder):
        if not filename.endswith(".zip"):
            continue

        mod_path = os.path.join(mod_folder, filename)
        try:
            with zipfile.ZipFile(mod_path, 'r') as zip_ref:
                if 'info.json' not in zip_ref.namelist() or LUA_ENTRY_FILE not in zip_ref.namelist():
                    print(f"⚠️ Skipping {filename}: Missing info.json or {LUA_ENTRY_FILE}")
                    continue

                with zip_ref.open("info.json") as info_file:
                    mod_info = json.load(info_file)
                    mod_name = mod_info.get("mod name", filename)

                print(f"📦 Loading mod: {mod_name}")

                with zip_ref.open(LUA_ENTRY_FILE) as lua_file:
                    lua_code = lua_file.read().decode('utf-8')
                    lua.execute(lua_code)
                    print(f"✅ Lua executed for mod: {mod_name}")

        except Exception as e:
            print(f"❌ Failed to load mod {filename}: {e}")
            traceback.print_exc()


class ModMaker(tk.Toplevel):
    def __init__(self, parent, barkengine_versions):
        super().__init__(parent)
        self.title("Mod Maker")
        self.geometry("400x400")
        self.parent = parent
        self.selected_files = []

        tk.Label(self, text="Mod Name:").pack(anchor="w", padx=10, pady=(10, 0))
        self.mod_name_entry = tk.Entry(self)
        self.mod_name_entry.pack(fill="x", padx=10)

        tk.Label(self, text="Mod Author:").pack(anchor="w", padx=10, pady=(10, 0))
        self.mod_author_entry = tk.Entry(self)
        self.mod_author_entry.pack(fill="x", padx=10)

        tk.Label(self, text="BarkEngine Version:").pack(anchor="w", padx=10, pady=(10, 0))
        self.version_var = tk.StringVar(value=barkengine_versions[0])
        self.version_dropdown = ttk.Combobox(self, values=barkengine_versions, state="readonly", textvariable=self.version_var)
        self.version_dropdown.pack(fill="x", padx=10)

        tk.Label(self, text="Additional files (max 10):").pack(anchor="w", padx=10, pady=(10, 0))
        self.files_listbox = tk.Listbox(self, height=6)
        self.files_listbox.pack(fill="both", padx=10, pady=(0, 5), expand=True)

        tk.Button(self, text="Add Files", command=self.add_files).pack(padx=10)
        tk.Button(self, text="Build Mod", command=self.build_mod).pack(pady=15)

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
                zipf.writestr("info.json", json.dumps(info_json, indent=4))
                for file_path in self.selected_files:
                    arcname = os.path.basename(file_path)
                    zipf.write(file_path, arcname)
            messagebox.showinfo("Success", f"Mod '{mod_name}' built and saved!")
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

        ttk.Label(self, text=f"BarkEngine Version: {self.current_version}").pack(pady=5)

        self.mod_list = ttk.Treeview(self, columns=("Name", "Author", "Mod Version", "Status"), show='headings')
        for col in self.mod_list["columns"]:
            self.mod_list.heading(col, text=col)
        self.mod_list.pack(fill=tk.BOTH, expand=True, padx=10)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Remove Selected Mod", command=self.remove_selected_mod).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Open Mod Maker", command=self.open_mod_maker).grid(row=0, column=1, padx=5)
        tk.Button(self, text="Add Mods (Click to Add)", command=self.add_mods).pack(pady=5)

        self.load_mods()

    def load_barkengine_version(self):
        if os.path.exists(DETAILS_FILE):
            try:
                with open(DETAILS_FILE, "r") as f:
                    data = json.load(f)
                    return data.get("barkengine_version", "Unknown")
            except Exception:
                return "Unknown"
        return "Unknown"

    def load_mods(self):
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

                            status = "OK" if mod_version == self.current_version else f"Mismatch (Expected {self.current_version})"
                    else:
                        name = mod_file
                        author = "-"
                        mod_version = "-"
                        status = "Missing info.json"
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
            mod_path = os.path.join(MODS_FOLDER, f"{mod_name}.zip")
            if os.path.exists(mod_path):
                try:
                    os.remove(mod_path)
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to remove: {e}")
            self.mod_list.delete(item)

    def open_mod_maker(self):
        versions = [self.current_version] if self.current_version != "Unknown" else ["0.1-alpha"]
        ModMaker(self, versions)

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
    run_lua_mods(app)
    app.mainloop()
