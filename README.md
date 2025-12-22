# Methane Minder 🌍

A full-stack application for visualizing and analyzing methane plume emissions data from Carbon Mapper. Built with FastAPI (Python) backend and Vue.js (TypeScript) frontend.

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Quick Start](#-quick-start)
  - [Docker Deployment (Recommended)](#docker-deployment-recommended)
  - [Local Development](#local-development)
- [Project Structure](#-project-structure)
- [Docker Architecture](#-docker-architecture)
- [API Documentation](#-api-documentation)
- [Data Dictionary](#-data-dictionary)
- [Development vs Production](#-development-vs-production)
- [Troubleshooting](#-troubleshooting)

---

## ✨ Features

- **Interactive Map**: Real-time methane plume visualization using Leaflet
- **Risk Assessment**: AI-powered risk analysis and forecasting
- **Emission Analytics**: Statistical analysis and time-series forecasting
- **Geospatial Data**: GeoParquet/GeoJSON support for efficient data handling
- **REST API**: FastAPI backend with automatic OpenAPI documentation
- **Responsive UI**: Modern Vue.js frontend with TailwindCSS and DaisyUI

---

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI 0.115+
- **Language**: Python 3.12+
- **Data Processing**: Pandas, GeoPandas, Shapely
- **ML/Analytics**: Scikit-learn, Statsmodels
- **Server**: Uvicorn (ASGI)

### Frontend
- **Framework**: Vue.js 3.5+
- **Language**: TypeScript 5.8+
- **Build Tool**: Vite 6.2+
- **Styling**: TailwindCSS 4.1+ with DaisyUI
- **Mapping**: Leaflet + Vue-Leaflet
- **Charts**: Chart.js + Vue-ChartJS
- **HTTP Client**: Axios

---

## 🚀 Quick Start

### Docker Deployment (Recommended)

**Prerequisites:**
- Docker Engine 20.10+
- Docker Compose 2.0+

**One Command Deployment:**

```bash
docker compose up --build
```

This will:
- Build the backend (Python/FastAPI) image
- Build the frontend (Vue.js/Nginx) image
- Start both services with health checks
- Set up networking between containers

**Access the Application:**

- **Frontend (Web UI)**: http://localhost
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

**Docker Commands:**

```bash
# Start in detached mode
docker compose up -d --build

# View logs
docker compose logs -f

# Stop services
docker compose down

# Rebuild from scratch
docker compose down && docker compose build --no-cache && docker compose up
```

---

### Local Development

**Prerequisites:**
- Python 3.12+
- Node.js 18+
- npm

#### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Install dependencies (using uv)
uv sync

# Or using pip
pip install -e .

# Start the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: http://localhost:8000

#### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will be available at: http://localhost:5173

---

## 📁 Project Structure

```
methane-minder/
├── backend/                    # Python FastAPI backend
│   ├── main.py                # Application entry point
│   ├── pyproject.toml         # Python dependencies
│   ├── Dockerfile             # Backend Docker image
│   └── src/
│       ├── app/
│       │   ├── api/v1/endpoints/  # API route handlers
│       │   ├── models/            # Data models
│       │   ├── routes/            # Route definitions
│       │   ├── services/          # Business logic
│       │   └── utils/             # Utility functions
│       └── data/              # Data files (CSV, GeoJSON, Parquet)
│
├── frontend/                   # Vue.js frontend
│   ├── src/
│   │   ├── App.vue           # Root component
│   │   ├── main.ts           # Application entry
│   │   ├── components/       # Vue components
│   │   └── stores/           # Pinia state management
│   ├── package.json          # Node dependencies
│   ├── Dockerfile            # Frontend Docker image
│   └── nginx.conf            # Nginx configuration
│
└── docker-compose.yml        # Docker orchestration
```

---

## 🐳 Docker Architecture

### Backend Container
- **Base Image**: Python 3.12-slim (multi-stage build)
- **Server**: Uvicorn (ASGI)
- **Port**: 8000
- **Features**:
  - Non-root user execution
  - Health checks
  - Optimized layer caching
  - Production-ready dependencies

### Frontend Container
- **Builder Stage**: Node 22-alpine
- **Runtime Stage**: Nginx 1.27-alpine
- **Port**: 80
- **Features**:
  - Static asset serving
  - API proxy to backend
  - Gzip compression
  - Security headers
  - SPA routing support

### Networking
- Both containers communicate via a private `methane-minder-network`
- Frontend proxies API requests to backend through Nginx
- Health checks ensure services are ready before accepting traffic

---

## 📚 API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

- `GET /health` - Health check
- `GET /v1/plumes` - Retrieve methane plume data
- `GET /v1/risk` - Risk assessment endpoints

---

## 📊 Data Dictionary

Data Dictionary for the data received from Carbon Mapper

| Column Name                   | Description                                                                 |
|------------------------------|-----------------------------------------------------------------------------|
| plume_id                     | Unique identifier for each detected methane plume.                         |
| plume_latitude               | Latitude coordinate (in decimal degrees) of the plume center.              |
| plume_longitude              | Longitude coordinate (in decimal degrees) of the plume center.             |
| datetime                     | Timestamp of when the plume was detected (UTC).                            |
| ipcc_sector                  | Source classification per IPCC (e.g., Energy, Waste, Agriculture).         |
| gas                          | Type of gas detected (usually CH₄ for methane).                            |
| emission_cmf_type           | Category of emission estimation method used (e.g., auto or manual).        |
| plume_bounds                | Polygon boundary of the plume, often as WKT or encoded string.              |
| instrument                   | Instrument used for detection (e.g., AVIRIS-NG, GAO, EMIT).                |
| mission_phase               | Phase of the mission when data was collected (e.g., prototype, operational).|
| published_at                | Date the plume record was published.                                        |
| modified                    | Last modified timestamp of the record.                                     |
| emission_version            | Version of the emissions estimation algorithm or dataset.                  |
| processing_software         | Software used to process plume data.                                       |
| gsd                         | Ground Sampling Distance in meters (spatial resolution).                   |
| sensitivity_mode            | Sensor sensitivity setting during acquisition.                             |
| off_nadir                   | Viewing angle off vertical, in degrees.                                    |
| emission_auto               | Automatically estimated emission rate (e.g., kg/hr).                        |
| emission_uncertainty_auto  | Uncertainty associated with auto emission estimate.                        |
| wind_speed_avg_auto        | Average wind speed used (m/s).                                              |
| wind_speed_std_auto        | Standard deviation of wind speed.                                          |
| wind_direction_avg_auto    | Average wind direction (degrees from North).                               |
| wind_direction_std_auto    | Standard deviation of wind direction.                                      |
| wind_source_auto           | Wind data source (e.g., HRRR model).                                        |
| platform                   | Platform used for data acquisition (e.g., aircraft, satellite).             |
| provider                   | Data provider or processing organization (e.g., JPL, EDF).                 |
| plume_tif                  | GeoTIFF file showing plume mask.                                           |
| plume_png                  | PNG preview of plume mask.                                                 |
| con_tif                    | Optional TIFF showing concentration or confidence.                          |
| rgb_tif                    | RGB image composite of the plume scene.                                    |
| rgb_png                    | PNG version of the RGB image.                                              |

---

## 🔧 Development vs Production

### Local Development
For development with hot reload:

```bash
# Backend
cd backend && uvicorn main:app --reload

# Frontend
cd frontend && npm run dev
```

**Benefits:**
- Instant code reload
- Better debugging experience
- Faster iteration

### Docker Deployment
Use Docker for:
- Staging environments
- Production deployments
- CI/CD pipelines
- Consistent testing environments

**Benefits:**
- Consistent environment across machines
- Production-ready configuration
- Isolated networking
- Easy scaling

---

## 🏗️ Docker Best Practices

### Multi-Stage Builds
Both Dockerfiles use multi-stage builds to minimize image sizes:
- **Backend**: Builder stage installs dependencies, runtime stage runs the app
- **Frontend**: Builder stage compiles Vue.js, nginx stage serves static files

### Build Optimizations
- **Layer Caching**: Dependencies installed before copying source code
- **Minimal Images**: Alpine and slim variants for smaller footprint
- **.dockerignore**: Excludes unnecessary files from build context

### Security
- Non-root users in containers
- Minimal base images (alpine/slim)
- Security headers in Nginx
- Read-only data mounts

---

## 🩺 Health Checks

Both services include health checks:
- **Backend**: HTTP check on `/health` endpoint
- **Frontend**: HTTP check on root path

View health status:
```bash
docker compose ps
```

---

## 🔍 Troubleshooting

### Port Conflicts
If port 80 or 8000 is already in use, edit `docker-compose.yml`:

```yaml
services:
  backend:
    ports:
      - "8001:8000"  # Change 8001 to any available port
  
  frontend:
    ports:
      - "8080:80"    # Change 8080 to any available port
```

### View Logs
```bash
# All services
docker compose logs -f

# Backend only
docker compose logs -f backend

# Frontend only
docker compose logs -f frontend

# Last 100 lines
docker compose logs --tail=100
```

### CORS Errors
The backend is configured to accept requests from `localhost:5173` (Vite) and `localhost:3000`. When using Docker, Nginx proxies requests so CORS isn't an issue.

### Missing Data Files
Ensure CSV and GeoJSON files exist in `backend/src/data/`:
- `methane-emissions.csv`
- `plumes_data_dictionary.csv`
- `plumes_raw_data.csv`
- `plumes.geojson`

### Rebuild from Scratch
```bash
docker compose down
docker compose build --no-cache
docker compose up
```

### Access Container Shell
```bash
# Backend container
docker compose exec backend sh

# Frontend container
docker compose exec frontend sh
```

---

## 📊 Resource Management

### View Container Resource Usage
```bash
docker stats
```

### Set Resource Limits
Edit `docker-compose.yml` to add resource constraints:

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
```

---

## 🚀 Production Deployment

### Build for Multiple Platforms
```bash
docker buildx build --platform linux/amd64,linux/arm64 -t methane-minder-backend backend/
```

### Push to Container Registry
```bash
# Tag images
docker tag methane-minder-backend:latest your-registry/methane-minder-backend:latest
docker tag methane-minder-frontend:latest your-registry/methane-minder-frontend:latest

# Push to registry
docker push your-registry/methane-minder-backend:latest
docker push your-registry/methane-minder-frontend:latest
```

### Environment Variables
For production, consider using environment files:

```bash
# Create .env file
cat > .env << EOF
BACKEND_PORT=8000
FRONTEND_PORT=80
ENVIRONMENT=production
EOF

# Reference in docker-compose.yml
docker compose --env-file .env up
```

---

## 🧪 Testing

### Frontend Tests
```bash
cd frontend

# Unit tests
npm run test:unit

# E2E tests (requires Playwright)
npx playwright install
npm run test:e2e
```

### Backend Tests
```bash
cd backend

# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

---

## 📝 License

This project uses data from Carbon Mapper's open data portal. Please refer to [Carbon Mapper's data license](https://carbonmapper.org/data) for attribution and usage guidelines.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📧 Contact

For questions or support, please open an issue on the repository.

---

**Built with ❤️ for environmental monitoring and climate action**
