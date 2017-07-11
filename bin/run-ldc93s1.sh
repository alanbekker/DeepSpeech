#!/bin/sh
set -xe
if [ ! -f DeepSpeech.py ]; then
    echo "Please make sure you run this from DeepSpeech's top level directory."
    exit 1
fi;

if [ ! -f "data/ldc93s1/ldc93s1.csv" ]; then
    echo "Downloading and preprocessing LDC93S1 example data, saving in ./data/ldc93s1."
    python3 -u bin/import_ldc93s1.py ./data/ldc93s1
fi;

checkpoint_dir=$(python3 -c 'from xdg import BaseDirectory as xdg; print(xdg.save_data_path("deepspeech/ldc93s1"))')

python3 -u DeepSpeech.py \
  --train_files data/ldc93s1/ldc93s1.csv \
  --dev_files data/ldc93s1/ldc93s1.csv \
  --test_files data/ldc93s1/ldc93s1.csv \
  --train_batch_size 1 \
  --dev_batch_size 1 \
  --test_batch_size 1 \
  --display_step 1 \
  --validation_step 1 \
  --n_hidden 494 \
  --epoch 50 \
  --checkpoint_dir "/home/ubuntu/DeepSpeech/logs/libribox/checkpoints" \
  --log_level 0 \
  --inference True \
  --top_paths 1 \
  --inference_file_path "/home/ubuntu/DeepSpeech/data/smoke_test/LDC93S1.wav" \
  --publish_wer_log True \
  --wer_log_file "/home/alan/Projects/DeepSpeech/logs/WER/werlog.js" \
  --export_dir "/home/alan/Projects/DeepSpeech/logs/export_models/"  \
  --summary_dir "/home/alan/Projects/DeepSpeech/logs/summaries/"     \
  "$@"


