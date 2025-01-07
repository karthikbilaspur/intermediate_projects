import pandas as pd
from collections import Counter
import numpy as np

# Sample user-item interaction data
data = {
    "User": [1, 1, 1, 2, 2, 3, 3, 3, 4, 4],
    "Item": [101, 102, 103, 101, 103, 101, 102, 104, 103, 104],
    "Rating": [5, 4, 3, 4, 5, 5, 3, 4, 3, 5]
}

# Sample item attributes (content-based features)
item_attributes = {
    101: {"Genre": "Action", "Director": "A"},
    102: {"Genre": "Comedy", "Director": "B"},
    103: {"Genre": "Action", "Director": "A"},
    104: {"Genre": "Comedy", "Director": "C"}
}

# Create DataFrame
df = pd.DataFrame(data)

# Calculate item similarities using Jaccard similarity (collaborative filtering)
def jaccard_similarity(item1, item2):
    users_item1 = set(df[df['Item'] == item1]['User'])
    users_item2 = set(df[df['Item'] == item2]['User'])
    intersection = users_item1.intersection(users_item2)
    union = users_item1.union(users_item2)
    return len(intersection) / len(union)

# Calculate content-based similarity
def content_based_similarity(item1, item2):
    attributes1 = item_attributes[item1]
    attributes2 = item_attributes[item2]
    common_attributes = set(attributes1.keys()).intersection(set(attributes2.keys()))
    similarity = len([attr for attr in common_attributes if attributes1[attr] == attributes2[attr]]) / len(common_attributes)
    return similarity

# Calculate hybrid similarity
def hybrid_similarity(item1, item2):
    collaborative_similarity = jaccard_similarity(item1, item2)
    content_based_similarity_value = content_based_similarity(item1, item2)
    return 0.6 * collaborative_similarity + 0.4 * content_based_similarity_value

# Function to get item recommendations
def get_recommendations(user, num_recommendations):
    user_items = set(df[df['User'] == user]['Item'])
    similar_items = {}
    
    for item in df['Item'].unique():
        if item not in user_items:
            similar_items[item] = hybrid_similarity(item, list(user_items)[0])
    
    # Sort similar items by hybrid similarity
    sorted_items = sorted(similar_items.items(), key=lambda x: x[1], reverse=True)
    
    # Return top N recommended items
    return [item[0] for item in sorted_items[:num_recommendations]]

# Example usage
user_id = 1
num_recommendations = 2

recommended_items = get_recommendations(user_id, num_recommendations)
print(f"Recommended items for User {user_id}: {recommended_items}")