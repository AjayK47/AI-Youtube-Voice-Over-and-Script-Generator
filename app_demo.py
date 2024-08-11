import streamlit as st
from duckduckgo_search import DDGS
import google.generativeai as genai
from gradio_client import Client
import soundfile as sf
from groq import Groq
import os
import tempfile
import time
import io

# Streamlit app
st.set_page_config(page_title="YouTube Script and Voiceover Generator", layout="wide")
st.title("YouTube Script and Voiceover Generator")

# Sidebar for Model Selection and API Keys
st.sidebar.header("Model and API Key Settings")

# Add a note about where to obtain API keys using st.info
st.sidebar.info(
    """
    **Where to obtain API keys:**
    - [Get your GROQ API key](https://console.groq.com/keys)
    - [Get your Gemini API key](https://aistudio.google.com/app/apikey)
    """
)


# Text Model Selection in Sidebar
text_model = st.sidebar.selectbox(
    "Select Text Generation Model:",
    ["gemini-1.5-pro", "gemini-1.5-flash", "gemma2-9b-it", "gemma2-2b-it", 
     "llama3-8b-8192", "llama-3.1-8b-instant", "llama-3.1-70b-versatile", 
     "gemma2-9b-it", "gemma-7b-it"],
    index=0  # Default to the first option
)

# Conditional API Key Input for Text Model
if text_model.startswith("gemini"):
    user_api_key = st.sidebar.text_input("Enter your Gemini API key:", type="password")
    if user_api_key:
        genai.configure(api_key=user_api_key)
elif text_model.startswith("llama") or text_model.startswith("gemma"):
    user_api_key = st.sidebar.text_input("Enter your Groq API key:", type="password")
    if user_api_key:
        os.environ['GROQ_API_KEY'] = user_api_key

# TTS Model Selection in Sidebar
tts_model = st.sidebar.selectbox(
    "Select TTS Model:",
    ["mrfakename/MeloTTS"],
    index=0  # Default to MeloTTS model
)

# User Input for Video Title
title = st.text_input("Enter the title of your YouTube video:")

# User Input for Video Length in Minutes
video_length = st.number_input("Enter the desired length of the video in minutes:", min_value=1, max_value=120, value=5)

def search_and_summarize(search_query):
    results = DDGS().text(
        keywords=search_query,
        region='us-en',
        safesearch='off',
        timelimit='2m',
        max_results=5
    )
    if not results:
        raise ValueError("No search results found.")
    text_content = [result['body'] for result in results]

    if text_model.startswith("gemini"):
        gemini = genai.GenerativeModel(text_model)
        summary = gemini.generate_content(
            "Summarize the following text: " + " ".join(text_content),
        )
        return summary.text
    else:  # Groq models
        llm = Groq(api_key=user_api_key)
        summary = llm.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": "Summarize the following text: " + " ".join(text_content)
                }
            ],
            model=text_model
        )
        return summary.choices[0].message.content

def generate_youtube_script(title, context, video_length, regenerate=False):
    regenerate_note = " (This is a regenerated script.)" if regenerate else ""
    prompt = f'''
    Generate a YouTube script voiceover based on the following title and context. Make it sound like a natural conversation, with pauses and a conversational tone.

    Title: {title}

    Context: {context}

    The voiceover should be suitable for a video that is approximately {video_length} minutes long. It should start with a strong introduction, followed by key points that highlight the main aspects of the topic, and conclude with a statement that leaves the viewer wanting to learn more.

    Only provide the voiceover text, without any additional formatting or instructions.{regenerate_note}
    '''

    if text_model.startswith("gemini"):
        gemini = genai.GenerativeModel(text_model)
        script = gemini.generate_content(prompt)
        return script.text
    else:  # Groq models
        llm = Groq(api_key=user_api_key)
        response = llm.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model=text_model
        )
        return response.choices[0].message.content

def text_to_speech(script):
    try:
        client = Client("mrfakename/MeloTTS")
        result = client.predict(
            text=script,
            speaker="EN-US",
            speed=1,
            language="EN",
            api_name="/synthesize"
        )
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            output_filename = temp_file.name
            data, samplerate = sf.read(result)
            sf.write(output_filename, data, samplerate)

        return output_filename
    except Exception as e:
        st.error(f"An error occurred during text-to-speech conversion: {str(e)}")
        return None

def delayed_file_cleanup(file_path, max_attempts=5, delay=1):
    for _ in range(max_attempts):
        try:
            if os.path.exists(file_path):
                os.unlink(file_path)
            return
        except PermissionError:
            time.sleep(delay)
    print(f"Warning: Unable to delete temporary file: {file_path}")

def generate_script():
    if title:
        try:
            summary = search_and_summarize(title)
            st.write("**Summary:**")
            st.write(summary)

            script = generate_youtube_script(title, summary, video_length)

            return script
        except Exception as e:
            st.error(f"An error occurred during script generation: {str(e)}")
            return None
    else:
        st.error("Please enter a title for the YouTube video.")
        return None

def generate_audio(script):
    with st.spinner("Converting text to speech..."):
        output_file = text_to_speech(script)
    
    if output_file:
        st.success("Audio conversion complete!")
        
        audio_file = open(output_file, 'rb')
        audio_bytes = audio_file.read()
        audio_file.close()
        
        st.audio(audio_bytes, format='audio/wav')
        
        st.download_button(
            label="Download Audio",
            data=audio_bytes,
            file_name="tts_output.wav",
            mime="audio/wav"
        )
        
        st.session_state['cleanup_file'] = output_file
    else:
        st.error("Failed to convert text to speech. Please try again.")

def main():
    if st.button("Generate Script"):
       if (text_model.startswith("gemini") and not user_api_key) or \
          ((text_model.startswith("llama") or text_model.startswith("gemma")) and not user_api_key):
           st.error("Please enter the required API keys.")
       else:
         script = generate_script()
         if script:
            st.session_state['current_script'] = script
            st.session_state['script_status'] = 'new'
    if 'current_script' in st.session_state:
        if st.session_state.get('script_status') == 'regenerated':
            st.write("**Regenerated Script:**")
            st.write(st.session_state['current_script'])
        else:
            st.write("**Generated Script:**")
            st.write(st.session_state['current_script'])

        script_action = st.radio(
            "What would you like to do with the script?",
            ("Generate Audio", "Edit Script", "Regenerate Script"),
            index=None  # This ensures no option is selected by default
        )
        
        if script_action == "Generate Audio":
            if st.button("Generate Audio"):
                generate_audio(st.session_state['current_script'])
        elif script_action == "Edit Script":
            edited_script = st.text_area("Edit Script", st.session_state['current_script'], height=300)
            if st.button("Generate Audio from Edited Script"):
                generate_audio(edited_script)
        elif script_action == "Regenerate Script":
            if st.button("Regenerate Script"):
                new_script = generate_script()
                if new_script:
                    st.session_state['current_script'] = new_script
                    st.session_state['script_status'] = 'regenerated'
                    st.rerun()

    # Attempt cleanup of previous file, if any
    if 'cleanup_file' in st.session_state:
        delayed_file_cleanup(st.session_state['cleanup_file'])
        del st.session_state['cleanup_file']

if __name__ == "__main__":
    main()
