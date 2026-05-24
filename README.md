# Smart Visual Inspection System

[![OpenCV](https://img.shields.io/badge/OpenCV-5C7CFA?style=for-the-badge&logo=opencv&logoColor=white)](#tech-stack)
[![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)](#tech-stack)
[![TorchVision](https://img.shields.io/badge/TorchVision-8F5B00?style=for-the-badge)](#tech-stack)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](#tech-stack)
[![Celery](https://img.shields.io/badge/Celery-37814A?style=for-the-badge&logo=celery&logoColor=white)](#tech-stack)
[![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)](#tech-stack)
[![Docker Compose](https://img.shields.io/badge/Docker%20Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)](#quick-start)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](#requirements)

A production-ready backend-oriented platform for **visual inspection** with asynchronous CV inference, job tracking, and result delivery via REST API.

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [System Architecture](#system-architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Requirements](#requirements)
- [Configuration](#configuration)
- [Visualization Legend](#visualization-legend)
- [API Reference](#api-reference)
- [CV Pipeline Flow](#cv-pipeline-flow)
- [Demo Results](#demo-results)
- [Development Workflow](#development-workflow)
- [Testing & Quality](#testing--quality)
- [Deployment Notes](#deployment-notes)
- [Roadmap](#roadmap)

---

## Overview

**Smart Visual Inspection System** processes input images (or frames) through a computer vision pipeline and exposes:

1. **Secure API access** (registration/token-based auth).
2. **Asynchronous analysis jobs** (Celery + Redis queue).
3. **Job lifecycle tracking** (status/result retrieval).
4. **Inference result artifacts** (processed image endpoint).

The project is designed for scalable inspection scenarios such as:

- transport monitoring,
- people/animal detection,
- edge-camera assisted analytics,
- and defect/event detection workflows.

---

## Key Features

- **CV-first architecture** built around preprocessing → inference → postprocessing stages.
- **Async execution** for non-blocking API responses under heavy workloads.
- **Token-based authentication** for protected endpoints.
- **Model introspection endpoint** to expose available inference options.
- **Containerized runtime** with Docker Compose for reproducible setup.
- **Clear modular structure** for API, CV logic, DB layer, and background tasks.

---

## System Architecture

```text
Client
  └──> FastAPI REST API
          ├──> Auth & validation
          ├──> Job creation / querying
          └──> Redis broker
                  └──> Celery worker
                          └──> CV Pipeline
                                  ├── Preprocessing
                                  ├── Inference
                                  └── Postprocessing
                                        └── Persist / expose results
```

---

## Tech Stack

### Computer Vision
- **OpenCV** — image preprocessing and frame-level transformations.
- **PyTorch / TorchVision** — deep-learning based detection pipeline.

### Backend & Async Processing
- **FastAPI** — high-performance REST API.
- **Celery** — background task orchestration.
- **Redis** — broker/result backend and fast state exchange.

### Infrastructure
- **Docker + Docker Compose** — local orchestration and consistent environments.
- **Python 3.11+** — main runtime.

---

## Project Structure

```text
app/
  api/              # REST endpoints, dependencies, API versioning
  core/             # configuration, security, storage utilities
  cv/               # preprocessing, inference, postprocessing, pipeline
  db/               # session and ORM models
  schemas/          # Pydantic request/response contracts
  tasks/            # Celery background jobs
  main.py           # FastAPI app entrypoint

tests/
  test_api/         # API and auth tests
  test_cv/          # computer vision unit tests
```

---

## Quick Start

```bash
docker compose up --build
```

After startup:
- API: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`

---

## Requirements

- Docker 24+
- Docker Compose v2+

For local non-container runs (optional):
- Python 3.11+
- Redis

---

## Configuration

Main runtime configuration is centralized in `app/core/config.py`.
Typical settings include:

- application mode/environment,
- security/auth parameters,
- queue/broker connection settings,
- storage/result-related paths.

> Tip: keep environment-specific values in `.env` files and never commit secrets.

---

## Visualization Legend

Annotated output images use category-based bounding box colors:

- 🟩 **Green** — transport objects (e.g., car, motorcycle, bus, train, truck, boat)
- 🟥 **Red** — people
- 🟦 **Blue** — animals
- 🟨 **Yellow** — fallback for other detected classes

This makes mixed scenes easier to read and quickly separates the three primary inspection groups.

---

## API Reference

### Authentication
- `POST /api/v1/auth/register` — create a user account.
- `POST /api/v1/auth/token` — obtain access token.

### Analysis & Jobs
- `POST /api/v1/analyze` — submit an analysis job.
- `GET /api/v1/jobs/{job_id}` — get job status/details.
- `GET /api/v1/jobs/{job_id}/image` — download/view processed image.
- `GET /api/v1/jobs` — list jobs.
- `DELETE /api/v1/jobs/{job_id}` — remove a job.

### Models & Health
- `GET /api/v1/models` — list available CV models.
- `GET /health` — service health endpoint.

Interactive docs are available at `/docs`.

---

## CV Pipeline Flow

1. **Input acquisition** from API payload.
2. **Preprocessing** with OpenCV transformations.
3. **Inference** through configured PyTorch/TorchVision model.
4. **Postprocessing** (filtering, formatting, optional overlays).
5. **Result publication** through job endpoint and output artifact endpoint.

---

## Demo Results

Below are sample annotated outputs with bounding boxes:

![img_4.png](imgs/img_4.png)
![img_5.png](imgs/img_5.png)
![Demo result 1](imgs/img.png)
![Demo result 2](imgs/img_1.png)
![img_8.png](imgs/img_8.png)
![img_7.png](imgs/img_7.png)
![Demo result 4](imgs/img_2.png)
![Demo result 3](imgs/img_3.png)

---

## Development Workflow

Run app stack:
```bash
docker compose up --build
```

Stop stack:
```bash
docker compose down
```

---

## Testing & Quality

Run locally:

```bash
docker compose exec api python -m pytest --cov=app
docker compose exec api ruff check .
docker compose exec api black --check .
```

---
