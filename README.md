# AITourGuide Project

This project is a voice-controlled assistant developed as an undergraduate project at the Department of Electrical & Computer Engineering, University of Peloponnese for the course "Digital Sound and Image Processing." The project was performed by Papadimitriou E. and Lalousi S., under the supervision of Associate Prof. Athanasios Koutras.

## Description

The TourGuide allows users to record audio, transcribe it to text, and interact with an AI-based conversation system. The project incorporates the following functionalities:

1. **Audio Recording:** The program records audio from the user's microphone in real-time and saves it as a WAV file.
2. **Speech-to-Text Transcription:** It utilizes Google Cloud's Speech-to-Text API for transcribing recorded audio into text.
3. **AI Response Generation:** The transcribed text is processed by the GPT-4 model via OpenAI's API to generate intelligent responses based on the conversation history.
4. **Text-to-Speech Synthesis:** The response is then converted back to speech using ElevenLabs' Text-to-Speech API, providing a seamless conversational experience.

The project aims to combine multiple APIs to create a functional voice assistant capable of real-time interaction with the user.

## Features

- **Real-time audio recording and transcription**
- **Conversational AI interaction using OpenAI's GPT models**
- **Voice synthesis for responding to user queries**
- **Keyboard-based controls for starting, stopping, and quitting the program**

## Requirements

To run this project, the following dependencies must be installed:

- Python 3.7 or higher
- `pyaudio` for audio input
- `google-cloud-speech` for speech-to-text transcription
- `openai` for interacting with the GPT models
- `elevenlabs` for text-to-speech conversion

You will also need to set up API keys for the following services:

- **OpenAI**: For GPT-4 (or GPT-3.5) integration
- **Google Cloud Speech-to-Text**: Requires a service account key
- **ElevenLabs Text-to-Speech**: For generating audio responses

## Setup Instructions

1. **Install Python Dependencies:**
   ```
   pip install pyaudio google-cloud-speech openai elevenlabs
   ```

2. **Configure API Keys:**
   - Set your OpenAI API key and ElevenLabs API key in the code.
   - Ensure your Google Cloud Speech-to-Text service account credentials are available and referenced in the code as `my_application.json`.

3. **Run the Application:**
   ```
   python Voice_Assistant.py
   ```

   - Press `'r'` to start recording, `'s'` to stop recording, and `'q'` to quit the application.

## Usage Notes

- Make sure your microphone is set up correctly, as the program relies on audio input.
- You may adjust the speech recognition configuration (e.g., language settings, speech contexts) in the code if needed.
- Be aware of any rate limits and usage quotas associated with the APIs used.

## License

This project is provided for educational purposes and may not be used for commercial applications without proper licensing.

---

Feel free to modify any sections to better fit the requirements or add more details.
