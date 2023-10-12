# TagMedX: Open-Source Medical Image Annotation 🏥

TagMedX is an open-source web app built with FastAPI, Next.js, and MySQL, designed for medical image tagging – both classification and detection. It's a tool for healthcare professionals, such as doctors and medical experts, to annotate medical images remotely for AI systems. 

## Dependencies
- Database -  mysql:8.1.0
- Database Admin Panel - phpmyadmin:5.2.1
- Backend (FastAPI) - python:3.8 - (additional dependencies in ./backend/requirements.txt)
- Frontend (Next.js + TS) -  node:20 - (additional dependencies in ./frontend/package.json)

## Backend

### Project structure


```
├── assets_readme             <- Images, diagrams for Readme.md
├── backend                   <- FastAPI backend
│   ├── features              <- Domain specific features
|   |   ├── examination       <- Sample examination related features
|   |   ├── groups            <- Group related features
|   |   ├── tasks             <- Tasks related features
|   |   ├── users             <- Users related features
|   |   |   ├── controllers   <- Router and endpoints /users /users/id
|   |   |   ├── schemas       <- Pydantic schemas for response
|   |   |   ├── services      <- Layer talking to Repositories
│   ├── models                <- SQLAlchemy data models
│   ├── repositories          <- SQLAlchemy queries
│   ├── utilities             <- Utilities like database connector or session
│   ├── requirements.txt      <- Packages to install
│   ├── Dockerfile            <- Dockerfile for Docker image
```

<br>
