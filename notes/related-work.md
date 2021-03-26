## 25th of March 2021


> What is your goal?

Idiomify: to implement a reverse dictionary search for idioms. Just idioms. 


> Have people tried reverse dictionary search for words?

Yes, they have. The gold baseline seems to be [one look](https://www.onelook.com/thesaurus/?s=to%20be%20straightforward).


> Has anyone done it? 

There are quite a bunch of papers worked on it.


*Building a Scalable Database-Driven Reverse Dictionary* (Shaw, 2011)
- why?
  - not only for L2 learners, but for writers as well.
- how?
  - situation: input phrase resembles the definition of the word the user is looking for, at least conceptually if not exactly.
 e.g. “talks a lot, but without much substance.” should return
  *garrulous* as one of the outputs, although "full of trivial conversation" definition of
  *garrulous* does not include any words in the input phrase.
- why is it hard?: The user does not necessarily    
  - it gets use of antonyms, hypernyms. Perhaps from WordNet.-> **I cannot do this with idioms**.
       
So I can't use their methods. Are there any methods that don't rely on WordNet?

*Implementing a Reverse Dictionary, based on word definitions, using a
Node-Graph Architecture* (Thorat, 2016)
  - why?
    - RD is a solution to so-called Tip-of-the-Tongue problem. (Schwartz and Metacalfe, 2011). "plagues" people
    when they want to articulate their thoughts.
    - can also be used to treat *word selection anomic aphasia*(Rohrer et al., 2008). (neurological disorder).
  - advantage? people have tried to embed phrases with RNN and LSTMs (distributional semantics approach),
      but they don't perform exceptionally well. Here, the authors employ a rule base approach that
    performs much better than the distributional semantics approach.
  - how?
    - they used a graph. 
    - but they also get use of relations of words from WordNet. -> **I cannot do this with idioms**.
  - result?
    - much better than distributional semantics method. (as they wanted)
    - as good as Onelook.
    
I can't use them as well, as they also rely on WordNet. And I don't have enough time to indulge into 
expert systems. My remarks on - "they don't perform exceptionally well" - hey but that doesn't mean they are terrible. 
an advantage of using that approach is that you don't need expert engineering to build RD, like you are doing in this paper.
What is that paper they are citing that with? 

```
Felix Hill, Kyunghyun Cho, Anna Korhonen,
and Yoshua Bengio. 2015. Learning to understand
phrases by embedding the dictionary. arXiv
preprint arXiv:1504.00548.
```

Okay, that seems more like what I'm looking for. 


*Learning to Understand Phrases by Embedding the Dictionary* (Hill, Cho - 조경현 교수님!, 2016)
- why?
  - distributional semantics approach to words - successful. But to "arbitrary-length phrases and sentences",
    proved to be far harder. why are phrases hard? because there are no gold standard for phrasal
    representations. (hard to find training data in good quality). Therefore hard to train, hard to
    evaluate.
- how?
  - to address "no gold standard" issue, they use the definitions found in everyday dictionary.
    definitions are high quality phrases. They are abundant. 
  - they train a neural embedding models to map (arbitrary-length phrases -> word embeddings (that actually makes sense!). 
    (qus- what if there is only one sense?) 
  - to test this, we apply the embedding model to two tasks:
    - reverse dictionary(Zock and Bilac, 2004). used by writers. solves tip-of-the-tongue issue. 
    - and general-knowledge crossword question answers. 
- goal?
  - to learn useful representation (embeddings) of **phrases and sentences**
- advantage?
  - people have proposed reverse dictionary models. But they generally
    require "hand-engineered features of the two sentences". 
- result?
  - performs as well or better than existing commercial systems, without
    **significant task-specific engineering**. (now that's what I want to buy.)
    
    
Now, that seems promising. All I need is just taking the same approach,
but this time do that with BERT, and with a set of idioms (not words).

That actually makes sense! Now I've got a good plan.

1. build a training set for idiomify. (idiom, definition). - where do I get this from
1. First, build idiom2vec from a huge corpus. -> I only need to do that for idioms .
3. Second, build idiomify model, but with bert!. (maps definitions to embeddings of the idioms)
4. third, query a phrase, and find the nearest neighbour to the output!
