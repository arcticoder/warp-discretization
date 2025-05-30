#!/usr/bin/env python3
"""
Generates finite-difference spatial stencils and truncation-error expansions
from the warp-bubble expressions in final_expressions.tex.
"""

import sympy as sp
from sympy.parsing.latex import parse_latex
import argparse
import re
import os

def extract_expressions(tex):
    """Extract all display-math LaTeX expressions between \\[ and \\]."""
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
            # Clean up the expression string
            s = s.strip()
            # Skip if it's an equation (contains =)
            if '=' in s:
                # Try to extract the right-hand side of the equation
                parts = s.split('=')
                if len(parts) >= 2:
                    s = parts[-1].strip()  # Take the last part (RHS)
                else:
                    continue
            
            sym_expr = parse_latex(s)
            
            # Check if the expression contains spatial variables
            free_symbols = sym_expr.free_symbols
            relevant_vars = [var for var in spatial_vars if var in free_symbols]
            
            if relevant_vars:
                for var in relevant_vars:
                    try:
                        stencil2, err2 = generate_central_diff(sym_expr, var, order=2)
                        stencil4, err4 = generate_central_diff(sym_expr, var, order=4)
                        stencils.append((sp.diff(sym_expr, var), stencil2, err2, var, "2nd order"))
                        stencils.append((sp.diff(sym_expr, var), stencil4, err4, var, "4th order"))
                    except Exception as e:
                        print(f"Warning: Could not generate stencil for {var}: {e}")
                        
        except Exception as e:
            print(f"Warning: Could not parse expression: {s[:50]}...: {e}")
            continue

    # Create stencils directory
    stencils_dir = "stencils"
    os.makedirs(stencils_dir, exist_ok=True)

    # Write out LaTeX document
    with open(args.output, 'w') as f:
        f.write(r"\documentclass{article}" + "\n")
        f.write(r"\usepackage{amsmath}" + "\n")
        f.write(r"\usepackage[margin=0.5in]{geometry}" + "\n")
        f.write(r"\begin{document}" + "\n\n")
        f.write(r"\section*{Finite Difference Stencils}" + "\n\n")
        
        for i, (deriv, stencil, err, var, order) in enumerate(stencils):
            f.write(f"% {order} derivative w.r.t. {var}\n")
            f.write(r"\[" + "\n")
            f.write(sp.latex(deriv) + " \\approx " + sp.latex(stencil) +
                    r" \quad (" + err + r")" + "\n")
            f.write(r"\]" + "\n\n")
            
            # Write individual stencil file
            var_name = str(var)
            order_name = order.replace(" ", "_")
            stencil_filename = os.path.join(stencils_dir, f"stencil_{var_name}_{order_name}_{i+1:03d}.tex")
            with open(stencil_filename, 'w') as stencil_file:
                stencil_file.write(r"\documentclass{article}" + "\n")
                stencil_file.write(r"\usepackage{amsmath}" + "\n")
                stencil_file.write(r"\usepackage[margin=0.5in]{geometry}" + "\n")
                stencil_file.write(r"\begin{document}" + "\n\n")
                stencil_file.write(f"\\section*{{Finite Difference Stencil: {order} derivative w.r.t. ${var_name}$}}\n\n")
                stencil_file.write(f"% Original derivative: {sp.latex(deriv)}\n")
                stencil_file.write(f"% Variable: {var_name}\n")
                stencil_file.write(f"% Order: {order}\n")
                stencil_file.write(f"% Error order: {err}\n\n")
                stencil_file.write(r"\[" + "\n")
                stencil_file.write(sp.latex(deriv) + " \\approx " + sp.latex(stencil) +
                                 r" \quad (" + err + r")" + "\n")
                stencil_file.write(r"\]" + "\n\n")
                stencil_file.write(r"\end{document}" + "\n")
        
        f.write(r"\end{document}")

    print(f"Wrote discretization document to {args.output}")
    print(f"Wrote {len(stencils)} individual stencil files to {stencils_dir}/ directory")

if __name__ == "__main__":
    main()
