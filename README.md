Naive Bayes Classifier for Movie Reviews

The pre-process.py script takes two directories of movie reviews, one positive and one negative.

All words in the reviews are lowercased, some noise is removed. The reviews from each directory are concatenated into movie-review-BOW-train-pos.txt and movie-review-BOW-train-neg.txt files. 

These files files are used to build a dictionary structure, where each key is a word (that appears in at least one of the reviews, as well as in the imdb.vocab vocabulary file), and each value is a list of lenght 2. In that list, the first item is the number of times this word appears in the positive reviews, and the second item is how many times the word appears in negative reviews.

The test data files (which are also movie reviews) are pre-processed in a similar way, and a list structure is built from them. In that list, each item is a dictionary that represents each individual movie review. In each of those dictionaries, the keys are words, and the values are the numbers of times those words appear in a review.

Once these data structures are produced, they are exported into JSON files.

The NB.py script takes the JSON files that were produced by the pre-process.py script and uses them to make predictions on the test data. For each movie review in the test directory, the algorithm in NB.py predicts whether that review is positive or negative, based on the training data, using Naive Bayes classifier with Bag Of Words features. The results are exported into an output file.

Lastly, the accuracy of the classifier is found by calculating the percentage of reviews that were predicted correctly.

Note: due to their size, the large training and test datasets were not included into this repository. Only a toy example was included to show the structure of the pre-processed data. In this example, a list that represents the test data was hardcoded into NB.py (testDocSmall variable). And the dictionary that represents the training data is in the movie-review-small.JSON file.
