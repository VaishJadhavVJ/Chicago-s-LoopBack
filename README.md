# LoopBack — AI for Safer, Smarter City Response

Built in 24 hours at **DemonHacks 2026** (DePaul University) by a team of 6.

LoopBack is a civic-tech platform that turns everyday city frustrations — ghost buses, broken streetlights, dangerous potholes — into structured, prioritized action items routed directly to the right city department.

## The Problem

Chicago receives millions of complaints every year. Most go nowhere. There's no accountability, no transparency, and no feedback loop between citizens and the city.

## How It Works

1. **Report** — Open the app, describe your issue in plain English. Location captured, report timestamped. Takes under 10 seconds.
2. **AI Triage** — Our LLM engine classifies the category, scores severity (1–5), and writes a professional complaint draft automatically.
3. **Deduplication** — Reports within the same area are grouped into a single task using geohash bucketing. One pin on the map = many voices.
4. **Department Routing** — Each task is routed to the responsible department (CTA Operations, City 311, Community Security) with a prioritized action queue.
5. **Safe Routes** — Plan your commute and see which routes have active issues. AI flags routes as green, yellow, or red.
6. **Gamification** — Earn XP for reporting, build streaks, climb the leaderboard. Civic engagement, gamified.

## Architecture

```
User (Mobile/Browser)
    │
    ▼
Clerk (Auth)
    │
    ▼
React + Vite + TypeScript (Frontend)
    │
    │  POST /reports
    ▼
FastAPI (Backend on Render)
    ├── geo.py        → Geohash computation
    ├── services.py   → Task dedup + severity scoring
    ├── llm.py        → LLM triage (severity, dept, complaint draft)
    ├── maps.py       → Mapbox route recommendations
    │
    ▼
Supabase PostgreSQL (Database)
    ├── users          → Profiles, XP, streaks, levels
    ├── reports        → Raw user submissions
    ├── tasks          → Deduplicated issue buckets
    ├── departments    → CTA_OPS, CITY_311, SECURITY
    ├── user_actions   → XP audit log
    ├── dept_workers   → Department personnel
    └── assigned_tasks → Worker-to-task assignments
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React, Vite, TypeScript |
| Auth | Clerk |
| Backend | Python, FastAPI |
| Database | PostgreSQL (Supabase) |
| ORM | SQLAlchemy |
| AI/LLM | OpenAI (GPT-4o-mini) |
| Maps | Mapbox API, Google Directions API |
| Deployment | Vercel (frontend), Render (backend) |
| Design | Figma, Lucidchart |

## Key Features

**LLM-Powered Triage** — Every report is processed by an AI that reads category, location, crowd signal, and sample reports to assign severity, route to the correct department, and generate a ready-to-send complaint draft.

**Geohash Deduplication** — Reports within ~150m of each other in the same category are automatically grouped into one task. A hundred complaints about the same pothole become one loud signal, not a hundred tickets.

**Severity Scoring** — Weighted formula: 65% average user priority + 35% crowd size. The more people report, the higher the severity. LLM can adjust by ±1 based on context.

**Safe Route Planning** — Input your start and end points. The system pulls routes from Mapbox, cross-references them with active issues, and flags each route as GREEN (safe), YELLOW (caution), or RED (avoid).

**Gamification** — XP system rewards civic participation. 10 XP for reporting, 25 XP for submitted complaints, 50 XP for streak bonuses. Leaderboard drives engagement.

## Database Schema

```
users (email PK)
  ├── reports (user_id FK → users)
  │     └── tasks (task_id FK ← reports)
  │           └── departments (assigned_dept_id FK ← tasks)
  │                 └── dept_workers (dept_id FK ← departments)
  │                       └── assigned_tasks (worker_id FK ← dept_workers)
  └── user_actions (user_id FK → users)
```

7 tables, fully normalized, with foreign keys, indexes, and seed data covering 30 Chicago neighborhoods.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/reports` | Submit a new report (triggers full AI pipeline) |
| GET | `/departments/{dept_id}/tasks` | Get prioritized task queue for a department |
| POST | `/routes/recommend` | Get safe route recommendation between two points |

## Running Locally

```bash
# Clone
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd chicago-loopback

# Backend
cd src/loopback
pip install -r requirements.txt
cp .env.example .env  # Add your keys
uvicorn main:app --reload

# Frontend
cd ../..
npm install
npm run dev
```

### Environment Variables

```
DATABASE_URL=postgresql+psycopg2://...    # Supabase connection string
OPENAI_API_KEY=sk-...                     # For LLM triage
MAPBOX_TOKEN=pk-...                       # For route recommendations
```

## Team

Built by 6 Masters CS students at DePaul University:

- **Frontend** — Rohan Singh, Meghana Rabba
- **Backend** — Vikas Ravikumar Karjigi, Sanath Manjunath
- **Database** — Vaishnavi Jadhav, Sriniwas

## Hackathon Result

Built and fully deployed end-to-end in 24 hours at DemonHacks 2026. Judges noted it was the only project with everything working and deployed. The project was in discussion for winning but teams with more theme-specific concepts were prioritized.

## License

MIT