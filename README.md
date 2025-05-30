# warp-discretization

A tool to generate finite-difference stencils and truncation-error expansions for all spatial derivatives appearing in warp-bubble metric, curvature and stress–energy expressions.

## Overview

This repo consumes the analytic results in `final_expressions.tex`—including metric components \(g_{\mu\nu}(x)\), curvature invariants \(R\), \(R_{\mu\nu}R^{\mu\nu}\), and stress–energy tensor \(T_{\mu\nu}(x)\)—and produces:

- **Spatial‐derivative stencils**  
  Central finite-difference formulas (2nd-order, 4th-order, etc.) for each nonzero spatial derivative of \(g_{ij}(x)\).
- **Error‐order expansions**  
  Taylor-series truncation errors (e.g. \(\mathcal{O}(h^2)\), \(\mathcal{O}(h^4)\)) for each stencil.
- **discretization.tex**  
  A standalone LaTeX document listing each stencil with its exact symbolic coefficients and error-order annotation.

## Prerequisites

- Python 3.8 or higher  
- [Sympy](https://www.sympy.org/)  
- A LaTeX distribution to compile the output (optional, for preview)

## Installation

```bash
git clone https://github.com/arcticoder/warp-discretization.git
cd warp-discretization
pip install -r requirements.txt
```

## Usage

```bash
python scripts/generate_stencils.py --input final_expressions.tex --output discretization.tex
```

-   `--input` should point to your local copy of `final_expressions.tex`.
    
-   `--output` is the generated LaTeX file containing all derivative approximations.
    

## Outputs

-   `discretization.tex`
    
-   (Optional) `stencils/` directory with individual stencil definitions in separate files.
