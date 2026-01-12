import streamlit as st
import json
import os
import pandas as pd

# --- CONFIGURATION & DATA ---
DB_FILE = "brain_v3.json"

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    # Default starter characters
    return {
        "Spider-Man": {"traits": {"superhero": 1, "real": 0, "red": 1}, "image": "https://tinyurl.com/spidey-img", "guess_count": 0},
        "Albert Einstein": {"traits": {"superhero": 0, "real": 1, "red": 0}, "image": "https://tinyurl.com/einstein-img", "guess_count": 0}
    }

def save_data(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# --- SESSION INITIALIZATION ---
if 'data' not in st.session_state:
    st.session_state.data = load_data()
if 'responses' not in st.session_state:
    st.session_state.responses = {}
if 'game_over' not in st.session_state:
    st.session_state.game_over = False

st.set_page_config(page_title="AI Genie Pro", page_icon="🧠", layout="wide")

# --- SIDEBAR: LEADERBOARD ---
st.sidebar.title("🏆 Leaderboard")
leader_list = [{"Character": k, "Guesses": v.get("guess_count", 0)} for k, v in st.session_state.data.items()]
if leader_list:
    df = pd.DataFrame(leader_list).sort_values(by="Guesses", ascending=False).head(5)
    st.sidebar.table(df.set_index("Character"))

# --- MAIN GAME LOGIC ---
st.title("🧞 AI Character Guesser")
st.write("Think of a character (Real or Fictional) and let the AI read your mind.")

def get_ranked_characters():
    scores = {}
    for name, info in st.session_state.data.items():
        match_score = 0
        for trait, user_val in st.session_state.responses.items():
            char_val = info["traits"].get(trait, 0.5)
            # Bayesian-lite: calculates proximity of answers
            match_score += (1 - abs(user_val - char_val))
        scores[name] = match_score
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)

all_traits = list(set(t for c in st.session_state.data.values() for t in c["traits"].keys()))
asked_traits = list(st.session_state.responses.keys())
remaining_traits = [t for t in all_traits if t not in asked_traits]

# --- UI WORKFLOW ---
if not st.session_state.game_over:
    ranked = get_ranked_characters()
    top_char, top_score = ranked[0]
    
    # Guessing Phase: Guess if we have enough info or asked 5+ questions
    if len(asked_traits) >= 5 or (len(asked_traits) >= 3 and top_score > (len(asked_traits) * 0.85)):
        st.subheader(f"I'm thinking of... **{top_char}**!")
        img = st.session_state.data[top_char].get("image")
        if img: st.image(img, width=300)
        
        c1, c2 = st.columns(2)
        if c1.button("✅ Yes, that's it!", use_container_width=True):
            st.session_state.data[top_char]["guess_count"] += 1
            save_data(st.session_state.data)
            st.balloons()
            st.session_state.game_over = True
            st.rerun()
        if c2.button("❌ No, try again / I win", use_container_width=True):
            st.session_state.game_over = "learn"
            st.rerun()
            
    # Questioning Phase
    elif remaining_traits:
        current_trait = remaining_traits[0]
        st.info(f"Question #{len(asked_traits) + 1}")
        st.header(f"Does your character have the trait: **'{current_trait}'**?")
        
        btn_cols = st.columns(5)
        options = [("Yes", 1.0), ("Probably", 0.75), ("Don't Know", 0.5), ("Probably Not", 0.25), ("No", 0.0)]
        for i, (label, val) in enumerate(options):
            if btn_cols[i].button(label, key=f"btn_{label}"):
                st.session_state.responses[current_trait] = val
                st.rerun()
    else:
        st.session_state.game_over = "learn"
        st.rerun()

# --- LEARNING UI ---
if st.session_state.game_over == "learn":
    st.divider()
    st.subheader("🏳️ I Give Up! Teach Me.")
    with st.form("learn_form"):
        new_name = st.text_input("Who were you thinking of?")
        new_img = st.text_input("Image URL (optional):")
        new_trait = st.text_input(f"What makes {new_name} unique? (e.g. 'has a beard')")
        submitted = st.form_submit_button("Submit to Database")
        
        if submitted and new_name and new_trait:
            new_entry_traits = st.session_state.responses.copy()
            new_entry_traits[new_trait] = 1.0
            st.session_state.data[new_name] = {
                "traits": new_entry_traits,
                "image": new_img,
                "guess_count": 0
            }
            # Set this new trait to 0 for everyone else
            for c in st.session_state.data:
                if c != new_name: st.session_state.data[c]["traits"][new_trait] = 0.0
            
            save_data(st.session_state.data)
            st.success("Success! I'll remember that.")
            st.session_state.clear()
            st.rerun()

if st.button("🔄 Restart Game"):
    st.session_state.clear()
    st.rerun()
