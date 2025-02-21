# Video Translation & Subtitling Pipeline

## **Project Overview**
This project automates the transcription, translation, and subtitle embedding process for videos using OpenAI Whisper, Deep Translator, and FFmpeg. It extracts speech from a **Chinese (Mandarin) video**, transcribes it into **Chinese text**, translates it into **English**, and embeds **English subtitles** into the video.

---

## **Project Structure**
```
📂 week_2_whisperTask
├── audio.mp3              # Extracted audio from the video
├── chinese.mp4            # Input video in Chinese
├── generate_srt.py        # Script to generate Chinese subtitles
├── subtitles_en.srt       # Translated English subtitles (SRT format)
├── subtitles_zh.srt       # Original Chinese subtitles (SRT format)
├── output.mp4             # Final video with burned-in English subtitles
├── transcribe.py          # Script to transcribe Chinese audio to text
├── transcript_zh.txt      # Transcribed Chinese text
├── translate_srt.py       # Script to translate subtitles from Chinese to English
└── README.md              # Project documentation (this file)
```

---

## **Installation & Setup**

### **1. Install Dependencies**
Ensure Python and FFmpeg are installed. Install the required libraries:
```bash
pip install openai-whisper deep-translator ffmpeg-python
```
For FFmpeg, install it via Homebrew on macOS:
```bash
brew install ffmpeg
```

---

## **Processing Steps**

### **1. Extract Audio from Video**
Run the following command to extract audio from the input video:
```bash
ffmpeg -i chinese.mp4 -vn -acodec mp3 audio.mp3
```
This creates an `audio.mp3` file from `chinese.mp4`.

---

### **2. Transcribe Chinese Audio**
Run the transcription script to generate a **Chinese transcript**:
```bash
python transcribe.py
```
This outputs a transcript file `transcript_zh.txt`.

---

### **3. Generate Chinese Subtitles (.srt)**
Generate a **Chinese subtitle file** using:
```bash
python generate_srt.py
```
This creates `subtitles_zh.srt`.

---

### **4. Translate Subtitles from Chinese to English**
Run the translation script to generate an English subtitle file:
```bash
python translate_srt.py
```
This produces `subtitles_en.srt`.

---

### **5. Convert `.srt` to `.ass` for FFmpeg**
If necessary, convert `.srt` subtitles to `.ass` format:
```bash
ffmpeg -i subtitles_en.srt subtitles_en.ass
```

---

### **6. Burn English Subtitles into Video**
Use FFmpeg to embed the English subtitles permanently:
```bash
ffmpeg -i chinese.mp4 -vf "ass=subtitles_en.ass" -c:v libx264 -c:a copy output.mp4
```
This generates `output.mp4` with **hardcoded English subtitles**.

---

## **Troubleshooting**

### **1. Module Not Found Errors**
If a module is missing, reinstall the package:
```bash
pip install <module_name>
```

### **2. FFmpeg Not Recognizing Subtitles**
- Ensure subtitles are in **`.ass` format**
- Verify timestamps in `.srt` follow the format:
  ```
  1
  00:00:00,000 --> 00:00:02,000
  Subtitle text here.
  ```
- If FFmpeg fails to burn subtitles, try using:
  ```bash
  ffmpeg -i chinese.mp4 -vf "subtitles=subtitles_en.srt:force_style='Fontsize=24'" -c:v libx264 -c:a copy output.mp4
  ```

---

## **Conclusion**
This project successfully transcribes a **Chinese video**, translates it into **English**, and **burns subtitles** into the final video using FFmpeg.

### **Future Improvements**
✅ Improve subtitle accuracy with Whisper Large model  
✅ Add automatic timestamp adjustments  
✅ Support multiple languages for translation  
