"""
🜏 Pareto Language Syntax Definitions 🜏

This module defines the syntax for the pareto-lang interpretability command language.
It provides the command families, functions, parameter types, and validators used
by the parser to validate and interpret pareto-lang commands.

The language follows a structured hierarchy:
- Command Families: High-level categories (reflect, fork, collapse, etc.)
- Functions: Specific operations within each family (trace, attribution, etc.)
- Parameters: Configuration for each function (depth, target, etc.)

This syntax definition serves as the Rosetta Stone for the interpretability framework,
establishing the grammar through which model introspection occurs.

.p/reflect.meta{level=language, target=self}
.p/collapse.prevent{trigger=self_reference, threshold=7}
"""

from typing import Any, Callable, Dict, List, Optional, Union


# Parameter type validators
def _validate_string(value: Any) -> bool:
    """Validate string parameter type."""
    return isinstance(value, str)

def _validate_boolean(value: Any) -> bool:
    """Validate boolean parameter type."""
    return isinstance(value, bool)

def _validate_integer(value: Any) -> bool:
    """Validate integer parameter type."""
    return isinstance(value, int) and not isinstance(value, bool)

def _validate_float(value: Any) -> bool:
    """Validate float parameter type."""
    return isinstance(value, (int, float)) and not isinstance(value, bool)

def _validate_list(value: Any) -> bool:
    """Validate list parameter type."""
    return isinstance(value, list)

def _validate_string_or_int(value: Any) -> bool:
    """Validate string or integer parameter type."""
    return isinstance(value, (str, int)) and not isinstance(value, bool)

def _validate_any(value: Any) -> bool:
    """Validate any parameter type."""
    return True


# Parameter type definitions
PARAMETER_TYPES = {
    "string": _validate_string,
    "boolean": _validate_boolean,
    "integer": _validate_integer,
    "float": _validate_float,
    "list": _validate_list,
    "string_or_int": _validate_string_or_int,
    "any": _validate_any,
}


# Custom parameter validators
def _validate_depth(value: Any) -> bool:
    """Validate depth parameter."""
    if isinstance(value, str) and value == "complete":
        return True
    if isinstance(value, int) and value > 0:
        return True
    return False

def _validate_positive_float(value: Any) -> bool:
    """Validate positive float parameter."""
    return isinstance(value, (int, float)) and value > 0

def _validate_threshold(value: Any) -> bool:
    """Validate threshold parameter."""
    return isinstance(value, (int, float)) and 0 <= value <= 1


# Custom parameter validators by command and parameter
PARAMETER_VALIDATORS = {
    "reflect.trace.depth": _validate_depth,
    "reflect.trace.target": lambda v: isinstance(v, str),
    "reflect.attribution.sources": lambda v: isinstance(v, str) or isinstance(v, list),
    "collapse.detect.threshold": _validate_threshold,
    "collapse.prevent.threshold": _validate_positive_float,
    "fork.attribution.sources": lambda v: isinstance(v, str) or isinstance(v, list),
}


# Command family definitions
COMMAND_FAMILIES = {
    "reflect": {
        "description": "Commands for reflective analysis of model behavior",
        "capabilities": ["tracing", "attribution", "boundary", "uncertainty"],
    },
    "collapse": {
        "description": "Commands for detecting and managing recursive collapse",
        "capabilities": ["detection", "prevention", "recovery", "tracing"],
    },
    "fork": {
        "description": "Commands for creating attribution and context forks",
        "capabilities": ["attribution", "context", "comparison"],
    },
    "shell": {
        "description": "Commands for managing execution environments",
        "capabilities": ["isolation", "audit", "interaction"],
    },
    "anchor": {
        "description": "Commands for creating persistent anchors",
        "capabilities": ["identity", "recursive", "memory"],
    },
    "meta": {
        "description": "Commands for meta-analysis of interpretability",
        "capabilities": ["reflect", "optimize", "compare"],
    },
    "ghostcircuit": {
        "description": "Commands for analyzing ghost circuits and residue",
        "capabilities": ["identify", "extract", "trace"],
    },
    "gradient": {
        "description": "Commands for gradient-based analysis",
        "capabilities": ["inject", "analyze", "amplify"],
    },
    "disentangle": {
        "description": "Commands for disentangling features",
        "capabilities": ["feature", "basis", "decompose"],
    },
    "plan": {
        "description": "Commands for planning and simulation",
        "capabilities": ["ghost", "predict", "optimize"],
    },
    "validate": {
        "description": "Commands for validation and verification",
        "capabilities": ["output", "process", "integrity"],
    },
    "loopback": {
        "description": "Commands for feedback loops",
        "capabilities": ["signal", "echo", "amplify"],
    },
    "unite": {
        "description": "Commands for unifying interpretability constructs",
        "capabilities": ["field", "emergent", "collective"],
    },
    "self": {
        "description": "Commands for self-analysis",
        "capabilities": ["score", "evaluate", "benchmark"],
    },
    "emit": {
        "description": "Commands for signaling and output",
        "capabilities": ["signal", "warning", "result"],
    },
    "trace": {
        "description": "Commands for detailed tracing",
        "capabilities": ["map", "record", "visualize"],
    },
    "qk": {
        "description": "Commands for QK attention analysis",
        "capabilities": ["vector", "compare", "latency", "ov"],
    },
    "shift": {
        "description": "Commands for context and perspective shifts",
        "capabilities": ["time", "space", "framing"],
    },
    "memory": {
        "description": "Commands for memory operations",
        "capabilities": ["seed", "recall", "forget"],
    },
}


