# ⚡ AutoTyper v4.0: Low-Level Input Simulator

A robust Python automation tool designed to bypass clipboard restrictions by simulating hardware-level keystrokes. Specifically built to handle complex character sets and Brazilian Portuguese accents.

## 🚀 Why this is different
Most autotypers fail with special characters (ã, é, ç). This version utilizes the `pynput` library to interface directly with the OS keyboard controller, ensuring 100% accuracy in text reproduction.

## 🛠️ Key Features
- **Multithreaded Execution:** Uses the `threading` library to keep the GUI responsive while the automation runs in the background.
- **Interactive GUI:** Built with `Tkinter` (ttk), featuring real-time progress bars, character counters, and time estimates.
- **Precision Timing:** Custom speed presets (from 15ms to 80ms) and a configurable initial delay for field selection.
- **Binary Ready:** Includes a `.spec` file for PyInstaller, allowing for easy distribution as a standalone executable.

## 📋 Technical Stack
- **Language:** Python 3.
- **Main Libraries:** `pynput` (Input Control), `Tkinter` (GUI), `Threading` (Async execution).
- **Packaging:** PyInstaller configuration for Windows/Linux deployment.

---
*Built to explore OS-level automation and asynchronous programming in Python.*
