# Build Front end
pushd frontend/
npm run build
popd

# Build Docker Images
docker-compose build

# Launch
docker-compose up -d
