
# coding: utf-8

# # Hurricane Analysis

# ##### An exploratory analysis of how Hurricanes Harvey, Irma and Jose are depicted in news headlines.

# Imports:

# In[516]:

import requests
import json
import pandas as pd
import nltk
from nltk import sent_tokenize, word_tokenize, pos_tag
from nltk.corpus import stopwords
import time
import matplotlib.pyplot as plt  
import seaborn as sns
import string
from wordcloud import WordCloud, STOPWORDS


# Looping through API pages and returning article headlines:

# In[ ]:

page=0
headlines=[]
while page<31:
    api_nytimes=("http://api.nytimes.com/svc/search/v2/articlesearch.json?api-key=815512165c1244589cb0b6be02fb59f7&fq=headline:Harvey&sort=newest&page=".strip()
                 + str(page))
    page1=requests.get(api_nytimes).json()
    page=page+1
    time.sleep(1)
    for article in page1['response']['docs']:
        print(article['headline']['main'])


# In[ ]:

#repeat for Irma
page=0
headlines=[]
while page<31:
    api_nytimes=("http://api.nytimes.com/svc/search/v2/articlesearch.json?api-key=815512165c1244589cb0b6be02fb59f7&fq=headline:Irma&sort=newest&page=".strip()
                 + str(page))
    page1=requests.get(api_nytimes).json()
    page=page+1
    time.sleep(1)
    for article in page1['response']['docs']:
        print(article['headline']['main'])


# In[ ]:

#repeat for Jose
page=0
headlines=[]
while page<1:
    api_nytimes=("http://api.nytimes.com/svc/search/v2/articlesearch.json?api-key=815512165c1244589cb0b6be02fb59f7&fq=headline:Jose&sort=newest&page=".strip()
                 + str(page))
    page1=requests.get(api_nytimes).json()
    page=page+1
    time.sleep(1)
    for article in page1['response']['docs']:
        print(article['headline']['main'])


# ## Hurricane Bigrams
# After copying and pasting the above into Excel Workbook, tokenize and analyze for bigrams:

# In[862]:

harveydf=pd.read_excel('/Users/anna/Desktop/PRISMOJI/Hurricane_Headlines.xlsx', 
                     sheetname="Harvey")
harvey=str(harveydf.Harvey.unique().tolist())
harvey=harvey.replace("'", "").replace(",", "").lower()

words=word_tokenize(harvey)

punctuation = list(string.punctuation)
stops=set(stopwords.words('english')+punctuation+['hurricane', 'harvey', 'irma', 'jose', 
                                                 'florida', 'texas', 'caribbean', 'houston',
                                                 'WHATS', 'HAPPENING','miami','georgia', 'orange', 'trump',
                                                 'daca'])

h_bigrams= [b for b in nltk.bigrams(words) if (b[0] == 'harvey') and b[1] not in stops]
harveybigrams=pd.DataFrame(h_bigrams)
harveybigrams.columns=['Hurricane Name', 'Word']

hcounts=harveybigrams['Word'].value_counts()
hcounts=pd.DataFrame(hcounts).reset_index()
hcounts.columns=['Word', 'Count']
hcounts=pd.concat([harveybigrams['Hurricane Name'], hcounts], axis=1).dropna()[:15]

sns.set_style('white')
ax=sns.factorplot(y='Word', x = 'Count', data=hcounts ,kind="bar", size=5, aspect=2, palette="PuBu")
plt.title('Harvey...')
ax.set(xlabel="", ylabel="")
plt.show()

harveycloud = WordCloud(stopwords=no,background_color='white',width=1200,
                  height=800).generate(" ".join(hcounts['Word'].values))
plt.imshow(harveycloud, alpha=0.8)
plt.axis('off')
plt.show()


# Repeat for Irma:

# In[877]:

irmadf=pd.read_excel('/Users/anna/Desktop/PRISMOJI/Hurricane_Headlines.xlsx', 
                     sheetname="Irma")
irma=str(irmadf.Irma.unique().tolist())
irma=irma.replace("'", "").replace(",", "").lower()

words=word_tokenize(irma)
punctuation = list(string.punctuation)

i_bigrams= [b for b in nltk.bigrams(words) if (b[0] == 'irma') and b[1] not in stops]
irmabigrams=pd.DataFrame(i_bigrams)
irmabigrams.columns=['Hurricane Name', 'Word']

icounts=irmabigrams['Word'].value_counts()[:10]
icounts=pd.DataFrame(icounts).reset_index()
icounts.columns=['Word', 'Count']
icounts=pd.concat([irmabigrams['Hurricane Name'], icounts], axis=1).dropna().drop([0])

sns.set_style('white')
ax=sns.factorplot(y='Word', x = 'Count', data=icounts ,kind="bar", size=4, aspect=1.7, palette="PuBu")
plt.title('Irma...')
ax.set(xlabel="", ylabel="")

plt.show()


# Jose has much less data, so a bar chart isn't necessarily useful:

# In[782]:

josedf=pd.read_excel('/Users/anna/Desktop/PRISMOJI/Hurricane_Headlines.xlsx', 
                     sheetname="Jose")
jose=str(josedf.Jose.unique().tolist())
jose=jose.replace("'", "").replace(",", "").lower()

