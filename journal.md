
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

I want to finish off the first iteration today. 
- [x] train & test split (80 / 20)
- [ ] implement the mini batch SGD
- [ ] define the loss - what loss should you use? What did Hills, Cho et. al use for the loss? And why?
- [ ] implement training with epochs


## 7th of April, 2021

그러게. 일도 안하면서 낮에 도대체 뭐하면서 지내는 건지?
공부를 할거면 진지하게, 일을 한다는 태도로 하자. 그게 중요하다.
그냥 막무가내로 놀고 싶을 때 놀고, 공부하고 싶을 때 공부하는 것은 어른답지 못한 것.
루틴을 만들고 지키자.

what is your goal? in the next 2-hour session?

Well, my goal is to finish my first iteration.

In the evening, my goal then would be to finish my second iteration - Improve upon the first iteration.

Before you go to bed, set out all the deadlines up ahead.

Cherish this moment. You are working. Preparing for your future. This summer.
You are paving your own path.

In the next three hours: you'll accomplish these:
- [X] build pytorch TensorDataset with the definitions 25
- [X] build pytorch dataloader with the inputs 25
- [ ] implement the optimizer.
- [ ] define the loss. learn what loss they usd in that paper 25
- [ ] implement training with epochs 25
- [ ] train the model, and finish the epoch. 25

See that goal in full color. You input a sentence. It outputs a list of the most probable idioms!


> Do I need to have the bert tokenizer within Idiomifier class?

No, I don't think so, as you need that only for preprocessing the training data.


tensorboard - Could I also use this to measure the
moment for early stopping?


## 10th of April, 2021

Need some refactoring on the loader.

The loaders should be path-independent, otherwise I can't use them when I 
pip install the library.



Just simply running the code on my server does not get use of the GPU.

cuda.is_available() returns false.

It seems I have to install cuda first. and then.. install cuda-supported pytorch.


see if I have a cuda supported gpu:
```commandline
(idiomifyenv) eubin@eubinCloud:~/idiomify$ lspci | grep -i nvidia
06:00.0 VGA compatible controller: NVIDIA Corporation TU104 [GeForce RTX 2080 Rev. A] (rev a1)
06:00.1 Audio device: NVIDIA Corporation TU104 HD Audio Controller (rev a1)
06:00.2 USB controller: NVIDIA Corporation TU104 USB 3.1 Host Controller (rev a1)
06:00.3 Serial bus controller [0c80]: NVIDIA Corporation TU104 USB Type-C UCSI Controller (rev a1)
```

I have a rtx 2080, which is compatible with cuda.


- 우분투에서 cuda 설치하기.
  - https://ghostweb.tistory.com/832
    

checking ubuntu version:
```commandline
eubin@eubinCloud:~$ lsb_release -a
No LSB modules are available.
Distributor ID:	Ubuntu
Description:	Ubuntu 20.04.1 LTS
Release:	20.04
Codename:	focal
```

Mine is 20.04.1.


checking cpu architecture:
```commandline
eubin@eubinCloud:~$ uname -m
x86_64
```

Mine is x86_64. amd64 in other words.
 

Next....
- https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&target_distro=Ubuntu&target_version=2004&target_type=runfilelocal
go there, select the right options,  and download a cuda installer. 
  

I had a problem where... apt install cuda won't work.


- https://askubuntu.com/questions/598607/package-dependency-problem-while-installing-cuda-on-ubuntu-14-04
using aptitude fixed the problem.
  

Now, I have to have some evaluation metric to track the training progress.


학습하는 것보다.. 테스팅을 하는 것이 더 오래 걸리면 ㅋㅋㅋㅋ 안되는데.. 음...


idiom2vec 모델을 뭣하러 가져오는 거지? 어치피...... target_embeddings가 있는데 말이지?

이걸.. 내일 수정을 해보자. 목표는 evaluation 속도를 높이는 것... 아무리 생각해봐도 지금은 너무 느려... ㅇㅇ.
배치 10개마다 하는게 맞을 듯. 애초에... 10000개를 돌고. 각 10000개 별로 2500개 루프를 또 돌아야 하니 말이지.
오래 걸릴만함. 거기에다가 maximum sorting도 진행하니.. 그래 그럴만 하지.


로스함수 - 피어슨 유사도도 사용가능할까? - 두 벡터 사이의 유사도는 전부 사용해보는게 중요할 것.
 - 어떤 로스함수를 사용해야하나?
 - 이것에 대한 실험이 필요할 것.


데이터 수집도 더 해보아야 한다.


알고있는 지식이란 지식은 다 활용해야 한다.
나중에 - Knowledge Distillation도 적용하면 굿일듯!! -> serving을 하기 위해서.
그 라이브러리를 활용하면 될것.

나중에 bert pos pretrained도. feature engineering을 위해 사용해볼 것.


> 001 버전 test accuracy:
```commandline
before it was trained

trained
warnings.warn(msg)
100%|██████████| 2728/2728 [03:24<00:00, 13.35it/s]
0.00036656891495601173
```



## 15th of April

로스가 줄어들지 않는다. 음...
Why is that?

Pre-training을 미리 했어야 했을수도. BERT에 대한 제대로 된 이해가 없었다. 
이 부분은, 
이게 되는가..? 

로스함수가..., 로스함수가 문제인건가? 아니, pre-training이 필요한 면이 있을 것. 


BERT로 구현은 일단 포기하고. word2vec으로 하자.
this will be managable.

일단 지금까지 해온건.. feature branch에 저장해두고. 나중에 할 수 있으면 돌아오기.

역시, keep it simple. start simple. Don't start with a moon shot. You'd end up wasting your time.

aha... so what you need is a doc2vec.
embedding doc in the same space as in the words.


```commandline
### feeling nervous ###
hard_done_by 0.47776693
at_arm's_length 0.4168237
comfortable_in_one's_own_skin 0.40860572
mint_chocolate_chip 0.39100903
dyed_in_the_wool 0.37792718
get_under_someone's_skin 0.37533173
surprise_surprise 0.37454492
hot_under_the_collar 0.3706216
out_of_sorts 0.36664337
no_spring_chicken 0.35896105
### a dilemma or difficult circumstance ###
in_the_driving_seat 0.4062037
catch-22 0.38944834
come_to_grips_with 0.38771
as_best_one_can 0.37420952
life-or-death 0.37196288
race_against_time 0.3703875
fill_one's_boots 0.36326396
all_one's_eggs_in_one_basket 0.35644692
get_one's_head_around 0.35432136
surprise_surprise 0.35314885

```

가능성이 보인다. 이미 definition도 있으므로, evaluation도 가능할 것.
다음으로 doc2vec, tfidf를 훈련하자. 어차피 collocation을 구하기 위해 각 idiom에 대한 tfidf도 구하게 될것이므로.
그걸 한번 해보자고.


다음으로 필요한건.
1. doc2vec training - 001.
2. tfidf (collocation) 


