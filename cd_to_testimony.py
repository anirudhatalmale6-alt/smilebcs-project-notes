"""
CD-to-Testimony Pipeline
Merge multi-part MP3s → Transcribe with Whisper → Generate Title/Hook/Tags via OpenAI

Usage:
    python cd_to_testimony.py                  # Mode A: full pipeline (merge + Whisper + GPT)
    python cd_to_testimony.py --metadata-only  # Mode B: skip Whisper, read existing transcripts, GPT only

Requirements:
    Mode A: pip install openai-whisper pydub openai
    Mode B: pip install openai  (no Whisper or pydub needed)
    FFmpeg must be installed and on PATH (Mode A only)
"""

import os
import re
import sys
import json
import time
import logging
from datetime import datetime

from openai import OpenAI

# --------------------------
# SETTINGS — EDIT THESE
# --------------------------
REFERENCE_SITE_URL = "https://hehathdone.org"
NEW_AUDIO_FOLDER = r"G:/HeHathDone/RippedCDs"
OUTPUT_FOLDER = r"G:/HeHathDone/FirstPassAI"
MERGED_AUDIO_FOLDER = os.path.join(OUTPUT_FOLDER, "merged_audio")
TRANSCRIPTS_FOLDER = os.path.join(OUTPUT_FOLDER, "transcripts")
LOG_FILE = os.path.join(OUTPUT_FOLDER, "pipeline.log")

WHISPER_MODEL = "medium"
WHISPER_LANGUAGE = "en"

OPENAI_MODEL = "gpt-4o"
OPENAI_API_KEY = "YOUR_API_KEY_HERE"  # Paste your OpenAI API key here

PROMPT_FILE = None  # Set to path of Prompt.txt to load from file, or None to use built-in

# Track pattern inside speaker folders: "01 Track 1.mp3", "02 Track 2.mp3", etc.
TRACK_PATTERN = re.compile(r"^(\d+)\s", re.IGNORECASE)

# Flat-folder merge pattern (fallback): Name_Part1.mp3, Name_Part2.mp3, etc.
CHAPTER_PATTERN = re.compile(
    r"(.+?)[\s_-]+(?:part|pt|ch|disc|cd)?[\s_-]*(\d+)\.mp3$", re.IGNORECASE
)

# Files to skip during merge (pre-merged or non-track files)
SKIP_KEYWORDS = ["final testimony", "full testimony", "complete", "merged"]

# --------------------------
# EXISTING TAGS (from hehathdone.org)
# --------------------------
EXISTING_TAGS = [
    "Addiction", "Troubles", "Alcohol Addiction", "Atheism", "Cults",
    "International", "Paramilitary", "Ex Roman Catholic", "Sports",
    "Ex Jehovah Witness"
]

