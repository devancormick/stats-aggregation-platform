# Stats Aggregation Platform

A centralized stats platform that scrapes data from multiple league management platforms and presents it in a clean, mobile-responsive website.

## Features

- Automated web scraping from multiple league management platforms
- Database storage for teams, players, games, and statistics
- Clean, fast-loading website with homepage, league pages, and team pages
- Daily automated data updates
- Mobile-responsive design
- Scalable architecture (starting with 3-5 leagues, expanding to 50+)

## Tech Stack

### Backend
- Python 3.9+
- FastAPI
- PostgreSQL
- BeautifulSoup4 / Scrapy
- Celery (for scheduled tasks)

### Frontend
- Next.js 14
- React
- Tailwind CSS
- TypeScript

## Project Structure

```
stats-aggregation-platform/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── models/
│   │   ├── scrapers/
│   │   └── utils/
│   ├── migrations/
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   ├── components/
│   │   └── lib/
│   └── package.json
├── scripts/
└── docs/
```

## Setup

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## Development

### Running Scrapers

```bash
python backend/app/scrapers/main.py
```

### Running API

```bash
cd backend
uvicorn app.main:app --reload
```

### Running Frontend

```bash
cd frontend
npm run dev
```

## License

MIT
