# Build Front end
pushd cube/dashboard-app/
npm run build
popd

# Build Docker Images
docker-compose build

# Launch
docker-compose up -d
