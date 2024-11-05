import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from networkx.algorithms.community import greedy_modularity_communities

# Seed for reproducibility
np.random.seed(42)

# Define number of users (nodes) and connections (edges)
num_users = 50
num_interactions = 200

# Initialize an undirected graph
G = nx.Graph()

# Add users (nodes) to the graph
G.add_nodes_from(range(1, num_users + 1))

# Randomly create edges (interactions) between users
for _ in range(num_interactions):
    user1, user2 = np.random.choice(range(1, num_users + 1), size=2, replace=False)
    G.add_edge(user1, user2)

# Draw the social graph
plt.figure(figsize=(10, 8))
nx.draw_networkx(G, with_labels=True, node_color='skyblue', edge_color='gray', node_size=500)
plt.title("Social Graph of User Interactions")
plt.show()

# Calculate centrality measures
degree_centrality = nx.degree_centrality(G)
betweenness_centrality = nx.betweenness_centrality(G)
closeness_centrality = nx.closeness_centrality(G)

# Combine centrality measures into a DataFrame for easy analysis
centrality_df = pd.DataFrame({
    'User': list(degree_centrality.keys()),
    'Degree Centrality': list(degree_centrality.values()),
    'Betweenness Centrality': list(betweenness_centrality.values()),
    'Closeness Centrality': list(closeness_centrality.values())
})

# Display top influential users by degree centrality
top_influential_users = centrality_df.sort_values(by='Degree Centrality', ascending=False).head(5)
print("Top Influential Users by Degree Centrality:")
print(top_influential_users)

# Find communities in the graph
communities = list(greedy_modularity_communities(G))

# Display community structure
print("Number of Communities Detected:", len(communities))
for i, community in enumerate(communities, start=1):
    print(f"Community {i}: {sorted(community)}")

# Visualize communities
colors = [i for i, community in enumerate(communities) for node in community]
plt.figure(figsize=(10, 8))
pos = nx.spring_layout(G)  # Position layout for better visualization
nx.draw(G, pos, node_color=colors, with_labels=True, node_size=500, cmap=plt.cm.Paired)
plt.title("Social Graph with Community Clusters")
plt.show()

# Insights on influential users
influential_user = top_influential_users.iloc[0]
print(f"The most influential user based on degree centrality is User {influential_user['User']}.")

# Check if this user belongs to a specific community
user_community = next((i for i, comm in enumerate(communities) if influential_user['User'] in comm), None)
if user_community is not None:
    print(f"User {influential_user['User']} is part of Community {user_community + 1} with {len(communities[user_community])} users.")
    
# Interaction frequency
interaction_counts = [G.degree(user) for user in G.nodes]
average_interactions = np.mean(interaction_counts)
print(f"Average number of interactions per user: {average_interactions:.2f}")

# Visualization of interaction frequency distribution
plt.figure(figsize=(8, 6))
plt.hist(interaction_counts, bins=10, color='skyblue', edgecolor='black')
plt.xlabel('Number of Interactions')
plt.ylabel('Frequency of Users')
plt.title('Distribution of User Interactions')
plt.show()
