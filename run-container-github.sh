#!/bin/sh

USERNAME=$1
VERSION=$2
DATA_FOLDER=$3
INPUT_FILE=$4

if [ -z "$USERNAME" ]; then
    echo "Error: Username parameter is required."
    echo "Usage: $0 <username> <version> <data-folder> <input-file>"
    exit 1
fi

if [ -z "$VERSION" ]; then
    echo "Error: Version parameter is required."
    echo "Usage: $0 <username> <version> <data-folder> <input-file>"
    exit 1
fi

if [ -z "$DATA_FOLDER" ]; then
    echo "Error: Data folder parameter is required."
    echo "Usage: $0 <username> <version> <data-folder> <input-file>"
    exit 1
fi

if [ -z "$INPUT_FILE" ]; then
    echo "Error: Input file parameter is required."
    echo "Usage: $0 <username> <version> <data-folder> <input-file>"
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

docker run --rm -v $(pwd)/$DATA_FOLDER:/app/data ghcr.io/$USERNAME/taxi-rides-outlier-detection:$VERSION /app/data/$INPUT_FILE
