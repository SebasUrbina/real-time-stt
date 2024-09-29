
## Real-Time Audio Transcription with Whisper

This repository contains a Python script that records audio in real-time, transcribes it using the Whisper model from [`faster-whisper`](https://github.com/SYSTRAN/faster-whisper), and stores the transcriptions. The transcription process runs continuously and the results are saved in a log file. 

### File Structure
- `audio_transcriber.py`: The main script that handles real-time audio recording and transcription.
- `requirements.txt`: A file listing the Python dependencies required to run the script.
- `README.md`: This file, providing documentation on how to use the project.

### How It Works
The script captures audio from your microphone, processes it in chunks, transcribes each chunk using the Whisper model, and logs the transcriptions. The transcription stops when the user interrupts the script (e.g., by pressing `Ctrl+C`).

### Prerequisites
Before running the script, ensure that your system meets the following requirements:
- Python 3.8 or higher
- A CUDA-capable GPU (if you plan to use GPU for faster transcription with the Whisper model)
- `PyAudio` installed to capture real-time audio
- Whisper model through `faster-whisper` for transcription

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/sebasurbina/real-time-stt.git
   cd real-time-stt
   ```

2. **Create a virtual environment** (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   Install the required Python packages using `pip`:
   ```bash
   pip install -r requirements.txt
   ```

4. **Install `PyAudio`**:
   Depending on your platform, you may need to install PyAudio separately:
   - On Linux:
     ```bash
     sudo apt-get install portaudio19-dev
     pip install pyaudio
     ```
   - On MacOS (with Homebrew):
     ```bash
     brew install portaudio
     pip install pyaudio
     ```
   - On Windows:
     You can download and install PyAudio from the [official site](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio).

### Usage

1. **Run the script**:
   Start the transcription by running the main script `audio_transcriber.py`:
   ```bash
   python audio_transcriber.py
   ```

2. **Interrupt the process**:
   The script will continue recording and transcribing until you manually stop it by pressing `Ctrl+C`. Once stopped, the transcriptions are saved in a file called `transcription_log.txt`.

### Example Output

```bash
2024-09-28 12:34:56 - INFO - Audio stream started.
2024-09-28 12:34:58 - INFO - Chunk recorded to temp_chunk.wav
2024-09-28 12:34:59 - INFO - Chunk transcribed: "Hello, how are you doing today?"
2024-09-28 12:35:00 - INFO - Temporary file temp_chunk.wav removed.
```

The final transcription will be logged in `transcription_log.txt`.

### Configuration

You can adjust the audio recording settings, the Whisper model size, and file paths by modifying the constants in the script:

- `CHUNK_SIZE`: Adjust the size of the audio chunk to capture in each loop.
- `RATE`: The sampling rate for recording audio (default: 16000 Hz).
- `MODEL_SIZE`: The size of the Whisper model to use (e.g., "tiny", "base", "medium").

### Requirements

All Python package dependencies are listed in `requirements.txt`. The primary libraries used in this project are:

- `faster-whisper`
- `pyaudio`
- `wave`
- `os`
- `logging`

### License

This project is licensed under the MIT License.
