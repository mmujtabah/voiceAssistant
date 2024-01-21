# voiceAssistant

## Overview

This is a simple voice assistant application built using Python and Tkinter. It utilizes Google's Generative AI for natural language processing and text-to-speech functionalities. The voice assistant listens to user commands, processes them, and provides responses.

## Features

- **Voice Recognition:** The assistant listens to voice commands using the SpeechRecognition library.
- **Natural Language Processing:** Powered by Google's Generative AI for understanding and generating human-like responses.
- **Text-to-Speech:** Utilizes the pyttsx3 library for converting text responses into speech.
- **YouTube Video Search:** You can command the assistant to search for videos on YouTube.

## Prerequisites

- Python 3.6 or higher
- Required Python libraries (install using `pip install -r requirements.txt`)
- Google API key for Generative AI (set as an environment variable)

## Getting Started

1. Clone the repository:  ```git clone https://github.com/your-username/voice-assistant.git```
2. Install dependencies:  ```pip install -r requirements.txt```
3. Set up your Google API key in .env file
4. Run the application: ```python main.py```

## Usage
1. Click the "Start" button to activate the voice assistant.
2. Issue voice commands, e.g., "Play music" or "What's the weather today?"
3. The assistant will respond with text and spoken messages.
4. Assistant can play videos or music on YouTube
5. Program can be exited by saying "exit" keyword.

## Additional Notes

* Make sure your microphone is properly set up for voice recognition.
* For optimal performance, use the application in a quiet environment.

## Contributing

* Contributions are welcome! If you find any issues or have improvements, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE[LICENSE] file for details.
