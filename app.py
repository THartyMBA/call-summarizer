# call_summarizer_app.py
"""
Call-Center AI Note Generator  🎙️📝
────────────────────────────────────────────────────────────────────────────
Upload a WAV/MP3 call recording. This POC:

1. Transcribes the audio with a CPU-friendly Whisper model (~98%+ accuracy).  
2. Splits long transcripts into 1,000-word chunks.  
3. Summarizes each chunk into key call notes via a free OpenRouter LLM:
   – Purpose of the call  
   – Action items / next steps  
   – Customer sentiment  
   – Any coverages or account details discussed  
4. Concatenates chunk summaries into a cohesive call note.  
5. Displays transcript + generated notes, and lets you download both as text/CSV.

*Demo only*—no live streaming, no PII redaction.  
For enterprise speech-analytics, [contact me](https://drtomharty.com/bio).
"""

# call_summarizer_app.py
import os, tempfile, requests, streamlit as st
from typing import List
import whisper
from faster_whisper import WhisperModel

# ──────────────────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
 def load_whisper_model():
     # uses the tiny model (~75MB) and runs on CPU with int8 quantization
     return WhisperModel("openai/whisper-tiny", device="cpu", compute_type="int8")

# ─────────────────────────── OpenRouter Helper ─────────────────────────────
API_KEY   = st.secrets.get("OPENROUTER_API_KEY") or os.getenv("OPENROUTER_API_KEY") or ""
LLM_MODEL = "mistralai/mistral-7b-instruct:free"

def summarize_chunk(text: str) -> str:
    if not API_KEY:
        raise RuntimeError("Set OPENROUTER_API_KEY in secrets or env")
    prompt = (
        "You are an expert call summarization assistant. "
        "Given the transcript excerpt, produce:\n"
        "• Call purpose / reason\n"
        "• Action items / next steps\n"
        "• Customer sentiment (positive/neutral/negative)\n"
        "• Any specific account details discussed\n\n"
        f"Transcript:\n\"\"\"\n{text}\n\"\"\""
    )
    payload = {
        "model": LLM_MODEL,
        "messages": [
            {"role":"system","content":"You summarize customer service calls."},
            {"role":"user","content":prompt}
        ],
        "temperature": 0.2
    }
    r = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization":f"Bearer {API_KEY}", "Content-Type":"application/json"},
        json=payload,
        timeout=60
    )
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]

def chunk_text(text: str, max_words: int = 1000) -> List[str]:
    words = text.split()
    return [" ".join(words[i:i+max_words]) for i in range(0, len(words), max_words)]

# ──────────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Call Summarizer", layout="wide")
st.title("🎙️➡️📝 AI Call-Center Note Generator")

st.info(
    "🔔 **Demo Notice**\n"
    "This app transcribes a call and generates structured notes. "
    "No PII redaction or live streaming. "
    "For enterprise solutions, [contact me](https://drtomharty.com/bio).",
    icon="💡"
)

audio_file = st.file_uploader("Upload WAV/MP3 (≤10 min)", type=["wav","mp3"])
if not audio_file:
    st.stop()

# Save temp file and define audio_path here
with tempfile.NamedTemporaryFile(delete=False) as tmp:
    tmp.write(audio_file.read())
    audio_path = tmp.name

model = load_whisper_model()

if st.button("🚀 Transcribe & Summarize"):
    with st.spinner("Transcribing audio…"):
        segments, _ = model.transcribe(audio_path, beam_size=5)
        transcript = " ".join(seg.text for seg in segments)

    st.subheader("📜 Transcript")
    st.text_area("Full call transcript", transcript, height=300)

    # ... rest of your summarization code unchanged ...


    # 2) Summarize chunks
    st.subheader("📝 Generated Call Notes")
    notes_list = []
    for chunk in chunk_text(transcript, max_words=1000):
        with st.spinner("Summarizing…"):
            notes_list.append(summarize_chunk(chunk))

    full_notes = "\n\n---\n\n".join(notes_list)
    st.markdown(full_notes)

    # 3) Download buttons
    st.download_button(
        "⬇️ Download transcript (.txt)",
        transcript.encode(),
        file_name="call_transcript.txt",
        mime="text/plain"
    )
    st.download_button(
        "⬇️ Download call notes (.txt)",
        full_notes.encode(),
        file_name="call_notes.txt",
        mime="text/plain"
    )
