import json
import math

# Prior probabilities for positive and negative classes
priorProbPos = 0.5
priorProbNeg = 0.5

# A toy example to test the correctness of the classifier function
priorProbComedy = 2/5
priorProbAction = 3/5
testDocSmall = [{"fast":1, "couple":1, "shoot":1, "fly":1}]
with open('movie-review-small.JSON') as json_file:
    trainDocSmall = json.load(json_file)
json_file.close()

# This function contains the logic of the Naive Bayes classifier
def predictClass(trainingData, testData, priorProb1, priorProb2, class1, class2, outputFile):
    wordsInClass1 = 0
    wordsInClass2 = 0
    for word in trainingData:
        wordsInClass1 += trainingData[word][0]
        wordsInClass2 += trainingData[word][1]
    output = open(outputFile, 'a')
    for i in range (len(testData)):
        probClass1 = math.log(priorProb1)
        probClass2 = math.log(priorProb2)
        for j in testData[i]:
            if(j in trainingData):
                probClass1 += math.log(pow((trainingData[j][0]+1)/(wordsInClass1+len(trainingData)), (testData[i][j])))
                probClass2 += math.log(pow((trainingData[j][1]+1)/(wordsInClass2+len(trainingData)), (testData[i][j])))
            else:
                probClass1 += math.log(pow((1/(wordsInClass1+len(trainingData))), (testData[i][j])))
                probClass2 += math.log(pow((1/(wordsInClass2+len(trainingData))), (testData[i][j])))
        output.write("\nProbability of " + class1 + ": " + str(probClass1))
        output.write("\nProbability of " + class2 + ": " + str(probClass2))
        if(probClass1 > probClass2):
            output.write("\nMost likely class: " + class1 + "\n")
        else:
            output.write("\nMost likely class: " + class2 + "\n")
    output.close()

# This function calls the classifier function, but first it loads the training and test data structures
def makePrecictions(testData, outputFile):
    with open('movie-review-BOW.JSON') as json_file:
        trainDict = json.load(json_file)
    json_file.close()
    with open(testData) as json_file1:
        testList = json.load(json_file1)
    json_file1.close()
    predictClass(trainDict, testList, priorProbPos, priorProbNeg, "pos", "neg", outputFile)

# This function simply calculates the percentages of correct predictions and appends them to the output files
def calculatePercentages(resultFile, givenClass):
    counterOfMismatches = 0
    file = open(resultFile, 'r+')
    text = file.read()
    if (givenClass == "pos"):
        counterOfMismatches = text.count("class: neg")
    else:
        counterOfMismatches = text.count("class: pos")
    percentage = 100 - ((counterOfMismatches/12500)*100)
    file.write("\nAccuracy of NB model for " + givenClass + " training directory: " + str(percentage) + " %")
    file.close


# Below are the function calls to predict the most likely classes for the small example, and for the large given datataset
# The training and test data structures for the small example were typed manually
# The training and test data structures for the large dataset were produced by the pre-process.py script and stored in JSON files
# Results were printed to the output files output-BOW-pos.txt and output-BOW-neg.txt

predictClass(trainDocSmall, testDocSmall, priorProbComedy, priorProbAction, "comedy", "action", "output-small.txt")

makePrecictions("movie-review-test-pos.JSON", "output-BOW-pos.txt")
makePrecictions("movie-review-test-neg.JSON", "output-BOW-neg.txt")

calculatePercentages("output-BOW-pos.txt", "pos")
calculatePercentages("output-BOW-neg.txt", "neg")
