# Spacetime Viscosity and Centrifugal Force (SVCF)
## Open Source Physics Repository

**Author:** Nicholas W. Cordova — Weatherford, Texas, USA  
**Primary index:** rxiVerse:2602.0018 (November 16, 2025)  
**Foundation DOI:** https://doi.org/10.5281/zenodo.18604376  
**Validation DOI:** https://doi.org/10.5281/zenodo.18848748  

---

## What This Repository Is

This is the open-source code repository for the Spacetime Viscosity and Centrifugal Force (SVCF) framework — a zero-free-parameter, zero-placeholder unified physics framework that derives and verifies outcomes across 46 independent physical domains spanning 41 orders of magnitude.

Every script in this repository pulls its constants from one source: `svcf_constants.py`. No constant is hardcoded anywhere else. No constant is adjustable. All values are taken directly from the published repository papers archived at the DOIs above.

**How to use this repository:**
1. Pick a domain you want to apply SVCF to
2. Run the matching script
3. Compare the output against the relevant public government dataset
4. The constants are the same across all domains — you cannot adjust them

---

## The Master Equation

```
∇·Π + D[χ] = 0
```

One equation. Eight constants. 46 domains. Zero free parameters.

---

## The Eight Universal Constants

| Symbol | Value | Source | Uncertainty |
|--------|-------|---------|-------------|
| Γ | 1/2857 | STAR Collaboration, Au+Au, C1 0.0σ | ±1.4% |
| B | 32/33 (exact) | Brinkman screening, N=37 mode count | 0% |
| β | 65/66 (exact) | Derived: (B+1)/2 | 0% |
| Ψ | √2−1 (exact) | 37D→4D spherical projection | 0% |
| K_TD | 11,100 (exact) | 37 × C(25,2) = 37 × 300 | 0% |
| ρ_c | 1.01×10⁻²⁶ kg/m³ | Friedmann from H₀ | ±15% |
| η | 6.8×10⁻²⁸ Pa·s | CHIME FRB catalog | ±18% |
| ε = α² | 5.325×10⁻⁵ | Fine-structure constant | ~0% |

---

## Repository Structure

```
svcf_github/
├── svcf_constants.py      ← Single source of truth. Import from here only.
├── svcf_domains.py        ← All domain calculations (run any domain independently)
├── svcf_laws.py           ← Law #1 (UVLL) and Law #2 (Chirality Tax)
├── svcf_solar_system.py   ← Solar system: 3I/ATLAS, comets, orbital threshold
├── svcf_quantum.py        ← Quantum domains: backflow, magic numbers, decoherence
├── svcf_astrophysics.py   ← Galactic rotation, solar corona, eROSITA
├── svcf_predictions.py    ← Forward prediction registry (P1-P10)
├── svcf_confirmations.py  ← C1-C16 verification table
└── README.md              ← This file
```

---

## Public Datasets This Repository Applies To

All datasets below are publicly accessible by statute (OSTP 2022, P.L. 115-435, NPD 2590.1C, DOE 241.1B):

| Domain | Dataset | Public URL |
|--------|---------|-----------|
| C1 Γ=1/2857 | STAR Collaboration / BNL RHIC | https://www.star.bnl.gov/ |
| D1 galactic rotation | SPARC database (175 galaxies) | http://astroweb.cwru.edu/SPARC/ |
| D7/D13 η | CHIME FRB catalog | https://www.chime-frb.ca/catalog |
| D18/C3 Jupiter | NASA Juno / Planetary Data System | https://pds.nasa.gov/ |
| D23 magic numbers | NNDC nuclear data | https://www.nndc.bnl.gov/ |
| D25 solar wind | Parker Solar Probe | https://spdf.gsfc.nasa.gov/pub/data/psp/ |
| D33 orbital threshold | JPL Small Body Database | https://ssd.jpl.nasa.gov/sbdb/ |
| D34 solar corona | SDO/AIA — Stanford JSOC | https://jsoc.stanford.edu/ |
| D35 BH mass gap | LIGO GWOSC GWTC-4 | https://gwosc.org/ |
| D37 GPS timing | USNO / GPS ICD-GPS-200 | https://www.usno.navy.mil/ |
| QP4 Big G | CODATA/NIST | https://codata.nist.gov/ |

