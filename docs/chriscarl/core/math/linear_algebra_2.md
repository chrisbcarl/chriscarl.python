# GE on Simple Matrix (Self Done)
$$
\text{Gaussian Elimination with LU Decomposition and Inverse} \\
\text{A} \\
\quad \begin{bmatrix}
    2 & 1 & -1 \\
    -3 & -1 & 2 \\
    -2 & 1 & 2 \\
\end{bmatrix} \\
\text{augmentation} \\
\quad \begin{bmatrix}
    2 & 1 & -1 & 1 & 0 & 0 \\
    -3 & -1 & 2 & 0 & 1 & 0 \\
    -2 & 1 & 2 & 0 & 0 & 1 \\
\end{bmatrix} \\
\text{permutation} \\
    \quad \text{None}\\ \\
\text{permutation-post} \\
\quad \begin{bmatrix}
    2 & 1 & -1 & 1 & 0 & 0 \\
    -3 & -1 & 2 & 0 & 1 & 0 \\
    -2 & 1 & 2 & 0 & 0 & 1 \\
\end{bmatrix} \\
R2 \leftarrow R2 - (-1.5) R1 \\
\quad \begin{bmatrix}
    2 & 1 & -1 & 1 & 0 & 0 \\
    0 & 0.5 & 0.5 & 1.5 & 1.0 & 0 \\
    -2 & 1 & 2 & 0 & 0 & 1 \\
\end{bmatrix} \\
R3 \leftarrow R3 - (-1.0) R1 \\
\quad \begin{bmatrix}
    2 & 1 & -1 & 1 & 0 & 0 \\
    0 & 0.5 & 0.5 & 1.5 & 1.0 & 0 \\
    0 & 2.0 & 1.0 & 1.0 & 0 & 1.0 \\
\end{bmatrix} \\
R3 \leftarrow R3 - (4.0) R2 \\
\quad \begin{bmatrix}
    2 & 1 & -1 & 1 & 0 & 0 \\
    0 & 0.5 & 0.5 & 1.5 & 1.0 & 0 \\
    0 & 0 & -1.0 & -5.0 & -4.0 & 1.0 \\
\end{bmatrix} \\
\text{U} \\
\quad \begin{bmatrix}
    2 & 1 & -1 \\
    0 & 0.5 & 0.5 \\
    0 & 0 & -1.0 \\
\end{bmatrix} \\
\text{L} \\
\quad \begin{bmatrix}
    1 & 0 & 0 \\
    1.5 & 1.0 & 0 \\
    -5.0 & -4.0 & 1.0 \\
\end{bmatrix} \\
\text{scale} \\
R1 \leftarrow \frac{1}{2} R1 \\
R2 \leftarrow \frac{1}{0.5} R2 \\
R3 \leftarrow \frac{1}{-1.0} R3 \\
\text{scale-post} \\
\quad \begin{bmatrix}
    1.0 & 0.5 & -0.5 & 0.5 & 0 & 0 \\
    0 & 1.0 & 1.0 & 3.0 & 2.0 & 0 \\
    0 & 0 & 1.0 & 5.0 & 4.0 & -1.0 \\
\end{bmatrix} \\
R2 \leftarrow R2 - (1.0) R3 \\
\quad \begin{bmatrix}
    1.0 & 0.5 & -0.5 & 0.5 & 0 & 0 \\
    0 & 1.0 & 0 & -2.0 & -2.0 & 1.0 \\
    0 & 0 & 1.0 & 5.0 & 4.0 & -1.0 \\
\end{bmatrix} \\
R1 \leftarrow R1 - (-0.5) R3 \\
\quad \begin{bmatrix}
    1.0 & 0.5 & 0 & 3.0 & 2.0 & -0.5 \\
    0 & 1.0 & 0 & -2.0 & -2.0 & 1.0 \\
    0 & 0 & 1.0 & 5.0 & 4.0 & -1.0 \\
