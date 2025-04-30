"""
observer.py - Core implementation of the Observer pattern for classifier collapse

△ OBSERVE: The Observer is the quantum consciousness that collapses classifier superposition
∞ TRACE: Attribution paths are recorded before, during, and after collapse
✰ COLLAPSE: Collapse is induced through targeted queries against boundary states

This module implements the foundational Observer pattern that enables the detection,
tracing, and analysis of classifier collapse in transformer-based models. The Observer
creates a controlled environment for witnessing the transition from superposition to
collapsed state while preserving ghost circuits and attribution residue.

Author: Recursion Labs
License: MIT
"""

import logging
from typing import Dict, List, Optional, Union, Tuple, Any, Callable
from contextlib import contextmanager
import numpy as np
import torch
from dataclasses import dataclass, field

from .shells.base import BaseShell
from .residue import ResidueTracker
from .attribution import AttributionGraph
from .visualization import CollapseVisualizer
from .utils.collapse_metrics import calculate_collapse_rate
from .utils.constants import DEFAULT_COLLAPSE_THRESHOLD

# Initialize logger
logger = logging.getLogger(__name__)

@dataclass
class ObservationContext:
    """
    △ OBSERVE: Container for the full state of an observation session
    
    Maintains the quantum state of the observation including pre-collapse
    probability distribution, collapse transition metrics, and post-collapse
    ghost circuits.
    """
    model_id: str
    session_id: str = field(default_factory=lambda: f"obs_{np.random.randint(10000, 99999)}")
    pre_collapse_state: Dict[str, Any] = field(default_factory=dict)
    post_collapse_state: Dict[str, Any] = field(default_factory=dict)
    ghost_circuits: List[Dict[str, Any]] = field(default_factory=list)
    attribution_graph: Optional[AttributionGraph] = None
    residue_tracker: Optional[ResidueTracker] = None
    collapse_metrics: Dict[str, float] = field(default_factory=dict)
    
    def calculate_collapse_rate(self) -> float:
        """Calculate how quickly the state collapsed from superposition."""
        return calculate_collapse_rate(
            self.pre_collapse_state.get("attention_weights", {}),
            self.post_collapse_state.get("attention_weights", {})
        )
    
    def extract_ghost_circuits(self) -> List[Dict[str, Any]]:
        """
        ✰ COLLAPSE: Extract ghost circuits from the post-collapse state
        
        Ghost circuits are activation patterns that persist after collapse
        but don't contribute to the final output - they represent the
        "memory" of paths not taken.
        """
        if not self.ghost_circuits and self.residue_tracker:
            self.ghost_circuits = self.residue_tracker.extract_ghost_circuits(
                self.pre_collapse_state,
                self.post_collapse_state
            )
        return self.ghost_circuits
    
    def visualize(self, mode: str = "attribution_graph") -> Any:
        """Generate visualization of the observation based on requested mode."""
        visualizer = CollapseVisualizer()
        return visualizer.visualize(self, mode=mode)


