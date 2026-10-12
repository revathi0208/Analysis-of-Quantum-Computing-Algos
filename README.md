# Analysis of Quantum Computing Algorithm

**Authors:** Revathi Gounder · Tikshita Gundaram · Sakshi Joshi  

---

## 🌟 Interactive Quantum Engine & Live Algorithm Solvers

This website provides a **live, fully interactive simulation and solver** demonstrating quantum computational advantage over classical computing.

### 🚀 What's New & Included:

1. **⚡ Deutsch–Jozsa Live Solver (Decision Problem):**
   - **Interactive Truth Table Editor:** Click any bit in the table to toggle its value ($0$ or $1$) or pick preset oracles.
   - **Classical Sequential Solver:** Tests inputs one-by-one with live visual ticking and query counters up to $2^{n-1} + 1$.
   - **Quantum Solver:** Evaluates the entire superposition via phase kickback and solves the problem in **exactly 1 query**.
   - **Live Proof:** Automatically proves whether the function is **Constant** or **Balanced**.

2. **🔐 Shor's Algorithm Live Solver (Factoring Problem):**
   - Select any integer $N$ ($15, 21, 33, 35, 77, 91$) and a co-prime base $a$.
   - Live modular exponentiation period-finding: solves the period $p$ of $f(x) = a^x \pmod N$.
   - Classical post-processing: extracts prime factors using $\gcd(a^{p/2} \pm 1, N)$ live!

3. **🕸️ QAOA Max-Cut Live Solver (Combinatorial Optimization):**
   - Graph visualizer for the 4-node ring ($0-1-2-3-0$).
   - Shows optimal bitstring cut partitions (`0101` and `1010`) achieving the maximum cut value of $4$.

4. **🌊 Live Quantum Wave Interference Physics:**
   - Real-time animated canvas demonstrating constructive vs. destructive wave interference.

5. **⏱️ Speed & Complexity Benchmark:**
   - Interactive slider from $n = 1$ to $40$ bits comparing classical time explosion against quantum constant time $\mathcal{O}(1)$.

6. **💻 Simulated Laboratory Terminal:**
   - Pre-loaded with executable scripts for Qiskit and C-DAC Qniverse OpenQASM 2.0.
   - Click **▶ Run in Simulator** to watch simulated terminal output execute with $1024$ shots!

---

## 🖥️ How to Run
Simply open your folder and double-click:
- [`index.html`](./index.html) or [`deutsch_jozsa_website.html`](./deutsch_jozsa_website.html)
