# 🚨 RescueRoute — Pathfinding Visualizer

RescueRoute is an interactive pathfinding visualizer built using Python and Pygame. It demonstrates how BFS and A* algorithms explore a grid to find a route from a starting point to an exit while avoiding obstacles.

## ✨ Features

- Interactive grid with a start point and exit
- Add obstacles using the mouse
- Animated search exploration
- Breadth-First Search (BFS) visualization
- A* search with Manhattan distance heuristic
- Comparison dashboard showing path length, explored cells, and search time
- Detects when no route is available

## 🛠️ Tech Stack

- Python
- Pygame
- `collections.deque`
- `heapq`
- `time`

## 🚀 How to Run

1. Install Python 3.13.
2. Install Pygame:

   ```bash
   py -3.13 -m pip install pygame==2.6.1
   ```

3. Run the project:

   ```bash
   py -3.13 main.py
   ```

## 🎮 Controls

| Control | Action |
|---|---|
| Left-click | Add or remove a wall |
| `1` | Run BFS |
| `2` | Run A* |
| `C` | Clear walls and results |
| Right-click | Run BFS |

## 🧠 Algorithms

**BFS (Breadth-First Search):** Explores cells level by level and finds a shortest path when every move has equal cost.

**A\* Search:** Uses path cost and a Manhattan-distance heuristic to guide the search toward the exit.

## 📊 Comparison Metrics

The dashboard compares:
- Number of moves in the resulting path
- Number of explored cells
- Search execution time in milliseconds

Execution time may vary by computer and run.

## 🎯 Purpose

This project was created as a learning project to understand graph algorithms, heuristic search, Python programming, and visualization.

**Note:** RescueRoute is an educational simulation, not a real emergency-navigation system.
## 📸 Project Demo

![RescueRoute Demo](rescueroute-demo.png)
