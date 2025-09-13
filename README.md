Thank you for taking the time to read my README.txt !

# Instructions

1. Open the files main4.py and stopwords.txt into the same directory.
2. Compile main4.py.
3. You will see an input prompt. "input here:"
4. Please enter the name of your desired input file and the number of corpus entries to use when training the classifier.

There are two sample input files provided with this repository. A tiny sample named tinyCorpus.txt, as well as a small sample named bioCorpus.txt.

## Sample Command Line Input
```
python3 main4.py
```
```
input here: tinyCorpus.txt 5
```

## Premise
This program uses a sample file of biographies to train and test a text classification model.

## Training 
Given an inputted sample and an interger N, the model is trained on the first N biographies in the sample.
The training process involves mapping words in biographies to the careers they describe. 
The recorded frequency of words will be used in testing the assignment of career categories to the testing data.

## Testing
The test is run against the biographies from the sample which were not included in the N biographies used for the training data.
The content of each biography is analyzed for each word's likelihood of falling in different career categories.
The career of the biography's subject is deduced from this analysis.

## Validation Testing
After testing the (sample data - N) entries against the N training data, I returned the correctness of my predictions.
The correctness is verified by checking the predicted career against the listed career in the biography for congruency.
This is supplemented with the prediction scores for each career, such as in the output example below.

## Output Example
```
Name: George Eliot      Prediction: writer       True
government : 0.01       music : 0.08    writer : 0.91
```

