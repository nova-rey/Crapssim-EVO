"""
Stub data models for Spec, DNA, PopulationManifest, BundleMeta.
Fields will be expanded once CSC spec is finalized.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional

@dataclass
class Spec:
    schema_version: str = "1.0"
    profile_id: str = ""
    params: Dict[str, float] = field(default_factory=dict)
    toggles: Dict[str, bool] = field(default_factory=dict)
    identity: Dict[str, str] = field(default_factory=dict)

@dataclass
class DNA:
    evo_schema_version: str = "0.1"
    gen_id: str = ""
    candidate_id: str = ""
    mode: str = "NORMAL"
    parents: List[Dict[str, str]] = field(default_factory=list)
    ops: List[str] = field(default_factory=list)
    rng: Dict[str, int] = field(default_factory=dict)
    trial_cohort: bool = False
    grace_remaining: int = 0
    hashes: Dict[str, str] = field(default_factory=dict)

@dataclass
class PopulationManifest:
    evo_schema_version: str = "0.1"
    gen_id: str = ""
    mode: str = "NORMAL"
    los: Optional[float] = None
    trigger: Optional[str] = None
    pop_size: Optional[int] = None
    elite_k: Optional[int] = None
    objectives: List[str] = field(default_factory=list)
    candidates: List[Dict[str, str]] = field(default_factory=list)

@dataclass
class BundleMeta:
    bundle_schema_version: str = "1.0"
    producer: str = ""
    run_id: str = ""
    format: str = "zip"
    created_utc: str = ""
    contents: Dict[str, str] = field(default_factory=dict)
    schemas: Dict[str, str] = field(default_factory=dict)
