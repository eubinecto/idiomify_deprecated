
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

> get idiom2vec model, and build the embedding labels for each idiom.

What should I do with the case of oov?:
```text
INFO:gensim.utils:Word2Vec lifecycle event {'fname': '/Users/eubin/Desktop/Projects/Big/idiomify/data/idiom2vec/idiom2vec_001.model', 'datetime': '2021-03-30T15:49:38.590558', 'gensim': '4.0.0', 'python': '3.8.6 (default, Oct  8 2020, 14:06:32) \n[Clang 12.0.0 (clang-1200.0.32.2)]', 'platform': 'macOS-10.16-x86_64-i386-64bit', 'event': 'loaded'}
Traceback (most recent call last):
  File "/Users/eubin/Desktop/Projects/Big/idiomify/idiomify/scripts/dataset/save_target_embeds.py", line 21, in <module>
    main()
  File "/Users/eubin/Desktop/Projects/Big/idiomify/idiomify/scripts/dataset/save_target_embeds.py", line 16, in main
    idiom_vec = idiom2vec_model.wv.get_vector(idiom)
  File "/Users/eubin/Desktop/Projects/Big/idiomify/idiomifyenv/lib/python3.8/site-packages/gensim/models/keyedvectors.py", line 422, in get_vector
    index = self.get_index(key)
  File "/Users/eubin/Desktop/Projects/Big/idiomify/idiomifyenv/lib/python3.8/site-packages/gensim/models/keyedvectors.py", line 396, in get_index
    raise KeyError(f"Key '{key}' not present")
KeyError: "Key 'American Dream' not present"
```
well.. you should leave them empty for now? If you don't have an embedding for American Dream, then
you simply cannot train idiomifier to laern def -> idiom mapping for that.

So, leave it empty.  -> leads to only 528 training instances. Well, that's just about enough for
prototyping the first iteration.


> Build train and eval set. (8:2)

You should split them up. You could use scikit learn for this..?
Wait, should I save them up 

Split it into train / eval set. This will later be used. - well, continue doing this tomorrow morning.


> How do I do transfer learning with a pre-trained bert? 

First of all, get the terminology right. What I want to do is slightly different from
"fine-tuning".

Fine-tuning optimizing the embeddings yet again with a custom corpus, whereas transfer learning is
training a pre-trained bert on a humongous corpus to have it carry out a new task, e.g. idiomify, for my case.

Then, how do I do transfer learning with transformers?

`Trainer()` seems to be what I'm looking for, as it is a simple framework for training
"any transformer models".

But how do I use it to have a transformer predict 200 numbers?



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


> In the next iteration

use a pos tagger maybe? to extract features from it. POS tagging does help.


## 31st of March, 2021

Today, is the reading day. Read papers, and come up with the architecture that fits you.
1. The primary goal here should be understanding BERT first. <- Make sure you read the paper

Continue from .. Build train and eval set.

Well, looks like you have to start reading papers, now.
Let's first read three papers.
1. Do some review on attention is all you need
2. First, I need reading BERT paper to begin with, and understand the math, mechanics
3. the distributional semantics -> reverse dictionary paper 
4. the BERT + reverse dictionary paper -> does that even work that well? Why 
5. another BERT + reverse dictionary paper
6. and also the one that pessimistically references 3. There are quite a lot of paper you might want to
read here.

What methods should you take? Your eyes are faster than your hands.
Read, understand, and find values from them. 


Hey, you might want to compare different models from different papers.

pretraining -> finetuning 으로의 연결을 보아야한다.


## 2nd of April, 2021

Here is the architecture of my first iteration.

1. def -> Bert -> def_vec (encoding the definition sentence)
2. def_vec -> perceptron_h -> def_vec_h
3. Loss = def_vec_h dot product with idiom_vec_h
4. train this over my dataset. (def, embedding)

Well, that would be my first iteration.

Then, you improve upon them by quantitative experiments.


> how do I do  def -> bert -> def_vec with transformer library?


Let's try this example.

## 3rd of April, 2021

```python
# forward pass
encoded = model(**tokenized)
print(encoded[0].shape)  # what is this? - this is a 3-dimensional tensor (e.g. [1, 6, 768])
print(encoded[1].shape)  # what is this? - this is a 2-dimensional tensor (e.g. [1, 768])
```

> What is the first one of the tuple?

That is the forward output from each transformer encoder layer. In original BERT, six layers were used, which 
is why we have 6 in the second dimension. Wait, 


> What is the second one of the tuple?

That is the output from the `[CLS]` token.


> BERT is pre-trained with a pair of sentences in Next Sentence Prediction task.
That is, the input has the form of `[CLS] + sent_1 + [SEP] + sent_2`. 
If we need not one, but two sentences to use BERT as the sentence encoder in the first place,
then how do you encode just one sentence? 

- https://datascience.stackexchange.com/questions/62658/how-to-get-sentence-embedding-using-bert

Apparently, we could `[PAD]` token as the placeholders for the second sentence.  But in order for this to work,
`[PAD]` must have been used pre-training. Otherwise, `[PAD]` would be a meaningless symbol to BERT.

- https://albertauyeung.github.io/2020/06/19/bert-tokenization.html

Sure enough, " the token `[PAD]` is used to represent paddings to the sentence.". So the token does have a meaning, 
namely "this is an empty space".

