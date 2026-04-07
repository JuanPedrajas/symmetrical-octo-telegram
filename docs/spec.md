# PRD: Phonetic-First Pronunciation Trainer (MVP)

## 1. Feature Overview
An interactive language learning tool that allows users to practice English pronunciation at the **phoneme level**. Unlike generic speech-to-text apps, this system provides granular feedback by comparing the user's spoken International Phonetic Alphabet (IPA) sequence against a "gold standard" dictionary, offering specific corrective hints (e.g., *"Sound should be X as in Word Y"*).

## 2. Core Requirements
* **Accuracy:** Must detect specific phoneme substitutions (e.g., /θ/ vs /f/).
* **Storage Efficiency:** User progress is tracked via a "Mastery Score" per phoneme rather than storing raw audio files.
* **Offline-Ready Logic:** The "Exact Match" comparison logic resides on the backend to keep the frontend lightweight.

## 3. Core Features
* **Dynamic Word Prompting:** Users are presented with words from curated or custom lists.
* **Phonetic Breakdown UI:** Post-recording, the word is displayed as a sequence of interactive IPA symbols (e.g., `/θ/ - /ɪ/ - /ŋ/ - /k/`).
* **Modular Error Feedback:** If a phoneme is missed, the app shows a specific corrective "Contrast Hint" based on a pre-defined Error Map.
* **Reference-Based List Management:** Users can create custom "Practice Sets" by referencing IDs from the Master Dictionary.
* **Adaptive Learning Loop:** Words with failed phonemes are automatically flagged for "Retry" or injected into future sessions.

## 4. Core Components
### A. The Master Dictionary (Source of Truth)
A static JSON/Database mapping of words to their phoneme sequences.
* *Example:* `{ "id": 101, "text": "Think", "ipa": ["θ", "ɪ", "ŋ", "k"] }`

### B. The Evaluation Engine (FastAPI)
* **Model:** `wav2vec2-lv60-phoneme` (Open Source).
* **Logic:** Performs a 1:1 index comparison between the model's output and the dictionary.

### C. The Error Map (Feedback Logic)
A lookup table for common phonetic errors.
* *Key:* `targetPhoneme_userPhoneme`
* *Value:* `"Sound should be [Target] as in [Word Y], not [User] as in [Word B]"`

## 5. App / User Flow
1.  **Selection:** User selects a "Word List" (e.g., "Difficult Th-Sounds").
2.  **Prompt:** App displays the target word "Think".
3.  **Recording:** User holds a button, speaks, and releases (Snapshot/Buffer).
4.  **Processing:** * React sends `.wav` Blob to FastAPI.
    * FastAPI runs inference $\rightarrow$ extracts IPA $\rightarrow$ compares to Dictionary.
5.  **Feedback:** React renders the word. Correct phonemes are **Green**. Incorrect are **Red**.
6.  **Correction:** User clicks a **Red** phoneme to see the "X as in Y" hint.
7.  **Loop:** User chooses to "Retry" the same word or move to the next.

## 6. Techstack
* **Frontend:** React (TypeScript), Tailwind CSS (for the Phonetic Breakdown UI).
* **Backend:** FastAPI (Python).
* **ML Libraries:** `transformers` (Hugging Face), `librosa` (audio processing), `torch`.
* **Database:** PostgreSQL (Storing User Profiles, Lists, and Mastery Scores).
* **Audio Capture:** Web MediaRecorder API.

## 7. Implementation Plan
* **Phase 1 (Infrastructure):** Set up FastAPI with `wav2vec2` and verify IPA transcription accuracy.
* **Phase 2 (Data):** Seed the Master Dictionary and the "Error Map" for top 20 common English mispronunciations.
* **Phase 3 (Frontend):** Build the "Phonetic Breakdown" component and audio recording state machine.
* **Phase 4 (Logic):** Implement the "Exact Match" alignment algorithm and feedback triggering.
* **Phase 5 (Persistence):** Add User Profiles and "Reference-based" list saving.

---

**Would you like me to generate the SQL schema for the `Master Dictionary` and `User Lists` to get the database started?**