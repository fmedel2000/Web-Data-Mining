"""
Author: Francisco Medel Molinero
Description of the script: Data Representation for each document and query using the Vector Space Model with binary, Term Frequency and TF-IDF representation and computing relevance scores for each combination of query, document using Euclidean distance and Cosine similarity measure.
Making an evaluation of the quality and difference of both scores and different weighting schemas, compute Precision, Recall, F-measure.
Input of the function: cranfield folder with data in csv format
Output of the function: output.csv
"""


# imports
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import numpy as np
import csv


# Function to get binary, term frequency and TF-IDF matrices using a vectorizer with data
def get_matrices(data):
    # Binary matrix
    vectorizer = CountVectorizer(binary=True)
    bin_matrix = vectorizer.fit_transform(data)

    # TF(term frequency) matrix
    vectorizer = CountVectorizer(binary=False)
    tf_matrix = vectorizer.fit_transform(data)

    # TF-IDF matrix
    vectorizer = TfidfVectorizer()
    tf_idf_matrix = vectorizer.fit_transform(data)

    return bin_matrix, tf_matrix, tf_idf_matrix


# Function to calculate cosine and euclidean's values
def cos_and_euclidean(matrix):
    # COSINE
    sim_cos = np.array(cosine_similarity(matrix[1400], matrix[0:(1400)])[0])
    sorted_cos = sim_cos.argsort()[::-1] + 1
    # EUCLIDEAN
    sim_eu = np.array(euclidean_distances(matrix[1400], matrix[0:(1400)])[0])
    sorted_eu = sim_eu.argsort() + 1

    return [sorted_cos[:20], sorted_eu[:20]]


# Function to obtain the relevant documents associated with the query
def get_relevant(query):
    rel = []
    with open("./cranfield/r/" + str(query + 1) + ".txt") as file:
        for line in file.readlines():
            rel.append(int(line))
    return rel


# Function to get the values of precision, recall and f_measure based on retrieved and relevant documents
def get_statistics(retrieved, relevant):
    rel_counter = 0
    for document in retrieved:
        if document in relevant:
            rel_counter += 1

    precision = rel_counter / len(retrieved)
    recall = rel_counter / len(relevant)

    if precision == 0 and recall == 0:
        f_measure = 0
    else:
        f_measure = 2 * (precision * recall) / (precision + recall)

    return [precision, recall, f_measure]


# Function to process data and get the statistics of the different methods -> Binary, Term or TD-IDF based on Cosine & Euclidean values
def processing(data, rel):
    # binary, TF and TF-IDF matrices
    bin_matrix, tf_matrix, tf_idf_matrix = get_matrices(data)

    # Cosine and euclidean for binary matrix
    bin_cos = cos_and_euclidean(bin_matrix)[0]
    bin_euclid = cos_and_euclidean(bin_matrix)[1]

    # Cosine and euclidean for TF matrix
    tf_cos = cos_and_euclidean(tf_matrix)[0]
    tf_euclid = cos_and_euclidean(tf_matrix)[1]

    # Cosine and euclidean for TF-IDF matrix
    tf_idf_cos = cos_and_euclidean(tf_idf_matrix)[0]
    tf_idf_euclid = cos_and_euclidean(bin_matrix)[1]

    # Binary stats
    bin_cos_stats = get_statistics(bin_cos, rel)
    bin_euclid_stats = get_statistics(bin_euclid, rel)

    # TF stats
    tf_cos_stats = get_statistics(tf_cos, rel)
    tf_euclid_stats = get_statistics(tf_euclid, rel)

    # TF-IDF stats
    tf_idf_cos_stats = get_statistics(tf_idf_cos, rel)
    tf_idf_euclid_stats = get_statistics(tf_idf_euclid, rel)

    # All stats in one variable
    stats = bin_cos_stats + bin_euclid_stats + tf_cos_stats + tf_euclid_stats + tf_idf_cos_stats + tf_idf_euclid_stats
    return stats


# Main function to process the data and saving the results/statistics in a csv file
def main():
    with open("output.csv", 'w') as file:
        output = csv.writer(file, delimiter=";")
        output.writerow(["query",
                         "Binary cosine precision", "Binary cosine recall", "Binary cosine f_measure",
                         "Binary euclidean precision", "Binary euclidean recall", "Binary euclidean f_measure",
                         "Term cosine precision", "Term cosine recall", "Term cosine f_measure",
                         "Term euclidean precision", "Term euclidean recall", "Term cosine f_measure",
                         "Tf_idf cosine precision", "Tf_idf cosine recall", "Tf_idf cosine f_measure",
                         "Tf_idf euclidean precision", "Tf_idf euclidean recall", "Tf_idf euclidean f_measure",
                         ])

        # prepare corpus
        corpus = []
        for d in range(1400):
            f = open("./cranfield/d/" + str(d + 1) + ".txt")
            corpus.append(f.read())
        # add query to corpus
        for q in range(225):
            f = open("./cranfield/q/" + str(q + 1) + ".txt")
            # corpus.append(f.read())
            data = list(corpus)
            data.append(f.read())

            row_builder = [q + 1]

            rel = get_relevant(q)
            row_builder += processing(data, rel)

            output.writerow(row_builder)

if __name__ == '__main__':
    main()
