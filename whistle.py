import numpy as np
import time
from gtts import gTTS
from pydub import AudioSegment
import os

# Audio Parameters
sample_rate = 44100  # Standard sampling rate
duration = 0.5  # Duration of each whistle in seconds
frequency = 800  # Base frequency of the whistle in Hz

def generate_whistle(duration, frequency):
    t = np.linspace(0, duration, int(duration * sample_rate), endpoint=False)
    wave = np.sin(2 * np.pi * frequency * t)
    noise = 0.1 * np.random.randn(len(wave))
    wave += noise
    wave *= 0.3  # Adjust amplitude for comfortable listening
    return wave

def play_whistle(whistle):
    AudioSegment(whistle.tobytes(), frame_rate=sample_rate, sample_width=2, channels=1).export("temp_whistle.wav", format="wav")
    os.system("start temp_whistle.wav")  # Play the audio file
    time.sleep(duration)  # Wait for the audio to finish playing
    os.remove("temp_whistle.wav")  # Remove the temporary audio file

def text_to_rhythm(text):
    words = text.split()
    word_durations = []
    for word in words:
        try:
            word_tts = gTTS(word)
            word_tts.save("temp_word.mp3")
            word_audio = AudioSegment.from_mp3("temp_word.mp3")
            word_durations.append(len(word_audio))
            os.remove("temp_word.mp3")
        except:
            word_durations.append(0)
    return word_durations

def main():
    # Example usage
    text = "Hello world, how are you today?"
    rhythm = text_to_rhythm(text)
    for duration in rhythm:
        if duration > 0:
            whistle = generate_whistle(duration / 1000, frequency)  # Convert duration to seconds
            play_whistle(whistle)
        else:
            time.sleep(0.5)  # Pause for words with zero duration

if __name__ == "__main__":
    main()
