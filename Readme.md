# 🚀 CP Analyzer Backend

**CP Analyzer** is a robust backend service designed to aggregate, analyze, and track competitive programming profiles. Built with **FastAPI**, it allows users to sync their performance statistics, contest histories, and activity streaks from platforms like **LeetCode** and **Codeforces** into a centralized database.

---

## ✨ Key Features

* **🔐 Secure Authentication**: JWT-based user authentication (signup, login, and profile management) using `pwdlib` for secure password hashing.
* **📊 LeetCode Integration**: Fetches and stores solved problem counts (Easy/Medium/Hard), contest ratings, global rankings, and calculates daily submission streaks.
* **🏆 Codeforces Integration**: Connects directly to the official Codeforces API to track user ratings, ranks, contest participation, and active coding streaks based on accepted submission history.
* **💾 Database Management**: Utilizes **SQLModel** (built on top of SQLAlchemy) for ORM modeling and **Alembic** for seamless database migrations.
* **⚡ High Performance**: Fully asynchronous routing and external HTTP requests using `httpx` and `asyncio.gather` for parallel API calls.
* **🔄 Smart Sync**: On-demand sync with deduplication — contest history never duplicates across syncs. Codeforces sync uses early-exit optimization via last synced submission ID.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| Database ORM | SQLModel / SQLAlchemy |
| Migrations | Alembic |
| Database | PostgreSQL (Docker) |
| Authentication | OAuth2 + JWT (PyJWT) |
| HTTP Client | httpx (async) |
| Password Hashing | pwdlib |
| Config Management | pydantic-settings |

---

## 📂 Project Architecture

```text
Cp_analyzer/backend/
├── main.py                  # FastAPI application instance & lifespan events
├── auth.py                  # JWT creation, decoding, and user auth logic
├── config.py                # Environment variable bindings
├── database.py              # SQLModel engine and session dependency
├── dependencies.py          # Reusable FastAPI dependencies (token decoder, get_current_user)
├── utils.py                 # Password hashing utilities
├── alembic.ini              # Alembic configuration
│
├── alembic/                 # Database migrations folder
│   ├── env.py               # Alembic environment setup with dynamic DB URL from .env
│   └── versions/            # Version history of database schema changes
│
├── models/                  # Database schema definitions (SQLModel table=True)
│   ├── users.py             # User model with UUID primary key
│   ├── leetcodeStats.py     # LeetCode profile, contest, and streak schemas
│   └── codeforcesStats.py   # Codeforces profile, contest, and streak schemas
│
├── routes/                  # API Routers (thin layer — calls services only)
│   ├── userRoutes.py        # /signup, /login, /profile endpoints
│   ├── leetcodeRoutes.py    # LeetCode sync and fetch endpoints
│   └── codeforcesRoutes.py  # Codeforces sync and fetch endpoints
│
└── services/                # Business logic and external API integration
    ├── leetcode.py          # LeetCode API requests, streak calculation, sync logic
    └── codeforces.py        # Codeforces official API requests, streak calculation, sync logic
```

---

## 📡 Core API Endpoints

All endpoints are prefixed with `/cp_analyzer`. Protected endpoints require a Bearer JWT token in the Authorization header.

### 👤 User Management
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | `/cp_analyzer/signup` | Register a new user | No |
| POST | `/cp_analyzer/login` | Authenticate and receive JWT token | No |
| GET | `/cp_analyzer/profile` | Fetch authenticated user's profile | Yes |
| PATCH | `/cp_analyzer/profile` | Update username, LC handle, CF handle | Yes |

### 🟢 LeetCode
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | `/cp_analyzer/profile/leetcode/sync` | Sync LeetCode profile stats and streaks | Yes |
| GET | `/cp_analyzer/profile/leetcode` | Retrieve saved LeetCode profile | Yes |
| POST | `/cp_analyzer/profile/leetcode/contest/sync` | Sync missing contest history | Yes |
| GET | `/cp_analyzer/profile/leetcode/contest` | Retrieve saved contest history | Yes |

