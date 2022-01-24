#!/bin/bash
echo "building database seed: $assembly"
python3 clinvar_vcf_parser.py $assembly && python3 ML_data_preprocessing.py && python3 train_model.py && python3 predict_clinvar_labels.py $assembly