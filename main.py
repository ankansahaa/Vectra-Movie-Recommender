import os
from src.processor import prepare_movie_data
from src.embedder import generate_embeddings, save_embeddings
from src.database import VectraDB

def initial_setup():
    """Run this only if you haven't generated vectors yet."""
    csv_path = 'data/tmdb_5000_movies.csv'
    vector_path = 'data/movie_vectors.pkl'
    cleaned_csv_path = 'data/cleaned_movies.csv'

    # 1. Clean the data
    df = prepare_movie_data(csv_path)
    df.to_csv(cleaned_csv_path, index=False)

    # 2. Generate and save embeddings
    vectors = generate_embeddings(df['tags'].tolist())
    save_embeddings(vectors, vector_path)
    print("✨ System setup complete!")

def run_search_engine():
    """The interactive loop for the user."""
    # Initialize the DB (loads files into memory once)
    db = VectraDB('data/cleaned_movies.csv', 'data/movie_vectors.pkl')

    print("\n" + "="*30)
    print("🎬 VECTRA MOVIE RECOMMENDER")
    print("="*30)
    print("Type 'exit' to quit.")

    while True:
        query = input("\n🔍 What kind of movie are you looking for? ")
        
        if query.lower() == 'exit':
            break

        results = db.search(query, top_k=5)
        
        print("\n🍿 Top Recommendations for you:")
        # We use itertuples for a clean print
        for row in results.itertuples():
            # Formatting the score as a percentage
            print(f"⭐ {row.title} (Match: {row.score*100:.1f}%)")

if __name__ == "__main__":
    # Check if BOTH the cleaned data AND the vectors exist
    csv_exists = os.path.exists('data/cleaned_movies.csv')
    vectors_exist = os.path.exists('data/movie_vectors.pkl')
    
    if not csv_exists or not vectors_exist:
        print("🛠️ First time setup: Cleaning data and building vectors...")
        initial_setup()
    
    # Now that we are sure the files exist, start the engine
    run_search_engine()