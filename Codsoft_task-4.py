import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
ratings_dict = {
    "user_id": [1, 1, 1, 2, 2, 3, 3, 3],
    "movie_id": [101, 102, 103, 101, 104, 102, 103, 104],
    "rating": [5, 3, 4, 4, 5, 2, 4, 4]
}
ratings_df = pd.DataFrame(ratings_dict)
movies_dict = {
    "movie_id": [101, 102, 103, 104],
    "title": ["Movie A", "Movie B", "Movie C", "Movie D"],
    "genres": ["Action|Adventure", "Action|Thriller", "Romance|Drama", "Action|Romance"]
}
movies_df = pd.DataFrame(movies_dict)
user_item_matrix = ratings_df.pivot(index='user_id', columns='movie_id', values='rating').fillna(0)
user_similarity = cosine_similarity(user_item_matrix)
user_similarity_df = pd.DataFrame(user_similarity, index=user_item_matrix.index, columns=user_item_matrix.index)
def recommend_items_user_based(user_id, user_item_matrix, user_similarity_df, top_n=3):
    similar_users = user_similarity_df[user_id].sort_values(ascending=False)
    similar_users = similar_users.drop(user_id)
    recommended_items = pd.Series(dtype=float)
    for sim_user, score in similar_users.items():
        sim_user_ratings = user_item_matrix.loc[sim_user]
        sim_user_ratings = sim_user_ratings[sim_user_ratings > 0]
        recommended_items = pd.concat([recommended_items, sim_user_ratings])
    recommended_items = recommended_items.groupby(recommended_items.index).mean().sort_values(ascending=False)
    recommended_items = recommended_items.drop(user_item_matrix.loc[user_id][user_item_matrix.loc[user_id] > 0].index, errors='ignore')
    return recommended_items.head(top_n)
print("User-Based Recommendations for User 1:\n", recommend_items_user_based(1, user_item_matrix, user_similarity_df))
item_similarity = cosine_similarity(user_item_matrix.T)
item_similarity_df = pd.DataFrame(item_similarity, index=user_item_matrix.columns, columns=user_item_matrix.columns)
def recommend_similar_items(item_id, item_similarity_df, top_n=3):
    similar_items = item_similarity_df[item_id].sort_values(ascending=False)
    similar_items = similar_items.drop(item_id)
    return similar_items.head(top_n)
print("Item-Based Similar Items for Movie 101:\n", recommend_similar_items(101, item_similarity_df))
tfidf = TfidfVectorizer(tokenizer=lambda x: x.split('|'))
tfidf_matrix = tfidf.fit_transform(movies_df['genres'])
item_similarity_content = cosine_similarity(tfidf_matrix)
item_similarity_content_df = pd.DataFrame(item_similarity_content, index=movies_df['title'], columns=movies_df['title'])
def recommend_items_based_on_content(item_title, item_similarity_content_df, top_n=3):
    similar_items = item_similarity_content_df[item_title].sort_values(ascending=False)
    similar_items = similar_items.drop(item_title)
    return similar_items.head(top_n)
print("Content-Based Recommendations for Movie A:\n", recommend_items_based_on_content("Movie A", item_similarity_content_df))
def recommend(user_id, item_title):
    print("\n--- Recommendations for User-Based Collaborative Filtering ---")
    print(recommend_items_user_based(user_id, user_item_matrix, user_similarity_df))
    print("\n--- Recommendations for Item-Based Collaborative Filtering ---")
    movie_id = movies_df[movies_df['title'] == item_title]['movie_id'].values[0]
    print(recommend_similar_items(movie_id, item_similarity_df))
    print("\n--- Recommendations for Content-Based Filtering ---")
    print(recommend_items_based_on_content(item_title, item_similarity_content_df))
user_id = 1
item_title = "Movie A"
recommend(user_id, item_title)
