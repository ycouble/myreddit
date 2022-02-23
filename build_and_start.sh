# Build Front end
cd cube/dashboard-app/
npm run build

# Build Docker Images
docker-compose build

# Launch
docker-compose up -d
