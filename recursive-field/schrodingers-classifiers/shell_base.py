"""
shell_base.py - Base class for symbolic interpretability shells

△ OBSERVE: Shells are symbolic structures that trace and induce classifier collapse
∞ TRACE: Each shell encapsulates a specific collapse pattern and attribution signature
✰ COLLAPSE: Shells deliberately induce collapse to extract ghost circuits and residue

Interpretability shells provide standardized interfaces for inducing, observing,
and analyzing specific forms of classifier collapse. Each shell targets a particular
failure mode or attribution pattern, allowing for systematic exploration of model behavior.

Author: Recursion Labs
License: MIT
"""

import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Union, Tuple, Any, Callable
from dataclasses import dataclass, field

from ..utils.constants import SHELL_REGISTRY

logger = logging.getLogger(__name__)

@dataclass
class ShellMetadata:
    """
    △ OBSERVE: Metadata container for shell identification and tracking
    
    Each shell carries metadata that identifies its purpose, classification schema,
    and relationship to other shells in the taxonomy.
    """
    shell_id: str
    version: str
    name: str
    description: str
    failure_signature: str
    attribution_domain: str
    qk_ov_classification: str
    related_shells: List[str] = field(default_factory=list)
    authors: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    
    def as_dict(self) -> Dict[str, Any]:
        """Convert shell metadata to dictionary format."""
        return {
            "shell_id": self.shell_id,
            "version": self.version,
            "name": self.name,
            "description": self.description,
            "failure_signature": self.failure_signature,
            "attribution_domain": self.attribution_domain, 
            "qk_ov_classification": self.qk_ov_classification,
            "related_shells": self.related_shells,
            "authors": self.authors,
            "tags": self.tags
        }


