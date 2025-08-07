# Agent Maze Playground

This repo is a playground for testing agent capabilities with complex, procedurally generated mazes.

## Usage

1. Install dependencies in a fresh virtual environment

```bash
uv venv
uv pip install .
```

2. Run the [attached notebook](./agent_maze.ipynb) to test the agent capabilities.

In the notebook, you can change
- the types of mazes generated
- the LLMs and modeles that are being tested
- the prompts
- the tools each agent has access to
- the metrics being tracked

## Details

Inside [procedural_maze_generator.py](./procedural_maze_generator.py) you can learn more about how the mazes are generated.
