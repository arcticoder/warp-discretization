# Warp Bubble Discretization

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![SymPy](https://img.shields.io/badge/SymPy-Latest-green.svg)](https://sympy.org)
[![LaTeX](https://img.shields.io/badge/LaTeX-Required-red.svg)](https://latex-project.org)

**Automated finite-difference stencil generation for warp bubble spacetime discretization**

This repository provides computational tools to generate finite-difference stencils and truncation-error expansions for spatial derivatives in warp-bubble spacetime expressions, enabling numerical simulation of exotic spacetime geometries.

## Key Features

- **Finite-Difference Stencils**: Automated generation of central difference formulas (2nd, 4th, 6th order)
- **Error Analysis**: Complete Taylor-series truncation error characterization
- **LaTeX Output**: Publication-ready discretization documentation
- **SymPy Integration**: Symbolic mathematics for exact coefficient computation
- **Pipeline Ready**: Integrates seamlessly with upstream warp-bubble repositories

## Mathematical Framework

The tool processes closed-form warp-bubble expressions to generate numerical discretization schemes:

### Input: Analytic Expressions
- **Metric Components**: g_μν(x) from warp-bubble geometry
- **Curvature Invariants**: R, R_μν R^μν, Riemann tensor components  
- **Stress-Energy Tensor**: T_μν(x) exotic matter distributions
- **Source**: `final_expressions.tex` from upstream pipeline

### Output: Discretization Schemes
- **Spatial Derivative Stencils**: Central finite-difference formulas for ∇_i, ∇_i∇_j operators
- **Error Order Expansions**: Complete O(h²), O(h⁴), O(h⁶) truncation analysis
- **Coefficient Tables**: Exact symbolic coefficients for each stencil point
- **LaTeX Documentation**: Ready-to-compile discretization.tex with all formulas

### Supported Orders
- **2nd Order**: O(h²) accuracy, 3-point stencils
- **4th Order**: O(h⁴) accuracy, 5-point stencils  
- **6th Order**: O(h⁶) accuracy, 7-point stencils
- **Custom**: User-configurable stencil orders and grid arrangements

## 🔧 Installation & Setup

### Prerequisites
```bash
# Core dependencies
pip install sympy>=1.9 numpy scipy matplotlib

# LaTeX distribution (for output compilation)
# Ubuntu/Debian: sudo apt-get install texlive-full
# macOS: brew install mactex
# Windows: Install MiKTeX or TeX Live
```

### Repository Setup
```bash
git clone https://github.com/arcticoder/warp-discretization.git
cd warp-discretization
pip install -r requirements.txt
```

## 🚀 Usage Guide

### Basic Stencil Generation
```bash
# Generate all discretization stencils
python scripts/generate_stencils.py --input final_expressions.tex --output discretization.tex

# Specify stencil order
python scripts/generate_stencils.py --input final_expressions.tex --output discretization.tex --order 4

# Generate with error analysis
python scripts/generate_stencils.py --input final_expressions.tex --output discretization.tex --error-analysis
```

### Advanced Options
```bash
# Custom grid spacing
python scripts/generate_stencils.py --input final_expressions.tex --spacing-symbol "Delta_x"

# Export individual stencils
python scripts/generate_stencils.py --input final_expressions.tex --export-individual --output-dir stencils/

# Generate validation code
python scripts/generate_stencils.py --input final_expressions.tex --generate-tests
```

## 📁 Output Structure

```
discretization.tex          # Main LaTeX document with all stencils
stencils/                   # Individual stencil files (optional)
├── first_derivatives.tex   # ∂/∂x, ∂/∂y, ∂/∂z stencils
├── second_derivatives.tex  # ∂²/∂x², ∂²/∂y², ∂²/∂z² stencils
├── mixed_derivatives.tex   # ∂²/∂x∂y, etc. stencils
└── error_analysis.tex      # Truncation error bounds
```

## 🔗 Pipeline Integration

This repository is part of the comprehensive warp-bubble simulation pipeline:

### Upstream Dependencies
- **[warp-bubble-assemble-expressions](../warp-bubble-assemble-expressions)**: Provides `final_expressions.tex`
- **[warp-bubble-einstein-equations](../warp-bubble-einstein-equations)**: Stress-energy tensor T_μν
- **[warp-bubble-exotic-matter-density](../warp-bubble-exotic-matter-density)**: Energy density analysis

### Downstream Applications  
- **[warp-solver-equations](../warp-solver-equations)**: Time integration schemes
- **[warp-solver-validation](../warp-solver-validation)**: Numerical validation framework
- **Numerical relativity codes**: Grid-based spacetime evolution

### Data Flow
```
Analytic Expressions → Finite-Difference Stencils → Time Integration → Validation
```

## 🧪 Validation & Testing

### Automated Tests
```bash
# Run all validation tests
python -m pytest tests/ -v

# Test stencil accuracy
python tests/test_stencil_accuracy.py

# Validate error bounds
python tests/test_error_analysis.py
```

### Benchmarking
```bash
# Compare with analytical derivatives
python scripts/benchmark_accuracy.py

# Performance profiling
python scripts/profile_generation.py
```

## 📖 Mathematical Details

### Finite-Difference Formulas
For a scalar field f(x), the nth-order central difference approximation:

```
f'(x) ≈ (1/h) Σ c_i f(x + ih)    [2nd order: c = [-1/2, 0, 1/2]]
f''(x) ≈ (1/h²) Σ c_i f(x + ih)   [2nd order: c = [1, -2, 1]]
```

### Error Analysis
Truncation error bounds for each stencil:
```
|Error| ≤ (h^p/p!) max|f^(p)(ξ)|    where p = order + 1
```

### Grid Considerations
- **Uniform spacing**: h = constant throughout domain
- **Boundary handling**: One-sided and modified stencils near boundaries
- **Stability analysis**: CFL conditions for time-stepping schemes

## 🎯 Applications

- **Numerical Relativity**: Spacetime evolution simulations
- **Warp Drive Research**: Exotic matter field dynamics
- **Computational Physics**: General PDE discretization
- **Algorithm Development**: Finite-difference method validation

## 🤝 Contributing

Contributions welcome! Areas of interest:
- Higher-order stencil implementations
- Adaptive grid refinement support
- GPU acceleration for large-scale problems
- Integration with finite element methods

## 📚 References

1. **Finite Difference Methods**: LeVeque, R. J., "Finite Difference Methods for ODEs and PDEs"
2. **Numerical Relativity**: Baumgarte & Shapiro, "Numerical Relativity: Solving Einstein's Equations on the Computer"
3. **Warp Drive Physics**: Alcubierre, M., Phys. Rev. D 53, 3571 (1994)

---

⭐ **Star this repository** if you find it useful for your numerical simulations!
