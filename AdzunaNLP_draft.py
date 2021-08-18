import re
#pip install nltk
#nltk.download('words')

from nltk.corpus import stopwords
from nltk.corpus import words
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
import nltk
import pandas as pd
import collections

# import lookup datasets
f = open(r'C:\Users\scott\OneDrive\AWS\Adzuna\keywords.txt', "r")
keywords = f.read().splitlines()
df = pd.read_csv(r'C:\Users\scott\OneDrive\AWS\Adzuna\slipped_the_net.txt', header=None)
slipped_the_net = df[0].tolist()
# job search results
df_results = pd.read_csv(r"C:\Users\scott\Downloads\AdzunaJobSearch_20210601201252.csv")



# remove stopwords from the keyword list and add word type tags to the remainder
# stopwords are words such as we, to, are, look
'''
Tags Description
JJ	Adjectives
NN	Nouns
RB	Adverbs
PRP	Pronouns
VB	Verbs
NNP: noun, proper, singular
'''
mylist = []
stop_words = set(stopwords.words('english'))
for s in df_results["full_description"]:
    if pd.isna(s) == False:
        #print('test is ' + s)
        s1 =  re.sub('[^a-zA-Z0-9\s]+', '', s)
        word_tokens = word_tokenize(s1)    
        s2 = [w for w in word_tokens if w.casefold() not in stop_words]
        tagged_s2 = nltk.pos_tag(s2)
        mylist.append(tagged_s2)
full_list = []
for x in mylist:
    for y in x:
        full_list.append(y)


# remove duplicates
#list_set = set(full_list)
#unique_list = (list(list_set))

# remove all words that aren't tagged as NNP (noun, proper, singular)
# we are only interested in technology names, which tend to be nouns
nnp_words=[]
for i in full_list:
    if i[1] ==  'NNP':
        nnp_words.append(i)
        

# here we are looking to keep existing techwords plus potential new techwords. We do this by 
# 1. keep the non english words. Technologies tend to be words that aren't in the english dictionary
# 2. keep all the words in our keywords.txt file

neng_words=[]
for i in nnp_words:
    if i[0].casefold() not in words.words() or i[0].casefold() in [k.casefold() for k in keywords]:
        neng_words.append(i)

# remove plurals
# this could probably get wrapped up in the above, but keeping separate to aid debugging
'''
Example of how wordnet.morphy works.... a = input, b = output
a = Firms, b = firm
a = LinuxBSD, b = None
a = NET, b = net
a = PMS, b = pms
a = Balancers, b = balancer
a = Requirements, b = requirement
a = Hadoop, b = None
'''
nplural_words=[]
for word in neng_words:
    word_morphed = wordnet.morphy(word[0].casefold())
    z = word[0] or word_morphed
    if z not in words.words() or z.casefold() in [k.casefold() for k in keywords]:
        nplural_words.append(word[0])

# what we should be left with are a list of tech words and some that aren't (we just haven't encountered them before)
# the only way to distinguish between the two is to look at the slip_words list and if we see any non tech words then add them to keywords.txt
tech_master = []
slip_words = []
for i in nplural_words:    
    if i.lower() in [k.lower() for k in keywords]:
        # it is a tech word therefore add it to the final output
        tech_master.append(i)
    elif i.lower() not in [s .lower() for s in slipped_the_net]:
        # this is a word that's slipped through the filtering that isnt a tech word (at least not that we know of)
        slip_words.append(i)

         

# new slip list and slip master list should be mutually exclusive
c1 = set(slip_words)
c2 = set(slipped_the_net)
#c1 & c2
print('INFO: Words that slipped the net are ...')
print(c1)

# To train the program to better recognise tech words, you need to look at the list above and
# determine if any need to be added to keywords.txt

# add newly discovered slip words to slip master list
c1 | c2
f = open(r'C:\Users\scott\OneDrive\AWS\Adzuna\slipped_the_net.txt', "w")
for s in (c1 | c2):
    f.write(s + '\n')
f.close()

# remove duplicates
list_set = set(slip_words)
slip_words = (list(list_set))

# count occurences of each tech word
occurrences = collections.Counter(tech_master)


