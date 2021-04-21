

# Idiomify: Building a collocation-supplemented reverse-dictionary of idioms for L2 learners
- wordcount: 10,000 - 15,000
- you are going to finish this up, right?
- yeah, I am freaking doing this.
- stop writing the code, and work on writing things up.
- who is your reader? - a professor in SLA.
- "the L2 learners" bit explains the motive for including collocations.

## Table of Contents
- introduction
  - Objective (clearly state the objective.)
  - motivation
  - related work
  - pipeline  
- methods
  - 
  - idiom2collocations
  - idiomify
- results
- discussion
- conclusion

## Abstract



> show an example of the usage of idiomify.

Picture this. You want to use an idiom.

> what is your conclusion?

- Will serve as a good baseline for reverse-dictionary of idioms. With further improvement,
  Should be able to help L2 learners's tip-of-the-tongue problem with idioms.
- the collocations alone - could be used to compile "Learner's Dictionary of Collocations of English Idioms"
- Both combined: 


## Introduction
> An overall illustration of the project should go here. Something like 
the one in the first page of LDA2Vec paper.

### Objective

> what is your aim?

To build a collocation-supplemented reverse-dictionary of idioms for L2 learners

> Just show what you have done up-front. Use one concrete example scenario.


### Motivation
#### Motivation for Idiomify
> Why build a reverse-dictionary?

**To solve the tip-of-the-tongue problem.**
- cite more than 2 research that illustrates the problem. ()


> why build a reverse-dictionary of idioms specifically?

**because... "tip-of-the-tongue" problem is more salient in the usage of idioms?**
- any research that backs this up? 


> why do you want to build one specifically L2 learners?

**Because idioms are hard to learn especially for L2 learners.**

#### Motivation for Idiom2collocaitons

> why extract collocations of idioms?

**Because reverse-dictionary of idioms alone is not enough, if it were to be truly useful for L2 learners**.


We have a very good example here:
```commandline
### cause something to fail or go wrong ###
screw-up 0.38500065
slip-up 0.34881598
stir-crazy 0.3009596
```
What should you choose in your context? They are all very similar to the queried definition!
This is when 

### Related Work

> What is a reverse dictionary?

Show one-look as an example. They are meant to solve tip-of-the-tongue problem.
Cite two researches that show this. okay? Show us an example.

> How have people tried to build one?

People have indeed tried doing this. The papers I have looked.
- ml approach: the modeling phrases paper (Cho)
- rule-based approach: the graph paper.

One thing to note: They all have used WordNet.

> If people have done it already, then why build one?

Although reverse-dictionary of words exist, there are none for idioms. 

> Why do 

> Why do you want to implement idiomify?

1. To solve tip-of-the-tongue problem with idioms.
   

> Why do you want to 
2. Just having a reverse dictionary is not enough; to use idioms precisely and
naturally - we need collocations.

   
> At the end of the introduction - what is your aim?

The project comes down to 

1. Identifying idioms.
2. Preprocessing data.
   - `idiom2sent`: raw tokens. [IDIOM] token.
   - `idiom2lemma2pos`: `idiom2sent` lemmatised and cleansed. (used for idiom2collocations and idiom2vec)
   - `idiom2bows`: `idiom2lemma2pos`, but grouped by idioms and stopwords are filtered. (used for idiom2vec) 
3. Modeling collocations.
   - tf and tfidf
     - explain the tfidf equation, and justify why it could be used to model collocation.
     - show a concrete example. But mention that more details will be laid out  
   - pmi 
4. Extracting collocations.
   - 
5. Training Idiom2vec.
   - what is word2vec?
   - training set lemmatised by default. proper nouns filtered by default. (makes sense)
     - do make sure to cite papers to back your argument.
   - stopwords included vs. stopwords removed. -> not sure which would be better.
6. Modeling phrase vectors.
  - sum?
  - average?
  - weighted average?
1. identify-idioms: For automatically identifying idioms from a large corpora.
2. idiom2collocations: For modeling collocations and thereby extracting then from corpora. 
3. idiom2vec: For getting a vector representation of idioms.
4. idiomify: The main goal; for .




## Methods and Justifications

The methods used with reasons, in chronological order, with concrete examples where needed.


1. identify-idioms
2. building `idiom2lemma2pos`
   - proper nouns were filtered. (something we've learned from )
2. idiom2collocations
   1. build `idiom2bows` from `idiom2lemma2pos`
      - lemmatised, stopwords are filtered.
   2. modeling collocation: tf and tfidf.
   3. modeling collocation: pmi
    
3. 

### Identifying idioms

> what & why?
- here, the "why" should be very brief. It should have been mentioned in the introduction.

> how?


> an example of identified idioms (what can it do?)


> evaluate?

- It is difficult to do this. So I've written tests. To ensure its robustness.
- Include the test cases here. 
- Hey, maybe if you push this to... spacy, and then they accept it? Then, this may be


### Pre-processing data


### Modeling collocations


### 

### idiom2collocations

> what & why?


> an example of extracted collocations


### idiom2vec

> what was the goal? Getting a numerical representation of idioms.
- could be many: tf, tfidf or anything built from the co-occurence matrix.
- here, we use Word2vec. (e.g. Glove) - give us an example (leader )

> why?

> intersecting with Glove

> an example of most similar search

### idiomify

> What was the goal? Using idiom2vec, search idioms that best describes a given phrase.


> an example of a search result


## Results and Discussion - what have you learned? from your experiments?

As for identify-idioms, you don't need to include them here. You descibe 

### idiom2collocations

### idiom2vec

1. a bonus - we can get similar idioms
1. some interesting analogies


### idiomify

1. without stopwords vs. with stopwords
2. simple mean vs. weighted mean

> What is your conclusion here?
- pmi -> is the best measure for collocations.
- idiom2vec, without stopwords, transfer learning => best model.
- idiomify -> weighted average is the best model. (weighted with respect to)

> How does averaging word vectors work so well?


> Can we do better?


### idiom2collocations

> show the preliminary experiment (that you've already written up)


> and then show the experiment (full coca_spok, full )

> How do I evaluate this?

1. tf
2. tfidf
3. pmi

Get the most representative examples for randomly sampled 100 idioms. (By hand.)
Add up the scores!


### idiomify

> How do I evaluate this?

As for randomly sampled 100 idioms.
Get the definitions from the dictionary.

> How could I improve upon this?


- break bow assumption - use BERT or LSTM.
  - the two papers.
  - in this case, we could use idiom2vec to train this!
    

### idiom2vec

> down-project the idioms, to visualise what? Before & after intersecting glove?

> How do I evaluate this?

See how these affect the performance on idiomify.

1. stopwords vs. stopwords filtered
2. no transfer learning vs. transfer learning (load projection weights from Glove)

