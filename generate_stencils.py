#!/usr/bin/env python3
"""
Generates finite-difference spatial stencils and truncation-error expansions
from the warp-bubble expressions in final_expressions.tex.
"""

import sympy as sp
from sympy.parsing.latex import parse_latex
import argparse
import re

def extract_expressions(tex):
    """Extract all display-math LaTeX expressions between \[ and \]."""
    return re.findall(r'\\\[(.*?)\\\]', tex, re.DOTALL)

def generate_central_diff(expr, var, order=2):
    """Generate a central finite-difference stencil for derivative wrt var."""
    h = sp.symbols('h')
    if order == 2:
        stencil = (expr.subs(var, var+h) - expr.subs(var, var-h)) / (2*h)
        error = 'O(h^2)'
    elif order == 4:
        stencil = (-expr.subs(var, var+2*h) + 8*expr.subs(var, var+h)
                   - 8*expr.subs(var, var-h) + expr.subs(var, var-2*h)) / (12*h)
        error = 'O(h^4)'
    else:
        raise ValueError("Unsupported stencil order: {}".format(order))
    return sp.simplify(stencil), error

def main():
    parser = argparse.ArgumentParser(
        description="Generate finite-difference stencils from LaTeX expressions"
    )
    parser.add_argument('--input', '-i', required=True,
                        help="Path to final_expressions.tex")
    parser.add_argument('--output', '-o', required=True,
                        help="Path to write discretization.tex")
    args = parser.parse_args()

    with open(args.input, 'r') as f:
        tex = f.read()

    expr_strs = extract_expressions(tex)

    # Define coordinates
    r, theta, phi, t = sp.symbols('r theta phi t')
    spatial_vars = [r, theta, phi]

    stencils = []
    for s in expr_strs:
        try:
            sym_expr = parse_latex(s)
        except Exception as e:
            print(f"Warning: Could not parse expression: {s[:30]}...: {e}")
            continue
        for var in spatial_vars:
            stencil2, err2 = generate_central_diff(sym_expr, var, order=2)
            stencils.append((sp.diff(sym_expr, var), stencil2, err2))

    # Write out LaTeX document
    with open(args.output, 'w') as f:
        f.write(r"\documentclass{article}\n")
        f.write(r"\usepackage{amsmath}\n")
        f.write(r"\begin{document}\n\n")
        for deriv, stencil, err in stencils:
            f.write(r"\[
")
            f.write(sp.latex(deriv) + " &\approx " + sp.latex(stencil) +
                    r" \quad (" + err + r")
")
            f.write(r"\]

")
        f.write(r"\end{document}")

    print(f"Wrote discretization document to {args.output}")

if __name__ == "__main__":
    main()
