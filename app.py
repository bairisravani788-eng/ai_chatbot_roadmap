import streamlit as st
from ollama import chat


# -----------------------------
# PAGE CONFIGURATION
# -----------------------------

st.set_page_config(
    page_title="AI Learning Roadmap",
    page_icon="🎓"
)


# -----------------------------
# TITLE
# -----------------------------

st.title("🎓 AI Learning Roadmap Generator")

st.write(
    "Tell me your career goal and current skills. "
    "AI will create a personalized learning roadmap for you."
)


# -----------------------------
# STUDENT DETAILS
# -----------------------------

st.sidebar.header("👨‍🎓 Student Details")

name = st.sidebar.text_input(
    "Name"
)

education = st.sidebar.selectbox(
    "Education",
    [
        "B.Tech CSE",
        "BCA",
        "B.Sc Computer Science",
        "Other"
    ]
)

career = st.sidebar.text_input(
    "Career Goal",
    placeholder="Example: Data Analyst"
)

skills = st.sidebar.text_input(
    "Current Skills",
    placeholder="Example: Python, Excel"
)

level = st.sidebar.selectbox(
    "Current Level",
    [
        "Beginner",
        "Intermediate",
        "Advanced"
    ]
)


# -----------------------------
# CHAT HISTORY
# -----------------------------

if "messages" not in st.session_state:

    st.session_state.messages = []


for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# -----------------------------
# CHAT INPUT
# -----------------------------

question = st.chat_input(
    "Ask for your learning roadmap..."
)


# -----------------------------
# AI
# -----------------------------

if question:

    with st.chat_message("user"):

        st.markdown(question)


    st.session_state.messages.append({

        "role": "user",

        "content": question

    })


    prompt = f"""

You are an AI Learning Roadmap Generator.

Student Information:

Name: {name}

Education: {education}

Career Goal: {career}

Current Skills: {skills}

Current Level: {level}


The student asked:

{question}


Create a practical and beginner-friendly learning roadmap.

Include:

1. Career goal
2. Required skills
3. Phase-by-phase roadmap
4. Beginner topics
5. Intermediate topics
6. Advanced topics
7. Projects
8. Tools to learn
9. Practice tasks
10. Interview preparation
11. Suggested learning order


Use this structure:

🎯 Career Goal

📚 Skills Required

🟢 Phase 1 — Fundamentals

🔵 Phase 2 — Core Skills

🟣 Phase 3 — Advanced Skills

🟠 Phase 4 — Projects

🔴 Phase 5 — Job Preparation

🚀 Final Roadmap


Keep the explanation simple.

Give practical examples.

Do not guarantee jobs or salaries.

"""


    try:

        with st.chat_message("assistant"):

            with st.spinner(
                "🤖 Creating your roadmap..."
            ):

                response = chat(

                    model="gemma3:1b",

                    messages=[

                        {
                            "role": "system",
                            "content": prompt
                        },

                        *st.session_state.messages

                    ]

                )


                answer = response[
                    "message"
                ][
                    "content"
                ]


            st.markdown(answer)


        st.session_state.messages.append({

            "role": "assistant",

            "content": answer

        })


    except Exception:

        st.error(
            "❌ Ollama is not running."
        )

        st.code(
            "ollama run gemma3:1b"
        )