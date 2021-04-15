# use the idiomify.train script.
# this is the first iteration of idiomifier.

python3 ../../idiomify/runners/train.py \
  --bert_model_name="deepset/sentence_bert" \
  --bert_embed_size=768 \
  --idiom2vec_embed_size=200 \
  --batch_size=20 \
  --epochs=20 \
  --learning_rate=0.001 \
  --loss_fn="cosine_sim" \
  --num_workers=5 \
  --def2embed_train_path="../../data/def2embed/def2embed_train.tsv" \
  --save_path="../../data/idiomifier/s_bert_idiomifier_001.model"