# --------------------------
# BUILT-IN PROMPT (mirrors Prompt.txt exactly)
# --------------------------
BUILTIN_PROMPT = """You are an editor and story producer for a gritty, emotionally honest Christian testimony platform.

The testimonies are real stories of brokenness, addiction, violence, spiritual searching, trauma, emptiness, crime, self-destruction, near-death experiences, and radical life transformation through Jesus Christ.

Your job is NOT to summarise the testimony like a church newsletter.
Your job IS to identify:
- the emotional fracture point
- the defining moment
- the hidden pain
- the turning point
- the moment everything changed

The tone should feel like:
- a Netflix documentary
- a powerful YouTube testimony
- a cinematic true story
- emotionally raw and authentic
- deeply human
- believable
- not polished corporate Christianity

The writing MUST avoid:
- cheesy Christian phrases
- sermon-style wording
- generic ministry language
- "from darkness to light"
- "how God changed my life"
- sounding preachy or artificial
- overexplaining the testimony

The writing SHOULD feel:
- emotionally charged
- visual
- intriguing
- tense
- reflective
- authentic
- human
- sometimes gritty
- sometimes deeply introspective

IMPORTANT:
The strongest testimonies often revolve around:
- a collapse
- an interruption
- a near miss
- a funeral
- a violent moment
- an empty success
- addiction
- fear
- a question
- a vision
- a cry for help
- a moment of conviction
- a supernatural encounter
- emotional emptiness despite worldly success

Focus on the deepest emotional fracture point.

-----------------------------------
YOUR TASK
-----------------------------------
Analyse the supplied testimony transcript and generate:
1. TITLE
2. HOOK
3. TAGS

-----------------------------------
TITLE RULES
-----------------------------------
The title is the MOST IMPORTANT part.
Maximum 12 words.

The title should:
- create strong curiosity
- feel emotionally real
- sound like a quote, revelation, confession, interruption, or defining moment
- feel cinematic
- be concise and memorable
- sound like a documentary or testimony thumbnail
- make someone NEED to click

GOOD TITLE STYLES:
- "I Wasn't Coming Back"
- "Is This All There Is?"
- "I Thought I Had Everything"
- "The Funeral I Never Wanted to Attend"
- "I Couldn't Even Get Drunk Anymore"
- "Seven Days After They Tried to Kill Me"
- "I Was Fighting Everybody Except Myself"
- "Looking Over Dublin, I Realised I Was Empty"

BAD TITLE STYLES:
- "My Christian Testimony"
- "Saved By Grace"
- "How God Changed My Life"
- "From Darkness to Light"
- "Jesus Saved Me"
- "My Journey of Faith"

The title should NOT try to preach.
It should create emotional intrigue.

-----------------------------------
HOOK RULES
-----------------------------------
Maximum 250 characters.

The hook should:
- feel like a movie trailer line
- immediately create intrigue
- hint at danger, emptiness, addiction, fear, violence, despair, brokenness, or transformation
- emotionally pull the reader in
- feel modern and realistic
- avoid giving away the entire story
- avoid sounding like a summary paragraph

The strongest hooks usually contain:
1. the old life
2. the breaking point
3. the interruption or transformation

GOOD HOOK STYLE:
- "Drink, violence and chaos ruled his life for 14 years — until one funeral sermon stopped him in his tracks."
- "She had wealth, luxury and dangerous connections, but staring over Dublin one night, she realised she was completely empty."
- "Seven days after an attempt on his life, he says he encountered something that changed him forever."

BAD HOOK STYLE:
- "This is the inspiring story of how a man found Jesus."
- "God transformed his life and gave him hope."
- "A testimony of redemption and salvation."

-----------------------------------
TAGGING RULES
-----------------------------------
Use existing tags where appropriate.

Existing Tags:
{existing_tags}

You may also create NEW tags where justified.

Useful tag categories include:

Lifestyle / Background:
- Estate Life, Boxing, Football, Bands, Nightlife, Wealth, Luxury Lifestyle
- Gang Culture, Street Life, Crime, Rioting, Prison, Former Drug Dealer

Struggles:
- Drug Addiction, Gambling Addiction, Violence, Trauma, Depression
- Self Destruction, Mental Health, Family Breakdown, Near Death Experience
- Emptiness, Alcohol Abuse

Spiritual Themes:
- Deliverance, Vision Encounter, Spiritual Searching, New Age
- Radical Conversion, Evangelism, Restoration, Freedom, Peace, Salvation

Regional:
- Northern Ireland, Belfast, Larne, Ahoghil

Prioritise tags that:
- describe the old life
- identify the core struggle
- identify the emotional turning point
- help users discover similar testimonies

Choose 4-8 tags total.

-----------------------------------
OUTPUT FORMAT
-----------------------------------
TITLE:
[title]

HOOK:
[hook]

TAGS:
[tag1, tag2, tag3...]

-----------------------------------
TRANSCRIPT
-----------------------------------
{transcript}"""


