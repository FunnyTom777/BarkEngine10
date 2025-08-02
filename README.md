# BarkEngine10

Welcome to **BarkEngine10** — the foundation of the BarkEngine universe! BarkEngine10 is the starting point for an exciting, moddable game engine built with Madness and powered by Python.

---

## Getting Started

### Installation

1.  **Download the latest release ZIP** from this repository.

2.  **Extract** the ZIP file anywhere you like on your computer.

3.  Open the extracted folder, **right-click** inside it (Windows) and choose **"Open Terminal"** or **"Open PowerShell window here"**.

4.  Type the following command and press **Enter**:

    ```bash
    python main.py
    ```

    Note: Make sure you have Python installed! We recommend Python 3.8 or higher. If you don’t have Python installed, you can download it from [python.org](https://www.python.org/).

### How to Use BarkEngine10

When you run `main.py`, the BarkEngine10 app window will open. Here’s what you can do:

*   **View Installed Mods:** It automatically scans the mods folder for available mods and displays them, including details like mod name, author, and the BarkEngine version it’s compatible with.
*   **Add Mods:** Use the Add Mods button to browse and add `.zip` mod files to your mods folder easily.
*   **Remove Mods:** Select any installed mod and click Remove Selected Mod to delete it from your system.
*   **Create Mods:** Click Open Mod Maker to launch the built-in mod creation tool (more on this below!).

### Making Mods

You have two ways to create mods for BarkEngine10:

1.  **Using the Built-in Mod Maker**

    The easiest way to create mods is with the Mod Maker:

    *   Click the Open Mod Maker button in the app.
    *   Fill out the form:
        *   **Mod Name** — Give your mod a catchy title!
        *   **Mod Author** — Your name or handle.
        *   **BarkEngine Version** — Pick the version your mod is compatible with (currently only 0.1-alpha).
        *   **Additional Files** — Add up to 10 extra files to include in your mod package (optional).

    Hit Build Mod, and your mod will be packaged into a `.zip` file with the proper structure and saved to the mods folder.

2.  **Making Mods Manually**

    If you prefer to craft your mods by hand or with your own tools, here’s how the mod structure works:

    *   Create a `.zip` archive that contains:
        *   An `info.json` file at the root of the archive. This file must contain the following JSON fields:

            ```json
            {
              "mod name": "Your Mod Name",
              "mod author": "Your Name or Alias",
              "BarkEngine version": "0.1-alpha"
            }
            ```

        *   Any other additional files your mod needs (e.g., assets, scripts, data files).

    *   Name your `.zip` file something descriptive (e.g., `SuperBarkMod.zip`).

    *   Place your mod `.zip` file inside the `mods` folder in the BarkEngine10 directory.

    *   Run BarkEngine10, and your mod will show up in the mod list.

### Where to Get Mods

You can find some preset mods in the "Mods" folder in this repo, i am still working on the BarkEngine Modhub... (the Code for the BarkEngine Modhub is actually included in this repo, so if you really want to you can use/work on that)

### Support & Contributions

If you run into bugs or have feature requests, feel free to open an issue.

Contributions are very welcome! Feel free to fork the repo and submit pull requests.

### license
This project is licensed under the [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.](https://creativecommons.org/licenses/by-nc-sa/4.0/)
You may use and modify the code and assets, but **commercial use is prohibited without permission.**


## Thanks for checking out BarkEngine10! Happy modding and barking! 🐾
— FunnyTom777 :D
