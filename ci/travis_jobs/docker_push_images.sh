# skip docker push if credentials are not set
if [ -z ${DOCKER_USERNAME+x} ] || [ -z ${DOCKER_PASSWORD+x} ]; then
    echo "DockerHub credentials not set. Skipping docker push"
    exit 0
fi

echo Timing docker push...
start_seconds=$SECONDS

echo "$DOCKER_PASSWORD" | docker login --username "$DOCKER_USERNAME" --password-stdin
docker push ${DOCKERHUB_TAG}

duration=$(( SECONDS - start_seconds ))
echo TIMING docker_setup
echo "Docker push took $(($duration / 60)) minutes and $(($duration % 60)) seconds."
echo
