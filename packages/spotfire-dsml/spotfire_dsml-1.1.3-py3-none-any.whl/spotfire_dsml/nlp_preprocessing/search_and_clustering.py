import pandas as pd
from sentence_transformers import SentenceTransformer, CrossEncoder, util
import time
from rank_bm25 import BM25Okapi
from sklearn.feature_extraction import _stop_words
import string
from tqdm.autonotebook import tqdm
import numpy as np

'''
Citations for reference
https://www.sbert.net/examples/applications/semantic-search/README.html [Sentence Transformers Documentation]
https://huggingface.co/tasks/sentence-similarity [HuggingFace Sentence Similarity]
'''

def init_embeddings(corpus, model_name='Snowflake/snowflake-arctic-embed-xs'):
    """
        Initial embeddings

        This function instantiates a sentence transformer model and creates embeddings

        Parameters
        ----------
        corpus : pandas series
            A text data column

        Returns
        -------
        model: Sentence Transformer object
            sentence transformer model
        corpus_embeddings: data frame
            corpus embeddings in torch array
    """

    model = SentenceTransformer(model_name)
    corpus_embeddings = model.encode(corpus, show_progress_bar=True, convert_to_tensor=True)
    print("Corpus loaded with {} sentences / embeddings".format(len(corpus)))
    return model, corpus_embeddings

def cosine_similarity(emb1, emb2):
    return float(util.pytorch_cos_sim(emb1, emb2))

def paraphrase_mining(corpus, model_name="all-MiniLM-L6-v2"):
    """
        Paraphrase mining

        This function performs cosine similarity for all pairs in a corpus (more efficient than individually done)

        Parameters
        ----------
        corpus : pandas series
            A text data column

        Returns
        -------
        res: data frame
            corpus texts and similarity measures for each pair
    """

    model = SentenceTransformer(model_name)
    paraphrases = util.paraphrase_mining(model, corpus)
    res= []
    for paraphrase in paraphrases[0:10]:
        score, i, j = paraphrase
        res.append({"corpus_id_1": i, "corpus_1": corpus[i], "corpus_id_2": j, "corpus_2": corpus[j], "score": score})
    return pd.DataFrame(res)

def symmetric_search(inp_question, model, corpus_embeddings, corpus):
    """
        Symmetric Search

        This function performs symmetric search given a query and embeddings from a corpus

        Parameters
        ----------
        inp_question : str
            text query
        model: sentence transformer object
            sentence transformer model
        corpus_embeddings: torch arr
            torch array of embeddings
        corpus: pd series
            string column of text

        Returns
        -------
        res: data frame
            ordered data frame of most similar corpus documents by score
    """

    start_time = time.time()
    question_embedding = model.encode(inp_question, convert_to_tensor=True)
    hits = util.semantic_search(question_embedding, corpus_embeddings)
    end_time = time.time()
    res = hits[0]
    for dictionary in res:
        dictionary['corpus'] = corpus[int(dictionary['corpus_id'])]
    return pd.DataFrame(res)

def bm25_tokenizer(text):
    tokenized_doc = []
    # We lower case our text and remove stop-words from indexing
    for token in text.lower().split():
        token = token.strip(string.punctuation)

        if len(token) > 0 and token not in _stop_words.ENGLISH_STOP_WORDS:
            tokenized_doc.append(token)
    return tokenized_doc

def init_asymmetric_search(corpus, biencoder_name='all-mpnet-base-v2', crossencoder_name='cross-encoder/ms-marco-MiniLM-L-6-v2'):
    """
        Initial embeddings

        This function instantiates a sentence transformer model and creates embeddings

        Parameters
        ----------
        corpus : pandas series
            A text data column

        Returns
        -------
        bm25: bm25 object
            bm25 model
        bi_encoder: Sentence Transformer object
            sentence transformer model
        cross_encoder: Sentence Transformer object
            sentence transformer model
        corpus_embeddings: data frame
            corpus embeddings in torch array
    """

    # We use the Bi-Encoder to encode all passages, so that we can use it with semantic search
    bi_encoder = SentenceTransformer(biencoder_name)
    bi_encoder.max_seq_length = 256  # Truncate long passages to 256 tokens

    # The bi-encoder will retrieve 100 documents. We use a cross-encoder, to re-rank the results list to improve the quality
    cross_encoder = CrossEncoder(crossencoder_name)

    corpus_embeddings = bi_encoder.encode(corpus, convert_to_tensor=True, show_progress_bar=True)


    tokenized_corpus = []
    for passage in tqdm(corpus):
        tokenized_corpus.append(bm25_tokenizer(passage))
    bm25 = BM25Okapi(tokenized_corpus)

    return bm25, bi_encoder, cross_encoder, corpus_embeddings


