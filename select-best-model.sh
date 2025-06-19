#/bin/bash
best_model=""
best_f1=0
for m in "$@"; do
    f1=$(python -c "import json; print(json.load(open('$m'))['True']['f1-score'])")
    if (( $(echo "$f1 > $best_f1" | bc -l) )); then
        best_f1=$f1
        best_model=$m
    fi
done
echo "${best_model} i the best model with f1-score ${best_f1}"
cp "${best_model%.metadata.json}" "model"