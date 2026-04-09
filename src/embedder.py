import pandas as pd
import pickle # To save our vectors to a file
from sentence_transformers import SentenceTransformer

def generate_embeddings(text_list, model_name='all-MiniLM-L6-v2'):
    """
    Turns a list of strings (tags) into a giant matrix of numbers.
    """
    print(f"🧠 Loading AI Model: {model_name}...")
    model = SentenceTransformer(model_name)
    
    print("⏳ Vectorizing movies... (this might take a minute)")
    # This is where the magic happens
    embeddings = model.encode(text_list, show_progress_bar=True)
    
    return embeddings

def save_embeddings(embeddings, filepath):
    """Saves the vectors so we don't have to re-calculate them every time."""
    with open(filepath, 'wb') as f:
        pickle.dump(embeddings, f)
    print(f"💾 Vectors saved to {filepath}")

if __name__ == "__main__":
    from processor import prepare_movie_data
    
    # 1. Get the clean data
    df = prepare_movie_data('data/tmdb_5000_movies.csv')
    
    # 2. Generate the math vectors
    movie_vectors = generate_embeddings(df['tags'].tolist())
    
    # 3. Save them to a file (so we can use them in database.py)
    save_embeddings(movie_vectors, 'data/movie_vectors.pkl')
    
    print(f"✅ Finished! Generated a matrix of shape: {movie_vectors.shape}")