#!/bin/sh
set -xe
if [ ! -f DeepSpeech.py ]; then
    echo "Please make sure you run this from DeepSpeech's top level directory."
    exit 1
fi;

if [ ! -d "${ds_dataroot}" ]; then
    ds_dataroot="librivox"
fi;

# Warn if we can't find the train files
if [ ! -f "${ds_dataroot}/librivox-train-clean-100.csv" ]; then
    echo "Warning: It looks like you don't have the LibriSpeech corpus"       \
         "downloaded and preprocessed. Make sure \$ds_dataroot points to the" \
         "folder where the LibriSpeech data is located, and that you ran the" \
         "importer script at bin/import_librivox.py before running this script."
fi;

checkpoint_dir=$(python3 -c 'from xdg import BaseDirectory as xdg; print(xdg.save_data_path("deepspeech/librivox"))')

python3 -u DeepSpeech.py \
  --train_files "$ds_dataroot/librivox-train-clean-100.csv,$ds_dataroot/librivox-train-clean-360.csv,$ds_dataroot/librivox-train-other-500.csv" \
  --dev_files "$ds_dataroot/librivox-dev-clean.csv,$ds_dataroot/librivox-dev-other.csv" \
  --test_files "$ds_dataroot/librivox-test-clean.csv,$ds_dataroot/librivox-test-other.csv" \
  --train_batch_size 8 \
  --dev_batch_size 8 \
  --test_batch_size 8 \
  --learning_rate 0.0001 \
  --epoch 5 \
  --display_step 1 \
  --validation_step 1 \
  --dropout_rate 0.30 \
  --default_stddev 0.046875 \
  --checkpoint_dir "/home/alan/Projects/DeepSpeech/logs/libribox/checkpoints" \
  --log_level 0 \
  --inference True \
  --inference_file_path "/home/alan/Projects/DeepSpeech/data/smoke_test/LDC93S1.wav" \
  --publish_wer_log True \
  --wer_log_file "/home/alan/Projects/DeepSpeech/logs/libribox/WER/werlog.js" \
  --export_dir "/home/alan/Projects/DeepSpeech/logs/libribox/export_models/"  \
  --summary_dir "/home/alan/Projects/DeepSpeech/logs/libribox/summaries/"     \
  # --limit_train 0 \
  # --limit_dev 0 \
  # --limit_test 0 \ 

  "$@"
