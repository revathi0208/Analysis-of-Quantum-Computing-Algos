"""
QAOA for Max-Cut — Qiskit Implementation
--------------------------------------------------
Solves the Max-Cut problem on a small graph using the Quantum
Approximate Optimization Algorithm (QAOA) — a hybrid quantum-classical
algorithm. This matches the structure used on the Qniverse platform:
Cost Layer (CX-RZ-CX per edge) + Mixer Layer (RX per qubit), with a
classical optimizer tuning the angles (gamma, beta).

Requirements:
    pip install qiskit qiskit-aer scipy networkx --break-system-packages

Run:
    python qaoa_maxcut.py
"""

import numpy as np
import networkx as nx
from scipy.optimize import minimize
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

# ---- Define the graph (4 nodes, forming a ring: 0-1-2-3-0) ----
EDGES = [(0, 1), (1, 2), (2, 3), (3, 0)]
N_NODES = 4
P_LAYERS = 1          # number of QAOA layers (p)
SHOTS = 2048

simulator = AerSimulator()


def build_qaoa_circuit(gamma, beta):
    """
    Builds the QAOA circuit for Max-Cut:
      1. Superposition (H on all qubits)
      2. Cost layer  -- encodes the graph edges, parameterized by gamma
      3. Mixer layer -- lets the circuit explore other solutions, parameterized by beta
      (repeated for P_LAYERS)
    """
    qc = QuantumCircuit(N_NODES, N_NODES)

    # Step 1: superposition -- every possible cut configuration
    qc.h(range(N_NODES))

    for layer in range(P_LAYERS):
        g = gamma[layer]
        b = beta[layer]

        # Step 2: Cost layer -- for each edge, CX - RZ(gamma) - CX
        for (i, j) in EDGES:
            qc.cx(i, j)
            qc.rz(2 * g, j)
            qc.cx(i, j)

        # Step 3: Mixer layer -- RX(2*beta) on every qubit
        for q in range(N_NODES):
            qc.rx(2 * b, q)

    qc.measure(range(N_NODES), range(N_NODES))
    return qc


def cut_value(bitstring, edges):
    """Classically counts how many edges are 'cut' by this partition."""
    x = bitstring[::-1]  # Qiskit bit order is reversed
    return sum(1 for (i, j) in edges if x[i] != x[j])


def expected_cut(params):
    """
    Runs the QAOA circuit with given parameters and returns the
    NEGATIVE average cut value (since scipy.minimize minimizes,
    and we want to MAXIMIZE the cut).
    """
    half = len(params) // 2
    gamma, beta = params[:half], params[half:]

    qc = build_qaoa_circuit(gamma, beta)
    compiled = transpile(qc, simulator)
    result = simulator.run(compiled, shots=SHOTS).result()
    counts = result.get_counts()

    avg_cut = sum(cut_value(bits, EDGES) * freq for bits, freq in counts.items()) / SHOTS
    return -avg_cut  # negative because scipy minimizes


def main():
    print(f"Running QAOA for Max-Cut on a {N_NODES}-node ring graph: {EDGES}\n")

    # Initial guess for gamma, beta (p layers each)
    init_params = np.random.uniform(0, np.pi, 2 * P_LAYERS)

    print("Optimizing circuit parameters (gamma, beta) using classical optimizer (COBYLA)...")
    result = minimize(expected_cut, init_params, method="COBYLA",
                       options={"maxiter": 100})

    best_params = result.x
    half = len(best_params) // 2
    gamma, beta = best_params[:half], best_params[half:]

    print(f"\nOptimal parameters found: gamma = {gamma}, beta = {beta}")
    print(f"Best expected cut value during optimization: {-result.fun:.3f}")

    # Final run with best parameters
    qc = build_qaoa_circuit(gamma, beta)
    compiled = transpile(qc, simulator)
    final_result = simulator.run(compiled, shots=SHOTS).result()
    counts = final_result.get_counts()

    print("\nTop measured partitions (bitstrings):")
    sorted_counts = sorted(counts.items(), key=lambda x: -x[1])
    for bits, freq in sorted_counts[:5]:
        cv = cut_value(bits, EDGES)
        prob = 100 * freq / SHOTS
        print(f"  {bits}  ->  cut value = {cv}   ({prob:.1f}% of runs)")

    best_bitstring = sorted_counts[0][0]
    best_cut = cut_value(best_bitstring, EDGES)

    # Verify against brute-force classical solution
    best_classical_cut = 0
    best_classical_partition = None
    for i in range(2 ** N_NODES):
        bits = format(i, f"0{N_NODES}b")
        cv = cut_value(bits, EDGES)
        if cv > best_classical_cut:
            best_classical_cut = cv
            best_classical_partition = bits

    print("\n" + "=" * 55)
    print(f"QAOA's most frequent result: {best_bitstring} -> cut value = {best_cut}")
    print(f"True optimal (brute-force classical): {best_classical_partition} -> cut value = {best_classical_cut}")
    if best_cut == best_classical_cut:
        print("SUCCESS: QAOA found the optimal Max-Cut solution!")
    else:
        print("QAOA found an approximate (near-optimal) solution.")
    print("=" * 55)


if __name__ == "__main__":
    main()
