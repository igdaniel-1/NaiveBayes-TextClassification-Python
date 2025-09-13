################  INPUT
# test case: tinyCorpus.txt 5
# test case: bioCorpus.txt 4
import math
# open up the stopwords file
stopwordFile = open("stopwords.txt", "r")
# read it into an array
stopwords = []
lines = stopwordFile.read().splitlines()
for line in lines:
    stopwords.extend(line.split())
stopwordFile.close()


# given a file, read that file
# read input and convert to our two parameters

input_line = input("input here:")
# input_line = "tinyCorpus.txt 5"
inputs = input_line.split()
file_name = inputs[0]
n_training = int(inputs[1])

file = open(file_name, "r")

################# helper functions
# paragraph extraction from input document 
def paragraphBuilder(paragraphArray):
    temp_paragraph = []
    paragraph = 0
    for line in file:
        line = line.rstrip('\n')
        if line:
            temp_paragraph.append(line)
        else:
            paragraphArray.append(temp_paragraph)
            paragraph += 1
            temp_paragraph = []
            continue
    paragraphArray.append(temp_paragraph)
    for paragraph in paragraphArray:
        if len(paragraph) == 0:
            paragraphArray.remove(paragraph)
    return paragraphArray


def checkCategoryInDictionary(new_category):
    for key in keywords:
        if new_category == key:
            return
    # if it isn't already in the dictionary, add it as a new key
    keywords[new_category] = []
    # add it to category occurences
    OccWGivenC[new_category] = {}
    # add it as a key to number of bios within that category
    NumBiosInCat[new_category] = 0      
    return

def checkIfInStopwords(word):
    if word in stopwords:
        return True
    return False
    # pass

# add the unique contents of a bibliography to its category's keywords
def addToKeywords(bibliography, category):
    # category hasn't been split into words yet, it's just a bunch of characters
    # split into words
    words = bibliography.split()
    for word in words:
        # remove punctuation
        word = word.rstrip(",. ")
        # convert to all lower case
        word = word.lower()
        # remove words that are less than 3 letters
        if len(word) < 3:
            continue
        # check if in stop words
        if checkIfInStopwords(word):
            continue
        # dont include category titles 
        if word in keywords:
            continue
        # check for repeats
        if word in keywords[category]:
            # add to occurences of word in category
            OccWGivenC[category][word] += 1
            continue
        # else, this is out first time encountering this word 
        # check if in the all_biblio_words array
        if word not in all_biblio_words:
            all_biblio_words.append(word)

        checkCategoryInDictionary(category)
        # print("in keywords:",category)
        OccWGivenC[category][word] = 1
        keywords[category].append(word)

def frequency_C(category):
    #  FreqT(C) = OccT (C)/|T|
    return NumBiosInCat[category] / abs(n_training)
    # pass

def frequency_WgivenC(word, category):
    #  FreqT(W|C) = OccT (W|C)/OccT (C),
    return OccWGivenC[category][word] / NumBiosInCat[category]

def prob_C(category):
    # P(C) = [FreqT(C) + e] / [1 + number of categories ∗ e]
    e = 0.1
    numerator = frequency_C(category) + e
    # print("num cats", num_categories)
    denominator = 1 + num_categories*e
    return numerator / denominator
    # pass

def prob_WgivenC(word, category):
    # P(W|C) = [FreqT(W|C) + e] / [1 + 2 ∗ e]
    e = 0.1
    numerator = frequency_WgivenC(word, category) + e
    denominator = 1+2*e
    return numerator / denominator
    # pass

def log_C(category):
    # L(C) = − log2(P(C))
    return -(math.log2(prob_C(category)))
    # pass

def log_WgivenC(word, category):
    # L(W|C) = − log2(P(W|C))
    return -(math.log2(prob_WgivenC(word,category)))
    # pass

def log_CgivenB(category, biography):
    # for all words in the bio
    sum = 0
    for word in biography:
        if word in all_biblio_words:
            sum += log_WgivenC(word, category)
            # print("current val in C|B:",curr_val)
    return log_C(category) + sum
    # pass







