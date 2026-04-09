import pandas as pd
import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from src.embedder import generate_embeddings

class VectraDB:
    def __init__(self, data_path, vector_path):
        # 1. Load our cleaned movie names/titles
        self.df = pd.read_csv(data_path)
        
        # 2. Load our pre-calculated math vectors
        with open(vector_path, 'rb') as f:
            self.vectors = pickle.load(f)
        print("🗄️ Vectra Database Loaded and Ready!")

    def search(self, query, top_k=5):
        """
        The core search logic:
        1. Turn query into a vector
        2. Compare it to all movie vectors
        3. Return the best matches
        """
        # Step 1: Vectorize the user's search term
        # We wrap [query] in a list because the embedder expects a list
        query_vector = generate_embeddings([query])
        
        # Step 2: Calculate Cosine Similarity
        # This compares the query_vector against ALL 4800+ movie vectors at once
        similarities = cosine_similarity(query_vector, self.vectors).flatten()
        
        # Step 3: Get the indices of the highest scores
        # argsort gives indices from low to high; [-top_k:] gets the best ones
        indices = similarities.argsort()[-top_k:][::-1]
        
        # Step 4: Return the movie details
        results = self.df.iloc[indices].copy()
        results['score'] = similarities[indices]
        return results[['id', 'title', 'score']]

if __name__ == "__main__":
    # Quick Test Run
    # Make sure you've run processor.py and embedder.py first!
    try:
        db = VectraDB('data/cleaned_movies.csv', 'data/movie_vectors.pkl')
        
        user_query = "A movie about space travel and black holes"
        print(f"\n🔍 Searching for: '{user_query}'...")
        
        recommendations = db.search(user_query)
        print("\n--- Top Recommendations ---")
        print(recommendations)
        
    except FileNotFoundError:
        print("❌ Error: Files not found. Did you run the other scripts first?")