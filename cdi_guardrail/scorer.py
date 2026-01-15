# cdi_guardrail/scorer.py

def compute_cdi(
    internal_pressure,
    boundary_violation,
    eps: float = 1e-12
):
    """
    Consistency Deviation Index

    CDI = P_internal / (P_internal + Boundary)
    """
    return internal_pressure / (internal_pressure + boundary_violation + eps)
