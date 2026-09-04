# RL-Envi-CodeFix

A general-purpose reinforcement learning environment for training and evaluating LLM coding agents on code-fixing tasks.

The agent receives buggy code, inspects the task description and source files, uses tools to modify the code, and runs the tests inside an isolated Docker sandbox. The environment assigns a reward based on the test result.

## Overview

- **Environment ID:** `RLVR-CodeAgent`
- **Type:** Multi-turn tool-use coding environment
- **Purpose:** Evaluate LLM coding agents on autonomous bug fixing
- **Model API:** OpenAI-compatible API (tested with OpenRouter)
- **Sandbox:** Docker
- **Test runner:** Pytest
- **Reward:** `1.0` when all tests pass, otherwise `0.0`

## How It Works

```text
task/README.md + main.py + tests
              ↓
          LLM Agent
              ↓
     read_file / write_file
              ↓
          run_tests
              ↓
        Docker Sandbox
              ↓
            Pytest
              ↓
       Pass → Reward 1.0
       Fail → Reward 0.0
```

The agent must inspect the code, identify the bug, modify the source, and verify its solution through execution.

## Task Format

Each task lives in `task/`:

```text
task/
├── main.py
├── test_main.py
└── README.md
```

### `main.py`

Contains the intentionally buggy implementation.

### `README.md`

Describes the expected behavior and requirements of the task.

Example:

```md
# Code Fix Task

Fix the bug in `main.py`.

The function should return the correct result for
the specified inputs.

All tests must pass.
```

The task can be any programming problem; it is not limited to a particular algorithm.

### `test_main.py`

Contains the objective tests used to determine whether the agent successfully fixed the code.

The agent may read the tests, but should modify the source code rather than the tests.

## Agent Tools

### `read_file`

Reads a file from the workspace.

### `write_file`

Modifies or creates a file in the workspace.

### `run_tests`

Runs:

```bash
python -m pytest task
```

inside Docker.

## Docker Sandbox

Code execution happens inside a Docker container.

The sandbox:

- Uses the `bugfix-sandbox` image
- Mounts the project as `/workspace`
- Runs tests from `/workspace`
- Streams test output
- Captures the exit code
- Removes the container after execution

Example:

```text
[Docker] Starting container...
[Docker] Command: python -m pytest task

============================== 3 passed ==============================

[Docker] Container finished with exit code 0
[Docker] Container removed.
```

## Reward

The verifier uses the Docker test process exit code:

```python
return 1.0 if "[exit_code=0]" in result else 0.0
```

Therefore:

- `exit_code=0` → all tests passed → **reward = 1.0**
- non-zero exit code → tests failed → **reward = 0.0**

The reward is independent of the number of tests.

## Requirements

- Python 3.11+
- `uv`
- Docker Desktop
- An OpenAI-compatible API key
- Pytest

## Installation

```bash
git clone https://github.com/YOUR_USERNAME/RL-Envi-CodeFix.git
cd RL-Envi-CodeFix
uv sync
```

Make sure Docker Desktop is running.

## Environment Variables

Create `.env`:

```env
OPENROUTER_API_KEY=your_api_key_here
```

Never commit `.env` to GitHub.

Use `.env.example` as a safe template:

```env
OPENROUTER_API_KEY=
```

## Run

```bash
uv run python run_agent.py
```

The agent will:

1. Read the task description.
2. Inspect the source code.
3. Identify the bug.
4. Modify the source code.
5. Run tests inside Docker.
6. Continue fixing if necessary.
7. Receive a reward based on the final result.

## Example

A task might contain a buggy `largest(arr)` implementation, with `README.md` describing that it must return the largest value.

The agent inspects the code, identifies the bug, edits `main.py`, and runs the tests.

If all tests pass:

```text
reward = 1.0
```

## Metrics

| Metric | Meaning |
|---|---|
| `score_result` | Final verifier reward |
| `num_turns` | Number of agent turns |
| `total_tool_calls` | Total tool calls |
| `read_file_calls` | Number of file reads |
| `write_file_calls` | Number of file modifications |
| `run_tests_calls` | Number of test executions |
| `avg_reward` | Average reward across rollouts |

## Project Structure

```text
RL-Envi-CodeFix/
│
├── task/
│   ├── main.py
│   ├── test_main.py
│   └── README.md
│
├── docker_tool.py
├── environment.py
├── run_agent.py
├── pyproject.toml
├── .env.example
├── .gitignore
└── README.md
```

## Why This Is an RL Environment

The environment provides an objective reward for the agent's actions.

The agent follows a loop:

```text
Observe → Reason → Act → Execute → Observe → Act ...
```

The final test result determines the reward.

This makes the project useful for experimenting with:

- LLM agents
- Tool use
- Code repair
- Agent trajectories
- Reward design
- Reinforcement learning
- Coding-model evaluation

## Creating New Tasks

For a new coding problem, replace:

```text
task/main.py
task/test_main.py
task/README.md
```

The environment itself does not need to change.

Tasks can cover:

- Algorithms
- Data structures
- String manipulation
- Mathematical functions
- File processing
- APIs
- Utilities
- Business logic

## Security

Docker provides isolation for code execution, but arbitrary untrusted code should still be treated carefully.

For stronger isolation, use resource limits, restricted networking, non-privileged containers, and appropriate Docker security settings.

Do not expose secrets or sensitive host files to the container.

## Roadmap

- [ ] More diverse coding tasks
- [ ] Multiple programming-language support
- [ ] Reward shaping
- [ ] Multiple test suites per task
- [ ] Automatic task generation
- [ ] Stronger sandbox restrictions
- [ ] Benchmarking multiple LLMs
- [ ] RL training integration

## License

MIT License.
