# Go Server – Run & Test Instructions

This guide covers how to **run** the Go server, **test** the application code, and handle **database initialization** and **seeding** via **Mage** commands. We also include instructions for terminating any processes that might be holding onto the default port.

---

## 1. Running the Go Server

To launch the server using the default settings:

```sh
go run cmd/server/main.go
```

- **Default Port**: 8081 (or configured in the code/environment variables).
- **Key Files**: 
  - `cmd/server/main.go` – the entry point for your Go application.
- **Runtime Environment**: 
  - Ensure any necessary environment variables (e.g., `DB_PATH`) are set before running.

---

## 2. Testing the Code

### 2.1 Using a Test Database

When running integration or acceptance tests, we recommend pointing the app to a dedicated **test database** to avoid overwriting real data:

```sh
DB_PATH=./words.test.db go run cmd/server/main.go
```

- **`DB_PATH`**: Points the application to `words.test.db` (or another test file) instead of the production DB.
- **Tip**: Ensure your test DB schema and test data are up-to-date or seeded before launching.

### 2.2 Running RSpec Tests

If you’re using **RSpec** (perhaps for integration tests in a Ruby environment) to verify the API endpoints:

1. **Single Spec**:
   ```sh
   rspec spec/api/words_spec.rb
   ```

2. **All Specs**:
   ```sh
   rspec spec/api/*
   ```
   
- **Continuous Integration**: In a CI pipeline, you can automate these commands to run after spinning up the Go server with the test database environment.

---

## 3. Killing the Server Process

If you need to free up port 8081 (or whichever port you use) from a previously running server, you can forcefully stop the process:

```sh
lsof -ti:8081 | xargs kill -9
```

- **Explanation**: 
  - `lsof -ti:8081` finds the process ID (PID) listening on port 8081.
  - `xargs kill -9` terminates that PID.
- **Warning**: Using `-9` (SIGKILL) forcefully stops the process without cleanup. Use with caution.

---

## 4. Mage Commands

We use [**Mage**](https://magefile.org/) as a task runner for common operations like database initialization, migrations, and seeding. Below are some typical commands:

1. **Initialize Test Database**  
   ```sh
   go run github.com/magefile/mage@latest testdb
   ```
   - Sets up or prepares a testing database schema.

2. **Initialize Production Database**  
   ```sh
   go run github.com/magefile/mage@latest dbinit
   ```
   - Creates the main `words.db` (or config-specific DB) with the necessary tables.

3. **Seed the Database**  
   ```sh
   go run github.com/magefile/mage@latest seed
   ```
   - Inserts initial data (e.g., sample vocabulary, user info) for use in demos or local testing.

> **Note**: These Mage targets (`testdb`, `dbinit`, `seed`) may vary depending on how your `magefile.go` is organized. Check your `magefile.go` or project README for specifics on optional arguments or environment variables.

---

## 5. Additional Recommendations

- **Configuration Management**: 
  - Store environment variables (e.g., `DB_PATH`, `PORT`) in `.env` files or use a dedicated config library to easily switch between dev, test, and production.
- **Automated Scripts**:
  - Combine these steps in a shell script or Makefile for one-command local setups (`make up` or `./setup.sh`).
- **CI/CD Integration**:
  - In a continuous integration setup, ensure your pipeline sequentially 1) initializes the test DB, 2) runs `go run ...` or `mage testdb`, and 3) executes RSpec tests.
