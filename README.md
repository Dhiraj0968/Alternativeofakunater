# 🧞 AI Genie Pro: Self-Learning Character Guesser

A powerful, self-learning alternative to Akinator built with **Python** and **Streamlit**. This AI uses weighted scoring logic to "read your mind" and guess the character you are thinking of. If it fails, it learns from you, expanding its database and getting smarter with every game.

## ✨ Features

- **🧠 Advanced Scoring Engine:** Uses a 5-point scale (Yes, Probably, Don't Know, Probably Not, No) to calculate match probabilities rather than simple binary filtering.
- **📈 Self-Learning Database:** When the AI loses, users can teach it new characters and unique traits, which are saved permanently to a JSON "brain."
- **🖼️ Visual Guesses:** Supports image URLs to display the character's face upon a successful guess.
- **🏆 Live Leaderboard:** Tracks the most popular characters and how many times they have been successfully guessed.
- **📱 Responsive UI:** Built with Streamlit for a clean, mobile-friendly web interface.

---

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have Python 3.8+ installed on your machine.

### 2. Installation
Clone this repository or copy the `app.py` file to your local machine. Then, install the required dependencies:

```bash
pip install streamlit pandas