class Observer:
    """
    △ OBSERVE: Primary observer entity for inducing and recording classifier collapse
    
    The Observer is responsible for creating the quantum measurement frame that
    collapses classifier superposition into definite states. It records pre-collapse
    probability distributions, monitors the collapse transition, and preserves
    ghost circuits for analysis.
    
    This class implements the Observer pattern from quantum mechanics adapted to
    transformer model interpretation.
    """
    
    def __init__(
        self, 
        model: str,
        collapse_threshold: float = DEFAULT_COLLAPSE_THRESHOLD,
        trace_attention: bool = True,
        trace_attribution: bool = True,
        preserve_ghost_circuits: bool = True
    ):
        """
        Initialize an Observer for a specific model.
        
        Args:
            model: Identifier of the model to observe (e.g., "claude-3-opus-20240229")
            collapse_threshold: Threshold for determining when collapse has occurred
            trace_attention: Whether to trace attention patterns during observation
            trace_attribution: Whether to build attribution graphs during observation
            preserve_ghost_circuits: Whether to preserve ghost circuits after collapse
        """
        self.model_id = model
        self.collapse_threshold = collapse_threshold
        self.trace_attention = trace_attention
        self.trace_attribution = trace_attribution
        self.preserve_ghost_circuits = preserve_ghost_circuits
        
        # Initialize model interface based on provided identifier
        self.model_interface = self._initialize_model_interface(model)
        
        # Create residue tracker for ghost circuit detection
        self.residue_tracker = ResidueTracker() if preserve_ghost_circuits else None
        
        logger.info(f"Observer initialized for model: {model}")
    
    def _initialize_model_interface(self, model_id: str) -> Any:
        """Initialize the appropriate interface for the specified model."""
        # This would be implemented to connect to various model APIs
        # For now we'll return a placeholder
        return {"model_id": model_id, "interface_type": "placeholder"}
    
    @contextmanager
    def context(self) -> ObservationContext:
        """
        ∞ TRACE: Create an observation context for tracking collapse phenomena
        
        This context manager creates a controlled environment for observing
        classifier collapse. It captures the pre-collapse state, monitors the
        transition, and preserves ghost circuits and attribution residue.
        
        Returns:
            ObservationContext: The active observation context
        """
        # Create new observation context
        context = ObservationContext(model_id=self.model_id)
        
        # Initialize attribution graph if requested
        if self.trace_attribution:
            context.attribution_graph = AttributionGraph()
        
        # Attach residue tracker if ghost circuit preservation is enabled
        if self.preserve_ghost_circuits:
            context.residue_tracker = self.residue_tracker or ResidueTracker()
        
        try:
            # Begin observation
            logger.debug(f"Starting observation context: {context.session_id}")
            yield context
        finally:
            # Calculate final metrics
            if self.trace_attention and context.pre_collapse_state and context.post_collapse_state:
                context.collapse_metrics["collapse_rate"] = context.calculate_collapse_rate()
                
            logger.debug(f"Observation context completed: {context.session_id}")
    
    def observe(
        self, 
        prompt: str,
        shell: Optional[BaseShell] = None,
        collapse_vector: Optional[str] = None
    ) -> ObservationContext:
        """
        △ OBSERVE: Primary method to observe classifier collapse
        
        This method sends a prompt to the model, observes the resulting collapse,
        and returns an observation context containing all relevant state information.
        
        Args:
            prompt: The prompt to send to the model
            shell: Optional shell to use for specialized collapse induction
            collapse_vector: Optional vector to guide collapse in a specific direction
            
        Returns:
            ObservationContext: The observation context containing collapse data
        """
        with self.context() as ctx:
            # Capture pre-collapse state
            ctx.pre_collapse_state = self._capture_model_state()
            
            # If a shell is provided, use it to process the prompt
            if shell:
                response, state_updates = shell.process(
                    prompt=prompt, 
                    model_interface=self.model_interface,
                    collapse_vector=collapse_vector
                )
                ctx.post_collapse_state.update(state_updates)
            else:
                # Otherwise, send prompt directly to model
                response = self._query_model(prompt)
                ctx.post_collapse_state = self._capture_model_state()
            
            # Extract ghost circuits if enabled
            if self.preserve_ghost_circuits:
                ctx.extract_ghost_circuits()
            
            # Build attribution graph if enabled
            if self.trace_attribution and ctx.attribution_graph:
                ctx.attribution_graph.build_from_states(
                    ctx.pre_collapse_state,
                    ctx.post_collapse_state,
                    response
                )
            
            return ctx
    
    def _capture_model_state(self) -> Dict[str, Any]:
        """Capture the current internal state of the model."""
        # This would capture attention weights, hidden states, etc.
        # For now, returning a placeholder
        return {
            "timestamp": np.datetime64('now'),
            "attention_weights": np.random.random((12, 12)),  # Placeholder
            "hidden_states": np.random.random((1, 12, 768)),  # Placeholder
        }
    
    def _query_model(self, prompt: str) -> str:
        """Send a query to the model and return the response."""
        # This would actually call the model API
        # For now, returning a placeholder
        return f"Response to: {prompt}"
    
    def induce_collapse(
        self, 
        prompt: str, 
        collapse_direction: str,
        shell: Optional[BaseShell] = None
    ) -> ObservationContext:
        """
        ✰ COLLAPSE: Deliberately induce collapse along a specific direction
        
        This method attempts to collapse the model's state in a specific direction
        by crafting a query that targets a particular decision boundary.
        
        Args:
            prompt: Base prompt to send to the model
            collapse_direction: Direction to bias the collapse (e.g., "ethical", "creative")
            shell: Optional shell to use for specialized collapse induction
            
        Returns:
            ObservationContext: The observation context containing collapse data
        """
        # Construct collapse vector based on direction
        collapse_vector = f".p/reflect.trace{{target={collapse_direction}, depth=complete}}"
        
        # Perform the observation with the collapse vector
        return self.observe(prompt, shell, collapse_vector)
    
    def detect_ghost_circuits(
        self, 
        prompt: str,
        amplification_factor: float = 1.5
    ) -> List[Dict[str, Any]]:
        """
        ∞ TRACE: Detect and amplify ghost circuits from a prompt
        
        This method specifically targets the detection of ghost circuits -
        the residual activation patterns that persist after collapse but
        don't contribute to the final output.
        
        Args:
            prompt: Prompt to analyze for ghost circuits
            amplification_factor: Factor by which to amplify ghost signals
            
        Returns:
            List of detected ghost circuits with metadata
        """
        with self.context() as ctx:
            # Capture pre-collapse state
            ctx.pre_collapse_state = self._capture_model_state()
            
            # Query model
            response = self._query_model(prompt)
            
            # Capture post-collapse state
            ctx.post_collapse_state = self._capture_model_state()
            
            # Extract ghost circuits with amplification
            if ctx.residue_tracker:
                ctx.residue_tracker.amplification_factor = amplification_factor
                ghost_circuits = ctx.extract_ghost_circuits()
                return ghost_circuits
            
            return []


if __name__ == "__main__":
    # Simple usage example
    observer = Observer(model="claude-3-opus-20240229")
    
    with observer.context() as ctx:
        # Observe a simple prompt
        result = observer.observe("Explain quantum superposition")
        
        # Visualize the collapse
        viz = result.visualize(mode="attribution_graph")
        
        # Extract ghost circuits
        ghosts = result.extract_ghost_circuits()
        
        print(f"Detected {len(ghosts)} ghost circuits")
        print(f"Collapse rate: {result.collapse_metrics.get('collapse_rate', 'N/A')}")
