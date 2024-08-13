from bertopic import BERTopic
import pandas as pd

''' Source for reference: https://github.com/MaartenGr/BERTopic '''

def run_bertopic(text_data, model):
    """
        Run Bertopic

        This function instantiates and runs the topic model algorithm

        Parameters
        ----------
        text_data : pandas series
            A text data column
        model : obj
            Bertopic instaniated model

        Returns
        -------
        topics: list
            1D list of topics
        probabilities: list
            2D array of all probabilities
    """

    # Fit the model on the provided text data
    topics, probabilities = model.fit_transform(text_data)

    # Return the topics and their probabilities
    return topics, probabilities

#main function call
def main(text_data):
    """
        Main

        This function instantiates and runs the topic model algorithm

        Parameters
        ----------
        text_data : pandas series
            A text data column

        Returns
        -------
        all_topics_df: data frame
            Access all topics
        topics_info_df: data frame
            Get all topics information
        docs_info_df: data frame
            Get all documents information
    """

    # Instantiate BERTopic model
    model = BERTopic()

    topics, probabilities = run_bertopic(text_data, model)
    all_topics = model.get_topics()
    topics_info_df = model.get_topic_info()
    docs_info_df = model.get_document_info(text_data)

    #reformat all_topics
    topics, keywords, scores = [], [], []
    for k, v in all_topics.items():
        for tok, score in v:
            topics.append(k)
            keywords.append(tok)
            scores.append(score)
    all_topics_df = pd.DataFrame(data={'topics': topics, 'keywords': keywords, 'score': score})

    return all_topics_df, topics_info_df, docs_info_df