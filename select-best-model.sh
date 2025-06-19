#/bin/bash
best_model=""
best_f1=0
for m in "$@"; do
    f1=$(python -c "import json; print(json.load(open('$m'))['True']['f1-score'])")
    if python -c "exit(0) if float('$f1') > float('$best_f1') else exit(1)"; then
        best_f1=$f1
        best_model=$m
    fi
done
echo "${best_model} is the best model with f1-score ${best_f1}"
cp "${best_model%.metadata.json}" "model"