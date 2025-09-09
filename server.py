from vosk import Model, KaldiRecognizer
import pyaudio
import json, threading
import time


model = None
recognizer = None
loaded = False

# Lista de palavras para reconhecer
commands = '["jump", "attack", "run", "stop", "defend"]'

def load_model():
    global model, recognizer, loaded
    print("Carregando modelo, aguarde...")
    model = Model(r"C:\\Users\\user\\Documents\\Workspace\\Godot\\godot-voice-controller\\vosk-model-en")
    recognizer = KaldiRecognizer(model, 16000, commands)
    loaded = True
    print("Modelo carregado com sucesso!")

# inicia thread para carregar o modelo
threading.Thread(target=load_model, daemon=True).start()

# espera até que o modelo esteja pronto
while not loaded:
    time.sleep(0.5)

# inicia captura de áudio
capture = pyaudio.PyAudio()
stream = capture.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=4096)
stream.start_stream()

print("Ready to listen...")

while True:
    data = stream.read(4096, exception_on_overflow=False)
    if recognizer.AcceptWaveform(data):
        result = json.loads(recognizer.Result())
        print("You say:", result.get("text", ""))
