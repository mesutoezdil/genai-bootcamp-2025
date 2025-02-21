import whisper

# Load the Whisper model
model = whisper.load_model("small")  # You can use 'base', 'medium', or 'large'

# Transcribe the Chinese audio
result = model.transcribe("audio.mp3", language="zh")  # 'zh' is for Chinese

# Save the transcript in Chinese
with open("transcript_zh.txt", "w", encoding="utf-8") as f:
    f.write(result["text"])

print("Chinese transcription completed. Saved as transcript_zh.txt")
