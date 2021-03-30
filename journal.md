
## 24th of March 2021

Started developing.


There are three main tasks at stake:

1. prepare the training data
2. train the model
3. optimize the model


> What data do I need?

First of all, you must have a dictionary of idioms, with well-defined definitions.

Time to go back to merge-idioms. 
1. change the name of the project to identify-idioms, first.
2. find some ways to extract and parse as many idioms as possible, with their definitions.
 

## 25th of March 2021

I'm not scraping idiom2collocations altogether, no.

I'll do that, AND do idiomify.

The goal is to:
1. output a list of idioms that best describe an input phrase.
2. with extracted collocations to pick the one that they really wanted.


## 28th of March 2021

So what's the plan you have?
Now I have a training set.
1. tokenize dataset.
2. Train idiom2vec with a relatively small dataset.
3. get a pretrained bert.
I want to get a preliminary model by today. A simple prototype. -> well maybe not so obvious. 
I want to visualise the attention weights. Understand the whole thing.



## 29th of March 2021

I was meaning to do this. But I know I haven't got time for this today.

The next thing you should do is... finish the first iteration.

Jot down the things that you should improve up on.


## 30th of March 2021

I have compiled defs from lingua & thefree. 
I have v 0.0.1 idiom2vec model.
Now it is time to build the bert. 

Now, what do I need?

> Preparing the dataset
Build train validation and test set. 70, 10, 20 might be enough?
1. compare the case of doing simple upsampling vs. no upsampling at all. (why does that work at all?)

> Training the model

That's the first iteration that I want to finish off with today.
Have some evaluation method.
Then, before you move on to increasing the quality of idiom embeddings,
do the best you can do with optimizing parameters external to the model (and understand the model)
e.g.
1. how are they tokenized? why?
2. Does upsampling ever work? why?
3. How long does it take to train it o CPU? why?
4. How do I visualise the attention weights? -> This is crucial for interpretability.
  - the mathematics behind it?
5. Look, what you should aim to do is more in learning stuff from experiments, than just solving the problem.

Anything that you can learn from Hands-on machine learning with scikit learn? 



> In later iteration - use a pos tagger maybe? to extract features from it. POS tagging does help.
