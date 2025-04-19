import os

def save_lyrics(lyrics, filename):
    # Create lyrics directory if it doesn't exist
    lyrics_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'generated_lyrics')
    os.makedirs(lyrics_dir, exist_ok=True)
    
    # Add .txt extension if not provided
    if not filename.endswith('.txt'):
        filename += '.txt'
    
    # Create full file path
    file_path = os.path.join(lyrics_dir, filename)
    
    # Save the lyrics
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(lyrics)
    
    return file_path