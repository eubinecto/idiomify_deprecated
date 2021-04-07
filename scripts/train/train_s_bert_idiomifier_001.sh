# use the idiomify.train script.
# this is the first iteration of idiomifier.
python3 -m idiomify.train \
  --bert_model_name="deepset/sentence_bert" \
  --bert_embed_size=768 \
  --idiom2vec_embed_size=100 \
  --batch_size=20 \
  --epochs=10 \
  --learning_rate=1e-5 \
  --save_path="../../data/idiomifier/s_bert_idiomifier_001.model"
