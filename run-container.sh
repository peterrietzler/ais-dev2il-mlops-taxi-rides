#!/bin/sh

DATA_FOLDER=$1
INPUT_FILE=$2

if [ -z "$DATA_FOLDER" ]; then
    echo "Error: Data folder parameter is required."
    echo "Usage: $0 <data-folder> <input-file>"
    exit 1
fi

if [ -z "$INPUT_FILE" ]; then
    echo "Error: Input file parameter is required."
    echo "Usage: $0 <data-folder> <input-file>"
    exit 1
fi

if [ ! -d "$DATA_FOLDER" ]; then
    echo "Error: Data folder '$DATA_FOLDER' does not exist or is not a directory."
    exit 1
fi

if [ ! -f "$DATA_FOLDER/$INPUT_FILE" ]; then
    echo "Error: Input file '$INPUT_FILE' does not exist in the data folder '$DATA_FOLDER'."
    exit 1
fi

docker run --rm -v $(pwd)/$DATA_FOLDER:/app/data taxi-rides-outlier-detection /app/data/$INPUT_FILE