words=word_tokenize(jose)
punctuation = list(string.punctuation)
j_bigrams= [b for b in nltk.bigrams(words) if (b[0] == 'jose')]
josebigrams=pd.DataFrame(j_bigrams)
josebigrams.columns=['Hurricane Name', 'Word']

jcounts=josebigrams['Word'].value_counts()
jcounts=pd.DataFrame(jcounts).reset_index()
jcounts.columns=['Word', 'Count']
jcounts=pd.concat([josebigrams['Hurricane Name'], jcounts], axis=1).drop([1,2,3,6])

sns.set_style('white')
ax=sns.factorplot(y='Word', x = 'Count', data=jcounts ,kind="bar", size=4, aspect=1, palette="PuBu")
plt.title('Jose...')
ax.set(xlabel="", ylabel="")
plt.show()


# Non-Interactive Chart of Hurricane Bigrams:

# In[852]:

stormverbs=pd.concat([hcounts,icounts,jcounts], axis=0)[:100] #all storms and their bigrams
stormverbs=stormverbs.dropna()
stormverbs=stormverbs.sort_values(by=['Count'], ascending=False)
stormverbs.head()
g = sns.factorplot(x='Count', y='Word', hue='Hurricane Name', kind='strip', data=stormverbs, size=4, aspect=2,
                  palette="PuBu")
g.set_xticklabels([])
g.set(xlabel="", ylabel="")
plt.show()


# Interactive version with Plotly:

# In[839]:

import plotly.plotly as py
import plotly
from plotly.graph_objs import *
py.sign_in('annamongillo', '64lcfd7Mmlak5ydHoCSF')
plotly.offline.init_notebook_mode(connected=True)
from IPython.display import HTML
HTML(filename='/Users/anna/Desktop/PRISMOJI/hurricanes.html')


# Word Cloud of all words in headlines:

# In[866]:

heads=harvey+irma+jose 
for word in stops:
    heads = heads.replace(" " + word + " ", " ")
heads=heads.replace("'", "").replace(",", "").replace("]", '').replace("[", '').replace(';', '').replace(':', '')
heads=heads.split()

headlinesdf=pd.DataFrame(heads)
headlinesdf.columns=['Words']

countsseries=pd.Series(' '.join(headlinesdf['Words']).lower().split()).value_counts()[:600]
countsdf=pd.DataFrame(countsseries).reset_index()
countsdf.columns=['Word', 'Count']

cloud = WordCloud(stopwords=no,background_color='white',width=1200,
                  height=800).generate(" ".join(countsdf['Word'].values))
plt.imshow(cloud, alpha=0.8)
plt.axis('off')
plt.show()


# Part of Speech Analysis:

# In[853]:

harveydf=pd.read_excel('/Users/anna/Desktop/PRISMOJI/Hurricane_Headlines.xlsx', 
                     sheetname="Harvey")
harvey=str(harveydf.Harvey.unique().tolist())
harvey=harvey.replace("'", "").replace(",", "")

irmadf=pd.read_excel('/Users/anna/Desktop/PRISMOJI/Hurricane_Headlines.xlsx', 
                     sheetname="Irma")
irma=str(irmadf.Irma.unique().tolist())
irma=irma.replace("'", "").replace(",", "")

josedf=pd.read_excel('/Users/anna/Desktop/PRISMOJI/Hurricane_Headlines.xlsx', 
                     sheetname="Jose")
jose=str(josedf.Jose.unique().tolist())
jose=jose.replace("'", "").replace(",", "")

heads=harvey+irma+jose
new = nltk.word_tokenize(heads)
tagged = nltk.pos_tag(new)

stopsupper=[word[:1].upper() + word[1:] for word in stops]

adj = [token for (token,tag) in tagged if  tag.startswith('JJ') and token.isalpha() and token not in stopsupper]
common_adj = nltk.FreqDist(adj)
adjectives=pd.DataFrame(common_adj.most_common(16))
adjectives.columns=['Adjective','Count']

verb = [token for (token,tag) in tagged if  tag.startswith('VB') and token.isalpha() and token not in stopsupper]
common_verb = nltk.FreqDist(verb)
verbs=pd.DataFrame(common_verb.most_common(20))
verbs.columns=['Verb','Count']

noun = [token for (token,tag) in tagged if  tag.startswith('NN') and token.isalpha() and token not in stopsupper]
common_noun = nltk.FreqDist(noun)
nouns=pd.DataFrame(common_noun.most_common(20))
nouns.columns=['Noun','Count']

sns.set_style('white')

ax1=sns.factorplot(x='Count', y = 'Noun', data=nouns ,kind="bar", size=4.25, aspect=1.9, palette="PuBu")
plt.title('Most Frequent Nouns in Hurricane Headlines')
ax1.set(xlabel="", ylabel="")
ax1.set(xticklabels=[])

ax2=sns.factorplot(x='Count', y = 'Adjective', data=adjectives ,kind="bar", size=4.25, aspect=1.9, palette="PuBu")
plt.title('Most Frequent Adjectives in Hurricane Headlines')
ax2.set(xlabel="", ylabel="")
ax1.set(xticklabels=[])

ax3=sns.factorplot(x='Count', y = 'Verb', data=verbs ,kind="bar", size=4.25, aspect=1.9, palette="PuBu")
plt.title('Most Frequent Verbs in Hurricane Headlines')
ax3.set(xlabel="", ylabel="")
ax3.set(xticklabels=[])

plt.show()

