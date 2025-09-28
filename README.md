# evacu-mate

evacu-mate is an emergency evacuation assistance prototype that combines a React + Vite frontend with a FastAPI backend. The system helps users find optimal evacuation routes and shelter locations during emergencies.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Project Setup](#project-setup)
- [Frontend Setup](#frontend-setup)
- [Backend Setup](#backend-setup)
- [MongoDB Setup](#mongodb-setup)
- [Auth0 Setup](#auth0-setup)
- [Environment Variables](#environment-variables)
- [Running the Application](#running-the-application)
- [Troubleshooting](#troubleshooting)

## Prerequisites

- Node.js 18+ and npm
- Python 3.10+ 
- MongoDB Atlas account (or local MongoDB instance)
- Auth0 account for authentication

## Project Setup

Clone the repository and navigate to the project folder:

```bash
git clone <repository-url>
cd evacu-mate
```

## Frontend Setup

### Initial Setup

1. Navigate to the frontend folder and create the React app:

```bash
cd frontend
npm create vite@latest . -- --template react
```

2. Install dependencies:

```bash
npm install
```

### Auth0 Integration

Install Auth0 React SDK:

```bash
npm install @auth0/auth0-react
```

### React Router

Install React Router for navigation:

```bash
npm install react-router-dom
```

### Run Frontend

Start the development server:

```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

## Backend Setup

### Virtual Environment Setup

1. Navigate to the backend folder:

```bash
cd ../backend
```

2. Create and activate a virtual environment:

**Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
```

**macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

### Install Dependencies

Install required packages:

```bash
pip install fastapi uvicorn
pip install -r app/requirements.txt
```

### Run Backend

Start the FastAPI server:

```bash
uvicorn app.main:app --reload --env-file .env
```

The backend will be available at `http://localhost:8000`

## MongoDB Setup

### Install MongoDB Driver

From the backend directory:

```bash
npm install mongodb
```

### Connection String

Your MongoDB connection string should follow this format:
```
mongodb+srv://<username>:<db_password>@cluster0.weokxqp.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
```

Replace `<username>` and `<db_password>` with your actual MongoDB Atlas credentials.

## Auth0 Setup

### Frontend Configuration

Create a `.env` file in the frontend folder with your Auth0 credentials:

```env
VITE_AUTH0_DOMAIN=dev-c3w8jffjhajnktc0.us.auth0.com
VITE_AUTH0_CLIENT_ID=S4aHj7wFVkS2xDUTVTxRXZd2hIbdXptP
```

## Environment Variables

### Frontend (.env in frontend folder)
```env
VITE_AUTH0_DOMAIN=your-auth0-domain
VITE_AUTH0_CLIENT_ID=your-auth0-client-id
```

### Backend (.env in backend folder)
```env
MONGO_URI=mongodb+srv://<username>:<password>@cluster0.weokxqp.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
MONGO_DB=your-database-name
GOOGLE_MAPS_API_KEY=your-google-maps-api-key
```

## Running the Application

### Start Backend
```bash
cd backend
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
uvicorn app.main:app --reload --env-file .env
```

### Start Frontend
```bash
cd frontend
npm run dev
```
