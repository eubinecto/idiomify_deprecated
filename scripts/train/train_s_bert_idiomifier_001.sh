# use the idiomify.train script.
# this is the first iteration of idiomifier.
python3 ../../idiomify/train.py \
  --bert_model_name="deepset/sentence_bert" \
  --bert_embed_size=768 \
  --idiom2vec_embed_size=100 \
  --batch_size=20 \
  --epochs=10 \
  --learning_rate=1e-5 \
  --def2embed_path="../../data/def2embed/def2embed_train.tsv" \
  --model_path="../../data/idiomifier/s_bert_idiomifier_001.model"
