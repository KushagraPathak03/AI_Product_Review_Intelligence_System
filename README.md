# 🚀 AI Product Review Intelligence System

**An AI-powered platform for collecting, analyzing, and summarizing electronic product reviews from multiple online sources using Web Scraping, Natural Language Processing (NLP), Large Language Models (LLMs), and Retrieval-Augmented Generation (RAG).**

---

![Python](https://img.shields.io/badge/Python-3.13-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red)
![Playwright](https://img.shields.io/badge/Playwright-Web%20Scraping-green)
![Status](https://img.shields.io/badge/Phase-3%20Completed-success)

---

# 📌 Overview

Purchasing an electronic product often requires reading hundreds or thousands of reviews across different websites. This project automates that process by collecting product information and reviews, intelligently matching products, storing the data in a structured database, and preparing it for AI-powered analysis.

The long-term goal is to build an intelligent platform capable of:

- Collecting reviews from multiple sources
- Understanding customer sentiment
- Summarizing thousands of reviews
- Comparing competing products
- Detecting fake reviews
- Answering user questions using Retrieval-Augmented Generation (RAG)

---

# ✨ Current Features

## Backend

- RESTful API using FastAPI
- SQLAlchemy ORM
- PostgreSQL Database
- Alembic Database Migrations
- Repository-Service Architecture
- Pydantic Validation

---

## Product Management

- Create Product
- Update Product
- Soft Delete Product
- Restore Product
- Product Search
- Duplicate Product Detection

---

## Review Management

- Create Review
- Update Review
- Search Reviews
- Duplicate Review Detection
- SHA-256 Hash Generation
- Review Statistics

---

## Amazon Product Scraper

### Product Search

- Search Amazon Products
- Extract Product Name
- Product Image
- Product URL
- Product Price
- Brand
- Category

---

### Product Detail Scraper

- Product Name
- Brand
- Category
- Selling Price
- MRP
- Discount
- Rating
- Review Count
- Availability
- Product Description
- Product Image

---

### Review Scraper

- Customer Reviews
- Review Title
- Review Text
- Reviewer Name
- Rating
- Review Date

---

# 🧠 Intelligent Product Matching (Phase 3)

One of the core challenges in review aggregation is correctly identifying the product requested by the user.

Instead of relying on simple keyword matching, this project implements a multi-stage intelligent matching pipeline.

### Electronic Product Validation

Rejects

- Empty queries
- Accessories
- Non-electronic products

Accepts

- Any electronic product from any brand

Examples

✅ HP OmniBook Ultra

✅ Lenovo Legion Pro 7

✅ Sony WH-1000XM6

✅ Canon EOS R50

✅ DJI Osmo Pocket 3

❌ Laptop Cover

❌ Samsung Charger

❌ Nike Shoes

---

### Product Normalization

Normalizes

- Case
- Spaces
- Special characters
- Marketing words
- Storage formatting

Example

Input

Apple iPhone 16 Pro (256 GB)

Normalized

apple iphone 16 pro 256gb

---

### Generic Product Parser

Automatically extracts

- Brand
- Product Family
- Model Number
- Storage
- Variant
- Product Category

Works for

- Smartphones
- Laptops
- Tablets
- Cameras
- TVs
- Monitors
- Earbuds
- Smartwatches
- Gaming Consoles

---

### Smart Product Matcher

Uses RapidFuzz similarity scoring combined with weighted matching.

Compares

- Brand
- Product Family
- Model Number
- Variant
- Storage
- Fuzzy Similarity

Returns the best matching Amazon product.

---

### Strict Product Matcher

Performs final verification before scraping.

Rejects

Galaxy S24 Ultra

when user requested

Galaxy S25 Ultra

Rejects

OnePlus 13R

when user requested

OnePlus 13

Ensures only the correct product is scraped.

---

### Automatic Category Detection

Automatically detects categories such as

- Smartphone
- Laptop
- Tablet
- Smartwatch
- Earbuds
- Camera
- Television
- Monitor
- Gaming Console

without relying on predefined brand lists.

---

# 🏗️ System Architecture

```text
                         User
                           │
                           ▼
                  FastAPI REST API
                           │
                           ▼
            Electronic Product Validator
                           │
                           ▼
                  Amazon Product Search
                           │
                           ▼
                 Product Result Filter
                           │
                           ▼
               Smart Product Matcher
                           │
                           ▼
               Strict Product Matcher
                           │
                           ▼
              Product Detail Scraper
                           │
                           ▼
              Automatic Category Detector
                           │
                           ▼
                    PostgreSQL Database
                           │
                           ▼
                  Customer Review Scraper
                           │
                           ▼
                  AI Processing (Phase 4)
                           │
                           ▼
                 Analytics Dashboard
```

---

# 🛠️ Technology Stack

| Category | Technology |
|----------|------------|
| Language | Python 3.13 |
| Backend | FastAPI |
| ORM | SQLAlchemy |
| Database | PostgreSQL |
| Migration | Alembic |
| Validation | Pydantic v2 |
| Web Scraping | Playwright, BeautifulSoup4, Requests |
| Product Matching | RapidFuzz |
| AI (Upcoming) | Hugging Face Transformers |
| Embeddings (Upcoming) | Sentence Transformers |
| Vector Database (Upcoming) | ChromaDB |
| LLM Framework (Upcoming) | LangChain |
| Dashboard (Upcoming) | NiceGUI |

---

# 📂 Repository Structure

```text
AI_Product_Review_Intelligence_System/
│
├── backend/
│   ├── alembic/
│   ├── app/
│   │   ├── common/
│   │   ├── core/
│   │   ├── database/
│   │   ├── product/
│   │   ├── review/
│   │   ├── scraper/
│   │   │   ├── amazon/
│   │   │   ├── matcher/
│   │   │   ├── scraper_service.py
│   │   │   ├── scraper_routes.py
│   │   │   ├── scraper_schema.py
│   │   │   └── scraper_dto.py
│   │   └── main.py
│   │
│   ├── tests/
│   ├── requirements.txt
│   └── README.md
│
├── frontend/        (Upcoming)
│
├── docs/            (Upcoming)
│
└── README.md
```
---

# ⚙️ Installation

## Prerequisites

Before setting up the project, ensure the following software is installed:

- Python 3.13+
- PostgreSQL 16+
- Git
- Playwright
- pip

---

## Clone the Repository

```bash
git clone https://github.com/KushagraPathak03/AI_Product_Review_Intelligence_System.git
```

Move to the backend directory.

```bash
cd AI_Product_Review_Intelligence_System/backend
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

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

## Install Playwright

```bash
playwright install
```

---

# 🔐 Environment Variables

Create a `.env` file inside the backend directory.

Example:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/AI_Product_Review_Intelligence_System

SECRET_KEY=your_secret_key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=60
```

> **Note:** Never commit your `.env` file to GitHub.

---

# 🗄️ Database Setup

## Create Database

Open PostgreSQL and create a new database.

```sql
CREATE DATABASE AI_Product_Review_Intelligence_System;
```

---

## Apply Database Migrations

```bash
alembic upgrade head
```

---

## Create New Migration

```bash
alembic revision --autogenerate -m "Migration Name"
```

---

# ▶️ Running the Application

Start the FastAPI development server.

```bash
uvicorn app.main:app --reload
```

The backend will start on:

```
http://127.0.0.1:8000
```

---

# 📖 API Documentation

FastAPI automatically generates interactive API documentation.

### Swagger UI

```
http://127.0.0.1:8000/docs
```

---

### ReDoc

```
http://127.0.0.1:8000/redoc
```

---

# 📡 Current API Modules

## Product APIs

- Create Product
- Get Product
- Update Product
- Soft Delete Product
- Restore Product
- Search Products

---

## Review APIs

- Create Review
- Get Reviews
- Update Review
- Search Reviews

---

## Amazon Scraper APIs

- Search Product
- Scrape Product Details
- Scrape Customer Reviews

---

# 🔄 Scraping Workflow

The Amazon scraping pipeline follows the workflow below.

```text
User Product Query
        │
        ▼
Electronic Product Validation
        │
        ▼
Amazon Product Search
        │
        ▼
Remove Accessories
        │
        ▼
Smart Product Matching
        │
        ▼
Strict Product Verification
        │
        ▼
Scrape Product Details
        │
        ▼
Automatic Category Detection
        │
        ▼
Save Product
        │
        ▼
Scrape Customer Reviews
        │
        ▼
Save Reviews
        │
        ▼
API Response
```

---

# 🧪 Testing

Run all tests.

```bash
pytest
```

Run a specific test.

```bash
pytest tests/test_strict_matcher.py
```

---

# 🛠️ Development Commands

### Start Backend

```bash
uvicorn app.main:app --reload
```

---

### Create Migration

```bash
alembic revision --autogenerate -m "Migration Name"
```

---

### Apply Migration

```bash
alembic upgrade head
```

---

### Downgrade Migration

```bash
alembic downgrade -1
```

---

### Install New Dependency

```bash
pip install package_name
pip freeze > requirements.txt
```

---

# 📁 Database Schema

Current core tables:

## products

Stores:

- Product Information
- Price
- Rating
- Availability
- Product URL
- Category
- Product Image

---

## reviews

Stores:

- Customer Reviews
- Rating
- Review Text
- Review Date
- Review Source
- SHA-256 Hash

---

# 🔒 Duplicate Detection

The backend prevents duplicate entries using:

### Products

- Product URL

### Reviews

- SHA-256 Hash

This ensures the database stores unique products and reviews even when the scraper is executed multiple times.

---

# 📊 Current Project Status

The project is being developed in multiple phases.

| Phase | Description | Status |
|--------|-------------|--------|
| Phase 1 | Backend Foundation (FastAPI, PostgreSQL, SQLAlchemy, Alembic) | ✅ Completed |
| Phase 2 | Amazon Product & Review Scraper | ✅ Completed |
| Phase 3 | Intelligent Product Matching System | ✅ Completed |
| Phase 4 | AI Review Intelligence | 🚧 In Progress |
| Phase 5 | Analytics Dashboard | ⏳ Planned |
| Phase 6 | Deployment & Scaling | ⏳ Planned |

---

# ✅ Completed Features

### Backend

- FastAPI REST APIs
- SQLAlchemy ORM
- PostgreSQL Integration
- Alembic Migrations
- Repository Pattern
- Service Layer
- Pydantic Validation

---

### Product Module

- Product CRUD
- Product Search
- Product Update
- Soft Delete
- Restore Product
- Duplicate Detection

---

### Review Module

- Review CRUD
- SHA-256 Duplicate Detection
- Review Statistics
- Review Storage

---

### Amazon Scraper

- Product Search
- Product Details Scraper
- Customer Review Scraper
- Product Images
- Ratings
- Prices
- Availability

---

### Intelligent Product Matching

- Generic Electronic Validator
- Generic Product Parser
- Product Normalizer
- Smart Product Matcher
- Strict Product Matcher
- Automatic Category Detection
- Accessory Removal
- Generic Brand Support

---

# 🚧 Upcoming Features

## Phase 4 — AI Review Intelligence

- Sentiment Analysis
- Aspect-Based Sentiment Analysis
- AI Product Summary
- AI Product Recommendation
- Competitor Comparison
- Product Pros & Cons Extraction

---

## Phase 5 — Analytics Dashboard

- NiceGUI Dashboard
- Sentiment Charts
- Rating Distribution
- Review Timeline
- Aspect Analysis
- Product Comparison Dashboard

---

## Phase 6 — AI Assistant

- RAG-based Product Chatbot
- ChromaDB Vector Database
- Semantic Search
- Natural Language Product Queries
- Buying Recommendation Assistant

---

## Future Scrapers

Additional review sources will be integrated.

- Amazon ✅
- Flipkart
- Reddit
- YouTube
- Best Buy
- Walmart
- GSMArena

---

# 🎯 Project Goals

This project aims to solve the following real-world problems:

- Reading thousands of product reviews manually
- Comparing products across platforms
- Identifying fake reviews
- Understanding customer sentiment
- Extracting important product insights
- Helping users make informed purchasing decisions

---

# 💡 Example Use Cases

### Product Search

Search any electronic product.

Example:

```
iPhone 16 Pro
Galaxy S25 Ultra
HP OmniBook Ultra
Sony WH-1000XM6
Canon EOS R50
```

---

### Review Collection

Collect customer reviews from multiple online platforms.

---

### AI Review Summary

Generate concise summaries from thousands of customer reviews.

---

### Product Comparison

Compare products using AI-generated insights.

Example:

```
iPhone 16 Pro

VS

Galaxy S25 Ultra
```

---

### Product Recommendation

Ask questions like:

```
Which laptop is best for programming?

Which phone has the best battery?

Is Galaxy Watch 8 worth buying?

Should I buy iPhone 16 Pro?
```

The future RAG assistant will answer these using real customer reviews.

---

# 📈 Project Roadmap

```text
Backend APIs
      │
      ▼
Amazon Scraper
      │
      ▼
Product Matching
      │
      ▼
AI Sentiment Analysis
      │
      ▼
AI Product Summary
      │
      ▼
RAG Chatbot
      │
      ▼
Analytics Dashboard
      │
      ▼
Cloud Deployment
```

---

# 📸 Screenshots

Screenshots and GIF demonstrations will be added as development progresses.

Future additions include:

- Swagger Documentation
- Dashboard
- Product Search
- AI Review Summary
- Sentiment Charts
- Product Comparison
- RAG Chatbot

---

# 🤝 Contributing

Contributions are welcome.

If you would like to improve this project:

1. Fork the repository.
2. Create a new feature branch.
3. Commit your changes.
4. Open a Pull Request.

---

# 📚 Learning Objectives

This project demonstrates:

- Backend Development
- REST API Design
- Database Design
- Web Scraping
- Product Matching Algorithms
- Natural Language Processing
- Large Language Models
- Retrieval-Augmented Generation
- AI Application Development
- Software Architecture

---

# 🛡️ License

This project is developed for educational, research, and portfolio purposes.

---

# 👨‍💻 Author

**Kushagra Pathak**

AI & Machine Learning Engineer

GitHub:
https://github.com/KushagraPathak03

---

# ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.

It helps others discover the project and motivates future development.

---

## 🚀 Next Milestone

**Phase 4 – AI Review Intelligence**

The next phase introduces AI-powered capabilities, including:

- Sentiment Analysis
- Aspect-Based Sentiment Analysis
- AI Product Summarization
- Competitor Comparison
- Product Recommendation Engine
- RAG-based Product Question Answering

Stay tuned for more updates!