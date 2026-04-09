import pandas as pd
import ast
import re

def convert_genres(genre_str):
    """
    TMDB stores genres as a stringified list of dicts. 
    This turns '[{"name": "Action"}]' into 'Action'.
    """
    try:
        # literal_eval is safer than eval() for string-to-list conversion
        genres_list = ast.literal_eval(genre_str)
        return " ".join([i['name'] for i in genres_list])
    except (ValueError, SyntaxError):
        return ""

def clean_text(text):
    """
    Removes the 'noise' so the embedder focuses on the meaning.
    """
    if not isinstance(text, str):
        return ""
    # Lowercase and remove special characters/punctuation
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text.strip()

def prepare_movie_data(filepath):
    """
    The main pipeline to go from CSV to a clean DataFrame.
    """
    print(f"📂 Loading data from {filepath}...")
    df = pd.read_csv(filepath)
    
    # 1. Grab essential columns and drop rows with missing info
    df = df[['id', 'title', 'overview', 'genres']].dropna()
    
    # 2. Clean the Genres
    df['genres'] = df['genres'].apply(convert_genres)
    
    # 3. Create 'tags' (The Semantic Fingerprint)
    # We combine plot (overview) + genres so the AI knows the 'vibe'
    df['tags'] = df['overview'] + " " + df['genres']
    
    # 4. Final text scrub
    df['tags'] = df['tags'].apply(clean_text)
    
    # 5. Keep only what we need for the database
    cleaned_df = df[['id', 'title', 'tags']]
    
    print(f"✅ Cleaned {len(cleaned_df)} movies successfully!")
    return cleaned_df

if __name__ == "__main__":
    # Test it out locally
    # Make sure you have the CSV in a 'data' folder!
    try:
        sample = prepare_movie_data('data/tmdb_5000_movies.csv')
        print(sample.head())
        print(sample.iloc[0]['tags'])
    except FileNotFoundError:
        print("❌ Skip: CSV file not found. Check your 'data/' folder.")