#!/bin/sh

USERNAME=$1
VERSION=$2
DATA_DIR=$3
DATE=$4


if [ -z "$USERNAME" ]; then
    echo "Error: Username parameter is required."
    echo "Usage: $0 USERNAME VERSION DATA_DIR [DATE]"
    exit 1
fi

if [ -z "$VERSION" ]; then
    echo "Error: Version parameter is required."
    echo "Usage: $0 USERNAME VERSION DATA_DIR [DATE]"
    exit 1
fi

if [ ! -d "$DATA_DIR" ]; then
    echo "Error: Data dir '$DATA_DIR' does not exist."
    echo "Usage: $0 DATA_DIR [DATE]"
    exit 1
fi

docker run --rm -v $(pwd)/$DATA_DIR:/data ghcr.io/$USERNAME/taxi-rides-outlier-detection:$VERSION /data $DATE