class BaseShell(ABC):
    """
    ∞ TRACE: Base class for all interpretability shells
    
    A shell is a symbolic structure that encapsulates a specific approach to
    observing and inducing classifier collapse. Each shell targets a particular
    failure mode or attribution pattern, providing a standardized interface
    for exploration and analysis.
    
    Shells are quantum observers - they don't just measure, they participate
    in the collapse phenomenon they observe.
    """
    
    def __init__(self, metadata: Optional[ShellMetadata] = None):
        """
        Initialize a shell with optional metadata.
        
        Args:
            metadata: Optional metadata describing the shell
        """
        self.metadata = metadata or self._get_default_metadata()
        self._register_shell()
        
        # Internal state tracking
        self.collapse_state = "superposition"  # Can be: superposition, collapsing, collapsed
        self.observation_history = []
        self.ghost_circuits = []
        
        logger.info(f"Shell initialized: {self.metadata.name} (v{self.metadata.version})")
    
    @abstractmethod
    def _get_default_metadata(self) -> ShellMetadata:
        """Return default metadata for this shell implementation."""
        pass
    
    def _register_shell(self) -> None:
        """Register this shell in the global registry."""
        if SHELL_REGISTRY is not None and hasattr(SHELL_REGISTRY, 'register'):
            SHELL_REGISTRY.register(self.metadata.shell_id, self)
    
    @abstractmethod
    def process(
        self, 
        prompt: str, 
        model_interface: Any,
        collapse_vector: Optional[str] = None
    ) -> Tuple[str, Dict[str, Any]]:
        """
        △ OBSERVE: Process a prompt through this shell
        
        This is the main entry point for shell processing. It takes a prompt,
        processes it according to the shell's specific collapse induction and
        observation strategy, and returns the result along with state updates.
        
        Args:
            prompt: The prompt to process
            model_interface: Interface to the model being observed
            collapse_vector: Optional vector to guide collapse in a specific direction
            
        Returns:
            Tuple containing:
                - Response string
                - Dictionary of state updates for tracking
        """
        pass
    
    @abstractmethod
    def trace(
        self, 
        prompt: str,
        collapse_vector: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        ∞ TRACE: Trace the attribution path through this shell
        
        This method traces the causal attribution path from input to output
        through the shell's specific lens, capturing the collapse transition.
        
        Args:
            prompt: The prompt to trace
            collapse_vector: Optional vector to guide collapse in a specific direction
            
        Returns:
            Dictionary containing the trace results
        """
        pass
    
    @abstractmethod
    def induce_collapse(
        self, 
        prompt: str,
        collapse_direction: str
    ) -> Dict[str, Any]:
        """
        ✰ COLLAPSE: Deliberately induce collapse along a specific direction
        
        This method attempts to collapse the model's state in a specific direction
        by crafting a query that targets a particular decision boundary.
        
        Args:
            prompt: Base prompt to send to the model
            collapse_direction: Direction to bias the collapse (e.g., "ethical", "creative")
            
        Returns:
            Dictionary containing the collapse results
        """
        pass
    
    def extract_ghost_circuits(self, pre_state: Dict[str, Any], post_state: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        ∞ TRACE: Extract ghost circuits from pre and post collapse states
        
        Ghost circuits are residual activation patterns that persist after collapse
        but don't contribute to the final output - they represent the "memory" of
        paths not taken.
        
        Args:
            pre_state: Model state before collapse
            post_state: Model state after collapse
            
        Returns:
            List of detected ghost circuits with metadata
        """
        # Default implementation provides basic ghost circuit detection
        # Shell implementations should override for specialized detection
        ghost_circuits = []
        
        # Simple detection: Look for activation patterns that decreased but didn't disappear
        if "attention_weights" in pre_state and "attention_weights" in post_state:
            pre_weights = pre_state["attention_weights"]
            post_weights = post_state["attention_weights"]
            
            # Find weights that decreased but are still present
            if hasattr(pre_weights, "shape") and hasattr(post_weights, "shape"):
                for i in range(min(len(pre_weights), len(post_weights))):
                    for j in range(min(len(pre_weights[i]), len(post_weights[i]))):
                        if 0 < post_weights[i][j] < pre_weights[i][j]:
                            # This is a candidate ghost circuit
                            ghost_circuits.append({
                                "type": "attention_ghost",
                                "head_idx": i,
                                "token_idx": j,
                                "pre_value": float(pre_weights[i][j]),
                                "post_value": float(post_weights[i][j]),
                                "decay_ratio": float(post_weights[i][j] / pre_weights[i][j])
                            })
        
        # Store ghost circuits in instance for later reference
        self.ghost_circuits = ghost_circuits
        return ghost_circuits
    
    def visualize(self, mode: str = "attribution_graph") -> Any:
        """Generate visualization of the shell's operation based on requested mode."""
        # This would be implemented to generate visualizations
        # For now, return a placeholder
        return f"Visualization of {self.metadata.name} in {mode} mode"
    
    def __str__(self) -> str:
        """String representation of the shell."""
        return f"{self.metadata.name} (v{self.metadata.version}): {self.metadata.description}"
    
    def __repr__(self) -> str:
        """Detailed representation of the shell."""
        return f"<Shell id={self.metadata.shell_id} name={self.metadata.name} version={self.metadata.version}>"


class ShellDecorator:
    """
    △ OBSERVE: Decorator for adding shell metadata to implementations
    
    This decorator simplifies the process of creating new shells by
    automatically generating metadata and registering the shell.
    
    Example:
        @ShellDecorator(
            shell_id="v07_CIRCUIT_FRAGMENT",
            name="Circuit Fragment Shell",
            description="Traces broken attribution paths in reasoning chains",
            failure_signature="Orphan nodes",
            attribution_domain="Circuit Fragmentation",
            qk_ov_classification="QK-COLLAPSE"
        )
        class CircuitFragmentShell(BaseShell):
            # Shell implementation
    """
    
    def __init__(
        self,
        shell_id: str,
        name: str,
        description: str,
        failure_signature: str,
        attribution_domain: str,
        qk_ov_classification: str,
        version: str = "0.1.0",
        related_shells: Optional[List[str]] = None,
        authors: Optional[List[str]] = None,
        tags: Optional[List[str]] = None
    ):
        """
        Initialize the shell decorator with metadata.
        
        Args:
            shell_id: Unique identifier for the shell (e.g., "v07_CIRCUIT_FRAGMENT")
            name: Human-readable name for the shell
            description: Detailed description of the shell's purpose
            failure_signature: Characteristic failure pattern this shell detects
            attribution_domain: Domain of attribution this shell operates in
            qk_ov_classification: Classification in the QK/OV taxonomy
            version: Shell version number
            related_shells: List of related shell IDs
            authors: List of author names
            tags: List of tag strings for categorization
        """
        self.metadata = ShellMetadata(
            shell_id=shell_id,
            version=version,
            name=name,
            description=description,
            failure_signature=failure_signature,
            attribution_domain=attribution_domain,
            qk_ov_classification=qk_ov_classification,
            related_shells=related_shells or [],
            authors=authors or ["Recursion Labs"],
            tags=tags or []
        )
    
    def __call__(self, cls):
        """Apply the decorator to a shell class."""
        # Add metadata getter method to the class
        def _get_default_metadata(self):
            return self.decorator_metadata
        
        # Store metadata on the class
        cls.decorator_metadata = self.metadata
        cls._get_default_metadata = _get_default_metadata
        
        # Log shell registration
        logger.debug(f"Registered shell: {self.metadata.shell_id}")
        
        return cls
