"""
svcf_constants.py
SPACETIME VISCOSITY AND CENTRIFUGAL FORCE
Open Source Physics Repository

rxiVerse:2602.0018  (November 16, 2025)
Zenodo: 10.5281/zenodo.18604376
Zenodo: 10.5281/zenodo.18848748
Author: Nicholas W. Cordova, Weatherford TX

All values taken directly from the published repository.
No derivation is performed here. These are the locked constants.
Every domain script imports from this file and nowhere else.
"""

import numpy as np

# ── SVCF FRAMEWORK CONSTANTS (locked, zero free parameters) ──────────────────

# Vacuum viscosity / dissipation eigenvalue
# Source: STAR Collaboration, Re_crit = 2857±43, Nature Jan 12 2026 (C1, 0.0 sigma)
# VINCERE_TABLE.txt: "STAR Reynolds Number: 2857 | 0.0sigma"
GAMMA     = 1.0 / 2857.0          # dimensionless dissipation eigenvalue
RE_CRIT   = 2857.0                 # critical Reynolds number (= 1/GAMMA)

# Compact dimension curvature / bulk saturation
# Source: SVCF_Repository_Master.md, SVCF_26_Domains_Summary.txt
B         = 32.0 / 33.0            # B = 0.96969...

# Viscous luminosity exponent (Law #1)
# Source: SVCF_Law1_UVLL_Repository_FINAL.pdf, AAS submission 74728
BETA      = 65.0 / 66.0            # beta = (B+1)/2 = 65/66

# Chirality / hoop stress constant
# Source: SVCF_Repository_Master.md: "Ψ = √2−1 = 0.414"
PSI       = np.sqrt(2.0) - 1.0     # Psi = 0.41421356...

# Tensor drag coupling
# Source: SVCF_Repository_Master.md: "N_chi = C(25,2) = 300", K_TD = 37 x 300
# Domain_23: "K_TD = 37 × 300 = 11,100"
K_TD      = 37 * 300               # = 11100

# Substrate density
# Source: VINCERE_TABLE.txt: "rho_c from H0 = 1.01e-26 kg/m^3 | Friedmann exact"
# SVCF_26_Domains_Summary.txt confirms
RHO_C     = 1.01e-26               # kg/m^3

# Dynamic viscosity
# Source: SVCF_Repository_Master.md, FRB catalog measurement
ETA       = 6.8e-28                # Pa.s

# Kinematic viscosity (derived)
NU        = ETA / RHO_C            # m^2/s

# Harmonic mode number
# Source: SVCF_Repository_Master.md Section 1.1: "k=9"
# Confirmed: St-Jean PRX Jan 7 2026 (C2, 0.00%)
K_MODE    = 9                      # exact integer

# Chirality tax (Law #2)
# Source: SVCF_Law2_Chirality_Tax_Law_FINAL.pdf, AAS submission 74776
ALPHA_FS  = 1.0 / 137.035999084   # fine structure constant (CODATA 2018)
EPSILON   = ALPHA_FS**2            # epsilon = alpha^2 = 5.325e-5

# ── STANDARD PHYSICAL CONSTANTS (CODATA 2018) ────────────────────────────────

C_LIGHT   = 2.99792458e8           # m/s
HBAR      = 1.054571817e-34        # J.s
G_NEWTON  = 6.67430e-11            # m^3 kg^-1 s^-2
K_BOLTZ   = 1.380649e-23           # J/K
M_SUN     = 1.98892e30             # kg
AU        = 1.495978707e11         # m
PC        = 3.085677581e16         # m  (parsec)
KPC       = 3.085677581e19         # m  (kiloparsec)
LY        = 9.4607304725808e15     # m  (light year)
M_PROTON  = 1.67262192369e-27      # kg
M_ELECTRON= 9.1093837015e-31       # kg

# ── MANIFOLD STRUCTURE ───────────────────────────────────────────────────────
# Source: SVCF_Repository_Master.md Section 1.1
# "4 observable + 1 temporal + 7 compact + 25 active = 37"

N_TOTAL     = 37
N_OBSERVABLE= 4
N_TEMPORAL  = 1
N_COMPACT   = 7
N_ACTIVE    = 25
N_CHI_MODES = 300    # C(25,2) = 25*24/2 = 300 independent chi modes
N_INTERNAL  = 33     # dim(Ker P) = 1+7+25 = 33

# ── NUCLEAR MAGIC NUMBERS (Domain 23) ────────────────────────────────────────
# Source: Domain_23_Nuclear_Magic_Numbers_FINAL.txt
# Shell degeneracy: d_n = {2, 6, 12, 8, 22, 32, 44}
# Phase alignment: theta_n = n * PSI * pi

SHELL_DEGENERACY = [2, 6, 12, 8, 22, 32, 44]  # d_n for shells n=1..7
MAGIC_NUMBERS    = [2, 8, 20, 28, 50, 82, 126] # cumulative sums
# Verification: cumsum([2,6,12,8,22,32,44]) = [2,8,20,28,50,82,126]

# ── QUICK REFERENCE PRINT ────────────────────────────────────────────────────

def print_constants():
    print("=" * 60)
    print("SVCF UNIVERSAL CONSTANTS")
    print("rxiVerse:2602.0018  |  Nov 16, 2025")
    print("=" * 60)
    print(f"  GAMMA    = 1/2857  = {GAMMA:.8e}  (Re_crit = {RE_CRIT})")
    print(f"  B        = 32/33   = {B:.10f}")
    print(f"  BETA     = 65/66   = {BETA:.10f}  (Law #1 exponent)")
    print(f"  PSI      = sqrt(2)-1 = {PSI:.10f}")
    print(f"  K_TD     = 37x300  = {K_TD}")
    print(f"  RHO_C    = {RHO_C:.3e} kg/m^3")
    print(f"  ETA      = {ETA:.3e} Pa.s")
    print(f"  NU       = {NU:.6e} m^2/s  (= ETA/RHO_C)")
    print(f"  K_MODE   = {K_MODE}  (harmonic mode, exact integer)")
    print(f"  EPSILON  = alpha^2 = {EPSILON:.6e}  (Law #2)")
    print(f"  ALPHA_FS = {ALPHA_FS:.9f}  (fine structure constant)")
    print()
    print("  Manifold: N=37 = 4+1+7+25")
    print(f"  Chi modes: C(25,2) = {N_CHI_MODES}")
    print(f"  Kernel dim: {N_INTERNAL}")
    print()
    print("  Magic numbers:", MAGIC_NUMBERS)
    print("  Shell degeneracy:", SHELL_DEGENERACY)
    print("  Algebraic checks:")
    print(f"    33*B - 32 = {33*B - 32:.2e}  (should be 0)")
    print(f"    PSI^2+2*PSI-1 = {PSI**2+2*PSI-1:.2e}  (should be 0)")
    print(f"    BETA = (B+1)/2 = {(B+1)/2:.10f}  (matches BETA: {(B+1)/2 == BETA})")
    print(f"    sum(SHELL_DEGENERACY) = {sum(SHELL_DEGENERACY)} = {MAGIC_NUMBERS[-1]}")
    import numpy as np
    cs = list(np.cumsum(SHELL_DEGENERACY))
    print(f"    cumsum = {[int(x) for x in cs]}")
    print(f"    matches MAGIC_NUMBERS: {[int(x) for x in cs] == MAGIC_NUMBERS}")
    print("=" * 60)


if __name__ == "__main__":
    print_constants()
