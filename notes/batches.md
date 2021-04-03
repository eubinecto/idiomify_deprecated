## 3rd of April, 2021


> Why do I need "batches" to begin with?

You could compute the loss once and for all with the entire training set. But that is not necessarily an optimal strategy.

why is that? There is [a good answer from Ian Good Fellow](https://www.quora.com/In-deep-learning-why-dont-we-use-the-whole-training-set-to-compute-the-gradient):
1. "you need to do O(m) computation and use O(m) memory, but you reduce the amount of uncertainty in the gradient by a factor of only O(sqrt(m))."
   You do get greater certainty on the gradient with greater batch size, but **you get diminishing return with it O(sqrt(m)).**  
2. "even using the entire training set does not really give you the true gradient". Your entire training set is just
a huge mini batch after all.
   
another [answer from Matthew Wilson](https://qr.ae/pG8gyz):
There is a trade-off between the frequency and accuracy of gradient updates.
- low frequency, high accuracy of gradient updates
  - computing the loss over the entire training set? What if there were trillions of data points? It would take ages to
    take just a single step towards the optima, when updating weights with mini batches of size 32 would have found the optima
    already. "The extra precision just isn’t worth waiting for when you could instead be moving to a better part of 
    the parameter space and getting closer to convergence based on an approximate gradient." 
- *adequate frequency, reasonable accuracy of gradient updates**
  - i.e. mini-batch SGD. this is what we want. Finding the sweet spot **takes experiments** - This is what we want to do!
- excessively small mini batches
  - cannot take full advantage of GPU parallelism. 
   
So, we need batches to perform mini batch SGD, where you split the training set into "batches". We compute the loss
for each batch, and thereby update the weights with respect to each batch. (not with respect to the entire training set).


> How do I optimise the number of batches?

- https://stats.stackexchange.com/a/326663

"In general, batch size of 32 is a good starting point, and you should also try with 64, 128, and 256.".
- small batch -> high noise -> more chance of escaping local optima
- large batch -> less noise -> less chance of escaping local optima.
- Wait, it seems "randomness" is not something we want to achieve here. It's just something we are reluctantly
accepting, in order to approximate the true gradient. -> Is this true?


> How do I implement stochastic gradient descent with pytorch?

