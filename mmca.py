# app.py

# Run using:
# streamlit run app.py

import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

# Louvain community detection
try:
    import community as community_louvain
except ImportError:
    import community.community_louvain as community_louvain


# -----------------------------
# Functions
# -----------------------------
def build_graph(edges):
    G = nx.Graph()
    G.add_edges_from(edges)
    return G


def detect_communities(G):
    return community_louvain.best_partition(G)


def find_influencers(G):
    degree = nx.degree_centrality(G)
    betweenness = nx.betweenness_centrality(G)

    combined_score = {
        node: (degree[node] + betweenness[node]) / 2
        for node in G.nodes()
    }

    influencers = sorted(combined_score.items(), key=lambda x: x[1], reverse=True)

    return influencers, degree, betweenness


def visualize_graph(G, partition):
    pos = nx.spring_layout(G, seed=42)
    colors = [partition[node] for node in G.nodes()]

    fig, ax = plt.subplots()
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color=colors,
        cmap=plt.cm.Set3,
        node_size=800,
        font_size=10,
        ax=ax
    )
    ax.set_title("Fan Network Graph")
    return fig


# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Fan Network Analysis", layout="wide")

st.title("🎬 Entertainment Fan Network Analysis")

st.markdown("Analyze fan communities and find influencers using graph theory.")

# -----------------------------
# User Input
# -----------------------------
st.sidebar.header("Input Data")

edge_input = st.sidebar.text_area(
    "Enter edges (format: A-B, B-C, C-D)",
    "A-B, A-C, B-C, D-E, E-F, D-F, C-D, G-H, H-I, G-I"
)

run_button = st.sidebar.button("Run Analysis")

# -----------------------------
# Process Input
# -----------------------------
def parse_edges(edge_text):
    edges = []
    pairs = edge_text.split(",")

    for pair in pairs:
        nodes = pair.strip().split("-")
        if len(nodes) == 2:
            edges.append((nodes[0].strip(), nodes[1].strip()))
    return edges


# -----------------------------
# Run Analysis
# -----------------------------
if run_button:
    edges = parse_edges(edge_input)

    if len(edges) == 0:
        st.error("Please enter valid edges!")
    else:
        G = build_graph(edges)
        partition = detect_communities(G)
        influencers, degree, betweenness = find_influencers(G)

        # Layout
        col1, col2 = st.columns(2)

        # -----------------------------
        # Influencers
        # -----------------------------
        with col1:
            st.subheader("🔥 Influencer Ranking")
            for node, score in influencers:
                st.write(f"{node} → {score:.4f}")

        # -----------------------------
        # Communities
        # -----------------------------
        with col2:
            st.subheader("👥 Communities")
            for node, comm in partition.items():
                st.write(f"{node} → Community {comm}")

        # -----------------------------
        # Graph Visualization
        # -----------------------------
        st.subheader("📊 Network Visualization")
        fig = visualize_graph(G, partition)
        st.pyplot(fig)

else:
    st.info("Enter data and click 'Run Analysis' 🚀")
