# Map-Coloring-Using-CSP-and-Heuristics
Python implementation of the Map Coloring problem using Constraint Satisfaction techniques including DFS, Forward Checking, Singleton Domain Propagation, and heuristics such as MRV, Degree Constraint, and Least Constraining Value. Tested on Australia and USA maps with performance analysis.
# Map Coloring Using CSP and Heuristics

This project implements the **Map Coloring Problem** using **Constraint Satisfaction Problem (CSP)** techniques in Python.  
The goal is to assign colors to regions such that no two adjacent regions share the same color, while minimizing the total number of colors used.

The solution is evaluated on two maps:

- Australia
- United States of America

Multiple search strategies and heuristics are implemented to compare performance.

---

## 🚀 Features

- Depth First Search (DFS)
- DFS with Forward Checking
- DFS with Forward Checking and Singleton Domain Propagation
- CSP Heuristics:
  - Minimum Remaining Values (MRV)
  - Degree Constraint
  - Least Constraining Value (LCV)
- Greedy estimation of chromatic number
- Backtracking counter
- Execution time measurement
- Comparison between heuristic and non-heuristic approaches

---

## 📂 Project Files

- `with_heuristics.py`  
  Full implementation including MRV, Degree Constraint, and LCV.

- `without_heuristics.py`  
  Baseline implementation using DFS, Forward Checking, and Singleton Propagation.

---

## 🛠 Requirements

- Python 3.x  

No external libraries are required.

---

## ▶️ How to Run

Clone the repository:

```bash
git clone https://github.com/yourusername/Map-Coloring-Using-CSP-and-Heuristics.git
cd Map-Coloring-Using-CSP-and-Heuristics
