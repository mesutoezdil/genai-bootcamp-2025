# Agential Workflow System

This project implements an agential workflow system that demonstrates the Think → Act → Observe → Refine cycle. It provides a FastAPI web application that manages tasks and executes them using various tools.

## Features

- Task management with priorities and status tracking
- Multiple tool integrations (web search, calculator, weather, text processing)
- RESTful API for task creation and execution
- Complete workflow cycle implementation
- Error handling and task refinement

## Project Structure

```
week_3_agenticWorkflow/
├── agent/
│   ├── __init__.py
│   ├── core.py        # Core agent implementation
│   └── models.py      # Data models
├── main.py           # FastAPI application
├── tools.py          # Tool implementations
└── requirements.txt  # Project dependencies
```

## Installation

1. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

Start the FastAPI server:
```bash
python main.py
```

The server will start at http://localhost:8000

## API Endpoints

- `POST /tasks` - Create a new task
- `GET /tasks` - List all tasks
- `GET /tasks/{task_id}` - Get a specific task
- `POST /tasks/{task_id}/execute` - Execute a task
- `GET /tools` - List available tools

## Example Usage

1. Create a task:
```bash
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Analyze Text", "description": "Analyze the given text for metrics", "priority": "high"}'
```

2. Execute a task:
```bash
curl -X POST http://localhost:8000/tasks/{task_id}/execute
```

3. List tasks:
```bash
curl http://localhost:8000/tasks
```

## Available Tools

1. **WebSearchTool**
   - Simulates web searches

2. **CalculatorTool**
   - Performs mathematical calculations

3. **WeatherTool**
   - Provides weather information

4. **TextProcessingTool**
   - Analyzes and processes text

## Development

The system follows a modular design:

1. **Agent Core (`agent/core.py`)**
   - Implements the Think → Act → Observe → Refine cycle
   - Manages tasks and tools

2. **Models (`agent/models.py`)**
   - Defines data structures for tasks and workflow results

3. **Tools (`tools.py`)**
   - Implements various tools the agent can use

4. **API (`main.py`)**
   - Provides RESTful endpoints for interaction

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License
