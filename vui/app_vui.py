from vui.s2t.audio_transcriber import AudioTranscriber

AUDIO_PATH = "rbg3.m4a"

if __name__ == "__main__":
    transcriber = AudioTranscriber()

    #1 trascrizione
    print("Transcribing audio...")
    transcribed_text = transcriber.transcribe_text_only(AUDIO_PATH)
    print("Transcribed text:")
    print(transcribed_text)