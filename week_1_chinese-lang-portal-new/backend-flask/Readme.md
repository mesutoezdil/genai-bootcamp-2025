# Database & Backend Setup Guide

This document details how to **initialize** and **seed** the database, manage cleanup, and run the backend API (Flask) for your application.

---

## 1. Database Initialization

### Step 1: Invoke DB Init

From the project root, run:

```bash
invoke init-db
```

**What this does**:
1. **Creates** the `words.db` SQLite3 database if it doesn’t already exist.
2. **Runs Migrations** located under the `seeds/` directory (or wherever your migration scripts are stored).
3. **Seeds Data** by importing sample or production data as specified in `lib/db.py`.

> **Note**: If you plan to add new seed files, ensure you **update** the logic in `lib/db.py` or your tasks to include them.

### Step 2: Verify Database

- Check for the new `words.db` file in your project directory.
- Optionally use a SQLite browser (e.g., [DB Browser for SQLite](https://sqlitebrowser.org/)) or `sqlite3 words.db` to confirm tables and records.

---

## 2. Clearing the Database

To entirely **wipe** the data, simply **delete** the `words.db` file:

```bash
rm words.db
```

**Result**:  
All existing schemas, tables, and data are removed. You can re-run `invoke init-db` to recreate everything from scratch.

> **Warning**: Deletion is permanent, so ensure you have backups or version control if this database is important.

---

## 3. Running the Backend API

Once the database is set up, start the **Flask** application with:

```bash
python app.py
```

### Expected Behavior

- The **Flask server** typically runs on port **5000** by default.  
- Open your browser at [http://localhost:5000](http://localhost:5000) (or use an API client like **Postman** or **cURL**) to test endpoints.

### Custom Configuration

- **Environment Variables**: You may have settings like `FLASK_ENV=development` or `DB_PATH=words.db`.  
- **Port Changes**: If needed, adjust `app.run(port=...)` in `app.py` or set environment variables.

