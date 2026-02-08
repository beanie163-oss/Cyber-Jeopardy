import streamlit as st
import time

st.set_page_config(page_title="Cybersecurity Jeopardy", layout="wide")

# ---- CYBER THEME ----
st.markdown("""
<style>
    /* Background + Text */
    body {
        background-color: #05090a;
        color: #00f6ff;
        font-family: "Courier New", monospace;
    }

    /* Title + Headers */
    h1, h2, h3, .stTitle, .stHeader {
        color: #00f6ff !important;
        text-shadow: 0 0 10px #00f6ff;
    }

    /* Buttons */
    .stButton>button {
        background-color: #001f24;
        color: #00f6ff;
        border-radius: 8px;
        border: 1px solid #00f6ff;
        box-shadow: 0 0 10px #00f6ff;
        transition: 0.2s ease-in-out;
    }

    .stButton>button:hover {
        background-color: #00f6ff;
        color: #001f24;
        transform: scale(1.05);
        box-shadow: 0 0 20px #00f6ff;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #001417;
        border-right: 2px solid #00f6ff;
    }

    /* Question box */
    .question-box {
        padding: 20px;
        border: 2px solid #00f6ff;
        border-radius: 10px;
        background-color: #001417;
        box-shadow: 0 0 15px #00f6ff;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🔐 Cybersecurity Jeopardy")
st.write("Choose a question, reveal the answer, and keep score!")

# ---- GAME DATA ----
categories = {
    "Networking": {
        100: ("What does TCP stand for?", "Transmission Control Protocol"),
        200: ("What device forwards packets between networks?", "Router"),
        300: ("What command shows your IP address in Windows?", "ipconfig"),
        400: ("What protocol uses port 53?", "DNS"),
    },
    "Cyber Attacks": {
        100: ("What does DDoS stand for?", "Distributed Denial of Service"),
        200: ("What attack tricks users into giving credentials?", "Phishing"),
        300: ("What malware encrypts your files?", "Ransomware"),
        400: ("What attack captures network traffic?", "Packet Sniffing"),
    },
    "Security Tools": {
        100: ("What tool scans networks for open ports?", "Nmap"),
        200: ("What tool captures packets?", "Wireshark / TShark"),
        300: ("What tool tests password strength?", "John the Ripper"),
        400: ("What Linux distro is used for penetration testing?", "Kali Linux"),
    },
    "OSINT": {
        100: ("What does OSINT stand for?", "Open Source Intelligence"),
        200: ("Name one OSINT search engine.", "Shodan"),
        300: ("What is the process of gathering public info on a target?", "Reconnaissance"),
        400: ("What site is used to check data breaches?", "HaveIBeenPwned"),
    }
}

# Final Jeopardy data
FINAL_JEOPARDY_QUESTION = "In cybersecurity, what does the CIA triad stand for?"
FINAL_JEOPARDY_ANSWER = "Confidentiality, Integrity, Availability"

# ---- SESSION STATE ----
if "score" not in st.session_state:
    st.session_state.score = 0

if "current_q" not in st.session_state:
    st.session_state.current_q = None

if "in_final" not in st.session_state:
    st.session_state.in_final = False

if "final_wager" not in st.session_state:
    st.session_state.final_wager = 0

if "games_played" not in st.session_state:
    st.session_state.games_played = 0

if "high_score" not in st.session_state:
    st.session_state.high_score = 0

# ---- SCOREBOARD / LEADERBOARD ----
st.sidebar.title("Scoreboard")
st.sidebar.write(f"**Current Score:** {st.session_state.score}")

st.sidebar.markdown("---")
st.sidebar.title("Leaderboard (Single Player)")
st.sidebar.write(f"**High Score:** {st.session_state.high_score}")
st.sidebar.write(f"**Games Played:** {st.session_state.games_played}")

def update_score(points):
    st.session_state.score += points
    if st.session_state.score > st.session_state.high_score:
        st.session_state.high_score = st.session_state.score

# ---- MAIN GAME BOARD (ONLY IF NOT IN FINAL JEOPARDY) ----
if not st.session_state.in_final:
    st.subheader("Main Board")

    cols = st.columns(len(categories))

    for idx, (cat, questions) in enumerate(categories.items()):
        with cols[idx]:
            st.header(cat)
            for value, qa in questions.items():
                q, a = qa
                if st.button(f"{value}", key=f"{cat}-{value}"):
                    st.session_state.current_q = (q, a, value)

    # Display selected question
    if st.session_state.current_q:
        q, a, value = st.session_state.current_q
        st.markdown("<div class='question-box'>", unsafe_allow_html=True)
        st.subheader(f"Question for {value} points:")
        st.write(q)

        if st.button("Reveal Answer"):
            st.success(a)
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Add Points"):
                    update_score(value)
                    st.session_state.current_q = None
            with col2:
                if st.button("Subtract Points"):
                    update_score(-value)
                    st.session_state.current_q = None
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    # Button to start Final Jeopardy
    if st.button("🚨 Start Final Jeopardy"):
        st.session_state.in_final = True
        st.session_state.current_q = None

# ---- FINAL JEOPARDY ROUND ----
else:
    st.subheader("🎯 Final Jeopardy")

    st.write("You’ve reached Final Jeopardy! Wager your points and answer the final question.")

    # Wager input
    max_wager = max(st.session_state.score, 0)
    wager = st.number_input(
        "Enter your wager:",
        min_value=0,
        max_value=max_wager,
        value=min(100, max_wager),
        step=10
    )

    if st.button("Lock In Wager"):
        st.session_state.final_wager = wager
        st.success(f"Wager locked in: {wager} points")

    if st.session_state.final_wager > 0:
        st.markdown("<div class='question-box'>", unsafe_allow_html=True)
        st.subheader("Final Jeopardy Question:")
        st.write(FINAL_JEOPARDY_QUESTION)

        # Timer
        if st.button("Start 30-Second Timer"):
            placeholder = st.empty()
            for i in range(30, 0, -1):
                placeholder.markdown(f"### ⏳ Time Remaining: {i} seconds")
                time.sleep(1)
            placeholder.markdown("### ⏳ Time's up!")

        # Answer + scoring
        player_answer = st.text_input("Type your answer here (for practice, not auto-graded):")

        if st.button("Reveal Final Answer"):
            st.info(f"Correct Answer: **{FINAL_JEOPARDY_ANSWER}**")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("I got it right ✅"):
                    update_score(st.session_state.final_wager)
                    st.success(f"You won {st.session_state.final_wager} points!")
            with col2:
                if st.button("I got it wrong ❌"):
                    update_score(-st.session_state.final_wager)
                    st.error(f"You lost {st.session_state.final_wager} points!")

            # End of game
            if st.button("End Game & Reset Board"):
                st.session_state.games_played += 1
                st.session_state.in_final = False
                st.session_state.final_wager = 0
                st.session_state.current_q = None

        st.markdown("</div>", unsafe_allow_html=True)
