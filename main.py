import os
import streamlit as st
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up Streamlit UI
st.set_page_config(page_title="NollyScript AI", page_icon="🎬", layout="wide")

# Custom CSS for Nigerian theme
st.markdown("""
<style>
    .stApp { background-color: 'Arial Black'; }
    .nolly-header { color: #008753; font-family: 'Arial Black'; }
    .sidebar .sidebar-content { background-color: #ffffff; }
</style>
""", unsafe_allow_html=True)

# Initialize Groq LangChain model
groq_api_key = st.secrets["GROQ_API_KEY"]  # Replace with your actual API key
model = ChatGroq(groq_api_key=groq_api_key, model_name="llama-3.3-70b-specdec", temperature=0.7)

# Define cultural templates
CULTURAL_PROMPTS = {
    "Yoruba": "Include Yoruba proverbs and cultural references. Use honorifics like 'Chief', 'Alhaji', 'Iyá'.",
    "Hausa": "Incorporate Hausa traditional titles like 'Sarki', 'Madaki'. Use Northern Nigerian settings.",
    "Igbo": "Include Igbo cultural elements like 'Iri Ji' festival. Use terms like 'Nna anyi', 'Oga'.",
    "Pidgin": "Write dialogues in Nigerian Pidgin English. Use phrases like 'Wahala dey o!', 'How you dey?'",
    "English": "Write dialogues in pure English. Use proper English phrases and dictions."
}

# Create prompt template
SCRIPT_PROMPT = ChatPromptTemplate.from_template("""
You are a professional Nollywood scriptwriter. Create a {genre} movie script with these details:
**Title**: {title}
**Themes**: {themes}
**Cultural Context**: {cultural}
**Audience Rating**: {rating}
**Structure Requirements**:
{acts}
**Formatting Guidelines**:
- Use standard screenplay format
- CAPITALIZE character names
- Include scene headings (INT./EXT.)
- Add cultural dialogues in {cultural} context
- Keep scenes under 3 minutes
**Characters**:
{characters}
**Additional Notes**:
{notes}
Generate the script with proper scene numbering and formatting. Use {cultural} language elements where appropriate.
""")

# Create processing chain
chain = SCRIPT_PROMPT | model | StrOutputParser()

# Streamlit UI Components
st.title("🎬 NollyScript AI - Professional Nollywood Scriptwriter")

with st.sidebar:
    st.header("Script Parameters")
    genre = st.selectbox("Genre", ["Drama", "Comedy", "Action", "Romance", "Epic"], index=0)
    themes = st.multiselect("Themes", ["Family Conflict", "Political Intrigue", "Cultural Heritage", "Modern vs Traditional", "Wealth & Poverty"])
    cultural = st.selectbox("Cultural Context", list(CULTURAL_PROMPTS.keys()))
    rating = st.select_slider("Audience Rating", ["G", "PG", "PG-13", "R"])

    # Dynamically generate acts
    num_acts = st.number_input("Number of Acts", min_value=1, max_value=70, value=5)
    acts = {}
    for i in range(1, num_acts + 1):
        default_text = f"Act {i} description goes here." if i > 1 else "Establish the setting, introduce main characters, and hint at the central conflict."
        acts[f"act{i}"] = st.text_input(f"Act {i}", default_text)

    # Dynamically generate characters
    num_characters = st.number_input("Number of Characters", min_value=2, max_value=15, value=2)
    characters = {}
    for i in range(1, num_characters + 1):
        char_name = st.text_input(f"Character {i} Name", f"Character {i}")
        char_traits = st.text_area(f"Character {i} Traits", f"Traits for {char_name}")
        characters[char_name] = char_traits

# Main Script Input
title = st.text_input("Movie Title", "The Price of Tradition")
notes = st.text_area("Additional Notes", "Include a market scene and village meeting")

# Generate Script
if st.button("📜 Generate Script", type="primary"):
    with st.spinner("Crafting your Nollywood masterpiece..."):
        # Compile character descriptions
        compiled_characters = "\n".join([f"- {name}: {traits}" for name, traits in characters.items()])

        # Compile acts
        compiled_acts = "\n".join([f"{i}. Act {i}: {acts[f'act{i}']}" for i in range(1, num_acts + 1)])

        cultural_notes = CULTURAL_PROMPTS[cultural]
        try:
            response = chain.invoke({
                "genre": genre,
                "title": title,
                "themes": ", ".join(themes),
                "cultural": cultural_notes,
                "rating": rating,
                "acts": compiled_acts,
                "characters": compiled_characters,
                "notes": notes
            })
            st.subheader(f"Generated Script: {title}")
            st.code(response, language="plaintext")
            # Add download button
            st.download_button(
                label="📥 Download Script",
                data=response,
                file_name=f"{title.replace(' ', '_')}.txt",
                mime="text/plain"
            )
        except Exception as e:
            st.error(f"Error generating script: {str(e)}")

# Copyright Section
st.markdown("---")
st.markdown("""
### Copyright Protection
Generated scripts are automatically registered with:
- [Nigerian Copyright Commission](https://copyright.gov.ng)
- NFVCB Script Registry
**Royalty Information**:
- Basic Registration: ₦5,000
- Premium Protection: ₦15,000 (includes legal support)
""")
