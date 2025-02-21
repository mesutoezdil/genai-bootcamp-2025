from datetime import timedelta
import whisper

# Load the Whisper model
model = whisper.load_model("small")

# Transcribe the audio with timestamps
result = model.transcribe("audio.mp3", language="zh")

# Function to format time for SRT subtitles
def format_time(seconds):
    return str(timedelta(seconds=int(seconds))).replace(".", ",") + "0"

srt_content = ""
for i, segment in enumerate(result["segments"]):
    start = format_time(segment["start"])
    end = format_time(segment["end"])
    text = segment["text"]
    
    srt_content += f"{i+1}\n{start} --> {end}\n{text}\n\n"

# Save the Chinese SRT file
with open("subtitles_zh.srt", "w", encoding="utf-8") as f:
    f.write(srt_content)

print("Chinese subtitles generated: subtitles_zh.srt")
