import os
import pyaudio
import wave
import tempfile
import openai
from google.cloud import speech
import sys
import threading
import time
from elevenlabs import play
from elevenlabs.client import ElevenLabs

# Set your API keys
chat_gpt_key = 'USE YOUR CHAT-GPT KEY HERE'
ELEVENLABS_KEY = 'USE YOUR ELEVENLABS KEY HERE'

openai.api_key = chat_gpt_key
client = ElevenLabs(api_key=ELEVENLABS_KEY)

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms
FORMAT = pyaudio.paInt16
CHANNELS = 1

# Global variable to control the recording
is_recording = False
stop_program = False
conversation_history = [{"role": "system", "content": "You are a helpful assistant."}]

def record_audio(file_path):
    global is_recording

    # Suppress ALSA messages by redirecting stderr to /dev/null
    with open(os.devnull, 'w') as devnull:
        audio = pyaudio.PyAudio()

        # Open stream
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True,
                            frames_per_buffer=CHUNK,
                            stream_callback=None)

        frames = []

        print("Press 'r' to start recording and 's' to stop recording.")
        while not is_recording:
            pass  # Wait for the user to start recording

        print("Recording...")
        while is_recording:
            data = stream.read(CHUNK)
            frames.append(data)

        print("Recording stopped.")

        # Stop and close the stream
        stream.stop_stream()
        stream.close()
        audio.terminate()

        # Save the recorded data as a WAV file
        with wave.open(file_path, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(audio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))


def transcribe_audio(file_path):
    client = speech.SpeechClient()

    with open(file_path, 'rb') as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        
        language_code="en-US",
        #language_code="el-GR",
        enable_automatic_punctuation=True,
        model="latest_long",  # Use the enhanced model
        #model="default",
        speech_contexts=[speech.SpeechContext(
            phrases=["OpenAI", "ChatGPT", "API", "transcription", "recognition"],
            boost=20.0
        )],
    )

    response = client.recognize(config=config, audio=audio)

    # Extract the transcription from the response
    for result in response.results:
        return result.alternatives[0].transcript

    return ""

def get_gpt_response(prompt, conversation_history):
    conversation_history.append({"role": "user", "content": prompt})

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",  # Use the appropriate model
        #model = "gpt-3.5-turbo",
        messages=conversation_history,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )
    
    message = response['choices'][0]['message']['content'].strip()
    conversation_history.append({"role": "assistant", "content": message})
    return message

def generate_and_play_audio(text):
    audio = client.generate(
        text=text,
        voice="Bill",  # You can change the voice based on available options
        model="eleven_multilingual_v2"
    )
    play(audio)

def listen_for_input():
    global is_recording, stop_program

    while True:
        user_input = input().strip().lower()
        if user_input == 'r':
            is_recording = True
        elif user_input == 's':
            is_recording = False
        elif user_input == 'q':
            stop_program = True
            break

def main():
    global stop_program, conversation_history
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "my_application.json"  # Update with your service account key file path

    print("Press 'r' to start recording, 's' to stop recording, and 'q' to quit the program.")
    
    input_thread = threading.Thread(target=listen_for_input)
    input_thread.daemon = True
    input_thread.start()

    while not stop_program:
        if is_recording:
            # Record audio
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
                record_audio(temp_audio_file.name)
                temp_audio_file_path = temp_audio_file.name

            # Transcribe audio
            print("Transcribing audio...")
            transcription = transcribe_audio(temp_audio_file_path)
            os.remove(temp_audio_file_path)  # Clean up the temporary file

            if transcription:
                print("You said:", transcription)

                # Get response from ChatGPT
                print("Getting response from ChatGPT...")
                response = get_gpt_response(transcription, conversation_history)
                print("ChatGPT Response:", response)

                # Generate and play audio
                print("Generating and playing audio...")
                generate_and_play_audio(response)
            else:
                print("No transcription could be made. Please try again.")
        else:
            time.sleep(0.1)  # Small delay to prevent high CPU usage

if __name__ == "__main__":
    main()