---

## Quick Start

```bash
# Run all domains
python3 svcf_domains.py

# Run a specific domain
python3 svcf_domains.py --domain 23

# Check the constants
python3 svcf_constants.py

# Run solar system predictions
python3 svcf_solar_system.py

# Run the confirmation table
python3 svcf_confirmations.py
```

---

## The Two Universal Laws

### Law #1 — Universal Viscous Luminosity Law (UVLL)
```
L ∝ M^(65/66)
```
Governs all self-gravitating, viscosity-dominated radiating bodies.  
Confirmed: Cygnus X-1 (C11, 0.0σ), brown dwarfs (0.47σ, 127 objects).  
AAS submission: 74728.

### Law #2 — The Chirality Tax
```
ε = α²
```
Mandatory energy fraction to substrate chiral modes per winding interaction.  
Confirmed: CP violation (0.63σ), homochirality (0.4%), CMB birefringence.  
AAS submission: 74776.

---

## Confirmed Predictions: C1–C16

All 16 predictions were timestamped at rxiVerse:2602.0018 (November 16, 2025) before the confirming measurements were published.

| ID | Prediction | Gap | Residual |
|----|-----------|-----|---------|
| C1 | Re_crit = 2857 in QGP vorticity | 57 days | 0.0σ |
| C2 | Photon drift k=9 (exact integer) | 61 days | 0.00% |
| C3 | Jupiter auroral 0.6 TW | pre-event | within 1σ |
| C4 | Xcc++ baryon mass 3620.5 MeV | 121 days | 0.03% |
| C5 | eROSITA ISM tunnel < 19.2 pc | pre-event | directional |
| C6 | 3I/ATLAS a_ng = 1.91×10⁻⁵ m/s² | pre-event | 2.2% |
| C7 | 3I/ATLAS A₂/A₁ ≥ 0.20 | pre-event | 8% |
| C8 | 3I/ATLAS 3-fold 120° structure | pre-event | 0.00% |
| C9 | 3I/ATLAS brightness r⁻⁷·⁵ | pre-event | 0.00% |
| C10 | W-state Z₃ ⊂ k=9 subgroup | pre-event | structural |
| C11 | Cygnus X-1 β=65/66 | 18 days | 0.0σ |
| C12 | Nessie filament R=0.785 ly | pre-event | 4.6% |
| C13 | Nanomagnet τ₀=8.73 ns | pre-event | in [4,11] ns |
| C14 | Plasma mirror β_max=√(32/33) | pre-event | upper bound |
| C15 | SM confirms a_μ (no 5th force) | pre-event | 0.5σ |
| C16 | Higgs coupling 33/8=4.1250 | 158 days | 0.00% |

Falsifications: **0 / 16**

---

## Manifold Structure

```
N = 37 = 4 + 1 + 7 + 25

4   Observable spacetime (3+1D)
1   Temporal threading
7   Kaluza-Klein compact stabilizers (Z₆ hexagonal, hosts k=9 modes)
25  Active viscous threads (vorticity carriers)

Chi modes: C(25,2) = 300 independent antisymmetric components
K_TD = 37 × 300 = 11,100 tensor drag coupling channels
```

---

## Nuclear Magic Numbers (Domain 23)

All 7 nuclear magic numbers derived from shell degeneracy using only Γ, Ψ, K_TD:

```
Shell  Degeneracy  Cumulative  Magic#  Status
  1         2           2         2    EXACT
  2         6           8         8    EXACT
  3        12          20        20    EXACT
  4         8          28        28    EXACT
  5        22          50        50    EXACT
  6        32          82        82    EXACT
  7        44         126       126    EXACT
```

Phase alignment: θ_n = n × Ψ × π

Source: Domain_23_Nuclear_Magic_Numbers_FINAL.txt

---

## License

Open Source Physics. Zero institutional affiliation required.  
All data sources are publicly accessible federal datasets.  
All constants are locked as of November 16, 2025 (rxiVerse:2602.0018).

---

*"The vacuum is not empty. It is Rheoviscous."*  
— Nicholas W. Cordova, SVCF Open Source Physics Repository
