https://github.com/Suleman910/agent-maze/releases

# Agent Maze — Test AI Agents in Complex Procedural Mazes 🧭🤖

[![Releases](https://img.shields.io/badge/Releases-Download-blue?logo=github&style=for-the-badge)](https://github.com/Suleman910/agent-maze/releases)

Short description
- Test agent capability with complex generated mazes.
- Use procedural mazes to benchmark navigation, planning, perception, and exploration.

Hero image
![Maze illustration](https://upload.wikimedia.org/wikipedia/commons/6/6e/Maze.png)

What this project does
- Generates mazes with configurable topology, size, and complexity.
- Runs agents in the mazes to test navigation, mapping, and decision-making.
- Logs trajectories, actions, and performance metrics.
- Provides tools to visualize maps and replay agent runs.

Releases
- Download the release asset from https://github.com/Suleman910/agent-maze/releases and execute the provided file to run a packaged demo or binary. The release asset contains a runnable build and example mazes.

Why use Agent Maze
- Create controlled, repeatable tests for agent algorithms.
- Compare search, RL, and hybrid agents on the same maps.
- Measure robustness to partial observations and noisy sensors.
- Produce datasets of trajectories and sensor streams for training.

Features
- Maze generators
  - Grid mazes with the standard algorithms: DFS, Kruskal, Prim.
  - Weighted mazes with variable traversal cost.
  - Multi-floor mazes and portals.
  - Dynamic obstacles that change per episode.
- Agent interfaces
  - Discrete action API (move, turn, scan).
  - Continuous control API (velocity, steer).
  - Sensor models: depth, lidar, occupancy, RGB (synthetic).
- Benchmarks and metrics
  - Time to goal, path optimality, collisions.
  - Coverage rate, exploration efficiency, revisits.
  - Resource usage: compute, memory, latency.
- Visuals and tools
  - Runtime map render.
  - Replay traces with heatmaps.
  - Export data to CSV, JSON, ROS bag.

Quick start (release)
- Visit the releases page and download the appropriate release asset from https://github.com/Suleman910/agent-maze/releases. The release contains a packaged binary and sample configuration files.
- After download, execute the release file on your platform. Follow the release notes for platform-specific commands and permissions.

Quick start (source)
- Clone the repo.
- Run the main entry with the example config.
- Use the included scripts to spawn a set of mazes and start agents.
- The repository includes sample agents: a BFS agent, an A* agent, and a simple RL baseline.

Example run concepts
- Run a deterministic benchmark
  - Fix the random seed.
  - Generate N mazes with fixed parameters.
  - Run each agent on each maze.
  - Collect metrics and produce a report.
- Run a stress test
  - Generate large mazes with dynamic obstacles.
  - Add sensor noise and limited FOV.
  - Measure agent adaptability and recovery time.

Configuration overview
- Maze config
  - size: width, height
  - density: wall density or branching factor
  - algorithm: dfs, prim, kruskal
  - dynamic: boolean for moving obstacles
- Agent config
  - action_space: discrete or continuous
  - sensors: list of active sensors and their parameters
  - policy: script or model path
- Run config
  - episodes: number of runs
  - max_steps: per-episode step cap
  - seed: deterministic runs

APIs and integration
- Agent API (conceptual)
  - reset() -> initial observation
  - step(action) -> observation, reward, done, info
  - render(mode) -> image or overlay
- Data export
  - Trajectories export in CSV or JSON
  - Sensor logs in HDF5 for dense data
  - ROS bag export for robotics integration

Benchmarks and reproducibility
- Use the config file to lock the maze generator and agent seed.
- Save the maze shapes and all random seeds in the run manifest.
- Re-run experiments with the same manifest to reproduce results.
- Use the provided scripts to compute aggregated metrics and produce plots.

Visualization and analysis
- Built-in heatmap renderer marks visit frequency.
- Path overlays show planned vs. executed paths.
- Use the GUI to scrub time and view sensor frames.
- Export frames to MP4 for presentation.

Sample outputs
- Trajectory CSV fields: episode, step, x, y, theta, action, reward.
- Metrics JSON: { "time_to_goal": value, "collisions": n, "coverage": pct }.
- Visual artifacts: heatmaps, overlay images, and per-step screenshots.

Agent designs that work well
- Classic search
  - A* with admissible heuristic works on full-map tasks.
  - Dijkstra fits variable cost mazes.
- Online mapping
  - SLAM-style occupancy maps help in partial-observation runs.
  - Frontier-based exploration improves coverage.
- Learning-based agents
  - RL agents with curiosity reward handle exploration bias.
  - Imitation learning helps in dense maze structures.
- Hybrid systems
  - Use global planner with local reactive controller.
  - Combine mapping and learned policies for robustness.

Example research use cases
- Compare planning algorithms under sensor dropouts.
- Measure the effect of map noise on localization.
- Evaluate sample efficiency of RL agents in complex topologies.
- Study transfer from small to large mazes.

Data format and storage
- Use structured folders for runs: /runs/{experiment}/{timestamp}/
- Store configs and manifests with each run.
- Use compressed archives for sensor logs to save space.
- Keep a lightweight summary file per experiment for quick comparisons.

Visualization assets
- Use the provided PNG and SVG outputs for presentations.
- The project stores a gallery of generated mazes for sampling.
- Use the heatmap overlays to diagnose policy failures.

Community and contributions
- Suggest new maze generators.
- Add new agent baselines and sensor models.
- Provide platform-specific packaging for Windows, macOS, Linux.
- Improve benchmark scripts or add statistical tests.

Testing and CI
- The repo includes unit tests for maze generators and agent wrappers.
- Run the test suite before pull requests.
- CI runs smoke checks and basic benchmarks for every PR.

Roadmap ideas
- Add multi-agent scenarios with competitive and cooperative tasks.
- Add 3D environments and support for simulated cameras.
- Provide a cloud-runner for large batch benchmarks.
- Add curriculum generation to scale difficulty across episodes.

Resources and references
- Classic maze algorithms: DFS backtracker, Prim, Kruskal.
- Path planning: A*, D*, RRT (for continuous control).
- SLAM approaches: occupancy grid mapping, particle filters.
- Reinforcement learning: PPO, DQN variants adapted for partial observations.

Files you will find in a release
- Packaged binary or executable for the platform.
- Example maze configs and agent configs.
- Sample dataset of recorded runs.
- A minimal GUI or headless runner script.
- README and release notes describing the package.

License
- The repository uses a permissive license to allow research and commercial use. See the LICENSE file for details.

How to cite
- Use the repository name and release tag in experimental writeups.
- Include run manifests and seed values in reproducibility appendices.

Contact and support
- Open issues for bug reports or feature requests on the GitHub repo.
- Use pull requests to submit fixes or new components.

Badges and status
- The releases badge above links to the release assets. Use it to access the packaged binaries.

Screenshots and demo images
- Maze sample
  ![Maze sample](https://upload.wikimedia.org/wikipedia/commons/6/6e/Maze.png)
- Heatmap example
  ![Heatmap example](https://upload.wikimedia.org/wikipedia/commons/thumb/2/2c/Heatmap.png/640px-Heatmap.png)

Contributing guidelines
- Fork the repo.
- Create a feature branch.
- Run tests and add new tests for your change.
- Open a PR with a clear description and a reproducible example.

Security
- Report security issues via the repository issue tracker.

Releases link (again)
- Download and run the packaged release from https://github.com/Suleman910/agent-maze/releases to try a ready-made demo.