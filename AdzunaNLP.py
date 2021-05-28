import re
#pip install nltk
#nltk.download('words')

from nltk.corpus import stopwords
from nltk.corpus import words
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
import nltk
import pandas as pd

# import lookup datasets
f = open(r'C:\Users\scott\OneDrive\DLG\Adzuna\keywords.txt', "r")
keywords = f.read().splitlines()
#f = open(r'C:\Users\scott\OneDrive\DLG\Adzuna\seeds.txt', "r")
#keywords = f.read().splitlines()
df = pd.read_csv(r'C:\Users\scott\OneDrive\DLG\Adzuna\slipped_the_net.txt', header=None)
slip_master = df[0].tolist()



#remove stopwords and tag the remainder
mylist = []
stop_words = set(stopwords.words('english'))
for s in df1["full_description"]:
    s1 =  re.sub('[^a-zA-Z0-9\s]+', '', s)
    word_tokens = word_tokenize(s1)    
    s2 = [w for w in word_tokens if w.casefold() not in stop_words]
    tagged_s2 = nltk.pos_tag(s2)
    mylist.append(tagged_s2)
full_list = []
for x in mylist:
    for y in x:
        full_list.append(y)


#remove duplicates
list_set = set(full_list)
unique_list = (list(list_set))

#remove all words that aren't tagged as NNP (noun, proper, singular)
'''
Tags Description
JJ	Adjectives
NN	Nouns
RB	Adverbs
PRP	Pronouns
VB	Verbs
NNP: noun, proper, singular
'''
nnp_words=[]
for i in unique_list:
    if i[1] ==  'NNP':
        nnp_words.append(i)
        
        
#remove english words or words that aren't tech words (based on what we've classified as a text word to date)
neng_words=[]
for i in nnp_words:
    if i[0].casefold() not in words.words() or i[0].casefold() in [k.casefold() for k in keywords]:
        neng_words.append(i)

#remove plurals
#this could probably get wrapped up in the above, but keeping separate to aid debugging
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

#bespoke filtering
ntech_words = []
slip_words = []
for i in nplural_words:
    if i not in slip_master:
        ntech_words.append(i)
    else:
        #store non techhie words that didnt get filtered out
        slip_words.append(i)
        
#validation step
#a = set(keywords)
#b = set(nplural_words)
#a - b

#for x in unique_list:
#    if x[0] == 'Agile':
#       print('found')


#store those non-techhie words, which haven't been captured already
c1 = set(slip_words)
c2 = set(slip_master)
c2 - c1

        