### 🔵 Codeforces
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | `/cp_analyzer/profile/codeforces/sync` | Sync CF rating, rank, and streaks | Yes |
| GET | `/cp_analyzer/profile/codeforces` | Retrieve saved Codeforces profile | Yes |
| POST | `/cp_analyzer/profile/codeforces/contest/sync` | Sync recent CF contests | Yes |
| GET | `/cp_analyzer/profile/codeforces/contest` | Retrieve saved CF contest history | Yes |

---

## 🐳 Database Setup with Docker

```bash
# Create a persistent volume
docker volume create postgres-data

# Run PostgreSQL container
docker run --name cp-postgres \
  -e POSTGRES_PASSWORD=yourpassword \
  -e POSTGRES_USER=youruser \
  -e POSTGRES_DB=cp_analyzer \
  -p 5432:5432 \
  -v postgres-data:/var/lib/postgresql/data \
  -d postgres:16
```

---

## ⚙️ Local Development Setup

### 1. Prerequisites
* Python 3.10+
* Docker (for PostgreSQL)
* Local LeetCode API wrapper running on `http://localhost:3000` (required for LeetCode sync)

### 2. Clone the Repository
```bash
git clone https://github.com/batcoder-1/Cp_analyzer.git
cd Cp_analyzer/backend
```

### 3. Create and Activate Virtual Environment
```bash
python -m venv venv

# macOS/Linux
source venv/bin/activate

# Windows
.\venv\Scripts\activate
```

### 4. Install Dependencies
```bash
pip install fastapi uvicorn sqlmodel sqlalchemy alembic PyJWT httpx python-dotenv pydantic-settings pwdlib
```

### 5. Configure Environment Variables
Create a `.env` file in the `backend/` directory:
```env
DATABASE_URL=postgresql://youruser:yourpassword@localhost:5432/cp_analyzer
SECRET_KEY=your_super_secret_jwt_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRES_MINUTES=1440
```

### 6. Run Database Migrations
```bash
alembic upgrade head
```

### 7. Start the Application
```bash
uvicorn main:app --reload
```

Access the interactive API docs at: **http://127.0.0.1:8000/docs**

---

## 🏗️ Key Architectural Decisions

**On-demand sync over scheduled background jobs** — Celery/Redis adds significant infrastructure complexity. For V1, users trigger sync manually. This is an explicit tradeoff documented in the roadmap.

**SQLModel over raw SQLAlchemy** — Eliminates duplication between Pydantic schemas and SQLAlchemy models. Single class definition serves both API validation and database representation.

**UUID primary keys for users** — Prevents sequential ID enumeration attacks on user-facing endpoints.

**Alembic for migrations** — `SQLModel.metadata.create_all()` only creates missing tables, never modifies existing ones. Alembic handles schema evolution safely without dropping data.

**Parallel API calls** — LeetCode sync uses `asyncio.gather()` to fetch profile and contest data simultaneously instead of sequentially, reducing sync latency.

**Batch commits** — All database writes within a single sync operation are committed in one transaction, not per-row. Prevents SQLAlchemy session identity map expiry issues during bulk inserts.

---

## ⚠️ Known Limitations & Roadmap

### V1 Limitations
- **Topic-wise breakdown**: LeetCode's public API does not expose per-topic solved counts without session cookie authentication. Investigated GraphQL endpoint — requires user session. Deferred to V2.
- **Streak accuracy**: Streaks are computed within the available submission history window (~1 year for LeetCode calendar, ~1 year paginated for Codeforces). Cross-year continuity requires scheduled background sync to maintain a permanent local record.
- **On-demand sync only**: Data freshness depends on manual user-triggered sync. Stale data is possible if user doesn't sync regularly.
- **LeetCode API dependency**: Relies on a third-party LeetCode API wrapper (`alfa-leetcode-api`) running locally on port 3000. Subject to upstream availability.

### V2 Planned
- [ ] Scheduled sync using **Celery + Redis** (background jobs, no manual trigger needed)
- [ ] Topic-wise breakdown via **LeetCode GraphQL API** investigation with session auth
- [ ] Incremental sync optimization — store `last_synced_submission_id` for early exit on CF sync
- [ ] Deployment with Docker Compose (FastAPI + PostgreSQL as services)
- [ ] Frontend dashboard (React) for visual analytics

---

## 📄 License

MIT License — feel free to use, modify, and distribute.