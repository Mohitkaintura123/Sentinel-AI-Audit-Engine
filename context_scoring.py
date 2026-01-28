# context_scoring.py

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def compute_relevance_scores(query, documents):
    """
    Computes semantic similarity between query and document summaries.
    
    Args:
        query (str): User query
        documents (list of str): Document summaries
    
    Returns:
        list of float: relevance scores (0 to 1)
    """
    corpus = [query] + documents

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(corpus)

    query_vector = tfidf_matrix[0]
    doc_vectors = tfidf_matrix[1:]

    similarities = cosine_similarity(query_vector, doc_vectors)[0]

    return similarities.tolist()
