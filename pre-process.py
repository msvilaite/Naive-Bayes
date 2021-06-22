import string
import os
import json
 
givenVocabulary = {} 
trainDict = {}
testList = []

# This function reads all the files in a given directory that contains movie reviews
# Then the reviews are cleaned up ("<br /><br />" symbols removed, some punctuation removed, ? and ! separated)
# Everything is lowercased
# And then all the reviews from a given directory are concatenated into one .txt file 
# Absolute paths have to be used when looping through filenames and opening files
def concatenateReviews(reviewDir, outputDir):
    print(os.path.expanduser("~/Desktop/" + reviewDir + "/"))
    outputFile = open(os.path.expanduser("~/Desktop/" + outputDir), 'a')
    for filename in os.listdir(os.path.expanduser("~/Desktop/" + reviewDir)):
        path = os.path.expanduser("~/Desktop/" + reviewDir + "/" + filename)
        file = open(path)
        text = file.read()
        text = text.replace("<br /><br />", " ")
        text = text.replace("\"", "")
        text = text.replace(".", "")
        text = text.replace(",", "")
        text = text.replace(";", "")
        text = text.replace("(", "")
        text = text.replace(")", "")
        text = text.replace("?", " ?")
        text = text.replace("!", " !")
        words = text.split()
        for i in range (len(words)):
            outputFile.write(words[i].lower() + " ")
        file.close()
        outputFile.write("\n")
    outputFile.close()

# The vocabulary from the imdb.vocab file is stored in a global dictionary, for efficient queries
def getVocab():
    with open("aclImdb/imdb.vocab") as vocFile:
        for line in vocFile:
            givenVocabulary[line.replace("\n","")] = 1
    vocFile.close()

# A structure of training data is produced, to be later stored in "movie-review-BOW.JSON" file, and to be passed to NB.py
def makeTrainDict(reviewFile, classIndex):
    f1 = open(reviewFile)
    listOfWords = f1.read().split()
    f1.close()
    for i in range(len(listOfWords)):
        if listOfWords[i] in trainDict:
            trainDict[listOfWords[i]][classIndex] += 1
        else:
            if listOfWords[i] in givenVocabulary:
                if classIndex == 1:
                    trainDict[listOfWords[i]] = [1,0]
                else:
                    trainDict[listOfWords[i]] = [0,1]

# Two testing data structures are produced, one for pos, one for neg
# They will also be stored in JSON files and passed to NB.py
def makeTestList(reviewFile):
    f1 = open(reviewFile)
    listOfReviews = f1.read().splitlines()
    f1.close()   
    for i in range(len(listOfReviews)):
        review = {}
        words = listOfReviews[i].split()
        for j in range(len(words)):
            if words[j] in review:
                review[words[j]] += 1
            else:
                review[words[j]] = 1
        testList.append(review)

# This function is used to export data structures into JSON files         
def createJSON(JSONfile, structure):
    with open(JSONfile, 'w') as outfile:
        json.dump(structure, outfile)
    outfile.close()



concatenateReviews("aclImdb/train/pos", "movie-review-BOW-train-pos.txt")
concatenateReviews("aclImdb/train/neg", "movie-review-BOW-train-neg.txt")

getVocab()
makeTrainDict("movie-review-BOW-train-pos.txt", 0)
makeTrainDict("movie-review-BOW-train-neg.txt", 1)
createJSON("movie-review-BOW.JSON", trainDict)

concatenateReviews("aclImdb/test/pos", "movie-review-BOW-test-pos.txt")
concatenateReviews("aclImdb/test/neg", "movie-review-BOW-test-neg.txt")

makeTestList("movie-review-BOW-test-pos.txt")
createJSON("movie-review-test-pos.JSON", testList)
makeTestList("movie-review-BOW-test-neg.txt")
createJSON("movie-review-test-neg.JSON", testList)