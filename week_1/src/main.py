from db.database import Database

def main():
    db = Database()
    
    # Example: Add a test word
    word_id = db.add_word(
        simplified="你好",
        pinyin="nǐ hǎo",
        english="hello",
        parts={"characters": ["你", "好"]}
    )
    
    # Example: Get all words
    words = db.get_words()
    for word in words:
        print(f"Word: {word['simplified']} ({word['pinyin']}) - {word['english']}")

if __name__ == "__main__":
    main()
