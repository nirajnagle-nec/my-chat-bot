import streamlit as st
import nltk

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

# Sample university database
universities = [
    {"name": "Trine University", "location": "indiana", "program": "MS in Engineering Management", "format": "hybrid", "tuition": 13000, "majors": ["engineering management", "business"], "day1_cpt": True, "start_dates": ["fall 2025", "spring 2026"]},
    {"name": "Ottawa University", "location": "kansas", "program": "MBA", "format": "online", "tuition": 25000, "majors": ["business", "management"], "day1_cpt": True, "start_dates": ["fall 2025", "spring 2026"]},
    {"name": "Campbellsville University", "location": "kentucky", "program": "MS in Computer Science", "format": "in-person", "tuition": 9000, "majors": ["computer science", "data science"], "day1_cpt": True, "start_dates": ["fall 2025", "spring 2026"]},
    {"name": "Harrisburg University", "location": "pennsylvania", "program": "MS in Information Systems", "format": "hybrid", "tuition": 12000, "majors": ["information technology", "management"], "day1_cpt": True, "start_dates": ["fall 2025", "spring 2026"]},
    {"name": "New England College", "location": "new hampshire", "program": "MS in Data Science", "format": "online", "tuition": 10000, "majors": ["data science", "computer science"], "day1_cpt": True, "start_dates": ["fall 2025", "spring 2026", "summer 2026"]},
]

# Extract preferences from input
def extract_preferences(text):
    keywords = text.lower().split()
    locations = ['kentucky', 'pennsylvania', 'indiana', 'kansas', 'new hampshire']
    formats = ['online', 'hybrid', 'in-person']
    majors = ['computer science', 'data science', 'business', 'information technology', 'management', 'engineering management']
    start_terms = ['fall 2025', 'spring 2026', 'summer 2026']

    location = next((word for word in keywords if word in locations), None)
    format_pref = next((word for word in keywords if word in formats), None)
    major = next((m for m in majors if m in text.lower()), None)
    start_term = next((term for term in start_terms if term in text.lower()), None)

    budget = None
    for word in keywords:
        word_clean = word.replace('$', '').replace(',', '')
        if word_clean.isdigit():
            budget = int(word_clean)
            break

    return {
        "location": location,
        "major": major,
        "format": format_pref,
        "budget": budget,
        "start_term": start_term
    }

def update_preferences(current, new_input):
    for key, value in new_input.items():
        if value is not None:
            current[key] = value
    return current

def find_matches(preferences):
    results = []
    for uni in universities:
        if preferences["location"] and preferences["location"] not in uni["location"]:
            continue
        if preferences["major"] and preferences["major"] not in [m.lower() for m in uni["majors"]]:
            continue
        if preferences["format"] and preferences["format"] != uni["format"]:
            continue
        if preferences["budget"] and preferences["budget"] < uni["tuition"]:
            continue
        if preferences["start_term"] and preferences["start_term"] not in [s.lower() for s in uni["start_dates"]]:
            continue
        results.append(uni)
    return results

# Streamlit UI
st.title("🎓 CPT University Chatbot")
st.markdown("Enter your preferences below. For example: _\"Looking for a computer science program in Pennsylvania under $13000 starting Fall 2025\"_")
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'user_preferences' not in st.session_state:
    st.session_state.user_preferences = {"location": None, "major": None, "format": None, "budget": None, "start_term": None}

user_input = st.text_input("You:", key="input")

if st.button("Send"):
    if user_input:
        st.session_state.chat_history.append(("You", user_input))
        new_prefs = extract_preferences(user_input)
        updated_prefs = update_preferences(st.session_state.user_preferences, new_prefs)
        st.session_state.user_preferences = updated_prefs

        matches = find_matches(updated_prefs)
        if matches:
            response = "Here are matching universities:\n"
            for uni in matches:
                response += f"- **{uni['name']}** ({uni['program']}) in {uni['location'].title()}, Tuition: ${uni['tuition']}, Format: {uni['format'].capitalize()}, Start Dates: {', '.join(uni['start_dates'])}\n"
        else:
            response = "❌ No matches found. Try changing some criteria."

        st.session_state.chat_history.append(("Bot", response))

if st.button("🔄 Reset Preferences"):
    st.session_state.user_preferences = {"location": None, "major": None, "format": None, "budget": None, "start_term": None}
    st.success("Preferences have been reset.")

if st.button("🧹 Clear Chat History"):
    st.session_state.chat_history = []
    st.success("Chat history cleared.")

# Display chat history
st.markdown("---")
st.subheader("💬 Chat History")
for sender, message in st.session_state.chat_history:
    st.markdown(f"**{sender}:** {message}")
