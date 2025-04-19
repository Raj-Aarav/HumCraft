import google.generativeai as genai

# ✅ STEP 1: Configure Gemini API
genai.configure(api_key="AIzaSyAKc-1PNgntZHQvUX0Vpf-NWgsWpA6gK24")

# ✅ STEP 2: User Input
user_genre = input("🎵 Enter the song genre: ").strip()
user_keywords = input("🔑 Enter keywords (comma-separated): ").strip()

# ✅ STEP 3: Create a Dynamic Prompt for Gemini
prompt_text = f"""
You are an expert in music and emotions.

Given the **song genre**: "{user_genre}" 
And **keywords**: "{user_keywords}"

Predict the **most appropriate emotion/mood** associated with the song. 
- Consider how these elements influence a listener's feelings.
- Return **only the single best mood name**, nothing else.
"""

# ✅ STEP 4: Generate Mood Prediction from Gemini
model = genai.GenerativeModel("gemini-1.5-pro")
response = model.generate_content(prompt_text)

# ✅ STEP 5: Extract and Print Mood
predicted_mood = response.text.strip()
print("\n🎭 **Predicted Mood:**", predicted_mood)

# ✅ STEP 6: Construct a Structured Prompt for Lyrics Generation
lyrics_prompt = f"""
🎵 **Song Genre**: {user_genre}
🎭 **Mood**: {predicted_mood}
🔑 **Themes/Keywords**: {user_keywords}

📜 **Instructions for Lyrics Generation**:
1. **Structure**: The lyrics should follow a structured format with:
   - **Verse 1**
   - **Chorus**
   - **Verse 2**
   - **Bridge**
   - **Chorus (Refrain)**
   - **Outro**
   
2. **Emotional Tone**: Ensure that the lyrics **match the predicted mood**: {predicted_mood}.
   - If it's **joyful**, make the lyrics uplifting and energetic.
   - If it's **melancholic**, use poetic and deep emotional expressions.
   - If it's **romantic**, add intimate and heartfelt lines.

3. **Style & Rhyme**:
   - Follow a **natural rhyme scheme** (AABB, ABAB, or free verse depending on the genre).
   - Use **vivid imagery & metaphors** to convey emotions.

4. **Incorporate the Given Keywords**: "{user_keywords}"
   - Ensure that these words appear **naturally** in the lyrics without being forced.
   - Make them central to the **song's theme**.

5. **Creativity & Originality**:
   - The lyrics should **feel like an actual song** that could be performed.
   - Avoid generic phrases—bring a **unique touch** to the song.

Now, generate the lyrics based on these instructions.
"""

# ✅ STEP 7: Print the Structured Prompt
print("\n📝 **Structured Prompt for Lyrics Generation:**\n")
print(lyrics_prompt)

# ✅ STEP 8: (Optional) Feed this prompt into Gemini/GPT for Lyrics Generation
lyrics_response = model.generate_content(lyrics_prompt)
generated_lyrics = lyrics_response.text.strip()

# ✅ STEP 9: Print the Generated Lyrics
print("\n🎶 **Generated Lyrics:**\n")
print(generated_lyrics)


# ##################

# ✅ STEP 10: Export for use in melody.py
if __name__ == "__main__":
    pass  # So Phase_1 doesn't execute when imported

# Expose these variables for external modules
__all__ = ['generated_lyrics', 'predicted_mood']
