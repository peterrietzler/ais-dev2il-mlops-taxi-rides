#/bin/sh

# Check if the required parameters are provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <username> <version>"
    echo "Example: $0 peterrietzler 1.0.0"
    exit 1
fi

USERNAME=$1
VERSION=$2

# Build the image and tag it for usage with the GitHub Container Registry
docker build -t ghcr.io/$USERNAME/taxi-rides-outlier-detection:$VERSION .

# Push the image
docker push ghcr.io/$USERNAME/taxi-rides-outlier-detection:$VERSION