# call-summarizer

🎙️ AI Call-Center Note Generator
A Streamlit proof-of-concept that takes a recorded call, transcribes it with Whisper, and generates structured call notes via an LLM—minimizing manual note-taking and unlocking call-center efficiency.

Demo only—no real-time streaming, PII redaction, or compliance controls.
For enterprise speech-analytics solutions, contact me.

🔍 What it does
Upload a WAV or MP3 call recording (≤ 10 min).

Transcribe the audio locally using faster-whisper (tiny/int8).

Chunk long transcripts into ~1,000-word segments.

Summarize each segment into:

Call purpose / reason

Action items / next steps

Customer sentiment

Account details discussed
via a free OpenRouter LLM.

Concatenate segment summaries into a cohesive call note.

Display the full transcript and generated notes.

Download both transcript and notes as text files.

✨ Key Features
High-accuracy transcription (~98 % on clear audio) with Whisper tiny (CPU-only).

Token-safe chunking to fit LLM context windows.

Structured summarization via OpenRouter (no heavyweight models).

Streamlit UI for upload, transcription, summarization, and download.

Single-file app: all logic in call_summarizer_app.py.

🔑 Secrets
The summarization step requires an OpenRouter API key.

Streamlit Community Cloud
In your app dashboard click ⋯ → Edit secrets

Add:

toml
Copy
Edit
OPENROUTER_API_KEY = "sk-or-xxxxxxxxxxxxxxxx"
Local development
Create ~/.streamlit/secrets.toml:

toml
Copy
Edit
OPENROUTER_API_KEY = "sk-or-xxxxxxxxxxxxxxxx"
—or—

bash
Copy
Edit
export OPENROUTER_API_KEY=sk-or-xxxxxxxxxxxxxxxx
🚀 Quick Start (Local)
bash
Copy
Edit
git clone https://github.com/THartyMBA/call-summarizer-app.git
cd call-summarizer-app
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run call_summarizer_app.py
Open http://localhost:8501 in your browser.

Upload your call recording and click Transcribe & Summarize.

Review the transcript and generated call notes.

Download the outputs for easy CRM integration.

☁️ Deploy on Streamlit Cloud
Push this repo (public or private) to GitHub under THartyMBA.

Visit streamlit.io/cloud → New app → select your repo/branch → Deploy.

Ensure you’ve added OPENROUTER_API_KEY in Secrets—no other configuration needed.

🛠️ Requirements
shell
Copy
Edit
streamlit>=1.32
faster-whisper
requests
tiktoken
🗂️ Repo Structure
vbnet
Copy
Edit
call-summarizer-app/
├─ call_summarizer_app.py   ← single-file Streamlit app
├─ requirements.txt
└─ README.md                ← you’re reading it
📜 License
CC0 1.0 – public-domain dedication. Attribution appreciated but not required.

🙏 Acknowledgements
Streamlit – effortless Python UIs

faster-whisper – CPU Whisper transcription

OpenRouter – free LLM gateway

tiktoken – token-safe chunking

Transform recorded calls into actionable notes—enjoy! 🎉