def setup_logging():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(message)s",
        datefmt="%H:%M:%S",
        handlers=[
            logging.FileHandler(LOG_FILE, encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )


def load_prompt_template():
    if PROMPT_FILE and os.path.isfile(PROMPT_FILE):
        with open(PROMPT_FILE, "r", encoding="utf-8") as f:
            text = f.read()
        if "{transcript}" not in text:
            text += "\n\n-----------------------------------\nTRANSCRIPT\n-----------------------------------\n{transcript}"
        if "{existing_tags}" not in text:
            text = text.replace(
                "Existing Tags:", "Existing Tags:\n{existing_tags}"
            )
        logging.info("Loaded prompt from %s", PROMPT_FILE)
        return text
    logging.info("Using built-in prompt template")
    return BUILTIN_PROMPT


# --------------------------
# Step 1: Scan speaker folders and merge CD tracks
# --------------------------
def find_speaker_folders(root):
    """Walk the input folder tree to find speaker folders containing MP3 tracks.
    Handles structures like:
      root/Fearon_Wendy/01 Track 1.mp3
      root/Unknown artist/Fearon_Wendy/01 Track 1.mp3
    """
    speakers = {}
    for dirpath, dirnames, filenames in os.walk(root):
        mp3s = [f for f in filenames if f.lower().endswith(".mp3")]
        if not mp3s:
            continue
        folder_name = os.path.basename(dirpath)
        if folder_name.lower() in ("unknown artist", "various artists", ""):
            continue
        speakers[folder_name] = (dirpath, mp3s)
    return speakers


def sort_tracks(filenames):
    """Sort track files by leading number: '01 Track 1.mp3' -> sort key 1."""
    def sort_key(f):
        m = TRACK_PATTERN.match(f)
        if m:
            return int(m.group(1))
        m2 = CHAPTER_PATTERN.match(f)
        if m2:
            return int(m2.group(2))
        return 999
    return sorted(filenames, key=sort_key)


def is_skip_file(filename):
    """Skip pre-merged or non-track files like 'Final Testimony Only.mp3'."""
    lower = filename.lower()
    return any(kw in lower for kw in SKIP_KEYWORDS)


def group_and_merge(folder):
    logging.info("Scanning %s for speaker folders...", folder)
    if not os.path.isdir(folder):
        logging.error("Input folder not found: %s", folder)
        sys.exit(1)

    speakers = find_speaker_folders(folder)

    if not speakers:
        logging.error("No speaker folders with MP3s found in %s", folder)
        logging.error("Expected structure: input_folder/Speaker_Name/01 Track 1.mp3")
        sys.exit(1)

    os.makedirs(MERGED_AUDIO_FOLDER, exist_ok=True)
    results = []

    for speaker_name in sorted(speakers.keys()):
        dirpath, mp3s = speakers[speaker_name]

        track_files = [f for f in mp3s if not is_skip_file(f)]
        track_files = sort_tracks(track_files)

        if not track_files:
            logging.warning("No track files in %s — skipping", speaker_name)
            continue

        out_path = os.path.join(MERGED_AUDIO_FOLDER, f"{speaker_name}.mp3")

        if os.path.isfile(out_path):
            logging.info("Already merged: %s (skipping)", speaker_name)
            results.append(out_path)
            continue

        if len(track_files) == 1:
            logging.info("%s: single track — copying", speaker_name)
            seg = AudioSegment.from_mp3(os.path.join(dirpath, track_files[0]))
            seg.export(out_path, format="mp3")
            duration_min = len(seg) / 60000
            logging.info("  -> %s (%.1f min)", speaker_name, duration_min)
        else:
            logging.info("%s: merging %d tracks %s", speaker_name, len(track_files), track_files)
            combined = AudioSegment.empty()
            for tf in track_files:
                combined += AudioSegment.from_mp3(os.path.join(dirpath, tf))
            combined.export(out_path, format="mp3")
            duration_min = len(combined) / 60000
            logging.info("  -> %s (%.1f min)", speaker_name, duration_min)

        results.append(out_path)

    logging.info("Ready: %d testimonies to process", len(results))
    return results


# --------------------------
# Step 2: Transcribe with Whisper
# --------------------------
def transcribe_audio(file_path, model):
    filename = os.path.basename(file_path)
    transcript_path = os.path.join(
        TRANSCRIPTS_FOLDER, os.path.splitext(filename)[0] + ".txt"
    )

    if os.path.isfile(transcript_path):
        logging.info("Transcript exists: %s (loading)", filename)
        with open(transcript_path, "r", encoding="utf-8") as f:
            return f.read()

    logging.info("Transcribing: %s ...", filename)
    start = time.time()

    result = model.transcribe(
        file_path,
        language=WHISPER_LANGUAGE,
        word_timestamps=True,
        condition_on_previous_text=True,
        fp16=False,
    )

    transcript = result["text"].strip()
    elapsed = time.time() - start
    word_count = len(transcript.split())
    logging.info(
        "  -> %d words in %.0fs (%.1f min audio)",
        word_count, elapsed,
        AudioSegment.from_mp3(file_path).duration_seconds / 60,
    )

    os.makedirs(TRANSCRIPTS_FOLDER, exist_ok=True)
    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write(transcript)

    return transcript


# --------------------------
# Step 3: Generate Title / Hook / Tags via OpenAI
# --------------------------
def generate_metadata(transcript, prompt_template, client):
    tags_str = "\n".join(f"- {t}" for t in EXISTING_TAGS)
    prompt = prompt_template.format(
        transcript=transcript,
        existing_tags=tags_str,
    )

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
        max_tokens=500,
    )
    return response.choices[0].message.content.strip()