# This function will search all wikipedia articles for passages that
# answer the query
def asymmetric_search(query, corpus, corpus_embeddings, bm25, bi_encoder, cross_encoder):
    """
        Asymmetric Search

        This function performs asymmetric search given a query and embeddings from a corpus

        Parameters
        ----------
        inp_question : str
            text query
        bm25: bm25 object
            bm25 model
        bi_encoder: sentence transformer object
            sentence transformer model
        cross_encoder: sentence transformer object
            sentence transformer model
        corpus_embeddings: torch arr
            torch array of embeddings
        corpus: pd series
            string column of text

        Returns
        -------
        res: data frame
            ordered data frame of most similar corpus documents by score
    """

    ##### BM25 search (lexical search) #####
    bm25_scores = bm25.get_scores(bm25_tokenizer(query))
    top_n = np.argpartition(bm25_scores, -20)[-20:]
    bm25_hits = [{'corpus_id': idx, 'score': bm25_scores[idx]} for idx in top_n]
    bm25_hits = sorted(bm25_hits, key=lambda x: x['score'], reverse=True)

    #lexical search (BM25) hits
    for hit in bm25_hits:
        hit['corpus'] = corpus[hit['corpus_id']]
        #print("\t{:.3f}\t{}".format(hit['score'], corpus[hit['corpus_id']].replace("\n", " ")))
    bm25_df = pd.DataFrame(bm25_hits)

    ##### Semantic Search #####
    # Encode the query using the bi-encoder and find potentially relevant passages
    question_embedding = bi_encoder.encode(query, convert_to_tensor=True)
    # question_embedding = question_embedding.cuda()
    hits = util.semantic_search(question_embedding, corpus_embeddings, top_k=32)
    hits = hits[0]  # Get the hits for the first query

    ##### Re-Ranking #####
    # Now, score all retrieved passages with the cross_encoder
    cross_inp = [[query, corpus[hit['corpus_id']]] for hit in hits]
    cross_scores = cross_encoder.predict(cross_inp)

    # Sort results by the cross-encoder scores
    for idx in range(len(cross_scores)):
        hits[idx]['cross-score'] = cross_scores[idx]

    # Bi-Encoder Retrieval hits
    hits = sorted(hits, key=lambda x: x['score'], reverse=True)
    for hit in hits:
        hit['corpus'] = corpus[hit['corpus_id']]
    biencoder_df = pd.DataFrame(hits)

    # Cross-Encoder Re-ranker hits"
    hits = sorted(hits, key=lambda x: x['cross-score'], reverse=True)
    for hit in hits:
        hit['corpus'] = corpus[hit['corpus_id']]
    crossencoder_df = pd.DataFrame(hits)

    return bm25_df, biencoder_df, crossencoder_df

def fast_clustering(corpus, corpus_embeddings, min_community_size=10, threshold=0.75):
    """
        Fast clustering

        An mash of agglomerative and Kmeans clustering from sentence transformers library

        Parameters
        ----------
        corpus_embeddings: torch arr
            torch array of embeddings
        corpus: pd series
            string column of text

        Returns
        -------
        clusters: data frame
            data frame of each document with designated cluster
    """

    print("Start clustering")
    start_time = time.time()
    # min_cluster_size: Only consider cluster that have at least 25 elements
    # threshold: Consider sentence pairs with a cosine-similarity larger than threshold as similar
    clusters = util.community_detection(corpus_embeddings, min_community_size=min_community_size, threshold=threshold)

    print("Clustering done after {:.2f} sec".format(time.time() - start_time))

    # Print for all clusters the top 3 and bottom 3 elements
    cluster_list=[]
    for i, cluster in enumerate(clusters):
        print("\nCluster {}, #{} Elements ".format(i + 1, len(cluster)))
        for sentence_id in cluster:
            cluster_list.append({'cluster': i, 'corpus_id': sentence_id, 'corpus': corpus[sentence_id]})

    return pd.DataFrame(cluster_list)


'''
SAMPLE USAGES FOR EMBEDDINGS-RETRIEVAL-CLUSTERING FLOWS
'''
#sample flow for asymmetric search
def run_asymmetric_search(query, corpus):
    bm25, bi_encoder, cross_encoder, corpus_embeddings = init_asymmetric_search(corpus)
    bm25_df, biencoder_df, crossencoder_df = asymmetric_search(query, corpus, corpus_embeddings, bm25, bi_encoder, cross_encoder)
    return bm25_df, biencoder_df, crossencoder_df

#sample flow for symmetric search
def run_symmetric_search(query, corpus):
    model, corpus_embeddings = init_embeddings(corpus)
    search_df = symmetric_search(query, model, corpus_embeddings, corpus)
    return search_df

#sample flow for clustering (can use any embeddings)
def run_clustering(corpus):
    model, corpus_embeddings = init_embeddings(corpus)
    return fast_clustering(corpus, corpus_embeddings)