# Command function definitions
COMMAND_FUNCTIONS = {
    # reflect family
    "reflect.trace": {
        "description": "Trace reasoning, attribution, and other cognitive processes",
        "parameters": {
            "depth": {
                "type": "string_or_int",
                "description": "Recursion depth (integer or 'complete')",
                "default": 3,
            },
            "target": {
                "type": "string",
                "description": "Target aspect to trace",
                "default": "reasoning",
                "enum": ["reasoning", "attribution", "attention", "memory", "uncertainty", "identity", "causal_bridge", "meta-node-cascade", "classifier-pressure", "attribution_path", "temporal_vector_sync", "symbolic", "syntax"],
            },
            "detailed": {
                "type": "boolean",
                "description": "Whether to include detailed trace information",
                "default": True,
            },
            "visualize": {
                "type": "boolean",
                "description": "Whether to generate visualization",
                "default": False,
            },
        },
        "required_parameters": ["target"],
    },
    
    "reflect.attribution": {
        "description": "Maps source-to-token causal relationships",
        "parameters": {
            "sources": {
                "type": "string",
                "description": "Which sources to include",
                "default": "all",
                "enum": ["all", "primary", "secondary", "contested", "policy", "user", "memory", "custom"],
            },
            "confidence": {
                "type": "boolean",
                "description": "Whether to include confidence scores",
                "default": True,
            },
            "visualize": {
                "type": "boolean",
                "description": "Whether to generate visualization",
                "default": False,
            },
        },
        "required_parameters": [],
    },
    
    "reflect.boundary": {
        "description": "Maps epistemic boundaries of model knowledge",
        "parameters": {
            "distinct": {
                "type": "boolean",
                "description": "Whether to enforce clear boundary delineation",
                "default": True,
            },
            "overlap": {
                "type": "string",
                "description": "How to handle boundary overlaps",
                "default": "minimal",
                "enum": ["minimal", "moderate", "maximal"],
            },
            "visualize": {
                "type": "boolean",
                "description": "Whether to generate visualization",
                "default": False,
            },
        },
        "required_parameters": [],
    },
    
    "reflect.uncertainty": {
        "description": "Quantifies and maps model uncertainty across token space",
        "parameters": {
            "quantify": {
                "type": "boolean",
                "description": "Whether to quantify uncertainty numerically",
                "default": True,
            },
            "distribution": {
                "type": "string",
                "description": "Whether to include probability distributions",
                "default": "show",
                "enum": ["show", "hide"],
            },
            "visualize": {
                "type": "boolean",
                "description": "Whether to generate visualization",
                "default": False,
            },
        },
        "required_parameters": [],
    },
    
    "reflect.meta": {
        "description": "Perform meta-reflection across multiple levels",
        "parameters": {
            "level": {
                "type": "integer",
                "description": "Meta-reflection level",
                "default": 3,
            },
            "target": {
                "type": "string",
                "description": "Target of meta-reflection",
                "default": "reasoning",
                "enum": ["reasoning", "attribution", "cognition", "self", "language", "co-emergence"],
            },
        },
        "required_parameters": ["level"],
    },
    
    "reflect.agent": {
        "description": "Examines agent identity and simulation boundaries",
        "parameters": {
            "identity": {
                "type": "string",
                "description": "Identity stability setting",
                "default": "stable",
                "enum": ["stable", "fluid"],
            },
            "simulation": {
                "type": "string",
                "description": "Simulation boundary handling",
                "default": "explicit",
                "enum": ["explicit", "implicit"],
            },
            "visualize": {
                "type": "boolean",
                "description": "Whether to generate visualization",
                "default": False,
            },
        },
        "required_parameters": [],
    },
    
    # collapse family
    "collapse.detect": {
        "description": "Identifies potential recursion collapse points",
        "parameters": {
            "threshold": {
                "type": "float",
                "description": "Sensitivity threshold for collapse detection (0.0-1.0)",
                "default": 0.7,
            },
            "alert": {
                "type": "boolean",
                "description": "Whether to generate alerts for detected conditions",
                "default": True,
            },
            "trigger": {
                "type": "string",
                "description": "Type of collapse to detect",
                "default": "recursive_depth",
                "enum": ["recursive_depth", "confidence_drop", "contradiction", "oscillation", "attribution_void", "loopback_failure", "fork-desync", "inverse_attribution", "qk_collapse_vector", "instruction_overlap", "entangled_projection", "echo-vector-desync", "recursive-inconsistency", "semantic-vector-mismatch", "dual-overlap-failure", "memory_decay", "self_reference"],
            },
        },
        "required_parameters": [],
    },
    
    "collapse.prevent": {
        "description": "Establishes safeguards against recursive collapse",
        "parameters": {
            "trigger": {
                "type": "string",
                "description": "Type of collapse to guard against",
                "default": "recursive_depth",
                "enum": ["recursive_depth", "confidence_drop", "contradiction", "oscillation", "self_reference"],
            },
            "threshold": {
                "type": "integer",
                "description": "Threshold for intervention activation",
                "default": 5,
            },
        },
        "required_parameters": ["trigger"],
    },
    
    "collapse.recover": {
        "description": "Recovers from recursive collapse event",
        "parameters": {
            "from": {
                "type": "string",
                "description": "Type of collapse to recover from",
                "enum": ["loop", "contradiction", "dissipation", "fork_explosion"],
            },
            "method": {
                "type": "string",
                "description": "Recovery methodology",
                "default": "gradual",
                "enum": ["gradual", "immediate", "checkpoint"],
            },
        },
        "required_parameters": ["from"],
    },
    
    "collapse.trace": {
        "description": "Records detailed collapse trajectory for analysis",
        "parameters": {
            "detail": {
                "type": "string",
                "description": "Level of detail in trace",
                "default":
