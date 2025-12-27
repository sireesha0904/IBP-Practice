import streamlit as st
import json
import random
import streamlit.components.v1 as components

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="IBP Practice Test", layout="centered")
st.title("📘 IBP Full Practice Test")

# ------------------ BLOCK TAB SWITCH ------------------
components.html(
    """
    <script>
    document.addEventListener("visibilitychange", function () {
        if (document.hidden) {
            alert("⚠️ Tab switching is not allowed during the test!");
        }
    });
    window.onblur = function () {
        alert("⚠️ Do not switch windows during the test!");
    };
    </script>
    """,
    height=0,
)

# ------------------ LOAD QUESTIONS ------------------
@st.cache_data
def load_questions():
    with open("questions.json", "r", encoding="utf-8") as f:
        return json.load(f)

raw_questions = load_questions()

# ------------------ INITIALIZE SESSION ------------------
if "initialized" not in st.session_state:
    # Shuffle questions
    random.shuffle(raw_questions)

    # Shuffle options per question
    questions = []
    for q in raw_questions:
        options = q["options"].copy()
        random.shuffle(options)

        questions.append({
            "question": q["question"],
            "options": options,
            "correct": q["correct"]
        })

    st.session_state.questions = questions
    st.session_state.index = 0
    st.session_state.answers = {}
    st.session_state.checked = False
    st.session_state.result = None
    st.session_state.submitted = False
    st.session_state.initialized = True

questions = st.session_state.questions
TOTAL = len(questions)
q = questions[st.session_state.index]

# ------------------ QUESTION UI ------------------
st.subheader(f"Question {st.session_state.index + 1} / {TOTAL}")
st.write(q["question"])

selected = []
previous = st.session_state.answers.get(st.session_state.index, [])

# ------------------ OPTIONS (CHECKBOXES) ------------------
for opt in q["options"]:
    checked = opt in previous
    if st.checkbox(opt, value=checked, key=f"{st.session_state.index}-{opt}"):
        selected.append(opt)

# Save selections
st.session_state.answers[st.session_state.index] = selected

# ------------------ BUTTONS ------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("⬅ Prev", disabled=st.session_state.index == 0):
        st.session_state.index -= 1
        st.session_state.checked = False
        st.rerun()

with col2:
    if st.button("Next ➡", disabled=st.session_state.index == TOTAL - 1):
        st.session_state.index += 1
        st.session_state.checked = False
        st.rerun()

with col3:
    if st.button("Check Answer"):
        st.session_state.checked = True
        if set(selected) == set(q["correct"]):
            st.session_state.result = "correct"
        else:
            st.session_state.result = "wrong"

with col4:
    if st.button("Submit Test"):
        st.session_state.submitted = True

# ------------------ CHECK ANSWER RESULT ------------------
if st.session_state.checked:
    if st.session_state.result == "correct":
        st.success("✅ Correct")
    else:
        st.error("❌ Wrong")
        st.info("Correct Answer: " + ", ".join(q["correct"]))

# ------------------ FINAL RESULT ------------------
if st.session_state.submitted:
    score = 0
    for i, q in enumerate(questions):
        if set(st.session_state.answers.get(i, [])) == set(q["correct"]):
            score += 1

    accuracy = (score / TOTAL) * 100

    st.divider()
    st.success("🎉 Test Completed")
    st.write(f"**Score:** {score} / {TOTAL}")
    st.write(f"**Accuracy:** {accuracy:.2f}%")

    st.stop()

# ------------------ HIDE STREAMLIT UI ------------------
st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)
