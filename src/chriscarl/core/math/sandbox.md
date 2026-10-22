WARNING: skipping conda hook...
psm1 imports...
    download-file.psm1
        * Get-FileDownload
    env-var.psm1
        * Get-CleanPath
        * Set-EnvVarRefresh
    is-admin.psm1
        * Get-IsAdmin
        * Invoke-AsAdmin
    llama-cli-func-ex.psm1
        * Get-LLMs
        * Invoke-Prompt
    start-elevated-context-block.psm1
        * Start-ElevatedContextBlock
    start-process-invoke-script.psm1
        * Invoke-Script
        * Invoke-ScriptBlock
PS C:\Users\chris\src\chriscarl.python> & c:/Users/chris/src/chriscarl.python/.venv/Scripts/Activate.ps1
(chriscarl-py3.12) PS C:\Users\chris\src\chriscarl.python> python
Python 3.12.10 (tags/v3.12.10:0cc8128, Apr  8 2025, 12:21:36) [MSC v.1943 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
Ctrl click to launch VS Code Native REPL (https://aka.ms/python-native-repl)
>>> from chriscarl.core.math import linear_algebra_2 as la
>>> A = [
... [2, 1, -1],
... [-3, -2, 2]
... ,
... [-2, 1, 2]]
>>> A
[[2, 1, -1], [-3, -2, 2], [-2, 1, 2]]
>>> la.gaussian_elimination(A)
([[1, 0, 0], [0, 1, 0], [0, 0, 1]], [[1, 0, 0], [3, 2, 0], [-14, -8, -2]], [[2, 1, -1], [0, -1, 1], [0, 0, -6]], [[1.0, 0, 0], [0, 1.0, 0], [0, 0, 1.0]], [[2.0, 1.0, 0], [-0.666666666666667, -0.6666666666666667, 0.3333333333333333], [2.333333333333333, 1.3333333333333333, 0.3333333333333333]], '$$\n\\text{Gaussian Elimination with LU Decomposition and Inverse} \\\\\n\\text{A} \\\\\n\\quad \\begin{bmatrix}\n    2 & 1 & -1 \\\\\n    -3 & -2 & 2 \\\\\n    -2 & 1 & 2 \\\\\n\\end{bmatrix} \\\\\n\\text{augmentation} \\\\\n\\quad \\begin{bmatrix}\n    2 & 1 & -1 & 1 & 0 & 0 \\\\\n    -3 & -2 & 2 & 0 & 1 & 0 \\\\\n    -2 & 1 & 2 & 0 & 0 & 1 \\\\\n\\end{bmatrix} \\\\\n\\text{permutation} \\\\\n    \\quad \\text{None}\\\\ \\\\\n\\text{permutation-post} \\\\\n\\quad \\begin{bmatrix}\n    2 & 1 & -1 & 1 & 0 & 0 \\\\\n    -3 & -2 & 2 & 0 & 1 & 0 \\\\\n    -2 & 1 & 2 & 0 & 0 & 1 \\\\\n\\end{bmatrix} \\\\\nR2 \\leftarrow 2 R2 - (-3) R1 \\\\\n\\quad \\begin{bmatrix}\n    2 & 1 & -1 & 1 & 0 & 0 \\\\\n    0 & -1 & 1 & 3 & 2 & 0 \\\\\n    -2 & 1 & 2 & 0 & 0 & 1 \\\\\n\\end{bmatrix} \\\\\nR3 \\leftarrow 2 R3 - (-2) R1 \\\\\n\\quad \\begin{bmatrix}\n    2 & 1 & -1 & 1 & 0 & 0 \\\\\n    0 & -1 & 1 & 3 & 2 & 0 \\\\\n    0 & 4 & 2 & 2 & 0 & 2 \\\\\n\\end{bmatrix} \\\\\nR3 \\leftarrow -1 R3 - (4) R2 \\\\\n\\quad \\begin{bmatrix}\n    2 & 1 & -1 & 1 & 0 & 0 \\\\\n    0 & -1 & 1 & 3 & 2 & 0 \\\\\n    0 & 0 & -6 & -14 & -8 & -2 \\\\\n\\end{bmatrix} \\\\\n\\text{U} \\\\\n\\quad \\begin{bmatrix}\n    2 & 1 & -1 \\\\\n    0 & -1 & 1 \\\\\n    0 & 0 & -6 \\\\\n\\end{bmatrix} \\\\\n\\text{L} \\\\\n\\quad \\begin{bmatrix}\n    1 & 0 & 0 \\\\\n    3 & 2 & 0 \\\\\n    -14 & -8 & -2 \\\\\n\\end{bmatrix} \\\\\n\\text{scale} \\\\\nR1 \\leftarrow \\frac{1}{2} R1 \\\\\nR2 \\leftarrow \\frac{1}{-1} R2 \\\\\nR3 \\leftarrow \\frac{1}{-6} R3 \\\\\n\\text{scale-post} \\\\\n\\quad \\begin{bmatrix}\n    1.0 & 0.5 & -0.5 & 0.5 & 0 & 0 \\\\\n    0 & 1.0 & -1.0 & -3.0 & -2.0 & 0 \\\\\n    0 & 0 & 1.0 & 2.333333333333333 & 1.3333333333333333 & 0.3333333333333333 \\\\\n\\end{bmatrix} \\\\\nR2 \\leftarrow 1.0 R2 - (-1.0) R3 \\\\\n\\quad \\begin{bmatrix}\n    1.0 & 0.5 & -0.5 & 0.5 & 0 & 0 \\\\\n    0 & 1.0 & 0 & -0.666666666666667 & -0.6666666666666667 & 0.3333333333333333 \\\\\n    0 & 0 & 1.0 & 2.333333333333333 & 1.3333333333333333 & 0.3333333333333333 \\\\\n\\end{bmatrix} \\\\\nR1 \\leftarrow 1.0 R1 - (-0.5) R3 \\\\\n\\quad \\begin{bmatrix}\n    1.0 & 0.5 & 0 & 1.6666666666666665 & 0.6666666666666666 & 0.16666666666666666 \\\\\n    0 & 1.0 & 0 & -0.666666666666667 & -0.6666666666666667 & 0.3333333333333333 \\\\\n    0 & 0 & 1.0 & 2.333333333333333 & 1.3333333333333333 & 0.3333333333333333 \\\\\n\\end{bmatrix} \\\\\nR1 \\leftarrow 1.0 R1 - (0.5) R3 \\\\\n\\quad \\begin{bmatrix}\n    1.0 & 0 & 0 & 2.0 & 1.0 & 0 \\\\\n    0 & 1.0 & 0 & -0.666666666666667 & -0.6666666666666667 & 0.3333333333333333 \\\\\n    0 & 0 & 1.0 & 2.333333333333333 & 1.3333333333333333 & 0.3333333333333333 \\\\\n\\end{bmatrix} \\\\\n\\operatorname{{rref}}(A) \\\\\n\\quad \\begin{bmatrix}\n    1.0 & 0 & 0 \\\\\n    0 & 1.0 & 0 \\\\\n    0 & 0 & 1.0 \\\\\n\\end{bmatrix} \\\\\nA^{-1} \\\\\n\\quad \\begin{bmatrix}\n    2.0 & 1.0 & 0 \\\\\n    -0.666666666666667 & -0.6666666666666667 & 0.3333333333333333 \\\\\n    2.333333333333333 & 1.3333333333333333 & 0.3333333333333333 \\\\\n\\end{bmatrix} \\\\\n$$')
>>> tpl = _
>>> P, L, U, rref, A_inverse, ops_string = tpl
>>> print(ops_string)
$$
\text{Gaussian Elimination with LU Decomposition and Inverse} \\
\text{A} \\
\quad \begin{bmatrix}
    2 & 1 & -1 \\
    -3 & -2 & 2 \\
    -2 & 1 & 2 \\
\end{bmatrix} \\
\text{augmentation} \\
\quad \begin{bmatrix}
    2 & 1 & -1 & 1 & 0 & 0 \\
    -3 & -2 & 2 & 0 & 1 & 0 \\
    -2 & 1 & 2 & 0 & 0 & 1 \\
\end{bmatrix} \\
\text{permutation} \\
    \quad \text{None}\\ \\
\text{permutation-post} \\
\quad \begin{bmatrix}
    2 & 1 & -1 & 1 & 0 & 0 \\
    -3 & -2 & 2 & 0 & 1 & 0 \\
    -2 & 1 & 2 & 0 & 0 & 1 \\
\end{bmatrix} \\
R2 \leftarrow 2 R2 - (-3) R1 \\
\quad \begin{bmatrix}
    2 & 1 & -1 & 1 & 0 & 0 \\
    0 & -1 & 1 & 3 & 2 & 0 \\
    -2 & 1 & 2 & 0 & 0 & 1 \\
\end{bmatrix} \\
R3 \leftarrow 2 R3 - (-2) R1 \\
\quad \begin{bmatrix}
    2 & 1 & -1 & 1 & 0 & 0 \\
    0 & -1 & 1 & 3 & 2 & 0 \\
    0 & 4 & 2 & 2 & 0 & 2 \\
\end{bmatrix} \\
R3 \leftarrow -1 R3 - (4) R2 \\
\quad \begin{bmatrix}
    2 & 1 & -1 & 1 & 0 & 0 \\
    0 & -1 & 1 & 3 & 2 & 0 \\
    0 & 0 & -6 & -14 & -8 & -2 \\
\end{bmatrix} \\
\text{U} \\
\quad \begin{bmatrix}
    2 & 1 & -1 \\
    0 & -1 & 1 \\
    0 & 0 & -6 \\
\end{bmatrix} \\
\text{L} \\
\quad \begin{bmatrix}
    1 & 0 & 0 \\
    3 & 2 & 0 \\
    -14 & -8 & -2 \\
\end{bmatrix} \\
\text{scale} \\
R1 \leftarrow \frac{1}{2} R1 \\
R2 \leftarrow \frac{1}{-1} R2 \\
R3 \leftarrow \frac{1}{-6} R3 \\
\text{scale-post} \\
\quad \begin{bmatrix}
    1.0 & 0.5 & -0.5 & 0.5 & 0 & 0 \\
    0 & 1.0 & -1.0 & -3.0 & -2.0 & 0 \\
    0 & 0 & 1.0 & 2.333333333333333 & 1.3333333333333333 & 0.3333333333333333 \\
\end{bmatrix} \\
R2 \leftarrow 1.0 R2 - (-1.0) R3 \\
\quad \begin{bmatrix}
    1.0 & 0.5 & -0.5 & 0.5 & 0 & 0 \\
    0 & 1.0 & 0 & -0.666666666666667 & -0.6666666666666667 & 0.3333333333333333 \\
    0 & 0 & 1.0 & 2.333333333333333 & 1.3333333333333333 & 0.3333333333333333 \\
\end{bmatrix} \\
R1 \leftarrow 1.0 R1 - (-0.5) R3 \\
\quad \begin{bmatrix}
    1.0 & 0.5 & 0 & 1.6666666666666665 & 0.6666666666666666 & 0.16666666666666666 \\
    0 & 1.0 & 0 & -0.666666666666667 & -0.6666666666666667 & 0.3333333333333333 \\
    0 & 0 & 1.0 & 2.333333333333333 & 1.3333333333333333 & 0.3333333333333333 \\
\end{bmatrix} \\
R1 \leftarrow 1.0 R1 - (0.5) R3 \\
\quad \begin{bmatrix}
    1.0 & 0 & 0 & 2.0 & 1.0 & 0 \\
    0 & 1.0 & 0 & -0.666666666666667 & -0.6666666666666667 & 0.3333333333333333 \\
    0 & 0 & 1.0 & 2.333333333333333 & 1.3333333333333333 & 0.3333333333333333 \\
\end{bmatrix} \\
\operatorname{{rref}}(A) \\
\quad \begin{bmatrix}
    1.0 & 0 & 0 \\
    0 & 1.0 & 0 \\
    0 & 0 & 1.0 \\
\end{bmatrix} \\
A^{-1} \\
\quad \begin{bmatrix}
    2.0 & 1.0 & 0 \\
    -0.666666666666667 & -0.6666666666666667 & 0.3333333333333333 \\
    2.333333333333333 & 1.3333333333333333 & 0.3333333333333333 \\
\end{bmatrix} \\
$$
>>>
>>>
>>> P, L, U, rref, A_inverse, ops_string = la.gaussian_elimination(A, float=False)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: gaussian_elimination() got an unexpected keyword argument 'float'
>>> P, L, U, rref, A_inverse, ops_string = la.gaussian_elimination(A, floating=False)
>>> print(ops_string)
$$
\text{Gaussian Elimination with LU Decomposition and Inverse} \\
\text{A} \\
\quad \begin{bmatrix}
    2 & 1 & -1 \\
    -3 & -2 & 2 \\
    -2 & 1 & 2 \\
\end{bmatrix} \\
\text{augmentation} \\
\quad \begin{bmatrix}
    2 & 1 & -1 & 1 & 0 & 0 \\
    -3 & -2 & 2 & 0 & 1 & 0 \\
    -2 & 1 & 2 & 0 & 0 & 1 \\
\end{bmatrix} \\
\text{permutation} \\
    \quad \text{None}\\ \\
\text{permutation-post} \\
\quad \begin{bmatrix}
    2 & 1 & -1 & 1 & 0 & 0 \\
    -3 & -2 & 2 & 0 & 1 & 0 \\
    -2 & 1 & 2 & 0 & 0 & 1 \\
\end{bmatrix} \\
R2 \leftarrow 2 R2 - (-3) R1 \\
\quad \begin{bmatrix}
    2 & 1 & -1 & 1 & 0 & 0 \\
    0 & -1 & 1 & 3 & 2 & 0 \\
    -2 & 1 & 2 & 0 & 0 & 1 \\
\end{bmatrix} \\
R3 \leftarrow 2 R3 - (-2) R1 \\
\quad \begin{bmatrix}
    2 & 1 & -1 & 1 & 0 & 0 \\
    0 & -1 & 1 & 3 & 2 & 0 \\
    0 & 4 & 2 & 2 & 0 & 2 \\
\end{bmatrix} \\
R3 \leftarrow -1 R3 - (4) R2 \\
\quad \begin{bmatrix}
    2 & 1 & -1 & 1 & 0 & 0 \\
    0 & -1 & 1 & 3 & 2 & 0 \\
    0 & 0 & -6 & -14 & -8 & -2 \\
\end{bmatrix} \\
\text{U} \\
\quad \begin{bmatrix}
    2 & 1 & -1 \\
    0 & -1 & 1 \\
    0 & 0 & -6 \\
\end{bmatrix} \\
\text{L} \\
\quad \begin{bmatrix}
    1 & 0 & 0 \\
    3 & 2 & 0 \\
    -14 & -8 & -2 \\
\end{bmatrix} \\
\text{scale} \\
R1 \leftarrow \frac{1}{2} R1 \\
R2 \leftarrow \frac{1}{-1} R2 \\
R3 \leftarrow \frac{1}{-6} R3 \\
\text{scale-post} \\
\quad \begin{bmatrix}
    1.0 & 0.5 & -0.5 & 0.5 & 0 & 0 \\
    0 & 1.0 & -1.0 & -3.0 & -2.0 & 0 \\
    0 & 0 & 1.0 & 2.333333333333333 & 1.3333333333333333 & 0.3333333333333333 \\
\end{bmatrix} \\
R2 \leftarrow 1.0 R2 - (-1.0) R3 \\
\quad \begin{bmatrix}
    1.0 & 0.5 & -0.5 & 0.5 & 0 & 0 \\
    0 & 1.0 & 0 & -0.666666666666667 & -0.6666666666666667 & 0.3333333333333333 \\
    0 & 0 & 1.0 & 2.333333333333333 & 1.3333333333333333 & 0.3333333333333333 \\
\end{bmatrix} \\
R1 \leftarrow 1.0 R1 - (-0.5) R3 \\
\quad \begin{bmatrix}
    1.0 & 0.5 & 0 & 1.6666666666666665 & 0.6666666666666666 & 0.16666666666666666 \\
    0 & 1.0 & 0 & -0.666666666666667 & -0.6666666666666667 & 0.3333333333333333 \\
    0 & 0 & 1.0 & 2.333333333333333 & 1.3333333333333333 & 0.3333333333333333 \\
\end{bmatrix} \\
R1 \leftarrow 1.0 R1 - (0.5) R3 \\
\quad \begin{bmatrix}
    1.0 & 0 & 0 & 2.0 & 1.0 & 0 \\
    0 & 1.0 & 0 & -0.666666666666667 & -0.6666666666666667 & 0.3333333333333333 \\
    0 & 0 & 1.0 & 2.333333333333333 & 1.3333333333333333 & 0.3333333333333333 \\
\end{bmatrix} \\
\operatorname{{rref}}(A) \\
\quad \begin{bmatrix}
    1.0 & 0 & 0 \\
    0 & 1.0 & 0 \\
    0 & 0 & 1.0 \\
\end{bmatrix} \\
A^{-1} \\
\quad \begin{bmatrix}
    2.0 & 1.0 & 0 \\
    -0.666666666666667 & -0.6666666666666667 & 0.3333333333333333 \\
    2.333333333333333 & 1.3333333333333333 & 0.3333333333333333 \\
\end{bmatrix} \\
$$
>>> map elementary matrices to geometric transforms
  File "<stdin>", line 1
    map elementary matrices to geometric transforms
        ^^^^^^^^^^
SyntaxError: invalid syntax
>>>
>>>
>>>
>>>
>>> print(ops_string)
$$
\text{Gaussian Elimination with LU Decomposition and Inverse} \\
\text{A} \\
\quad \begin{bmatrix}
    2 & 1 & -1 \\
    -3 & -2 & 2 \\
    -2 & 1 & 2 \\
\end{bmatrix} \\
\text{augmentation} \\
\quad \begin{bmatrix}
    2 & 1 & -1 & 1 & 0 & 0 \\
    -3 & -2 & 2 & 0 & 1 & 0 \\
    -2 & 1 & 2 & 0 & 0 & 1 \\
\end{bmatrix} \\
\text{permutation} \\
    \quad \text{None}\\ \\
\text{permutation-post} \\
\quad \begin{bmatrix}
    2 & 1 & -1 & 1 & 0 & 0 \\
    -3 & -2 & 2 & 0 & 1 & 0 \\
    -2 & 1 & 2 & 0 & 0 & 1 \\
\end{bmatrix} \\
R2 \leftarrow 2 R2 - (-3) R1 \\
\quad \begin{bmatrix}
    2 & 1 & -1 & 1 & 0 & 0 \\
    0 & -1 & 1 & 3 & 2 & 0 \\
    -2 & 1 & 2 & 0 & 0 & 1 \\
\end{bmatrix} \\
R3 \leftarrow 2 R3 - (-2) R1 \\
\quad \begin{bmatrix}
    2 & 1 & -1 & 1 & 0 & 0 \\
    0 & -1 & 1 & 3 & 2 & 0 \\
    0 & 4 & 2 & 2 & 0 & 2 \\
\end{bmatrix} \\
R3 \leftarrow -1 R3 - (4) R2 \\
\quad \begin{bmatrix}
    2 & 1 & -1 & 1 & 0 & 0 \\
    0 & -1 & 1 & 3 & 2 & 0 \\
    0 & 0 & -6 & -14 & -8 & -2 \\
\end{bmatrix} \\
\text{U} \\
\quad \begin{bmatrix}
    2 & 1 & -1 \\
    0 & -1 & 1 \\
    0 & 0 & -6 \\
\end{bmatrix} \\
\text{L} \\
\quad \begin{bmatrix}
    1 & 0 & 0 \\
    3 & 2 & 0 \\
    -14 & -8 & -2 \\
\end{bmatrix} \\
\text{scale} \\
R1 \leftarrow \frac{1}{2} R1 \\
R2 \leftarrow \frac{1}{-1} R2 \\
R3 \leftarrow \frac{1}{-6} R3 \\
\text{scale-post} \\
\quad \begin{bmatrix}
    1.0 & 0.5 & -0.5 & 0.5 & 0 & 0 \\
    0 & 1.0 & -1.0 & -3.0 & -2.0 & 0 \\
    0 & 0 & 1.0 & 2.333333333333333 & 1.3333333333333333 & 0.3333333333333333 \\
\end{bmatrix} \\
R2 \leftarrow 1.0 R2 - (-1.0) R3 \\
\quad \begin{bmatrix}
    1.0 & 0.5 & -0.5 & 0.5 & 0 & 0 \\
    0 & 1.0 & 0 & -0.666666666666667 & -0.6666666666666667 & 0.3333333333333333 \\
    0 & 0 & 1.0 & 2.333333333333333 & 1.3333333333333333 & 0.3333333333333333 \\
\end{bmatrix} \\
R1 \leftarrow 1.0 R1 - (-0.5) R3 \\
\quad \begin{bmatrix}
    1.0 & 0.5 & 0 & 1.6666666666666665 & 0.6666666666666666 & 0.16666666666666666 \\
    0 & 1.0 & 0 & -0.666666666666667 & -0.6666666666666667 & 0.3333333333333333 \\
    0 & 0 & 1.0 & 2.333333333333333 & 1.3333333333333333 & 0.3333333333333333 \\
\end{bmatrix} \\
R1 \leftarrow 1.0 R1 - (0.5) R3 \\
\quad \begin{bmatrix}
    1.0 & 0 & 0 & 2.0 & 1.0 & 0 \\
    0 & 1.0 & 0 & -0.666666666666667 & -0.6666666666666667 & 0.3333333333333333 \\
    0 & 0 & 1.0 & 2.333333333333333 & 1.3333333333333333 & 0.3333333333333333 \\
\end{bmatrix} \\
\operatorname{{rref}}(A) \\
\quad \begin{bmatrix}
    1.0 & 0 & 0 \\
    0 & 1.0 & 0 \\
    0 & 0 & 1.0 \\
\end{bmatrix} \\
A^{-1} \\
\quad \begin{bmatrix}
    2.0 & 1.0 & 0 \\
    -0.666666666666667 & -0.6666666666666667 & 0.3333333333333333 \\
    2.333333333333333 & 1.3333333333333333 & 0.3333333333333333 \\
\end{bmatrix} \\
$$
>>>