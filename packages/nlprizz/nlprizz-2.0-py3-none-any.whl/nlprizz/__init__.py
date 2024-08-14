def pip():
    print(""" 

Practical 1-5
playsound  			 #pip install playsound 
gtts 				 #pip install gtts 
speech_recognition   #pip install SpeechRecognition pydub
nltk       		     #pip install nltk
gensim				 #pip install gensim
spacy 				 #pip install spacy 
en_core_web_sm       #python -m spacy download en_core_web_sm
keras 				 #pip install keras
tensorflow  		 #pip install tensorflow
keras_preprocessing  #pip install keras_preprocessing
indicnlp			 #pip install indic-nlp-library
langid				 #pip install nltk langid indic-nlp-library tensorflow torch torchvision torchaudio


Practical 6-11
nltk       		   #pip install nltk
sklearn 		   #pip install scikit-learn
spacy 			   #pip install -U spacy
en_core_web_sm     #python -m spacy download en_core_web_sm
textdistance       #pip install textdistance

          
Python Environment commands
python -m venv venv
venv\Scripts\\activate
          
venv\Scripts\deactivate
                 

"""
    )

def index():
    print("""          

                
Practical 1: 
1c) Convert the given text into speech.
1d) Convert the audio file into speech.
                                     

Practical 2:
2a) Study of various corpus - Brown, Inaugural, Reuters, udhr with various methods like 
    fields, raw, words, sents, categories.
2b) Create and use your own corpora (plaintext, categorical).
2c) Study conditional frequency distribution.
2d) Study of tagged corpora with methods like tagged_sents, tagged_words.
2e) Write a program to find the most frequent noun tags.
2f) Map words to the properties using Python Dictionaries.
2g1) Study DefaultTagger
2g2) Study Regular expression tagger
2g3) Study UnigramTagger
2h) Find different words from a given plaintext without any spaces by comparing this text with a given corpus of words. 
    Also find the score of words

          
Practical 3:
3a) Study of Wordnet Dictionary with methods as synsets, definitions, examples, antonyms.
3b) Study lemmas, hyponyms, hypernyms, entailments.
3c) Write a program using python to find synonym and antonym of word "active" using Wordnet.
3d) Compare two nouns.
3e1) Handling stopword: Using nltk, add or remove stop words in NLTK's Default stop word list.
3e2) Handling stopword: Using Gensim, add or remove stop words in Default Gensim stop words List.
3e3) Handling stopword: Using SpaCy, add or remove Stop Words in Default SpaCy stop words List.


Practical 4: Text Tokenization
4a) Tokenization using Python's split() function.
4b) Tokenization using Regular Expression (RegEx).
4c) Tokenization using NLTK.
4d) Tokenization using spaCy library.
4e) Tokenization using Keras.
4f) Tokenization using Gensim.          
          

Practical 5: Study the important libraries for Indian language and perform the following:
5a) Word tokenization in Hindi 
5b) Generate similar sentences from a given Hindi text input
5c) Identify the Indian language from the given text.
          

Practical 6: Illustrate Part-of-Speech
6a) Part of speech Tagging and chunking of user defined text.
6b) Named Entity recognition of user defined text.
6c) Named Entity recognition with diagram using NLTK corpus - treebank
          

Practical 7:
7a) Define grammar using nltk. Analyse a sentence using the same.
7b) Accept the input string with Regular expression of FA: 101+
7c) Accept the input string with Regular expression of FA: (a+b)*bba
7d) Implementation of Deductive Chart Parsing using context free grammar and a given sentence.
          
          
Practical 8: 
8a) Study PorterStemmer, LancasterStemmer, RegexpStemmer, SnowballStemmer
8b) Study WordNet Lemmatizer          

          
Practical 9:
    Implement Naive Bayes classifier

          
Practical 10:
10a) Speech Tagging using Spacy and NLTK.       
10b1) Statistical parsing: Usage of Give and Gave in the Penn Treebank sample.
10b2) Statistical parsing: Probabilistic parser  
          
10c) Malt parsing: Parse a sentence and draw a tree using malt parsing 
    (CHANGE THE SLIP) (NOT POSSIBLE) (Code is Available!)         
          

Practical 11:          
11a) Multiword Expressions in NLP
11b) Normalized Web Distance and Word Similarity
11c) Word Sense Disambiguation 
      
             
""")
    