# build the paragraph storage class
class Paragraph:
    def __init__(self, name, category, bibliography):
        self.name = name
        self.category = category
        self.bibliography = bibliography

    def normalize(self):
        normalized_words = []
        words = self.bibliography.split()
        for word in words:
            # remove punctuation
            word = word.rstrip(",. ")
            # convert to all lower case
            word = word.lower()
            # remove words that are less than 3 letters
            if len(word) < 3:
                continue
            # check if in stop words
            if checkIfInStopwords(word):
                continue
            # dont include its own category title 
            if word == self.category:
                continue
            # if it wasn't used at all in the training set
            if word not in all_biblio_words:
                continue
            # if we've already stored it, skip
            if word in normalized_words:
                continue
            normalized_words.append(word)

        self.bibliography = normalized_words

    def valid(self, prediction):
        if prediction == self.category:
            return True
        return False
    








   
    
################# main 
# build the training paragraphs 
num_categories = 0
all_paragraphs = []           
all_paragraphs = paragraphBuilder(all_paragraphs)
total_num_paragraphs = len(all_paragraphs)

training_paragraphs = []

for paragraph in range(0, n_training):
    training_paragraphs.append(all_paragraphs.pop(0))

test_paragraphs = all_paragraphs    ## with the front n_training elements are removed 

# 3.1.1 Normalization
all_biblio_words = []
keywords = {}
# 3.1.2 Counting
# number of bios in each category
NumBiosInCat = {}
# occurences of a word in a bibliography given a category
OccWGivenC = {}

# extract bibliographies from the training set, 
for paragraph in training_paragraphs:
    # first line is name, we can skip
    # second line is category, remove any spaces, and make it lower case
    category = paragraph[1].lower().rstrip()
    # check if in dictionary, adds if it isn't already there
    checkCategoryInDictionary(category)
    NumBiosInCat[category] += 1

    bibliography = ''
    # print("len para",len(paragraph))
    # bibliography holds onto all characters, not split into words yet
    for sentence in range(2, len(paragraph)):
        # print(sentence)
        bibliography += paragraph[sentence] + " "
    addToKeywords(bibliography, category)

# add all the words that have 0 occurrences to OccWGivenC as val 0
for word in all_biblio_words:
    for category in keywords:
        # print("cat:",category)
        if word not in keywords[category]:
            OccWGivenC[category][word] = 0

# 3.1.3 Probabilities
num_categories = len(keywords)

# print(frequency_C("government"))
# print(frequency_WgivenC("american", "government"))
# print(prob_C("government"))
# print(prob_WgivenC("american", "government"))
# print(log_C("government"))
# print(log_WgivenC("american", "government"))

guess_accuracy = []

# 3.2 Applying the classifier to the test data
for paragraph in test_paragraphs:
    # grab bib
    name = paragraph[0]
    category = paragraph[1]
    category = category.lower().rstrip()
    bibliography = ''
    for sentence in range(2, len(paragraph)):
        bibliography += paragraph[sentence] + " "
    current_para = Paragraph(name,category,bibliography)
    # normalize the bibliography
    current_para.normalize()



    # Step 4. To recover the actual probabilities: Let k be the number of categories
    # 4.a 
    max_prob = ("nothing", 0)
    min_prob = ("nothing", 10000)
    c_values = []
    for category in keywords:
        ci = log_CgivenB(category, current_para.bibliography)
        if ci >= max_prob[1]:
            max_prob = (category, ci)
        if ci <= min_prob[1]:
            min_prob = (category, ci)
        c_values.append(ci)
    
    prediction = min_prob[0]
    valid = current_para.valid(prediction)
    guess_accuracy.append(valid)
    print("Name:",name,"\tPrediction:", prediction, "\t", valid)

    # 4.b
    x_vals = []
    s = 0
    for ci in c_values:
        if (ci - min_prob[1]) < 7:
            xi = 2**(min_prob[1]-ci)
        else:
            xi = 0
        s+=xi
        x_vals.append(xi)
    # 4.c 
    keyword_array = [category for category in keywords]
    count = 0
    for xi in x_vals:
        # P(Ck|B) = xi/s
        # print("P(C|B):",xi/s, end="\t")
        print(keyword_array[count],":",round(xi/s, 2), end="\t")
        count+=1
    print("\n")

# calculate accuracy
sum = 0 
for guess in guess_accuracy:
    if guess == True:
        sum +=1
percent_correct = round(sum / len(guess_accuracy), 2)

print("Overall accuracy:",sum,"out of", len(guess_accuracy), "=", percent_correct)

    








# print tests
# for category in NumBiosInCat:
#     print("number of bios in category", category, ":", NumBiosInCat[category])

# # tester print out keywords for each category
# for category in keywords:
#     print("category", category, ":")
#     for word in keywords[category]:
#         print(word)
