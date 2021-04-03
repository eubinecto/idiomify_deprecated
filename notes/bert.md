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

