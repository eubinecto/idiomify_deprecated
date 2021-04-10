# use the idiomify.train script.
# this is the first iteration of idiomifier.
python3 ../../idiomify/train.py \
  --bert_model_name="deepset/sentence_bert" \
  --bert_embed_size=768 \
  --idiom2vec_embed_size=100 \
  --batch_size=20 \
  --epochs=3 \
  --learning_rate=0.001 \
  --num_workers=5 \
  --log_dir="../data/idiomifier/idiomifier_s_bert_001_log" \
  --def2embed_path="../../data/def2embed/def2embed_train.tsv" \
  --model_path="../../data/idiomifier/s_bert_idiomifier_001.model"
