# Video Translation & Subtitling Pipeline

This guide describes how to **transcribe**, **translate**, and **embed subtitles** into a video using **OpenAI Whisper**, **Deep Translator**, and **FFmpeg**. It automates the entire workflow—from audio extraction to hardcoding the final translated subtitles.  

By following this step-by-step process, you’ll seamlessly convert **Chinese (Mandarin) audio** into readable **English subtitles** burned into the video.  

---

## Table of Contents

1. [Introduction & Objectives](#1-introduction--objectives)  
2. [Key Components](#2-key-components)  
3. [Project Structure](#3-project-structure)  
4. [Installation & Setup](#4-installation--setup)  
5. [Pipeline Overview](#5-pipeline-overview)  
   1. [Extract Audio from Video](#51-extract-audio-from-video)  
   2. [Transcribe Chinese Audio](#52-transcribe-chinese-audio)  
   3. [Generate Chinese Subtitles (.srt)](#53-generate-chinese-subtitles-srt)  
   4. [Translate Subtitles to English](#54-translate-subtitles-to-english)  
   5. [Convert .srt to .ass](#55-convert-srt-to-ass)  
   6. [Burn English Subtitles into Video](#56-burn-english-subtitles-into-video)  
6. [Troubleshooting](#6-troubleshooting)  
   1. [Missing Modules](#61-missing-modules)  
   2. [FFmpeg Subtitle Issues](#62-ffmpeg-subtitle-issues)  
7. [Best Practices & Optimization](#7-best-practices--optimization)  
8. [Future Improvements](#8-future-improvements)  
9. [Conclusion](#9-conclusion)

---

## 1. Introduction & Objectives

In multimedia and content localization, the need to **transcribe** and **translate** video content is ever-growing. The **Video Translation & Subtitling Pipeline** project addresses this demand by offering an automated workflow for:

- **Extracting** audio from a video file.  
- **Transcribing** the spoken Mandarin into text (via **OpenAI Whisper**).  
- **Translating** the text from Chinese to English (using **Deep Translator**).  
- **Embedding** the final English subtitles into the video (with **FFmpeg**).  

### Core Goals

- Provide a **repeatable** process that can be extended to other languages.  
- Minimize **manual** steps, ensuring a smoother pipeline from raw media to a fully subtitled video.  
- Offer **flexibility** for advanced users to tweak transcription or translation settings.

---

## 2. Key Components

1. **OpenAI Whisper**  
   - Used for **speech recognition** and transcription.  
   - Noted for its high accuracy, especially for Mandarin audio.  

2. **Deep Translator**  
   - Provides an API-based **translation** engine.  
   - Transforms Chinese subtitles into English text.  

3. **FFmpeg**  
   - A powerful, open-source tool for **audio/video processing**.  
   - Used here to extract audio, convert file formats, and **embed subtitles**.  

---

## 3. Project Structure

A recommended directory layout to keep code and media assets organized:

```
week_2_whisperTask/
├── audio.mp3               # Extracted audio track from the video
├── chinese.mp4             # Original input video with Mandarin audio
├── generate_srt.py         # Python script to generate .srt subtitles in Chinese
├── subtitles_en.srt        # Translated English subtitles (SRT format)
├── subtitles_zh.srt        # Original Chinese subtitles (SRT format)
├── output.mp4              # Final video with hardcoded English subtitles
├── transcribe.py           # Python script to transcribe audio to Chinese text
├── transcript_zh.txt       # Plain text transcript of the Mandarin speech
├── translate_srt.py        # Python script to translate .srt from Chinese to English
└── README.md               # Project documentation (this file)
```

> **Note**: The filenames are suggestions. You can rename them to fit your own naming conventions or organizational preferences.

---

## 4. Installation & Setup

Before running the pipeline, ensure both **Python** and **FFmpeg** are installed on your system.

### 4.1 Python Package Installation

1. **Install Required Libraries**:
   ```bash
   pip install openai-whisper deep-translator ffmpeg-python
   ```
   - **`openai-whisper`**: For speech-to-text functionality.
   - **`deep-translator`**: For translating the transcript from Chinese to English.
   - **`ffmpeg-python`**: A Pythonic interface for FFmpeg commands.

2. **FFmpeg**:
   - If you are on **macOS**, install via Homebrew:
     ```bash
     brew install ffmpeg
     ```
   - On **Windows** or **Linux**, you can download it from [ffmpeg.org](https://ffmpeg.org/) or use your OS package manager.

> **Tip**: Verify your installation by running `ffmpeg -version`. You should see version details if FFmpeg is successfully installed.

---

## 5. Pipeline Overview

The pipeline is divided into six main steps, from audio extraction to embedding subtitles in the final video.

---

### 5.1 Extract Audio from Video

**Goal**: Obtain an audio-only file (e.g., `.mp3`) from your original Mandarin video.

**Command**:
```bash
ffmpeg -i chinese.mp4 -vn -acodec mp3 audio.mp3
```
- **`-i chinese.mp4`**: Input video file.
- **`-vn`**: Disables video processing (only extracts audio).
- **`-acodec mp3`**: Specifies the MP3 audio codec.
- **`audio.mp3`**: Output file containing the audio stream.

---

### 5.2 Transcribe Chinese Audio

**Goal**: Convert the Mandarin speech in `audio.mp3` into Chinese text.

1. **Run**:
   ```bash
   python transcribe.py
   ```
2. **Result**:
   - A file named `transcript_zh.txt` containing the text transcript in Chinese.

**Script Highlights (`transcribe.py`)**:
- Uses **OpenAI Whisper** for high-accuracy speech recognition.  
- Optionally, you can customize the `model` size or additional parameters to refine accuracy.

---

### 5.3 Generate Chinese Subtitles (.srt)

**Goal**: Convert the raw transcript into a properly timed `.srt` file.

1. **Run**:
   ```bash
   python generate_srt.py
   ```
2. **Result**:
   - A file named `subtitles_zh.srt` with time-coded Chinese subtitles.

**Script Highlights (`generate_srt.py`)**:
- Parses `transcript_zh.txt` and assigns line breaks & timestamps.  
- Each subtitle block typically follows the format:  
  ```plaintext
  1
  00:00:00,000 --> 00:00:05,000
  这是一条示例字幕
  ```

---

### 5.4 Translate Subtitles to English

**Goal**: Translate the Chinese `.srt` into English.

1. **Run**:
   ```bash
   python translate_srt.py
   ```
2. **Result**:
   - A file named `subtitles_en.srt` with each subtitle entry translated to English.

**Script Highlights (`translate_srt.py`)**:
- Reads `subtitles_zh.srt` line by line.  
- Calls **Deep Translator** (or another translation service) for each block of text.  
- Preserves timestamps while replacing the content with English.

---

### 5.5 Convert `.srt` to `.ass`

**Goal**: Some FFmpeg commands may require `.ass` subtitles for correct rendering or advanced styling.  

```bash
ffmpeg -i subtitles_en.srt subtitles_en.ass
```
- **`subtitles_en.srt`**: Input subtitle file in SRT format.
- **`subtitles_en.ass`**: Output subtitle file in ASS format.

> **Note**: The `.ass` format allows for more detailed styling (e.g., fonts, colors, positions). If you prefer SRT, you can skip this step, although certain FFmpeg filters may behave differently.

---

### 5.6 Burn English Subtitles into Video

**Goal**: Produce a new video file with **hardcoded** (burned-in) English subtitles.

1. **Command**:
   ```bash
   ffmpeg -i chinese.mp4 -vf "ass=subtitles_en.ass" -c:v libx264 -c:a copy output.mp4
   ```
   - **`-i chinese.mp4`**: The original video.
   - **`-vf "ass=subtitles_en.ass"`**: The video filter that applies the `.ass` subtitles layer.  
   - **`-c:v libx264`**: Encodes video with x264 codec.  
   - **`-c:a copy`**: Copies the existing audio without re-encoding.
   - **`output.mp4`**: The final video file.

> **Alternate Approach**: If you prefer to **overlay SRT** directly, you can use:
  ```bash
  ffmpeg -i chinese.mp4 \
         -vf "subtitles=subtitles_en.srt:force_style='Fontsize=24'" \
         -c:v libx264 -c:a copy output.mp4
  ```

---

## 6. Troubleshooting

### 6.1 Missing Modules

If you encounter `ModuleNotFoundError` or similar messages:

1. Double-check the library name in your Python script.  
2. Reinstall the module:
   ```bash
   pip install <module_name>
   ```
3. Confirm you’re using the same **Python environment** (virtualenv, conda, or system-wide) in which you installed the modules.

---

### 6.2 FFmpeg Subtitle Issues

1. **Subtitle Timestamps**  
   - Ensure your `.srt` file uses the standard format:
     ```plaintext
     1
     00:00:00,000 --> 00:00:02,000
     This is a sample subtitle
     ```
   - Missing or inconsistent timestamps may lead to subtitles not displaying properly.

2. **Ass Filter vs. SRT Filter**  
   - When burning subtitles, specify the correct filter. `ass=subtitles_en.ass` is used for `.ass` format, while `subtitles=subtitles_en.srt` is for `.srt`.

3. **Font and Styling**  
   - If the text is not rendering or looks off, customize the `force_style` parameter (font name, size, color).  
   - Example:
     ```bash
     -vf "subtitles=subtitles_en.srt:force_style='FontName=Arial,FontSize=28'"
     ```

4. **No Subtitles Burned**  
   - Check if FFmpeg outputs any warning messages about your subtitle file.  
   - Ensure the `.srt` or `.ass` file is in the same directory and spelled correctly in the command.

---

## 7. Best Practices & Optimization

1. **Use Higher-Accuracy Models**  
   - If your system can handle it, consider larger Whisper models to improve transcription accuracy.

2. **Adjust Translation Service**  
   - Deep Translator can be swapped for other providers (e.g., Google Translate, Microsoft Translator) as needed.  
   - Evaluate costs or API limits if using a paid service.

3. **Batch Translations**  
   - If your subtitles are very long, batch process the lines to reduce API calls and improve efficiency.

4. **Automate with a Single Script**  
   - Combine all steps (audio extraction → transcription → subtitle generation → translation → burning) into one orchestrated Python script for ease of use.

---

## 8. Future Improvements

1. **Timestamp Alignment**  
   - Dynamically adjust timestamps if transcription timestamps differ from actual speech segments.

2. **Multi-Language Support**  
   - Extend the pipeline to other languages (e.g., Japanese, Spanish).  
   - Store or toggle language pairs for quick reconfiguration.

3. **Whisper Large Model**  
   - Use **Whisper Large** to improve accuracy for complex audio scenarios (background noise, multiple speakers, etc.).

4. **Enhanced Styling**  
   - Incorporate `.ass` styling features like text outlines, shadows, or custom positioning for more professional subtitle presentations.

---

## 9. Conclusion

With this **Video Translation & Subtitling Pipeline**, you can **extract** Chinese audio, **transcribe** it to text, **translate** that text into English, and **burn** the translated subtitles into a new video file—all in a largely automated fashion. This workflow is not only scalable but also customizable, allowing you to plug in different transcription or translation services, tailor your subtitle styling, and manage various language pairs.

By following these steps and best practices, you’ll maintain a **straightforward**, **repeatable**, and **efficient** approach to localizing video content. If you encounter any challenges, consult the **Troubleshooting** section for tips or explore further enhancements to refine the pipeline for your specific needs.
