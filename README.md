# AI Youtube Voice Over and Script Generator
Generating Voice over audio for Youtube Videos based on Youtube Title

This project is a Streamlit application that leverages various AI models to generate YouTube scripts and voiceovers. It aims to assist content creators in producing high-quality YouTube videos with minimal effort.

### Live link : https://ai-youtube-voice-over-generator.streamlit.app
- No Elven labs feautre in this Link

### Audio Demo
- Title : what is phenomenon beyond northern lights ---
[Demo Samlpe Link](https://drive.google.com/file/d/1ZvUR4bttk6EIRcYnfAsnVYMTA_EAoqUb/view?usp=sharing)

## WorkFlow
![Workflow](https://github.com/user-attachments/assets/07d4c8ad-d8f8-4fea-bcd6-f5948f6185af)

## Requirements

- [Google Gemini Api Key](https://aistudio.google.com/app/apikey)
- [Groq API](https://console.groq.com/keys)
- [ElevenLabs API](https://elevenlabs.io/api)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/AI-YouTube-Voice-Over-Generator.git
    cd AI-YouTube-Voice-Over-Generator
    ```

2. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the Streamlit application:
    ```bash
    streamlit run app.py
    ```

## Usage

### API Keys

- **Gemini Models**: Enter your Gemini API key in the sidebar if you are using Gemini-based text generation models.
- **Groq Models**: Enter your Groq API key in the sidebar if you are using Groq-based text generation models.
- **ElevenLabs TTS**: Enter your ElevenLabs API key in the sidebar if you select the ElevenLabs text-to-speech model.

### Generating Scripts

1. **Enter Video Title**: Input the title for your YouTube video.
2. **Set Video Length**: Specify the desired video length in minutes.
3. **Generate Script**: Click the "Generate Script" button.
4. **Edit Script**: Modify the generated script if needed.

### Generating Voiceovers

1. **Select TTS Model**: Choose a TTS model in the sidebar.
2. **Generate Audio**: Click the "Generate Audio" button after the script is ready.
3. **Download Audio**: Listen to and download the generated audio.

### Regenerating and Editing

- **Regenerate Script**: Click to create a new script if desired.
- **Edit Script**: Update the script and convert it to audio.



## Contributing
Contributions are welcome! Please open an issue or submit a pull request if you have suggestions for improvements or new features.

## Acknowledgments
- [mrfakename](https://huggingface.co/mrfakename) for Hosting freely Hosting MELLO TTS model, without there contribution it woudn't be a possibilty to provide free TTS service to end users

## Improvements
- **Local Text Generation**: Implement the use of local text generation models to enhance performance and reduce dependency on external APIs.
- **Local TTS Models**: Integrate local TTS models for better audio generation and faster processing times.
- **Voice Cloning**: Allow users to choose from a variety of voices for TTS, including options for voice cloning based on user preferences.