def prog(num):
    if num =="1c":
        print(""" --- Pract 1c ---                                       

# text to speech 
# pip install gtts 
# pip install playsound 

from playsound import playsound

# import required for text to speech conversion 
from gtts import gTTS

mytext = "Welcome to Practical 1: Natural Language programming." 
language = "en" 
myobj = gTTS(text=mytext, lang=language, slow=False) 
myobj.save("myfile.mp3") 
playsound("myfile.mp3") 
print("Text converted into speech succesfully")

        """)

    elif num =="1d":
        print(""" --- Pract 1d  ---
              
#pip install SpeechRecognition pydub 
import speech_recognition as sr


filename = "test.wav" 
# initialize the recognizer 
r = sr.Recognizer() 
# open the file 
with sr.AudioFile(filename) as source: 
# listen for the data (load audio to memory) 
    audio_data = r.record(source) 
# recognize (convert from speech to text) 
    text = r.recognize_google(audio_data) 
    print(text)
              

        """)
    
    elif num =="2a":
        print(""" --- Pract 2a  ---
              
#pip install nltk

import nltk

# Download necessary corpora
nltk.download('brown')
nltk.download('inaugural')
nltk.download('reuters')
nltk.download('udhr')

from nltk.corpus import brown, inaugural, reuters, udhr

# Open a file to save the output
with open("corpus_statistics.txt", "w") as file:

    # Function to write statistics for each corpus to the file
    def write_corpus_stats(corpus, corpus_name, file):
        file.write(f"\\n\\n{corpus_name} Corpus:\\n")
        if corpus_name != 'UDHR':  # UDHR doesn't have categories
            file.write(f"File ids of {corpus_name} corpus:\\n {corpus.fileids()}\\n")
        if hasattr(corpus, 'categories'):
            file.write(f"\\nCategories in {corpus_name} corpus:\\n {corpus.categories()}\\n")

        file.write(f"\\nStatistics for {corpus_name} corpus texts:\\n")
        file.write('AvgWordLen\\tAvgSentenceLen\\tNo.ofTimesEachWordAppearsOnAvg\\tFileName\\n')
        for fileid in corpus.fileids():
            num_chars = len(corpus.raw(fileid))
            num_words = len(corpus.words(fileid))
            num_sents = len(corpus.sents(fileid)) if hasattr(corpus, 'sents') else 1  # UDHR doesn't have sentences
            num_vocab = len(set([w.lower() for w in corpus.words(fileid)]))
            file.write(f"{int(num_chars/num_words)}\\t\\t{int(num_words/num_sents)}\\t\\t{int(num_words/num_vocab)}\\t\\t{fileid}\\n")

    # Brown corpus statistics
    write_corpus_stats(brown, 'Brown', file)

    # Inaugural corpus statistics
    write_corpus_stats(inaugural, 'Inaugural', file)

    # Reuters corpus statistics
    write_corpus_stats(reuters, 'Reuters', file)

    # UDHR corpus statistics (UDHR has no sentences or categories)
    file.write(f"\\n\\nUDHR Corpus:\\n")
    file.write(f"File ids of UDHR corpus:\\n {udhr.fileids()}\\n")
    file.write(f"\\nStatistics for UDHR corpus texts:\\n")
    file.write('AvgWordLen\\tAvgSentenceLen\\tNo.ofTimesEachWordAppearsOnAvg\\tFileName\\n')
    for fileid in udhr.fileids():
        num_chars = len(udhr.raw(fileid))
        num_words = len(udhr.words(fileid))
        num_vocab = len(set([w.lower() for w in udhr.words(fileid)]))
        file.write(f"{int(num_chars/num_words)}\\t\\t-\\t\\t{int(num_words/num_vocab)}\\t\\t{fileid}\\n")
              
        """)
    
    elif num =="2b":
        print(""" --- Pract 2b  ---
              
#pip install nltk

import nltk
from nltk.corpus import PlaintextCorpusReader

# Assuming input.txt is in the same directory as the script
corpus_root = '.'  # Current directory
filelist = PlaintextCorpusReader(corpus_root, '2b_input.txt')

file_to_process = '2b_input.txt' 

print('\\n File list: \\n')
print(filelist.fileids())

# Display statistics for the text
print('\\n\\nStatistics for the text:\\n')
print('AvgWordLen\\tAvgSentenceLen\\tno.ofTimesEachWordAppearsOnAvg\\tFileName')

num_chars = len(filelist.raw(file_to_process))
num_words = len(filelist.words(file_to_process))
num_sents = len(filelist.sents(file_to_process))
num_vocab = len(set([w.lower() for w in filelist.words(file_to_process)]))

print(int(num_chars / num_words), '\\t\\t\\t', int(num_words / num_sents), '\\t\\t\\t', int(num_words / num_vocab), '\\t\\t',file_to_process )

              
        """)
    
    elif num =="2c":
        print(""" --- Pract 2c  ---
              
#pip install nltk


# Process a sequence of pairs
text = ['The', 'Fulton', 'County', 'Grand', 'Jury', 'said', ...]
pairs = [('news', 'The'), ('news', 'Fulton'), ('news', 'County'), ...]

import nltk
from nltk.corpus import brown

fd = nltk.ConditionalFreqDist(
    (genre, word)
    for genre in brown.categories()
    for word in brown.words(categories=genre)
)

genre_word = [
    (genre, word)
    for genre in ['news', 'romance']
    for word in brown.words(categories=genre)
]

print(len(genre_word))
print(genre_word[:4])
print(genre_word[-4:])

cfd = nltk.ConditionalFreqDist(genre_word)
print(cfd)
print(cfd.conditions())
print(cfd['news'])
print(cfd['romance'])
print(list(cfd['romance']))

from nltk.corpus import inaugural

cfd = nltk.ConditionalFreqDist(
    (target, fileid[:4])
    for fileid in inaugural.fileids()
    for w in inaugural.words(fileid)
    for target in ['america', 'citizen']
    if w.lower().startswith(target)
)

from nltk.corpus import udhr

languages = [
    'Chickasaw', 'English', 'German_Deutsch',
    'Greenlandic_Inuktikut', 'Hungarian_Magyar', 'Ibibio_Efik'
]

cfd = nltk.ConditionalFreqDist(
    (lang, len(word))
    for lang in languages
    for word in udhr.words(lang + '-Latin1')
)

cfd.tabulate(conditions=['English', 'German_Deutsch'], samples=range(10), cumulative=True)

              
        """)
    
    elif num =="2d":
        print(""" --- Pract 2d  ---
              
#pip install nltk

import nltk
from nltk import tokenize
nltk.download('punkt')
nltk.download('words')
para = "Hello! My name is Abc Pqr. Today we will be learning NLTK."
sents = tokenize.sent_tokenize(para)
print("\\nsentence tokenization\\n===================\\n",sents)
# word tokenization
print("\\nword tokenization\\n===================\\n")
for index in range(len(sents)):
 words = tokenize.word_tokenize(sents[index])
 print(words)


print("#"*200)

import nltk
from nltk.corpus import brown, treebank

# Download necessary resources
nltk.download('brown')
nltk.download('treebank')

# Function to print tagged sentences and tagged words for a corpus
def print_tagged_corpus_info(corpus, corpus_name):
    print(f"\\n\\n{corpus_name} Corpus Tagged Sentences:\\n===================")
    print(corpus.tagged_sents()[:2])  # Display first 2 tagged sentences

    print(f"\\n{corpus_name} Corpus Tagged Words:\\n===================")
    print(corpus.tagged_words()[:10])  # Display first 10 tagged words

# Study of tagged corpora (Brown and Treebank)
print_tagged_corpus_info(brown, 'Brown')
print_tagged_corpus_info(treebank, 'Treebank')

              
        """)
    
    elif num =="2e":
        print(""" --- Pract 2e  ---
              
#pip install nltk

import nltk
from collections import defaultdict

nltk.download('averaged_perceptron_tagger')
text = nltk.word_tokenize("Abc likes to play cricket. Abc does not like to play with hearts. ")
tagged = nltk.pos_tag(text)
print(tagged)

# Checking if it is a noun or not
addNounWords = []
count = 0
for words in tagged:
    val = tagged[count][1]
    if val in ('NN', 'NNS', 'NNPS', 'NNP'):
        addNounWords.append(tagged[count][0])
    count += 1

print(addNounWords)

temp = defaultdict(int)
# Memoizing count
for sub in addNounWords:
    for wrd in sub.split():
        temp[wrd] += 1

# Getting max frequency
res = max(temp, key=temp.get)
# Printing result
print("Word with maximum frequency: " + str(res))
            

              
        """)
    
    elif num =="2f":
        print(""" --- Pract 2f  ---
              
# Creating and printing a dictionary by mapping words to their properties
word_properties = {
    "apple": {"type": "noun", "definition": "a fruit", "length": 5},
    "run": {"type": "verb", "definition": "to move swiftly", "length": 3},
    "blue": {"type": "adjective", "definition": "a color", "length": 4}
}

# Print the entire dictionary
print("Word Properties Dictionary:\\n", word_properties)

# Access and print properties of a specific word
word = "apple"
print(f"\\nProperties of '{word}':\\n", word_properties[word])

# Get and print the length of the dictionary
print("\\nNumber of words in the dictionary:", len(word_properties))

# Print the type of the dictionary
print("\\nType of the dictionary:", type(word_properties))

              
        """)

    elif num =="2g1":
        print(""" --- Pract 2g1  ---
              
#pip install nltk

import nltk
from nltk.tag import DefaultTagger
from nltk.corpus import treebank

# Creating and evaluating the DefaultTagger
exptagger = DefaultTagger('NN')
testsentences = treebank.tagged_sents()[1000:]
print("DefaultTagger Evaluation:", exptagger.evaluate(testsentences))

# Tagging a list of sentences
tagged_sentences = exptagger.tag_sents([['Hi', ','], ['How', 'are', 'you', '?']])
print("Tagged Sentences:", tagged_sentences)

              
        """)
    
    elif num =="2g2":
        print(""" --- Pract 2g2  ---
              
#pip install nltk

from nltk.corpus import brown 
from nltk.tag import RegexpTagger 

# Selecting a test sentence from the Brown corpus (news category)
test_sent = brown.sents(categories='news')[0] 

# Creating the RegexpTagger with specified patterns
regexp_tagger = RegexpTagger( 
    [
        (r'^-?[0-9]+(.[0-9]+)?$', 'CD'),   # cardinal numbers 
        (r'(The|the|A|a|An|an)$', 'AT'),   # articles 
        (r'.*able$', 'JJ'),                # adjectives 
        (r'.*ness$', 'NN'),                # nouns formed from adjectives      
        (r'.*ly$', 'RB'),                  # adverbs        
        (r'.*s$', 'NNS'),                  # plural nouns   
        (r'.*ing$', 'VBG'),                # gerunds              
        (r'.*ed$', 'VBD'),                 # past tense verbs 
        (r'.*', 'NN')                      # nouns (default)                    
    ]) 

# Printing the tagger
print(regexp_tagger) 

# Tagging the test sentence
print(regexp_tagger.tag(test_sent)) 
              

        """)
    
    elif num =="2g3":
        print(""" --- Pract 2g3  ---
              
#pip install nltk

from nltk.tag import UnigramTagger
from nltk.corpus import treebank

# Training the UnigramTagger
train_sents = treebank.tagged_sents()[:10]
tagger = UnigramTagger(train_sents) # Initializing

# Tagging a sentence with the trained tagger
print(treebank.sents()[0])
print('\\n', tagger.tag(treebank.sents()[0]))

# Overriding the context model with a specific tag for 'Pierre'
tagger = UnigramTagger(model={'Pierre': 'NN'})
print('\\n', tagger.tag(treebank.sents()[0]))
              

        """)
    
    elif num =="2h":
        print(""" --- Pract 2h  ---

              
from __future__ import with_statement
import re

words = []
testword = []
ans = []

print("MENU")
print("-----------")
print("1. Hash tag segmentation")
print("2. URL segmentation")
print("Enter the input choice for performing word segmentation:")
choice = int(input())

if choice == 1:
    text = "#whatismyname"
    print("Input with HashTag:", text)
    pattern = re.compile("[^\w']")
    a = pattern.sub('', text[1:])  # Remove the hash symbol
elif choice == 2:
    text = "www.whatismyname.com"
    print("Input with URL:", text)
    a = re.split(r'\s|(?<!\d)[,.](?!\d)', text)
    splitwords = ["www", "com", "in"]
    a = "".join([each for each in a if each not in splitwords])
else:
    print("Wrong choice...try again")
    a = ''

if a:
    print("Processed input:", a)
    
    try:
        with open("words.txt", 'r') as f:
            lines = f.readlines()
            words = [e.strip().lower() for e in lines]  # Ensure words are in lowercase
    except FileNotFoundError:
        print("The word list file was not found. Please check the file path.")
        exit()

    def Seg(a):
        ans = []
        length = len(a)
        for k in range(1, length + 1):
            if a[0:k].lower() in words:
                print(a[0:k], "- appears in the corpus")
                ans.append(a[0:k])
                break
        if ans:
            return max(ans, key=len)
        return ''

    test_tot_itr = 0
    answer = []
    test_length = len(a)

    while test_tot_itr < test_length:
        ans_words = Seg(a[test_tot_itr:])
        if ans_words:
            test_itr = len(ans_words)
            answer.append(ans_words)
            test_tot_itr += test_itr
        else:
            print("No further segmentation possible.")
            break

    Aft_Seg = " ".join(answer)
    print("\\nOutput:")
    print("---------")
    print("After segmentation:", Aft_Seg)
    
    # Score calculation
    C = len(answer)
    N = len(a)  # Assuming score is proportionate to the length of the input text
    score = C * N / N
    print("Score:", score)

              
        """)
    
    elif num =="3a":
        print(""" --- Pract 3a  ---
              
#pip install nltk

import nltk 
nltk.download('wordnet')
from nltk.corpus import wordnet

# Finding synsets for the word "computer"
synsets = wordnet.synsets("computer")
print("Synsets for 'computer':", synsets)

# Getting definition and example of the word "computer"
definition = wordnet.synset("computer.n.01").definition()
print("Definition of 'computer.n.01':", definition)

examples = wordnet.synset("computer.n.01").examples()
print("Examples of 'computer.n.01':", examples)

# Getting antonyms for the word "buy"
antonyms = wordnet.lemma('buy.v.01.buy').antonyms()
print("Antonyms of 'buy':", antonyms)

              
        """)
    
    elif num =="3b":
        print(""" --- Pract 3b  ---
              
#pip install nltk

import nltk
from nltk.corpus import wordnet

nltk.download('wordnet')

# Synsets for the word "computer"
print("Synsets for 'computer':", wordnet.synsets("computer"))

# Lemma names for a specific synset
print("Lemma names for 'computer.n.01':", wordnet.synset("computer.n.01").lemma_names())

# All lemmas for each synset
print("\\nAll lemmas for each synset of 'computer':")
for e in wordnet.synsets("computer"):
    print(f'{e} --> {e.lemma_names()}')

# Print all lemmas for a given synset
print("\\nAll lemmas for the synset 'computer.n.01':", wordnet.synset('computer.n.01').lemmas())

# Get the synset corresponding to a lemma
print("\\nSynset corresponding to the lemma 'computing_device' in 'computer.n.01':", wordnet.lemma('computer.n.01.computing_device').synset())

# Get the name of the lemma
print("Name of the lemma 'computing_device' in 'computer.n.01':", wordnet.lemma('computer.n.01.computing_device').name())

# Hyponyms give more specific concepts of the word
print("\\nHyponyms of 'computer.n.01':", wordnet.synset('computer.n.01').hyponyms())

# List of hyponyms words of 'computer'
print("Hyponym words of 'computer':", [lemma.name() for synset in wordnet.synset('computer.n.01').hyponyms() for lemma in synset.lemmas()])

# Semantic similarity in WordNet
vehicle = wordnet.synset('vehicle.n.01')
car = wordnet.synset('car.n.01')
print("\\nLowest common hypernym of 'vehicle' and 'car':", car.lowest_common_hypernyms(vehicle))

# Finding entailments of the verb "snore"
snore_synset = wordnet.synset('snore.v.01')
print("\\nEntailments of 'snore':", snore_synset.entailments())

# Checking the entailments for another verb, "eat"
eat_synset = wordnet.synset('eat.v.01')
print("Entailments of 'eat':", eat_synset.entailments())

              
        """)
    
    elif num =="3c":
        print(""" --- Pract 3c  ---
              
#pip install nltk

import nltk
from nltk.corpus import wordnet

# Download WordNet data if not already downloaded
nltk.download('wordnet')

# Find synsets for the word "active"
synsets = wordnet.synsets("active")
print(f"Synsets for 'active': {synsets}")

# Find synonyms for "active"
synonyms = set()
for synset in synsets:
    for lemma in synset.lemmas():
        synonyms.add(lemma.name())

print(f"\\nSynonyms of 'active': {synonyms}")

# Find antonyms for "active"
antonyms = set()
for synset in synsets:
    for lemma in synset.lemmas():
        for antonym in lemma.antonyms():
            antonyms.add(antonym.name())

print(f"\\nAntonyms of 'active': {antonyms}")

              
        """)
    
    elif num =="3d":
        print(""" --- Pract 3d  ---
              
#pip install nltk

import nltk
from nltk.corpus import wordnet

# Download WordNet data if not already downloaded
nltk.download('wordnet')

# Get synsets for 'football' and 'soccer'
syn1 = wordnet.synsets('football')
syn2 = wordnet.synsets('soccer')

# Compare each synset of 'football' with each synset of 'soccer'
for s1 in syn1:
    for s2 in syn2:
        print("Comparing synsets:")
        print(f"{s1} ({s1.pos()}) [{s1.definition()}]")
        print(f"{s2} ({s2.pos()}) [{s2.definition()}]")
        similarity = s1.path_similarity(s2)
        print(f"Path similarity: {similarity}")
        print()

              
        """)
    
    elif num =="3e1":
        print(""" --- Pract 3e1  ---
              
#pip install nltk

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download the stopwords data
nltk.download('stopwords')

# Example text
text = "Abc likes to play cricket, however he is not too fond of basketball."

# Tokenize the text into words
text_tokens = word_tokenize(text)

# Filter out stop words using NLTK's default stop words list
tokens_without_sw = [word for word in text_tokens if not word.lower() in stopwords.words('english')]
print("Tokens without stop words (default):", tokens_without_sw)

# Add the word 'play' to the stop words list
all_stopwords = stopwords.words('english')
all_stopwords.append('play')

# Tokenize the text again
text_tokens = word_tokenize(text)

# Filter out stop words using the modified stop words list
tokens_without_sw = [word for word in text_tokens if not word.lower() in all_stopwords]
print("Tokens without stop words (with 'play' added):", tokens_without_sw)

# Remove 'not' from the stop words list
all_stopwords.remove('not')

# Tokenize the text again
text_tokens = word_tokenize(text)

# Filter out stop words using the updated stop words list
tokens_without_sw = [word for word in text_tokens if not word.lower() in all_stopwords]
print("Tokens without stop words (with 'not' removed):", tokens_without_sw)

              
        """)
    
    elif num =="3e2":
        print(""" --- Pract 3e2  ---
              
# Install necessary packages
# pip install gensim
# pip install nltk


import gensim
from gensim.parsing.preprocessing import remove_stopwords, STOPWORDS
import nltk
from nltk.tokenize import word_tokenize

# Ensure necessary NLTK data is downloaded
nltk.download('punkt')
nltk.download('stopwords')

# Sample text for processing
text = "Abc likes to play cricket, however he is not too fond of basketball."

# Remove stop words using Gensim's default stop words list
filtered_sentence = remove_stopwords(text)
print("Filtered sentence (default stop words):", filtered_sentence)

# Display the default Gensim stop words
all_stopwords = gensim.parsing.preprocessing.STOPWORDS
print("Default Gensim stop words:", all_stopwords)

# Add 'likes' and 'play' to the list of stop words
all_stopwords_gensim = STOPWORDS.union(set(['likes', 'play']))

# Tokenize the text
text_tokens = word_tokenize(text)

# Filter out the updated list of stop words
tokens_without_sw = [word for word in text_tokens if not word.lower() in all_stopwords_gensim]
print("Tokens without stop words (with 'likes' and 'play' added):", tokens_without_sw)

# Remove 'not' from the set of stop words
sw_list = {"not"}
all_stopwords_gensim = STOPWORDS.difference(sw_list)

# Tokenize the text again
text_tokens = word_tokenize(text)

# Filter out the updated list of stop words
tokens_without_sw = [word for word in text_tokens if not word.lower() in all_stopwords_gensim]
print("Tokens without stop words (with 'not' removed):", tokens_without_sw)

              
        """)
    
    elif num =="3e3":
        print(""" --- Pract 3e3  ---
              
#pip install spacy 
#pip install nltk
#python -m spacy download en_core_web_sm 
#python -m spacy download en 

import spacy
import nltk
from nltk.tokenize import word_tokenize

# Load SpaCy model
sp = spacy.load('en_core_web_sm')

# Get the default set of stop words from SpaCy
stop_words = sp.Defaults.stop_words

# Add the word 'play' to the stop word collection
stop_words.add("play")

# Sample text
text = "Abc likes to play cricket, however he is not too fond of basketball."

# Tokenize the text using NLTK
text_tokens = word_tokenize(text)

# Remove stop words from the tokenized text
tokens_without_sw = [word for word in text_tokens if word.lower() not in stop_words]
print("Tokens without stop words (with 'play' added):", tokens_without_sw)

# Remove 'not' from stop word collection
stop_words.remove('not')

# Tokenize the text again
tokens_without_sw = [word for word in text_tokens if word.lower() not in stop_words]
print("Tokens without stop words (with 'not' removed):", tokens_without_sw)


              
        """)
    
    elif num =="4a":
        print(""" --- Pract 4a  ---
              
text = "" This tool is in a beta stage. Electric cars are running petrol cars raw and rough experience. It also supports custom battery model, prebuilt charging model, and the Autonomous Driving API You can use this tool for creation of monitors, alarms, and dashboards that spotlight changes. The release of these three tools will enable developers to create visual rich experiences for Electric cars with advanced infotainment systems. Electric car manufacturers describe these tools as the collection of tech and tools for creating visually rich and interactive driving experiences.""
data = text.split('.')
for i in data:
 print(i.strip())              
              
        """)
    
    elif num =="4b":
        print(""" --- Pract 4b  ---
              
#pip install nltk

import nltk
# import RegexpTokenizer() method from nltk
from nltk.tokenize import RegexpTokenizer

# Create a reference variable for Class RegexpTokenizer
tk = RegexpTokenizer('\s+', gaps = True)

# Create a string input
str = "winner winner chicken dinner"

tokens = tk.tokenize(str) # Use tokenize method
 
print(tokens)

              
        """)
    
    elif num =="4c":
        print(""" --- Pract 4c  ---
              
#pip install nltk


import nltk
from nltk.tokenize import RegexpTokenizer
 
# Create a reference variable for Class RegexpTokenizer
tk = RegexpTokenizer('\s+', gaps = True)
 
# Create a string input
str = "There will be only one winner, let's go!! "
 
tokens = tk.tokenize(str)		# Use tokenize method

print(tokens)

              
        """)
    
    elif num =="4d":
        print(""" --- Pract 4d  ---
              
#pip install spacy 
#python -m spacy download en 

import spacy

nlp = spacy.blank("en")

str = "Mayday! Mayday! Officer prince reporting enemey artilary heading towards north"		#string input
# Create an instance of document, doc object is a container for a sequence of Token objects.
doc = nlp(str)
 
words = [word.text for word in doc]	# Read & words
print(words)

              
        """)
    
    elif num =="4e":
        print(""" --- Pract 4e  ---
              
#pip install keras
#pip install tensorflow
#pip install keras_preprocessing

import keras
from keras_preprocessing.text import text_to_word_sequence
# Create a string input
str = "Tokenization using Keras and Tensorflow"
tokens = text_to_word_sequence(str)     
# tokenizing the text
print(tokens)

              
        """)
    
    elif num =="4f":
        print(""" --- Pract 4f  ---
              
#pip install gensim

from gensim.utils import tokenize
 
# Create a string input
input_str = "Players unknown battlegrounds ready to launch"
 
tokens = list(tokenize(input_str)) # Tokenize the text
 
print(tokens)

              
        """)

    elif num =="5a":
        print(""" --- Pract 5a  ---
              
#pip install indic-nlp-library



import sys
from indicnlp import common

# The path to the local git repo for Indic NLP library
INDIC_NLP_LIB_HOME = r"indic_nlp_library"
# The path to the local git repo for Indic NLP Resources
INDIC_NLP_RESOURCES = r"indic_nlp_resources"

# Add library to Python path
sys.path.append(r'{}\src'.format(INDIC_NLP_LIB_HOME))

# Set environment variable for resources folder
common.set_resources_path(INDIC_NLP_RESOURCES)

# Import Indic Tokenize Module
from indicnlp.tokenize import indic_tokenize

# Input string in Hindi
indic_string = 'सुनो, कुछ आवाज़ आ रही है। फोन?'

print('Input String: {}'.format(indic_string))
print('Tokens: ')

# Tokenize and print each token
for t in indic_tokenize.trivial_tokenize(indic_string):
    print(t)

              
        """)
    
    elif num =="5b":
        print(""" --- Pract 5b  ---
              
synonyms = {
    "खुश": ["प्रसन्न", "आनंदित", "खुशी"],
    "बहुत": ["अधिक", "बहुत ज्यादा", "काफी"]
}
 
# Function to generate similar sentences by replacing some words with synonyms
def generate_similar_sentences(input_sentence, num_sentences=5):
    similar_sentences = []
 
    # Replace some words with synonyms 
    for word, word_synonyms in synonyms.items():
        for synonym in word_synonyms:
            modified_sentence = input_sentence.replace(word, synonym)
            similar_sentences.append(modified_sentence)
    return similar_sentences[:num_sentences]
 
input_sentence = "मैं आज बहुत खुश हूँ।"
similar_sentences = generate_similar_sentences(input_sentence)
print("Original sentence:", input_sentence)
print("Similar sentences:")
for sentence in similar_sentences:
    print("-", sentence)

              
        """)
    
    elif num =="5c":
        print(""" --- Pract 5c  ---
              
#pip install nltk langid indic-nlp-library tensorflow torch torchvision torchaudio

 
import nltk
import langid
from indicnlp.tokenize import indic_tokenize
 
nltk.download('punkt')
 
# Word Tokenization in Hindi
def tokenize_hindi(text):
    tokens = indic_tokenize.trivial_tokenize(text)
    return tokens
 
# Identify the Indian Language from the Given Text
def identify_language(text):
    lang, _ = langid.classify(text)
    return lang
 
# Example usage
hindi_text = "नमस्ते, आप कैसे हैं?"
 
# Example usage
marathi_text = "नमस्कार, कसे आहात?"
 
# Example usage
gujarati_text = "હેલો, કેમ છો?"
 
# Word Tokenization in Hindi
tokens = tokenize_hindi(hindi_text)
print("Tokenized words:", tokens)

# Identify the Indian Language from the Given Text
language = identify_language(hindi_text)
print("Identified language:", language)
 
# Identify the Indian Language from the Given Text
language = identify_language(marathi_text)
print("Identified language:", language)
 
# Identify the Indian Language from the Given Text
language = identify_language(gujarati_text)
print("Identified language:", language)              
              
        """)

    elif num =="6a":
        print(""" --- Pract 6a  ---

#pip install nltk
#pip install numpy

import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

from nltk import tokenize
from nltk import tag
from nltk import chunk


para = "Natural language processing (NLP) is a machine learning technology that gives computers the ability to interpret, manipulate, and comprehend human language."
sents = tokenize.sent_tokenize(para)

print("\\nsentence tokenization\\n===================\\n",sents)
# word tokenization
print("\\nword tokenization\\n===================\\n")

for index in range(len(sents)):
    words = tokenize.word_tokenize(sents[index])
    print(words)

# POS Tagging
tagged_words = []
for index in range(len(sents)):
    tagged_words.append(tag.pos_tag(words))
print("\\nPOS Tagging\\n===========\\n",tagged_words)

# chunking
tree = []
for index in range(len(sents)):
    tree.append(chunk.ne_chunk(tagged_words[index]))
print("\\nchunking\\n========\\n")
print("Tree: ",tree)
                        
              
        """)

    elif num =="6b":
        print(""" --- Pract 6b  ---
                         
#pip install -U spacy
#python -m spacy download en_core_web_sm

import spacy

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")
# Input
entities = "My name is Tom and I have a friend named Jerry"
print(entities)

# Process the text with spaCy
doc = nlp(entities)
    
# Extract named entities
entities = [(ent.text, ent.label_) for ent in doc.ents]
     
# Print recognized entities and their labels
if entities:
    print("Named Entities and their labels:")
    for entity, label in entities:
        print(f"{entity}: {label}")
else:
    print("No named entities found.")
              
              
        """)

    elif num =="6c":
        print(""" --- Pract 6c  ---

#pip install nltk

import nltk 
nltk.download('treebank') 
from nltk.corpus import treebank_chunk 
treebank_chunk.tagged_sents()[0] 
treebank_chunk.chunked_sents()[0] 
treebank_chunk.chunked_sents()[0].draw() 
                        
              
        """)

    elif num =="7a":
        print(""" --- Pract 7a  ---

#pip install nltk

import nltk
from nltk import tokenize

grammar1 = nltk.CFG.fromstring(\"""
S -> VP
VP -> VP NP
NP -> Det NP
Det -> 'that'
NP -> 'flight'
VP -> 'Book'
\""")

sentence = "Book that flight"
all_tokens = tokenize.word_tokenize(sentence)
print(all_tokens)

parser = nltk.ChartParser(grammar1)
for tree in parser.parse(all_tokens):
    print(tree)
    tree.draw()
                     
              
        """)
    
    elif num =="7b":
        print(""" --- Pract 7b  ---
                         
def FA(s):
    # if the length is less than 3 then it can't be accepted, Therefore end the process.
    if len(s) < 3:
        return "Rejected"
    if s[0] == '1':
        if s[1] == '0':
            if s[2] == '1':
                for i in range(3, len(s)):
                    if s[i] != '1':
                        return "Rejected"
                return "Accepted"  # if all 4 nested if true
            return "Rejected"  # else of 3rd if
        return "Rejected"  # else of 2nd if
    return "Rejected"  # else of 1st if

inputs = ['1', '10101', '101', '10111', '01010', '100', '', '10111101', '1011111']
for i in inputs:
    print(FA(i))
              
              
        """)

    elif num =="7c":
        print(""" --- Pract 7c  ---

def FA(s):
    # Check if the string contains only 'a' and 'b'
    if not all(c in 'ab' for c in s):
        return "Rejected"
    
    # Check if the length of the string is at least 3
    if len(s) < 3:
        return "Rejected"
    
    # Check if the string ends with 'bba'
    if s[-3:] == 'bba':
        return "Accepted"
    else:
        return "Rejected"

# Test cases
inputs = ['bba', 'ababbba', 'abba', 'abb', 'baba', 'bbb', '']
for i in inputs:
    print(f"{i}: {FA(i)}")

                    
              
        """)
    
    elif num =="7d":
        print(""" --- Pract 7d  ---
                         
#pip install nltk

import nltk
nltk.download('punkt')
from nltk import tokenize
grammar1 = nltk.CFG.fromstring(\"""
  S -> NP VP
  PP -> P NP
  NP -> Det N | Det N PP | 'I'
  VP -> V NP | VP PP
  Det -> 'a' | 'my'
  N -> 'bird' | 'balcony'
  V -> 'saw'
  P -> 'in'
  \""")
sentence = "I saw a bird in my balcony"
for index in range(len(sentence)):
  all_tokens = tokenize.word_tokenize(sentence)
print(all_tokens)
# all_tokens = ['I', 'saw', 'a', 'bird', 'in', 'my', 'balcony']
parser = nltk.ChartParser(grammar1)
for tree in parser.parse(all_tokens):
  print(tree)
  tree.pretty_print()

              
        """)
    
    elif num =="8a":
        print(""" --- Pract 8a  ---
                        
#pip install nltk

# PorterStemmer 
import nltk
from nltk.stem import PorterStemmer

word_stemmer = PorterStemmer()
print(word_stemmer.stem('writing'))

#LancasterStemmer 
import nltk
from nltk.stem import LancasterStemmer
Lanc_stemmer = LancasterStemmer()
print(Lanc_stemmer.stem('writing'))

#RegexpStemmer 
import nltk
from nltk.stem import RegexpStemmer
Reg_stemmer = RegexpStemmer('ing$|s$|e$|able$', min=4)
print(Reg_stemmer.stem('writing'))

#SnowballStemmer 
import nltk
from nltk.stem import SnowballStemmer
english_stemmer = SnowballStemmer('english')
print(english_stemmer.stem ('writing'))
              
              
        """)
    
    elif num =="8b":
        print(""" --- Pract 8b  ---
                        
#pip install nltk

import nltk
from nltk.stem import WordNetLemmatizer
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()
print("word :  lemma") 
print("rocks :", lemmatizer.lemmatize("rocks"))
print("corpora :", lemmatizer.lemmatize("corpora"))
 
# a denotes adjective in "pos"
print("better :", lemmatizer.lemmatize("better", pos ="a"))
              
              
        """)
    
    elif num =="9":
        print(""" --- Pract 9  ---
                        
#pip install pandas
#pip install nltk
#pip install regex
#pip install scikit-learn

import pandas as pd
import numpy as np
import re
import nltk
nltk.download('stopwords')

# Load the data
sms_data = pd.read_csv("spam.csv", encoding='latin-1')

# Rename columns if necessary
sms_data.rename(columns={'v1': 'Category', 'v2': 'Message'}, inplace=True)

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

stemming = PorterStemmer()
corpus = []

for i in range(len(sms_data)):
    s1 = re.sub('[^a-zA-Z]', ' ', sms_data['Message'][i])
    s1 = s1.lower()
    s1 = s1.split()
    s1 = [stemming.stem(word) for word in s1 if word not in set(stopwords.words('english'))]
    s1 = ' '.join(s1)
    corpus.append(s1)

from sklearn.feature_extraction.text import CountVectorizer
countvectorizer = CountVectorizer()
x = countvectorizer.fit_transform(corpus).toarray()
print(x)

y = sms_data['Category'].values
print(y)

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, stratify=y, random_state=2)

# Multinomial Naïve Bayes.
from sklearn.naive_bayes import MultinomialNB
multinomialnb = MultinomialNB()
multinomialnb.fit(x_train, y_train)

# Predicting on test data:
y_pred = multinomialnb.predict(x_test)
print(y_pred)

# Results of our Models
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
print(classification_report(y_test, y_pred))
print("accuracy_score: ", accuracy_score(y_test, y_pred))
              
              
        """)
    
    elif num =="10a":
        print(""" --- Pract 10a  ---
                        
#pip install -U spacy
#pip install nltk
#python -m spacy download en_core_web_sm


import spacy
import nltk
from nltk.corpus import state_union
from nltk.tokenize import PunktSentenceTokenizer
nltk.download('state_union')

# Load the spaCy model
sp = spacy.load("en_core_web_sm")
# Create our training and testing data:
train_text = state_union.raw("2005-GWBush.txt")
sample_text = state_union.raw("2006-GWBush.txt")

# Train the Punkt tokenizer:
custom_sent_tokenizer = PunktSentenceTokenizer(train_text)

# Tokenize:
tokenized = custom_sent_tokenizer.tokenize(sample_text)

def pos_tagging(text):

    #Using spacy
    # Process the text
    doc = sp(text)
    
    # Extract and print part-of-speech tags
    pos_tags = [(token.text, token.pos_, token.tag_) for token in doc]    
    return pos_tags

def main():
    # Input text for POS tagging "Trump is president of America"
    text = input("Enter a sentence for POS tagging: ")
    
    # Get POS tags
    tags = pos_tagging(text)
    
    # Print POS tags
    print("\nPart-of-Speech Tags:")
    for word, pos, tag in tags:
        print(f"{word:10} {pos:5} {tag}")
    process_content()


def process_content():
    #NLTK
    try:
        for i in tokenized[:2]:
            words = nltk.word_tokenize(i)
            tagged = nltk.pos_tag(words)
            print(tagged)
    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    main()

              
              
        """)
    
    elif num =="10b1":
        print(""" --- Pract 10b1  ---
                        
#pip install nltk
# Probabilistic parser
# Usage of "Give" and "Gave" in the Penn Treebank sample

import nltk

def give(t):
    return t.label() == 'VP' and len(t) > 2 and t[1].label() == 'NP' \\
           and (t[2].label() == 'PP-DTV' or t[2].label() == 'NP') \\
           and ('give' in t[0].leaves() or 'gave' in t[0].leaves())

def sent(t):
    return ' '.join(token for token in t.leaves() if token[0] not in '*-0')

def print_node(t, width):
    output = "%s %s: %s / %s: %s" % \\
             (sent(t[0]), t[1].label(), sent(t[1]), t[2].label(), sent(t[2]))
    if len(output) > width:
        output = output[:width] + "..."
    print(output)

for tree in nltk.corpus.treebank.parsed_sents():
    for t in tree.subtrees(give):
        print_node(t, 72)
              
              
        """)
    
    elif num =="10b2":
        print(""" --- Pract 10b2  ---

#pip install nltk

import nltk
from nltk import PCFG

grammar = PCFG.fromstring('''
NP -> NNS [0.5] | JJ NNS [0.3] | NP CC NP [0.2]
NNS -> "men" [0.1] | "women" [0.2] | "children" [0.3] | NNS CC NNS [0.4]
JJ -> "old" [0.4] | "young" [0.6]
CC -> "and" [0.9] | "or" [0.1]
''')

print(grammar)

viterbi_parser = nltk.ViterbiParser(grammar)
token = "old men and women".split()
obj = viterbi_parser.parse(token)

print("Output:")
for x in obj:
    print(x)
               
              
        """)
    
    elif num =="10c":
        print(r""" --- Pract 10c  ---
                        
#pip install nltk

#1. Java should be installed.
#2. maltparser-1.7.2 zip file should be copied in
#C:\Users\AppData\Local\Programs\Python\Python39 folder and should be
#extracted in the same folder.
#3. engmalt.linear-1.7.mco & engmalt.poly-1.7.mco file should be copied to
#C:\Users\ AppData\Local\Programs\Python\Python39 folder

from nltk.parse import malt
mp = malt.MaltParser('maltparser-1.7.2','engmalt.linear-1.7.mco')
#file
t = mp.parse_one('I saw a bird from my window.'.split()).tree()
print(t)
t.draw()


    """)
    
    elif num =="11a":
        print(""" --- Pract 11a  ---
                        
from nltk.tokenize import MWETokenizer
from nltk import sent_tokenize, word_tokenize

# Sample text
text = \"""
After years of hard work, she finally kicked the bucket. 
Her friends hit the nail on the head when they said she was over the moon about her new job. 
Unfortunately, things soon went downhill when she had to bite the bullet and confront her fears.
\"""

# Define multiword expressions (MWEs) to recognize
mwe_phrases = [
    ('kicked', 'the', 'bucket'),
    ('hit', 'the', 'nail', 'on', 'the', 'head'),
    ('over', 'the', 'moon'),
    ('went', 'downhill'),
    ('bite', 'the', 'bullet')
]

# Create MWETokenizer with the defined multiword expressions
tokenizer = MWETokenizer(mwe_phrases, separator='_')

# Tokenize the text into sentences
sentences = sent_tokenize(text)

print("Tokenized Sentences with MWEs:")
for sentence in sentences:
    # Tokenize each sentence into words, recognizing the MWEs
    tokenized_sentence = tokenizer.tokenize(word_tokenize(sentence.lower()))
    print("Original Sentence: ", sentence)
    print("Tokenized Sentence: ", tokenized_sentence)
    print()
              
              
        """)
    
    elif num =="11b":
        print(""" --- Pract 11b  ---

#pip install textdistance
#pip install scikit-learn
#pip install numpy

import numpy as np
import re
import textdistance
import sklearn  
from sklearn.cluster import AgglomerativeClustering

texts = [
    'Reliance supermarket', 'Reliance hypermarket', 'Reliance', 'Reliance', 'Reliance downtown', 'Relianc market',
    'Mumbai', 'Mumbai Hyper', 'Mumbai dxb', 'mumbai airport',
    'k.m trading', 'KM Trading', 'KM trade', 'K.M. Trading', 'KM.Trading'
]

def normalize(text):
    # Keep only lower-cased text and numbers
    return re.sub('[^a-z0-9]+', ' ', text.lower())

def group_texts(texts, threshold=0.4):
    # Replace each text with the representative of its cluster
    normalized_texts = np.array([normalize(text) for text in texts])
    distances = 1 - np.array([
        [textdistance.jaro_winkler(one, another) for one in normalized_texts]
        for another in normalized_texts
    ])
    clustering = AgglomerativeClustering(
        distance_threshold=threshold,  # this parameter needs to be tuned carefully
         metric="precomputed", linkage="complete", n_clusters=None
    ).fit(distances)
    centers = dict()
    for cluster_id in set(clustering.labels_):
        index = clustering.labels_ == cluster_id
        centrality = distances[:, index][index].sum(axis=1)
        centers[cluster_id] = normalized_texts[index][centrality.argmin()]
    return [centers[i] for i in clustering.labels_]

print(group_texts(texts))

                  
              
        """)
    
    elif num =="11c":
        print(""" --- Pract 11c  ---

#pip install nltk

#Word Sense Disambiguation
import nltk
from nltk.corpus import wordnet as wn
from nltk.wsd import lesk

# Ensure you have the WordNet data downloaded
nltk.download('wordnet')
nltk.download('omw-1.4')  # Open Multilingual Wordnet for better results

# Define a function to perform WSD using the Lesk algorithm
def disambiguate_word(word, sentence):
    # Use the Lesk algorithm to find the sense of the word in the given sentence
    sense = lesk(sentence, word)
    return sense

# Example sentences
sentence1 = "He went to the bank to withdraw money."
sentence2 = "She read a book on the shelf."
print(sentence1)
print(sentence2)

# Perform WSD for 'bank'
sense_bank = disambiguate_word('bank', sentence1)
print(f"Senses for 'bank': {sense_bank}")

# Perform WSD for 'book'
sense_book = disambiguate_word('book', sentence2)
print(f"Senses for 'book': {sense_book}")

# Print the definitions of the identified senses
if sense_bank:
    print(f"Definition of 'bank' sense: {sense_bank.definition()}")
else:
    print("No sense found for 'bank'")

if sense_book:
    print(f"Definition of 'book' sense: {sense_book.definition()}")
else:
    print("No sense found for 'book'")
                                      
              
        """)



    
    else:
        print("Invalid input")

#prog('10c')
#index()  
#pip() 
        