import pyaudio
import wave
import os
import logging
from faster_whisper import WhisperModel

# Configuración básica de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constantes para configuración de audio y modelo
CHUNK_SIZE = 1024  # Tamaño del bloque de datos de audio
RATE = 16000  # Tasa de muestreo en Hz
CHANNELS = 1  # Número de canales de audio (mono)
FORMAT = pyaudio.paInt16  # Formato de audio (16-bit PCM)
MODEL_SIZE = "medium"  # Tamaño del modelo Whisper para la transcripción
TEMP_CHUNK_FILE = 'temp_chunk.wav'  # Archivo temporal donde se guarda cada bloque de audio
LOG_FILE = 'transcription_log.txt'  # Archivo donde se almacenará la transcripción acumulada

class AudioTranscriber:
    """
    Clase que maneja la grabación de audio en tiempo real, su transcripción mediante Whisper,
    y la eliminación de archivos temporales. Encapsula las funcionalidades clave para gestionar
    el flujo de audio y transcripción de manera eficiente.
    """
    
    def __init__(self, model_size=MODEL_SIZE, device="cuda", compute_type="float16"):
        """
        Inicializa la clase con el modelo Whisper y la configuración de PyAudio.

        :param model_size: Tamaño del modelo Whisper a utilizar.
        :param device: Dispositivo en el que se correrá el modelo (e.g., 'cuda' para GPU).
        :param compute_type: Tipo de cómputo a utilizar para el modelo (e.g., 'float16').
        """
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type)
        self.p = pyaudio.PyAudio()
        self.stream = None

    def start_stream(self):
        """
        Inicia el stream de audio usando PyAudio con los parámetros de formato y tasa de muestreo configurados.
        """
        self.stream = self.p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK_SIZE)
        logging.info("Audio stream started.")

    def stop_stream(self):
        """
        Detiene y cierra el stream de audio y libera los recursos de PyAudio.
        """
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
            self.p.terminate()
            logging.info("Audio stream stopped.")

    def record_chunk(self, file_path=TEMP_CHUNK_FILE, chunk_length=1):
        """
        Graba un bloque de audio (chunk) y lo guarda en un archivo temporal.

        :param file_path: Ruta del archivo temporal donde se almacenará el audio.
        :param chunk_length: Duración en segundos del bloque de audio a grabar.
        """
        frames = []
        for _ in range(0, int(RATE / CHUNK_SIZE * chunk_length)):
            data = self.stream.read(CHUNK_SIZE)
            frames.append(data)

        # Guardar el bloque de audio en un archivo WAV
        with wave.open(file_path, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(self.p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))

        logging.info(f"Chunk recorded to {file_path}")

    def transcribe_chunk(self, file_path):
        """
        Transcribe el bloque de audio almacenado en el archivo temporal utilizando el modelo Whisper.

        :param file_path: Ruta del archivo de audio a transcribir.
        :return: Transcripción en texto del audio.
        """
        segments, _ = self.model.transcribe(file_path)
        transcription = "".join(segment.text for segment in segments)
        logging.info(f"Chunk transcribed: {transcription}")
        return transcription

    def clean_up(self, file_path):
        """
        Elimina el archivo temporal de audio después de la transcripción.

        :param file_path: Ruta del archivo a eliminar.
        """
        if os.path.exists(file_path):
            os.remove(file_path)
            logging.info(f"Temporary file {file_path} removed.")

def main():
    """
    Función principal que controla el flujo de grabación, transcripción y manejo del audio en tiempo real.
    Graba el audio en bloques, los transcribe, imprime la transcripción y guarda el resultado acumulado en un archivo.
    """
    transcriber = AudioTranscriber()
    accumulated_transcription = ""  # Variable que acumula la transcripción completa

    try:
        # Inicia el stream de audio
        transcriber.start_stream()

        # Bucle principal de grabación y transcripción
        while True:
            # Graba un bloque de audio
            transcriber.record_chunk()
            
            # Transcribe el bloque grabado
            transcription = transcriber.transcribe_chunk(TEMP_CHUNK_FILE)
            print(transcription)

            # Acumula la transcripción
            accumulated_transcription += transcription + " "
            
            # Elimina el archivo temporal de audio
            transcriber.clean_up(TEMP_CHUNK_FILE)

    except KeyboardInterrupt:
        # Captura la interrupción del teclado (Ctrl+C) y guarda la transcripción acumulada en un archivo
        logging.info("Transcription stopped by user.")
        with open(LOG_FILE, 'w') as log_file:
            log_file.write(accumulated_transcription)
        logging.info(f"Final transcription written to {LOG_FILE}")

    except Exception as e:
        # Manejo de cualquier error inesperado
        logging.error(f"An error occurred: {e}")

    finally:
        # Asegura que el stream de audio se detenga y los recursos se liberen correctamente
        transcriber.stop_stream()
        logging.info(f"LOG: {accumulated_transcription}")

# Punto de entrada del script
if __name__ == '__main__':
    main()