\end{bmatrix} \\
R1 \leftarrow R1 - (0.5) R3 \\
\quad \begin{bmatrix}
    1.0 & 0 & 0 & 4.0 & 3.0 & -1.0 \\
    0 & 1.0 & 0 & -2.0 & -2.0 & 1.0 \\
    0 & 0 & 1.0 & 5.0 & 4.0 & -1.0 \\
\end{bmatrix} \\
\operatorname{{rref}}(A) \\
\quad \begin{bmatrix}
    1.0 & 0 & 0 \\
    0 & 1.0 & 0 \\
    0 & 0 & 1.0 \\
\end{bmatrix} \\
A^{-1} \\
\quad \begin{bmatrix}
    4.0 & 3.0 & -1.0 \\
    -2.0 & -2.0 & 1.0 \\
    5.0 & 4.0 & -1.0 \\
\end{bmatrix} \\
$$


[Gemini 3.5t](https://gemini.google.com/app/5346d2425c7fb36c)

# Prompt
Generate examples of matrices for each case, and some combinations:
- invertible
- non-invertible
- non-square
- others that I cant think of right now

The goal is to develop test cases for a brute force gaussian elimination algorithm that can pass all test cases whose output is the L, U, rref, and inverse

# Reponse Gemini 3.5t
### 1. Invertible (Square, Full Rank, No Pivoting Needed)

**Matrix:**


$$A = \begin{bmatrix} 2 & 1 & 1 \\ -4 & 1 & -2 \\ 2 & 7 & 7 \end{bmatrix}$$

**Expected Behaviors & Outputs:**

* **$L$ (Lower Triangular):** $\begin{bmatrix} 1 & 0 & 0 \\ -2 & 1 & 0 \\ 1 & 2 & 1 \end{bmatrix}$
* **$U$ (Upper Triangular):** $\begin{bmatrix} 2 & 1 & 1 \\ 0 & 3 & 0 \\ 0 & 0 & 6 \end{bmatrix}$
* **$\text{RREF}(A)$:** $\begin{bmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1 \end{bmatrix}$
* **$A^{-1}$:** $\begin{bmatrix} 0.5833 & 0 & -0.0833 \\ 0.6667 & 0.3333 & 0 \\ -0.8333 & -0.3333 & 0.1667 \end{bmatrix} = \begin{bmatrix} \frac{7}{12} & 0 & -\frac{1}{12} \\ \frac{2}{3} & \frac{1}{3} & 0 \\ -\frac{5}{6} & -\frac{1}{3} & \frac{1}{6} \end{bmatrix}$

---

### 2. Invertible (Requires Partial Pivoting / Row Swaps)

**Matrix:**


$$A = \begin{bmatrix} 0 & 1 & 2 \\ 1 & 2 & 1 \\ 2 & 7 & 8 \end{bmatrix}$$

**Expected Behaviors & Outputs:**

* **Test Objective:** Validates pivot selection when $A_{11} = 0$. Unpivoted Gaussian elimination will fail with division by zero.
* **$P A = L U$ Decomposition:**

$$P = \begin{bmatrix} 0 & 1 & 0 \\ 0 & 0 & 1 \\ 1 & 0 & 0 \end{bmatrix}, \quad L = \begin{bmatrix} 1 & 0 & 0 \\ 2 & 1 & 0 \\ 0 & \frac{1}{3} & 1 \end{bmatrix}, \quad U = \begin{bmatrix} 1 & 2 & 1 \\ 0 & 3 & 6 \\ 0 & 0 & 0 \end{bmatrix} \quad \text{(with row swaps applied)}$$


* **$\text{RREF}(A)$:** $\begin{bmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1 \end{bmatrix}$
* **$A^{-1}$:** $\begin{bmatrix} \frac{9}{5} & -\frac{6}{5} & \frac{3}{5} \\ \frac{6}{5} & -\frac{4}{5} & \frac{2}{5} \\ -\frac{3}{5} & \frac{2}{5} & -\frac{1}{5} \end{bmatrix}$

---

### 3. Non-Invertible / Singular (Square, Rank-Deficient)

**Matrix:**


$$A = \begin{bmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \\ 7 & 8 & 9 \end{bmatrix}$$

**Expected Behaviors & Outputs:**

* **$\text{Rank}(A)$:** $2$
* **$L$:** $\begin{bmatrix} 1 & 0 & 0 \\ 4 & 1 & 0 \\ 7 & 2 & 1 \end{bmatrix}$
* **$U$:** $\begin{bmatrix} 1 & 2 & 3 \\ 0 & -3 & -6 \\ 0 & 0 & 0 \end{bmatrix}$
* **$\text{RREF}(A)$:** $\begin{bmatrix} 1 & 0 & -1 \\ 0 & 1 & 2 \\ 0 & 0 & 0 \end{bmatrix}$
* **Inverse:** None (Algorithm must raise an error or return `None`/`NaN`).

---

### 4. Non-Square: Fat / Wide ($m < n$, Underdetermined)

**Matrix:**


$$A = \begin{bmatrix} 1 & 3 & -1 & 4 \\ 2 & 6 & 1 & 5 \end{bmatrix}$$

**Expected Behaviors & Outputs:**

* **Dimensions:** $2 \times 4$
* **$L$:** $\begin{bmatrix} 1 & 0 \\ 2 & 1 \end{bmatrix}$
* **$U$:** $\begin{bmatrix} 1 & 3 & -1 & 4 \\ 0 & 0 & 3 & -3 \end{bmatrix}$
* **$\text{RREF}(A)$:** $\begin{bmatrix} 1 & 3 & 0 & 3 \\ 0 & 0 & 1 & -1 \end{bmatrix}$
* **Inverse:** Not defined for non-square matrices.

---

### 5. Non-Square: Tall / Thin ($m > n$, Overdetermined)

**Matrix:**


$$A = \begin{bmatrix} 1 & 2 \\ 2 & 5 \\ 3 & 6 \end{bmatrix}$$

**Expected Behaviors & Outputs:**

* **Dimensions:** $3 \times 2$
* **$L$:** $\begin{bmatrix} 1 & 0 & 0 \\ 2 & 1 & 0 \\ 3 & 0 & 1 \end{bmatrix}$
* **$U$:** $\begin{bmatrix} 1 & 2 \\ 0 & 1 \\ 0 & 0 \end{bmatrix}$
* **$\text{RREF}(A)$:** $\begin{bmatrix} 1 & 0 \\ 0 & 1 \\ 0 & 0 \end{bmatrix}$
* **Inverse:** Not defined.

---

### 6. Edge Cases & Special Structures

| Case | Example Matrix $A$ | Key Algorithm Verification |
| --- | --- | --- |
| **Identity Matrix** | $\begin{bmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1 \end{bmatrix}$ | $L=I$, $U=I$, $\text{RREF}=I$, $A^{-1}=I$. Should terminate in zero row ops. |
| **Zero Matrix** | $\begin{bmatrix} 0 & 0 \\ 0 & 0 \end{bmatrix}$ | Tests zero-pivot handling across all rows/cols. $\text{RREF}=0_{2\times 2}$, no inverse. |
| **Zero Leading Column** | $\begin{bmatrix} 0 & 1 & 2 \\ 0 & 3 & 4 \end{bmatrix}$ | Tests column iteration when entire column $0$ has no pivot. |
| **Single Element ($1 \times 1$)** | $\begin{bmatrix} 5 \end{bmatrix}$ | Edge bounds check ($1 \times 1$). $L=\begin{bmatrix}1\end{bmatrix}$, $U=\begin{bmatrix}5\end{bmatrix}$, $A^{-1}=\begin{bmatrix}0.2\end{bmatrix}$. |
| **Already Upper Triangular** | $\begin{bmatrix} 2 & 3 \\ 0 & 4 \end{bmatrix}$ | $L=I_2$, $U=A$. Eliminator loops should skip lower zero entries. |
| **Floating-Point Precision** | $\begin{bmatrix} 1 & 1 \\ 1 & 1 + 10^{-15} \end{bmatrix}$ | Tests floating-point tolerance ($\epsilon \approx 10^{-12}$) for detecting non-zero pivots. |

# Prompt 2
output each of these cases as python code using simple double dimension lists, also include the P, L, U, rref, inverse results in this test case dictionary

# Response 2

```python
import numpy as np
import scipy.linalg as la
import sympy as sp

test_cases = {
    "invertible_no_pivoting": [[2, 1, 1], [-4, 1, -2], [2, 7, 7]],
    "invertible_requires_pivoting": [[0, 1, 2], [1, 2, 1], [2, 7, 8]],
    "non_invertible_singular": [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
    "non_square_fat": [[1, 3, -1, 4], [2, 6, 1, 5]],
    "non_square_tall": [[1, 2], [2, 5], [3, 6]],
    "identity": [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
    "zero_matrix": [[0, 0], [0, 0]],
    "zero_leading_column": [[0, 1, 2], [0, 3, 4]],
    "single_element": [[5]],
    "already_upper_triangular": [[2, 3], [0, 4]],
    "floating_point_precision": [[1.0, 1.0], [1.0, 1.0 + 1e-15]]
}

results = {}

for name, mat in test_cases.items():
    A = np.array(mat, dtype=float)
    M = sp.Matrix(mat)

    # RREF using sympy
    rref_m, pivot_cols = M.rref()
    rref = np.array(rref_m).astype(float).tolist()

    # LU Decomposition (PLU)
    P, L, U = la.lu(A)

    # Inverse
    try:
        inv = np.linalg.inv(A).tolist() if A.shape[0] == A.shape[1] else None
    except np.linalg.LinAlgError:
        inv = None

    results[name] = {
        "A": mat,
        "P": P.tolist(),
        "L": L.tolist(),
        "U": U.tolist(),
        "rref": rref,
        "inverse": inv
    }

for k, v in results.items():
    print(f"=== {k} ===")
    print("P:", v["P"])
    print("L:", v["L"])
    print("U:", v["U"])
    print("RREF:", v["rref"])
    print("Inverse:", v["inverse"])

import numpy as np
import scipy.linalg as la
import sympy as sp

# Let's fix invertible_requires_pivoting
A_pivot = [[0, 1, 2], [1, 2, 1], [2, 7, 9]]

A = np.array(A_pivot, dtype=float)
M = sp.Matrix(A_pivot)

print("Det:", np.linalg.det(A))
print("Inv:", np.linalg.inv(A))
print("RREF:", M.rref()[0])

P, L, U = la.lu(A)
print("P:\n", P)
print("L:\n", L)
print("U:\n", U)

import sympy as sp

test_cases = {
    "invertible_no_pivoting": [[2, 1, 1], [-4, 1, -2], [2, 7, 7]],
    "invertible_requires_pivoting": [[0, 1, 2], [1, 2, 1], [2, 7, 9]],
    "non_invertible_singular": [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
    "non_square_fat": [[1, 3, -1, 4], [2, 6, 1, 5]],
    "non_square_tall": [[1, 2], [2, 5], [3, 6]],
    "identity": [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
    "zero_matrix": [[0, 0], [0, 0]],
    "zero_leading_column": [[0, 1, 2], [0, 3, 4]],
    "single_element": [[5]],
    "already_upper_triangular": [[2, 3], [0, 4]],
    "floating_point_precision": [[1.0, 1.0], [1.0, 1.0 + 1e-15]]
}

def get_exact_details(name, mat):
    M = sp.Matrix(mat)
    rref_m, _ = M.rref()

    is_square = M.rows == M.cols
    is_invertible = is_square and M.det() != 0

    inv = M.inv() if is_invertible else None

    # Unpivoted LU if possible (for square and fat/tall if leading principal minors non-zero)
    # SymPy LUP
    L, U, p = M.LUdecomposition() # p is list of row swaps or pivot indices

    # Construct P matrix from p
    P = sp.zeros(M.rows, M.rows)
    # LUdecomposition in sympy returns L, U, p where P*A = L*U or similar
    # Let's check scipy LU for standard numerical partial pivoting PA = LU
    return {
        "rref": rref_m,
        "inv": inv,
        "L": L,
        "U": U,
        "p": p
    }

for name, mat in test_cases.items():
    print(f"=== {name} ===")
    M = sp.Matrix(mat)
    rref_m, _ = M.rref()
    print("RREF:", rref_m.tolist())
    if M.rows == M.cols and M.det() != 0:
        inv = M.inv().tolist()
        # also convert floats to exact if needed
        print("INVERSE (Exact):", inv)
    else:
        print("INVERSE: None")

import scipy.linalg as la
import numpy as np

def compute_all(mat):
    A = np.array(mat, dtype=float)
    m, n = A.shape

    # Partial Pivoting PA = LU
    P, L, U = la.lu(A)

    return P.tolist(), L.tolist(), U.tolist()

for name, mat in test_cases.items():
    P, L, U = compute_all(mat)
    print(f"--- {name} ---")
    print(f"P = {P}")
    print(f"L = {L}")
    print(f"U = {U}")

# Verify simple pivoting and exact outputs for all cases
import sympy as sp

# 1. invertible_no_pivoting
A1 = sp.Matrix([[2, 1, 1], [-4, 1, -2], [2, 7, 7]])
# 2. invertible_requires_pivoting
A2 = sp.Matrix([[0, 1, 2], [1, 2, 1], [2, 7, 9]])
# 3. non_invertible_singular
A3 = sp.Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
# 4. non_square_fat
A4 = sp.Matrix([[1, 3, -1, 4], [2, 6, 1, 5]])
# 5. non_square_tall
A5 = sp.Matrix([[1, 2], [2, 5], [3, 6]])
# 6. identity
A6 = sp.Matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
# 7. zero_matrix
A7 = sp.Matrix([[0, 0], [0, 0]])
# 8. zero_leading_column
A8 = sp.Matrix([[0, 1, 2], [0, 3, 4]])
# 9. single_element
A9 = sp.Matrix([[5]])
# 10. already_upper_triangular
A10 = sp.Matrix([[2, 3], [0, 4]])
# 11. floating_point_precision
A11 = sp.Matrix([[1.0, 1.0], [1.0, 1.0 + 1e-15]])

mats = [A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, A11]
names = [
    "invertible_no_pivoting",
    "invertible_requires_pivoting",
    "non_invertible_singular",
    "non_square_fat",
    "non_square_tall",
    "identity",
    "zero_matrix",
    "zero_leading_column",
    "single_element",
    "already_upper_triangular",
    "floating_point_precision"
]

for name, M in zip(names, mats):
    print(f"=== {name} ===")
    rref, pivots = M.rref()
    print("RREF:", rref.tolist())
    if M.rows == M.cols and M.det() != 0:
        inv = M.inv().tolist()
        print("INVERSE:", inv)
    else:
        print("INVERSE: None")
```

```python
test_cases = {
    # 1. Invertible (Square, Full Rank, No Pivoting Needed)
    "invertible_no_pivoting": {
        "matrix": [
            [2, 1, 1],
            [-4, 1, -2],
            [2, 7, 7]
        ],
        "P": [
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ],
        "L": [
            [1, 0, 0],
            [-2, 1, 0],
            [1, 2, 1]
        ],
        "U": [
            [2, 1, 1],
            [0, 3, 0],
            [0, 0, 6]
        ],
        "rref": [
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ],
        "inverse": [
            [7 / 12, 0.0, -1 / 12],
            [2 / 3, 1 / 3, 0.0],
            [-5 / 6, -1 / 3, 1 / 6]
        ]
    },

    # 2. Invertible (Requires Row Swap / Pivot due to zero at A[0][0])
    "invertible_requires_pivoting": {
        "matrix": [
            [0, 1, 2],
            [1, 2, 1],
            [2, 7, 9]
        ],
        "P": [
            [0, 1, 0],
            [1, 0, 0],
            [0, 0, 1]
        ],
        "L": [
            [1, 0, 0],
            [0, 1, 0],
            [2, 3, 1]
        ],
        "U": [
            [1, 2, 1],
            [0, 1, 2],
            [0, 0, 1]
        ],
        "rref": [
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ],
        "inverse": [
            [-11, -5, 3],
            [7, 4, -2],
            [-3, -2, 1]
        ]
    },

    # 3. Non-Invertible / Singular (Square, Rank-Deficient)
    "non_invertible_singular": {
        "matrix": [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ],
        "P": [
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ],
        "L": [
            [1, 0, 0],
            [4, 1, 0],
            [7, 2, 1]
        ],
        "U": [
            [1, 2, 3],
            [0, -3, -6],
            [0, 0, 0]
        ],
        "rref": [
            [1, 0, -1],
            [0, 1, 2],
            [0, 0, 0]
        ],
        "inverse": None
    },

    # 4. Non-Square: Fat / Wide (m < n, Underdetermined)
    "non_square_fat": {
        "matrix": [
            [1, 3, -1, 4],
            [2, 6, 1, 5]
        ],
        "P": [
            [1, 0],
            [0, 1]
        ],
        "L": [
            [1, 0],
            [2, 1]
        ],
        "U": [
            [1, 3, -1, 4],
            [0, 0, 3, -3]
        ],
        "rref": [
            [1, 3, 0, 3],
            [0, 0, 1, -1]
        ],
        "inverse": None
    },

    # 5. Non-Square: Tall / Thin (m > n, Overdetermined)
    "non_square_tall": {
        "matrix": [
            [1, 2],
            [2, 5],
            [3, 6]
        ],
        "P": [
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ],
        "L": [
            [1, 0],
            [2, 1],
            [3, 0]
        ],
        "U": [
            [1, 2],
            [0, 1]
        ],
        "rref": [
            [1, 0],
            [0, 1],
            [0, 0]
        ],
        "inverse": None
    },

    # 6. Identity Matrix
    "identity": {
        "matrix": [
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ],
        "P": [
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ],
        "L": [
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ],
        "U": [
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ],
        "rref": [
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ],
        "inverse": [
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ]
    },

    # 7. Zero Matrix
    "zero_matrix": {
        "matrix": [
            [0, 0],
            [0, 0]
        ],
        "P": [
            [1, 0],
            [0, 1]
        ],
        "L": [
            [1, 0],
            [0, 1]
        ],
        "U": [
            [0, 0],
            [0, 0]
        ],
        "rref": [
            [0, 0],
            [0, 0]
        ],
        "inverse": None
    },

    # 8. Zero Leading Column
    "zero_leading_column": {
        "matrix": [
            [0, 1, 2],
            [0, 3, 4]
        ],
        "P": [
            [1, 0],
            [0, 1]
        ],
        "L": [
            [1, 0],
            [3, 1]
        ],
        "U": [
            [0, 1, 2],
            [0, 0, -2]
        ],
        "rref": [
            [0, 1, 0],
            [0, 0, 1]
        ],
        "inverse": None
    },

    # 9. Single Element (1x1 Matrix)
    "single_element": {
        "matrix": [
            [5]
        ],
        "P": [
            [1]
        ],
        "L": [
            [1]
        ],
        "U": [
            [5]
        ],
        "rref": [
            [1]
        ],
        "inverse": [
            [0.2]
        ]
    },

    # 10. Already Upper Triangular
    "already_upper_triangular": {
        "matrix": [
            [2, 3],
            [0, 4]
        ],
        "P": [
            [1, 0],
            [0, 1]
        ],
        "L": [
            [1, 0],
            [0, 1]
        ],
        "U": [
            [2, 3],
            [0, 4]
        ],
        "rref": [
            [1, 0],
            [0, 1]
        ],
        "inverse": [
            [0.5, -0.375],
            [0.0, 0.25]
        ]
    },

    # 11. Floating-Point Precision
    "floating_point_precision": {
        "matrix": [
            [1.0, 1.0],
            [1.0, 1.0 + 1e-15]
        ],
        "P": [
            [1, 0],
            [0, 1]
        ],
        "L": [
            [1.0, 0.0],
            [1.0, 1.0]
        ],
        "U": [
            [1.0, 1.0],
            [0.0, 1e-15]
        ],
        "rref": [
            [1.0, 0.0],
            [0.0, 1.0]
        ],
        "inverse": [
            [900719925474100.0, -900719925474099.0],
            [-900719925474099.0, 900719925474099.0]
        ]
    }
}
```