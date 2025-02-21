from googletrans import Translator

# Read the Chinese transcript
with open("transcript_zh.txt", "r", encoding="utf-8") as f:
    chinese_text = f.read()

# Initialize the translator
translator = Translator()

# Translate from Chinese to English
translated_text = translator.translate(chinese_text, src="zh-CN", dest="en").text

# Save the English translation
with open("transcript_en.txt", "w", encoding="utf-8") as f:
    f.write(translated_text)

print("Translation to English completed. Saved as transcript_en.txt")
