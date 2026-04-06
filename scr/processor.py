import pandas as pd
import ast # This helps us read the "messy" JSON strings in the CSV

def convert_genres(genre_str):
    """
    The CSV stores genres like: '[{"name": "Action"}, {"name": "Adventure"}]'
    This function turns that into a simple string: 'Action Adventure'
    """
    genres = []
    # ast.literal_eval converts the string into a real Python list
    for i in ast.literal_eval(genre_str):
        genres.append(i['name'])
    return " ".join(genres)

def prepare_movie_data(filepath):
    print("🚀 Starting Data Clean-up...")
    
    # 1. Load the data
    df = pd.read_csv(filepath)
    
    # 2. Select only the columns we actually need for the "Vibe"
    # We need 'id' and 'title' to show the results, and 'overview' + 'genres' for the math.
    df = df[['id', 'title', 'overview', 'genres']].dropna()
    
    # 3. Clean the Genres (Turning JSON into plain text)
    print("🧹 Cleaning Genre strings...")
    df['genres'] = df['genres'].apply(convert_genres)
    
    # 4. Create the "Tags" column (The "Semantic Fingerprint")
    # We combine the plot and the genre so the AI has full context.
    df['tags'] = df['overview'] + " " + df['genres']
    
    # 5. Final Polish: Lowercase everything (AI models prefer consistency)
    df['tags'] = df['tags'].apply(lambda x: x.lower())
    
    # We only keep the ID, Title, and the Tags for the next step
    new_df = df[['id', 'title', 'tags']]
    
    print(f"✅ Success! {len(new_df)} movies are cleaned and ready.")
    return new_df

if __name__ == "__main__":
    # This part runs only if you execute this file directly
    try:
        cleaned_data = prepare_movie_data('data/tmdb_5000_movies.csv')
        print("\n--- Preview of Cleaned Data ---")
        print(cleaned_data.head())
    except FileNotFoundError:
        print("❌ Error: Could not find 'tmdb_5000_movies.csv' in the 'data/' folder.")