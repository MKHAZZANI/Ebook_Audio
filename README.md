
# 📖 Ebook-Audiobook Converter 🎧

A simple yet powerful tool to convert your ebooks into audiobooks, bringing your library to life! This application provides a user-friendly graphical interface and a robust command-line interface for all your conversion needs.

---

## ✨ Features

- **Multiple File Formats:** Supports `.txt`, `.pdf`, and `.docx` files.
- **Dual TTS Engines:** Choose between the high-quality online voices from **Microsoft Edge TTS** or a local **pyttsx3** engine.
- **Voice Selection:** A wide variety of voices to choose from, allowing you to customize your listening experience.
- **Cross-Platform:** Works on Windows, macOS, and Linux.
- **User-Friendly GUI:** An intuitive graphical interface built with Flet for easy conversions.
- **Powerful CLI:** A command-line interface for power users and automation.
- **Audio Controls:** Play, pause, and restart your generated audio directly from the application.

---

## 🚀 Getting Started

Follow these instructions to get the Ebook-Audiobook Converter up and running on your system.

### Prerequisites

- **Python 3:** Make sure you have Python 3 installed on your system. You can download it from [python.org](https://python.org).

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/MKHAZZANI/Ebook-AudioBook.git 
    cd Ebook-AudioBook
    ```

2.  **Install the required packages:**

    The application relies on several Python packages. You can install them all with a single command:

    ```bash
    pip install flet flet-audio edge-tts pyttsx3 pypdf2 python-docx click
    ```

---

## 🖥️ Usage

You can use the application in two ways: through the graphical user interface (GUI) or the command-line interface (CLI).

### Graphical User Interface (GUI)

The GUI provides an easy-to-use interface for converting your ebooks.

-   **Windows:**

    ```bash
    python app_gui.py
    ```

-   **macOS / Linux:**

    ```bash
    python3 app_gui.py
    ```

### Command-Line Interface (CLI)

The CLI is perfect for power users and for integrating the converter into scripts.

-   **Windows:**

    ```bash
    python converter\core\src\main.py convert <your_ebook.txt>
    ```

-   **macOS / Linux:**

    ```bash
    python3 converter/core/src/main.py convert <your_ebook.txt>
    ```

**CLI Options:**

-   `--output`: Specify the output audio file path. Defaults to `output.wav`.

    *Example:*

    ```bash
    python converter\core\src\main.py convert my_book.pdf --output my_audiobook.wav
    ```

---

## 🛠️ Troubleshooting

-   **`pyttsx3` issues:** If you encounter issues with the `pyttsx3` engine, it might be due to a problem with the local speech synthesis engine on your system. We recommend using the `edge-tts` engine for the best results.
-   **Permissions:** Make sure you have the necessary permissions to read the ebook file and write the output audio file.

---

Enjoy your new audiobooks! 📚🎧
