# Build Front end
pushd frontend/
npm install
npm run build
popd

# Build Docker Images
docker-compose build

# Launch
docker-compose up -d
