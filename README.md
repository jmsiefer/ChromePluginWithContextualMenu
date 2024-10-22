# Basecamp Bridge Extension

## Overview

The Basecamp Bridge Extension is a Chrome extension integrated with OpenAI's API to improve productivity by allowing predefined text insertion, rewriting text in different tones, simplifying English, and providing quick access to project files within Basecamp. This project demonstrates a useful integration of automation and AI tools within the Chrome environment.

## Features

- **Insert Predefined Text:** Quickly insert standardized templates into text areas.
- **Rewrite Text:** Rewrite highlighted text in positive or neutral tones using OpenAI’s API.
- **Simplify English:** Simplify complex English content to a concise, action-oriented format.
- **Jump to Files:** Navigate directly to project-related files in Basecamp.
- **API Key Management:** Easily set and manage your OpenAI API key through the extension.

## Why Use Basecamp Bridge?

This tool simplifies and speeds up repetitive text-based tasks, making it perfect for:
- **Project Managers**: Standardize communication templates across teams.
- **Content Creators**: Rewrite and simplify content with the click of a button.
- **Teams Using Basecamp**: Quickly navigate to attachments or files within projects.

## How It Works

1. **Predefined Templates**:
   - Insert pre-written text templates directly into text areas.
   - Ideal for project kickoffs, task assignments, and regular updates.

2. **Text Rewriting**:
   - Select text and rewrite it using OpenAI API in different tones (e.g., positive or neutral).

3. **Simplify English**:
   - Highlight text and get a simplified version optimized for clarity and action.

4. **Jump to Files**:
   - Navigate to project files within Basecamp from any project-related page.

5. **API Key Management**:
   - Store your OpenAI API key securely within Chrome's storage for easy access.

## Getting Started

### Prerequisites

- Google Chrome browser.
- OpenAI API Key.

### Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Make sure the required files are present:
   - `Basecamp Bridge.py`
   - `BCB.png`

3. Run the Python script to generate the extension:
   ```bash
   python Basecamp\ Bridge.py
   ```

4. Load the Chrome extension:
   - Open Chrome and go to `chrome://extensions/`.
   - Enable **Developer Mode**.
   - Click **Load unpacked** and select the generated `basecamp_bridge_extension` folder.

### Usage

- On any Basecamp page, use the GUI buttons for:
  - **Insert KO Template**: Add a pre-written template to your message.
  - **Rewrite Text**: Change the tone of highlighted text.
  - **Simplify English**: Simplify selected content for easier readability.
  - **Jump to Files**: Navigate directly to attachments in the current project.

### API Key Setup

1. Click the **Set OpenAI API Key** button in the extension’s GUI.
2. Enter your API key when prompted and click **Save**.

## Troubleshooting

- Ensure the OpenAI API key is correctly stored.
- Verify that the extension is loaded correctly in **Developer Mode**.
- Confirm that the required files (`BCB.png`) are in place.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

Special thanks to all contributors and open-source tools used in this project.
