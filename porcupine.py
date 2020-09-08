#!/usr/bin/env python3
import struct
import pyaudio
import pvporcupine
from matrix.pushtotalk import main

porcupine = None
pa = None
audio_stream = None

def picovoice():
    try:
        porcupine = pvporcupine.create(keywords=["picovoice", "blueberry"])

        pa = pyaudio.PyAudio()

        audio_stream = pa.open(
                        rate=porcupine.sample_rate,
                        channels=1,
                        format=pyaudio.paInt16,
                        input=True,
                        frames_per_buffer=porcupine.frame_length)

        while True:
            pcm = audio_stream.read(porcupine.frame_length)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

            keyword_index = porcupine.process(pcm)

            if keyword_index >= 0:
                print("Hotword Detected")
                audio_stream.close()
                main()
                print("Done")
    except KeyboardInterrupt:
        if porcupine is not None:
            porcupine.delete()
            print("deleting porc")

        if audio_stream is not None:
            audio_stream.close()
            print("closing stream")

        if pa is not None:
            pa.terminate()
            print("terminating pa")
        
            exit(0)
                
    finally:
        if porcupine is not None:
            porcupine.delete()
            print("deleting porc")

        if audio_stream is not None:
            audio_stream.close()
            print("closing stream")

        if pa is not None:
            pa.terminate()
            print("terminating pa")
        
        picovoice()

picovoice()
