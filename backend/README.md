# AI Product Review Intelligence System

An AI-powered platform for collecting, analyzing, and summarizing electronic product reviews from multiple online sources using web scraping, natural language processing, and large language models.

**Backend Service** built with FastAPI, PostgreSQL, SQLAlchemy, Playwright, and AI-powered review intelligence.

---

# Project Overview

The backend provides APIs and services for:

- Product Management
- Review Management
- Duplicate Review Detection
- Amazon Product Search
- Amazon Product Detail Scraping
- Review Collection
- AI Sentiment Analysis (Upcoming)
- AI Review Summarization (Upcoming)
- Fake Review Detection (Upcoming)
- RAG-based Product Q&A (Upcoming)

---

# Tech Stack

## Backend

- FastAPI
- Python 3.13
- SQLAlchemy 2.0
- Pydantic v2

## Database

- PostgreSQL
- Alembic

## Web Scraping

- Playwright
- BeautifulSoup4
- Requests

## Supported Sources

- Amazon (Implemented)
- Flipkart (Planned)
- Reddit (Planned)
- YouTube (Planned)

## AI (Upcoming)

- Hugging Face Transformers
- Sentence Transformers
- ChromaDB
- LangChain

---

# Features

## Product Module

- Create Product
- Update Product
- Delete Product (Soft Delete)
- Restore Product
- Search Products
- Filter Products
- Duplicate Product Detection

---

## Review Module

- Create Review
- Update Review
- Delete Review
- Search Reviews
- Filter Reviews
- Average Rating
- Review Count
- Duplicate Review Detection (SHA-256)

---

## Amazon Scraper

### Product Search

- Search products by keyword
- Parse Amazon search results
- Canonical Amazon product URLs
- Brand detection
- Category detection
- Product image extraction

### Product Detail

- Product title
- Brand
- Category
- Selling price
- MRP
- Discount percentage
- Overall rating
- Review count
- Stock availability
- Product description
- Main product image

### Current Status

- Amazon Search Scraper ✅
- Product Detail Scraper ✅
- Review Scraper 🚧 In Progress

## Database

- PostgreSQL Integration
- Alembic Migrations
- Repository Pattern
- Service Layer
- Clean Architecture

---

# Project Structure

```
backend/
│
├── alembic/
│   └── versions/
│
├── app/
│   ├── common/
│   ├── core
│   ├── database/
│   ├── product/
│   ├── review/
│   ├── scraper/
│   ├── amazon/
│   │   ├── amazon_constants.py
│   │   ├── amazon_parser.py
│   │   ├── amazon_scraper.py
│   │   └── amazon_utils.py
│   ├── base_scraper.py
│   ├── scraper_dto.py
│   ├── scraper_routes.py
│   ├── scraper_schema.py
│   └── scraper_service.py
│
└── main.py
├── requirements.txt
├── alembic.ini
└── README.md
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/KushagraPathak03/AI_Product_Review_Intelligence_System.git
```

Move to backend directory

```bash
cd AI_Product_Review_Intelligence_System/backend
```

---

## Create Virtual Environment

Windows

```bash
python -m venv venv
venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file.

Example

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/AI_Product_Review_Intelligence_System
```

---

# Database Migration

```bash
alembic upgrade head
```

---

# Run Application

```bash
uvicorn app.main:app --reload
```

Application

```
http://127.0.0.1:8000
```

Swagger

```
http://127.0.0.1:8000/docs
```

ReDoc

```
http://127.0.0.1:8000/redoc
```

---

# Development Commands

Create Migration

```bash
alembic revision --autogenerate -m "Migration Name"
```

Apply Migration

```bash
alembic upgrade head
```

Run Server

```bash
uvicorn app.main:app --reload
```

---

# Current Progress

| Module | Status |
|---------|--------|
| Product Management | ✅ Completed |
| Review Management | ✅ Completed |
| Duplicate Detection | ✅ Completed |
| SHA-256 Review Hashing | ✅ Completed |
| PostgreSQL Integration | ✅ Completed |
| Alembic Migration | ✅ Completed |
| Repository Pattern | ✅ Completed |
| Playwright Integration | ✅ Completed |
| Amazon Product Search | ✅ Completed |
| Amazon Product Parser | ✅ Completed |
| Amazon Product Detail Scraper | ✅ Completed |
| Amazon Review Scraper | 🚧 In Progress |
| AI Sentiment Analysis | ⏳ Planned |
| Review Summarization | ⏳ Planned |
| Fake Review Detection | ⏳ Planned |
| Vector Database | ⏳ Planned |
| RAG Chatbot | ⏳ Planned |
| Dashboard | ⏳ Planned |
| Docker Deployment | ⏳ Planned |

---

# Architecture

```
                 FastAPI
                    │
                    ▼
                 API Routes
                    │
                    ▼
                 Services
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
    Repositories         Web Scrapers
          │                   │
          ▼                   ▼
     PostgreSQL         Amazon / Flipkart
          │
          ▼
     AI Processing (Upcoming)
          │
          ▼
 ChromaDB + LangChain (Upcoming)

```

---

# Future Roadmap

- Amazon Review Scraper
- Flipkart Product & Review Scraper
- Reddit Review Scraper
- YouTube Review Analyzer
- Product Comparison Engine
- AI Sentiment Analysis
- AI Review Summarization
- Fake Review Detection
- ChromaDB Vector Database
- LangChain RAG Chatbot
- NiceGUI Analytics Dashboard
- Docker Deployment
- CI/CD Pipeline
- AWS Deployment

---

# Author

**Kushagra Pathak**

GitHub:
https://github.com/KushagraPathak03

---

# License

This project is developed for educational, research, and portfolio purposes.