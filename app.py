import streamlit as st
import cv2
import time
from utils.llm import generate_question, evaluate_answer

st.title("🤖 AI Interview Room")

# -------------------------------
# SESSION STATE
# -------------------------------
if "started" not in st.session_state:
    st.session_state.started = False

if "captured" not in st.session_state:
    st.session_state.captured = False

if "question" not in st.session_state:
    st.session_state.question = ""

if "answers" not in st.session_state:
    st.session_state.answers = []

if "ended" not in st.session_state:
    st.session_state.ended = False


# -------------------------------
# START INTERVIEW
# -------------------------------
if not st.session_state.started:
    if st.button("🚀 Start Interview"):
        st.session_state.started = True
        st.rerun()


# -------------------------------
# CAPTURE PHOTO (WITH RETAKE)
# -------------------------------
elif not st.session_state.captured:

    st.subheader("📸 Capture Your Photo")
    st.info("⏳ Initializing camera...")

    cap = cv2.VideoCapture(0)
    time.sleep(2)

    ret, frame = cap.read()

    if ret:
        st.image(frame, channels="BGR")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("📸 Capture"):
                cv2.imwrite("candidate.jpg", frame)
                st.session_state.captured = True
                st.success("Photo Captured ✅")
                cap.release()
                st.rerun()

        with col2:
            if st.button("🔄 Retake"):
                cap.release()
                st.rerun()

    cap.release()


# -------------------------------
# INTERVIEW SECTION
# -------------------------------
else:

    # Generate first question
    if not st.session_state.ended and st.session_state.question == "":
        st.session_state.question = generate_question()

    # -------------------------------
    # ACTIVE INTERVIEW
    # -------------------------------
    if not st.session_state.ended:

        st.subheader("💬 Interview Question")
        st.write(st.session_state.question)

        # END BUTTON
        col1, col2 = st.columns(2)
        with col2:
            if st.button("🛑 End Interview"):
                st.session_state.ended = True
                st.rerun()

        # FORM (auto clears input)
        with st.form("answer_form", clear_on_submit=True):
            answer = st.text_input("Your Answer")
            submitted = st.form_submit_button("Submit Answer")

        if submitted and answer.strip():

            with st.spinner("🧠 Evaluating..."):
                result = evaluate_answer(
                    st.session_state.question,
                    answer
                )

            st.write("### 📊 Evaluation")
            st.write(result)

            st.success("✅ Answer submitted! Next question loaded.")

            # store data
            st.session_state.answers.append({
                "question": st.session_state.question,
                "answer": answer,
                "evaluation": result
            })

            # next question
            st.session_state.question = generate_question()

            st.rerun()

    # -------------------------------
    # FINAL REPORT
    # -------------------------------
    if st.session_state.ended:

        st.success("🛑 Interview Ended")

        st.write("## 📄 Final Report")

        for i, item in enumerate(st.session_state.answers):
            st.write(f"### Q{i+1}: {item['question']}")
            st.write(f"**Answer:** {item['answer']}")
            st.write(f"**Evaluation:** {item['evaluation']}")
            st.write("---")

        # RESTART BUTTON
        if st.button("🔄 Restart Interview"):
            st.session_state.started = False
            st.session_state.captured = False
            st.session_state.question = ""
            st.session_state.answers = []
            st.session_state.ended = False
            st.rerun()