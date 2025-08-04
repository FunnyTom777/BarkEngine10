![secret message? cool... but dont ask why the banner is not working >:C](/assets/banner.png)

# BarkEngine10

Welcome to **BarkEngine10** — the foundation of the BarkEngine universe! BarkEngine10 is a moddable game engine built with Python with lua mod support.

---

## 🚀 Getting Started

### Installation

1.  **Download the latest release ZIP** from this repository.
2.  **Extract** the ZIP file anywhere you like on your computer.
3.  Open the extracted folder, right-click inside it (Windows) and choose **"Open Terminal"** or **"Open PowerShell window here"**.
4.  Type the following command and press **Enter**:

    ```bash
    python main.py
    ```

    *   ✅ **Make sure you have Python 3.8+ installed.** If not, download it from [https://www.python.org/downloads/](https://www.python.org/downloads/).
    *   Also install the required dependencies:

        ```bash
        pip install -r requirements.txt
        ```

---

## 🐾 What You Can Do

When you run `main.py`, the BarkEngine10 app window will open. Here’s a quick overview of what it offers:

*   **View Installed Mods:**  It scans the `mods/` folder and displays all your loaded mods neatly.
*   **Add Mods Easily:** Click the "Add Mod" button to browse and install `.zip` mod files.
*   **Remove Mods:** Select a mod and delete it with one click.
*   **Create Mods:** Launch the built-in **Mod Maker** to generate ready-to-use mods with Lua scripts!

---

## 🔧 Modding BarkEngine10 (Lua Support!)

You can now write **mods using Lua!** That’s right – no more DML (Dave Mod Loader was the original way of making mods, but it has now been depecated in return for built in lua mod support!), just zip up a Lua file (and a info.json) and go wild.

### 🧱 Mod Structure

Each mod is a `.zip` file with these essential files:

*   `info.json`:  Required metadata about your mod (name, author, BarkEngine version).
*   `mod.lua`: Your Lua code that runs when BarkEngine loads the mod.

**Example `info.json`:**

```json
{
  "mod name": "Cool Bark Mod",
  "mod author": "You!",
  "BarkEngine version": "0.1-alpha"
}
```

**Example `mod.lua`:**

```lua
print_debug("Mod loaded!")
alert("Bark!", "Hello from Lua!")
open_window("Lua made this window")
```

Simply put your `.zip` into the `mods/` folder, and BarkEngine10 will load and execute `mod.lua`.

🧠 **Lua Modding API**

Your Lua mods can call these functions:

| Function          | Description                               |
|-------------------|-------------------------------------------|
| `open_window(title)` | Opens a new UI window with a title         |
| `alert(title, message)` | Shows a message box popup                |
| `print_debug(msg)`   | Prints debug info to the console          |
| `get_mod_name()`    | Returns the current mod’s name            |
| `ask_file()`       | Opens a file picker (returns path)        |
| `save_file(text)`  | Opens a save dialog and saves text         |

*More Lua functions and integrations will come in future versions – like custom UI, game objects, and inter-mod communication!*

✨ **Creating Mods with the Mod Maker**

The easiest way to create a new mod is using the built-in Mod Maker:

1.  Click "Open Mod Maker".
2.  Fill in:
    *   Mod Name
    *   Author
    *   Target BarkEngine Version
3.  Optionally, add up to 10 files (images, sounds, scripts, etc.).
4.  Click "Build Mod" – it creates a `.zip` mod and places it in the `mods/` folder!

📦 **Where to Find Mods**

*   A few sample mods are already in the `mods/` folder of this repository.
*   The code for the BarkEngine Modhub is included (in early alpha). Feel free to mess with it or build your own version.

🤝 **Support & Contributing**

Found a bug? Have a feature idea? Open an issue!

📜 **License**

This project is licensed under the
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-nc-sa/4.0/)

✅ You may use and modify the code and assets.
❌ Commercial use is prohibited without permission.

🐶 **Thanks for checking out BarkEngine10!** Happy modding!

— FunnyTom777 :D