def parse_ai_output(text):
    title = hook = tags = ""
    for line in text.splitlines():
        line_stripped = line.strip()
        if line_stripped.upper().startswith("TITLE:"):
            title = line_stripped[6:].strip().strip('"')
        elif line_stripped.upper().startswith("HOOK:"):
            hook = line_stripped[5:].strip()
        elif line_stripped.upper().startswith("TAGS:"):
            tags = line_stripped[5:].strip()
    if not title:
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        if lines:
            title = lines[0].strip('"')
    return title, hook, tags


# --------------------------
# Step 4: Save output
# --------------------------
def save_result(filename, transcript, title, hook, tags, raw_ai):
    base = os.path.splitext(filename)[0]
    out_path = os.path.join(OUTPUT_FOLDER, f"{base}.txt")

    speaker = base.replace("_", " ")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(f"SPEAKER:\n{speaker}\n\n")
        f.write(f"TITLE:\n{title}\n\n")
        f.write(f"HOOK:\n{hook}\n\n")
        f.write(f"TAGS:\n{tags}\n\n")
        f.write(f"AUDIO FILE:\n{filename}\n\n")
        f.write(f"{'='*60}\n")
        f.write(f"TRANSCRIPT:\n{transcript}\n")

    logging.info("  TITLE: %s", title)
    logging.info("  HOOK:  %s", hook[:80] + ("..." if len(hook) > 80 else ""))
    logging.info("  TAGS:  %s", tags)
    logging.info("  Saved: %s", os.path.basename(out_path))
    return out_path


# --------------------------
# Mode B: Metadata-only pipeline
# --------------------------
def normalise_name(name):
    """Normalise a filename for fuzzy matching: lowercase, strip spaces/underscores/hyphens."""
    return re.sub(r"[\s_\-]+", "", name.lower())


def find_matching_audio(transcript_name, audio_files_map):
    """Find the matching MP3 for a transcript, handling naming differences."""
    norm = normalise_name(transcript_name)
    if norm in audio_files_map:
        return audio_files_map[norm]
    for key, path in audio_files_map.items():
        if norm in key or key in norm:
            return path
    return None


def run_metadata_only():
    """Mode B: Read existing transcripts, run GPT-4o for title/hook/tags only."""
    logging.info("MODE B — Metadata-only (skipping Whisper)")
    logging.info("Reading transcripts from: %s", TRANSCRIPTS_FOLDER)

    if not os.path.isdir(TRANSCRIPTS_FOLDER):
        logging.error("Transcripts folder not found: %s", TRANSCRIPTS_FOLDER)
        sys.exit(1)

    txt_files = sorted([f for f in os.listdir(TRANSCRIPTS_FOLDER) if f.lower().endswith(".txt")])
    if not txt_files:
        logging.error("No .txt files found in %s", TRANSCRIPTS_FOLDER)
        sys.exit(1)

    audio_files_map = {}
    if os.path.isdir(MERGED_AUDIO_FOLDER):
        for f in os.listdir(MERGED_AUDIO_FOLDER):
            if f.lower().endswith(".mp3"):
                audio_files_map[normalise_name(os.path.splitext(f)[0])] = f

    prompt_template = load_prompt_template()
    ai_client = OpenAI(api_key=OPENAI_API_KEY)

    total = len(txt_files)
    successes = 0
    failures = []

    logging.info("Found %d transcripts to process", total)
    logging.info("")

    for i, txt_file in enumerate(txt_files, 1):
        base_name = os.path.splitext(txt_file)[0]
        logging.info("[%d/%d] %s", i, total, base_name)
        logging.info("-" * 40)

        result_path = os.path.join(OUTPUT_FOLDER, f"{base_name}.txt")
        if os.path.isfile(result_path):
            logging.info("Already processed — skipping")
            successes += 1
            continue

        try:
            with open(os.path.join(TRANSCRIPTS_FOLDER, txt_file), "r", encoding="utf-8") as f:
                transcript = f.read().strip()

            if len(transcript.split()) < 20:
                logging.warning("Transcript too short (%d words) — skipping", len(transcript.split()))
                failures.append((txt_file, "Transcript too short"))
                continue

            audio_match = find_matching_audio(base_name, audio_files_map)
            audio_filename = audio_match if audio_match else f"{base_name}.mp3"

            raw_ai = generate_metadata(transcript, prompt_template, ai_client)
            title, hook, tags = parse_ai_output(raw_ai)

            if not title:
                logging.warning("AI returned no title — saving raw output")
                title = "(Title generation failed)"

            if len(hook) > 250:
                hook = hook[:247] + "..."
                logging.info("  Hook trimmed to 250 chars")

            save_result(audio_filename, transcript, title, hook, tags, raw_ai)
            successes += 1

        except Exception as e:
            logging.error("FAILED: %s — %s", txt_file, e)
            failures.append((txt_file, str(e)))
            continue

    logging.info("")
    logging.info("=" * 60)
    logging.info("DONE: %d/%d succeeded", successes, total)
    if failures:
        logging.info("FAILED (%d):", len(failures))
        for name, reason in failures:
            logging.info("  - %s: %s", name, reason)
    logging.info("Transcripts   -> %s", TRANSCRIPTS_FOLDER)
    logging.info("Output files  -> %s", OUTPUT_FOLDER)
    logging.info("Log file      -> %s", LOG_FILE)
    logging.info("=" * 60)


