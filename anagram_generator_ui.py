import itertools
import streamlit as st
import re
from collections import Counter
import datetime

# טעינת קובץ מילים בעברית (יש להוסיף קובץ מילים תקני)
def load_hebrew_dictionary():
    try:
        with open("hebrew_words.txt", "r", encoding="utf-8") as f:
            words = set(word.strip() for word in f.readlines())
        return words
    except FileNotFoundError:
        return set()

hebrew_dict = load_hebrew_dictionary()

# פונקציה לניקוי הטקסט
def clean_text(text):
    return re.sub(r"[^א-ת]", "", text)

# בדיקה אם כל תווי מילה קיימים במאגר התווים של המשפט
def is_valid_word(word, letter_bank):
    return not (Counter(word) - letter_bank)

# יצירת מילים מתוך אותיות המשפט
def generate_sentence_anagrams(sentence):
    letters = clean_text(sentence)
    letter_bank = Counter(letters)
    valid_words = [w for w in hebrew_dict if is_valid_word(w, letter_bank) and len(w) > 1]
    sorted_words = sorted(valid_words, key=lambda w: (-len(w), w))
    return sorted_words[:200]  # עד 200 מילים אפשריות

# פונקציה לשמירת תוצאות לקובץ טקסט
def save_results_to_file(results):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"anagram_results_{timestamp}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(results))
    return filename

# הגדרת ממשק משתמש עם Streamlit
st.set_page_config(page_title="יוצר אנגרמות בעברית", layout="centered", page_icon="🧠")

st.markdown("""
    <div style='text-align: center; background-color: #f0f0f5; padding: 20px; border-radius: 15px;'>
        <h1 style='color: #6a0dad;'>🧠 יוצר אנגרמות חכם</h1>
        <p>הכנס מילה או משפט בעברית, וקבל אנגרמות תקינות עם משמעות</p>
    </div>
""", unsafe_allow_html=True)

user_input = st.text_area("הכנס מילה או משפט בעברית:", "", height=100)
save_results = st.checkbox("📥 שמור את התוצאות כקובץ")

if st.button("🔍 צור אנגרמות"):
    if not user_input.strip():
        st.warning("אנא הכנס טקסט תקני בעברית")
    else:
        results = generate_sentence_anagrams(user_input)
        if results:
            st.success(f"נמצאו {len(results)} מילים תקינות מהמשפט:")
            st.markdown(", ".join(results))

            if save_results:
                filename = save_results_to_file(results)
                st.info(f"✅ התוצאות נשמרו לקובץ בשם: {filename}")
        else:
            st.error("לא נמצאו מילים תקינות במילון על בסיס האותיות שהוזנו")

st.markdown("""
    <hr style='margin-top:40px;'>
    <div style='text-align: center;'>
        <small style='color:gray;'>מונע על ידי Python ו-Streamlit • גרסה מתקדמת • מחולל אנגרמות בעברית</small>
    </div>
""", unsafe_allow_html=True)