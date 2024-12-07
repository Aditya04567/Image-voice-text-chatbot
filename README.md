# Image Voice Text AI Chatbot

## Overview

The Image-voice-text-chatbot is a conversational AI application that leverages Google's Gemini API for advanced text and image processing. Users can engage with the chatbot through text input or image uploads, and receive intelligent responses and detailed descriptions. This project aims to provide an interactive and user-friendly experience for exploring AI capabilities.

## Presentation

[Image Voice Text AI Chatbot.pdf](https://github.com/user-attachments/files/18048787/Image.Voice.Text.AI.Chatbot.pdf)

## Features

- **Text-based Chat**: Users can send messages and receive instant responses from the chatbot.
- **Image Analysis**: Users can upload images, and the chatbot will analyze and describe them in detail.
- **Speech Recognition**: Users can enable speech recognition to send messages by speaking, making interaction hands-free.
- **Text-to-Speech**: The chatbot can read responses aloud, enhancing accessibility and user engagement.

## Technologies Used

- **Backend**: Python with Flask for server-side logic.
- **Frontend**: HTML, CSS, and JavaScript for a responsive user interface.
- **AI Integration**: Google Generative AI SDK for processing text and images.
- **Image Processing**: PIL (Pillow) for handling image uploads and manipulations.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- Python 3.x
- pip (Python package installer)
- A valid API key for Google Gemini

## Screenshot

![image](https://github.com/user-attachments/assets/4eb7a971-ac44-4e9f-8a90-6e92808f2c43)
![image](https://github.com/user-attachments/assets/1062c440-9a40-43d0-9a6e-bb1e4ba71c34)
![image](https://github.com/user-attachments/assets/2e4c9220-58b3-4bcf-ab96-fc4224b15fb0)




## Installation

Follow these steps to set up the project locally:

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Aditya04567/Image-voice-text-chatbot.git
   cd Image-voice-text-chatbot

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API key**:

   Replace the placeholder in `app.py` with your API key:

   ```python
   API_KEY = "YOUR_GOOGLE_GEMINI_API_KEY"
   ```

4. **Run the Flask application**:

   ```bash
   python app.py
   ```

5. **Access the chatbot**:

   Open your web browser and navigate to `http://127.0.0.1:5000`.

---

## Project Structure

```plaintext
gemini-ai-chatbot/
│
├── app.py                  # Main application file
├── chatbot_core.py         # Chatbot logic and API integration
├── static/                 # Static files (CSS, images)
│   └── styles.css          # Styles for the frontend
├── templates/              # HTML templates for rendering pages
│   ├── index.html          # Main landing page
│   └── chat.html           # Chat interface
└── requirements.txt        # Python package dependencies
```

---

## Usage

### Text Chat
Type your message in the input field and press "Send" to receive a response.

### Image Chat
Upload an image using the file input, and the chatbot will analyze and describe it.

### Speech Recognition
Enable speech recognition to send messages via voice. Toggle the checkbox to activate/deactivate.

### Text-to-Speech
The chatbot will read its responses aloud when this feature is enabled.

---


## License

This project is licensed under the MIT License. See the [LICENSE](https://opensource.org/license/MIT) file for more details.

---
``` 