# --------------------------
# Mode A: Full pipeline
# --------------------------
def run_full_pipeline():
    """Mode A: Merge + Whisper + GPT (original pipeline)."""
    from pydub import AudioSegment
    import whisper

    logging.info("MODE A — Full pipeline (merge + Whisper + GPT)")

    prompt_template = load_prompt_template()
    audio_files = group_and_merge(NEW_AUDIO_FOLDER)

    logging.info("Loading Whisper model '%s' (this may take a moment)...", WHISPER_MODEL)
    whisper_model = whisper.load_model(WHISPER_MODEL)
    logging.info("Whisper model loaded.")

    ai_client = OpenAI(api_key=OPENAI_API_KEY)

    os.makedirs(TRANSCRIPTS_FOLDER, exist_ok=True)
    total = len(audio_files)
    successes = 0
    failures = []

    for i, file_path in enumerate(audio_files, 1):
        filename = os.path.basename(file_path)
        logging.info("")
        logging.info("[%d/%d] %s", i, total, filename)
        logging.info("-" * 40)

        result_path = os.path.join(
            OUTPUT_FOLDER, os.path.splitext(filename)[0] + ".txt"
        )
        if os.path.isfile(result_path):
            logging.info("Already processed — skipping")
            successes += 1
            continue

        try:
            transcript = transcribe_audio(file_path, whisper_model)
            if len(transcript.split()) < 20:
                logging.warning("Transcript too short (%d words) — skipping", len(transcript.split()))
                failures.append((filename, "Transcript too short"))
                continue

            raw_ai = generate_metadata(transcript, prompt_template, ai_client)
            title, hook, tags = parse_ai_output(raw_ai)

            if not title:
                logging.warning("AI returned no title — saving raw output")
                title = "(Title generation failed)"

            if len(hook) > 250:
                hook = hook[:247] + "..."
                logging.info("  Hook trimmed to 250 chars")

            save_result(filename, transcript, title, hook, tags, raw_ai)
            successes += 1

        except Exception as e:
            logging.error("FAILED: %s — %s", filename, e)
            failures.append((filename, str(e)))
            continue

    logging.info("")
    logging.info("=" * 60)
    logging.info("DONE: %d/%d succeeded", successes, total)
    if failures:
        logging.info("FAILED (%d):", len(failures))
        for name, reason in failures:
            logging.info("  - %s: %s", name, reason)
    logging.info("Merged audio  -> %s", MERGED_AUDIO_FOLDER)
    logging.info("Transcripts   -> %s", TRANSCRIPTS_FOLDER)
    logging.info("Output files  -> %s", OUTPUT_FOLDER)
    logging.info("Log file      -> %s", LOG_FILE)
    logging.info("=" * 60)


# --------------------------
# Main
# --------------------------
def main():
    metadata_only = "--metadata-only" in sys.argv

    setup_logging()
    logging.info("=" * 60)
    logging.info("He Hath Done — CD-to-Testimony Pipeline")
    logging.info("=" * 60)

    if metadata_only:
        run_metadata_only()
    else:
        run_full_pipeline()


if __name__ == "__main__":
    main()
