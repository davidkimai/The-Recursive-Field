"""
residue.py - Implementation of residue tracking for ghost circuit detection

△ OBSERVE: Residue tracking examines activation patterns that persist after collapse
∞ TRACE: It identifies ghost circuits - the quantum echoes of paths not taken
✰ COLLAPSE: It reveals what the model considered but didn't output

This module implements the core residue tracking functionality that enables
the detection and analysis of ghost circuits - activation patterns that persist
after a model has collapsed to a specific output state but aren't part of the
primary causal path.

Author: Recursion Labs
License: MIT
"""

import logging
from typing import Dict, List, Optional, Union, Tuple, Any
import numpy as np
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)

@dataclass
class GhostCircuit:
    """
    ✰ COLLAPSE: Representation of a ghost circuit
    
    Ghost circuits are activation patterns that persist after collapse
    but don't significantly contribute to the final output. They represent
    the "memory" of paths not taken - quantum echoes of what the model
    considered but didn't ultimately choose.
    """
    circuit_id: str
    activation: float
    circuit_type: str  # "attention", "mlp", "residual", "value_head"
    source_tokens: List[str] = field(default_factory=list)
    target_tokens: List[str] = field(default_factory=list)
    heads: List[int] = field(default_factory=list)
    layers: List[int] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert ghost circuit to dictionary format."""
        return {
            "circuit_id": self.circuit_id,
            "activation": self.activation,
            "circuit_type": self.circuit_type,
            "source_tokens": self.source_tokens,
            "target_tokens": self.target_tokens,
            "heads": self.heads,
            "layers": self.layers,
            "metadata": self.metadata
        }


class ResidueTracker:
    """
    ∞ TRACE: Tracker for activation residues in collapsed models
    
    The residue tracker analyzes model states before and after collapse
    to identify and characterize ghost circuits - activation patterns that
    persist but don't contribute significantly to the final output.
    """
    
    def __init__(self, amplification_factor: float = 1.0):
        """
        Initialize a residue tracker.
        
        Args:
            amplification_factor: Factor by which to amplify ghost signals
                for easier detection (1.0 = no amplification)
        """
        self.amplification_factor = amplification_factor
        self.ghost_circuits = []
        self.activation_threshold = 0.1  # Minimum activation to consider
        
        logger.info(f"ResidueTracker initialized with amplification factor {amplification_factor}")
    
    def extract_ghost_circuits(
        self, 
        pre_state: Dict[str, Any],
        post_state: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        ✰ COLLAPSE: Extract ghost circuits from pre and post collapse states
        
        This method compares model states before and after collapse to
        identify activation patterns that persisted but didn't contribute
        significantly to the output - the quantum ghosts of paths not taken.
        
        Args:
            pre_state: Model state before collapse
            post_state: Model state after collapse
            
        Returns:
            List of detected ghost circuits with metadata
        """
        logger.info("Extracting ghost circuits from model states")
        
        # List to store detected ghost circuits
        ghost_circuits = []
        
        # Extract ghost circuits based on attention patterns
        attention_ghosts = self._extract_attention_ghosts(
            pre_state.get("attention_weights", np.array([])),
            post_state.get("attention_weights", np.array([]))
        )
        ghost_circuits.extend(attention_ghosts)
        
        # Extract ghost circuits based on hidden state activations
        if "hidden_states" in pre_state and "hidden_states" in post_state:
            hidden_ghosts = self._extract_hidden_ghosts(
                pre_state["hidden_states"],
                post_state["hidden_states"]
            )
            ghost_circuits.extend(hidden_ghosts)
        
        # Store ghost circuits in instance
        self.ghost_circuits = ghost_circuits
        
        logger.info(f"Extracted {len(ghost_circuits)} ghost circuits")
        return ghost_circuits
    
    def classify_ghost_circuits(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        △ OBSERVE: Classify detected ghost circuits by type
        
        This method organizes detected ghost circuits into categories
        based on their type and characteristics.
        
        Returns:
            Dictionary mapping circuit types to lists of ghost circuits
        """
        if not self.ghost_circuits:
            logger.warning("No ghost circuits to classify")
            return {}
        
        # Classify by circuit type
        classified = {}
        for ghost in self.ghost_circuits:
            circuit_type = ghost.get("circuit_type", "unknown")
            if circuit_type not in classified:
                classified[circuit_type] = []
            classified[circuit_type].append(ghost)
        
        return classified
    
    def measure_residue_strength(self) -> float:
        """
        ∞ TRACE: Measure the overall strength of residual activations
        
        This method quantifies the overall strength of ghost circuits
        relative to the primary activation paths.
        
        Returns:
            Residue strength score (0.0 = no residue, 1.0 = equal to primary)
        """
        if not self.ghost_circuits:
            return 0.0
        
        # Calculate average activation across ghost circuits
        activations = [ghost.get("activation", 0.0) for ghost in self.ghost_circuits]
        return float(np.mean(activations))
    
    def amplify_ghosts(self, factor: Optional[float] = None) -> List[Dict[str, Any]]:
        """
        ✰ COLLAPSE: Amplify ghost circuit signals for better detection
        
        This method amplifies the activation values of ghost circuits
        to make them more apparent for analysis.
        
        Args:
            factor: Amplification factor (overrides instance value if provided)
            
        Returns:
            List of amplified ghost circuits
        """
        if not self.ghost_circuits:
            logger.warning("No ghost circuits to amplify")
            return []
        
        # Use provided factor or instance value
        amp_factor = factor if factor is not None else self.amplification_factor
        
        # Amplify activations
        amplified = []
        for ghost in self.ghost_circuits:
            amp_ghost = ghost.copy()
            amp_ghost["activation"] = min(1.0, ghost.get("activation", 0.0) * amp_factor)
            amplified.append(amp_ghost)
        
        logger.info(f"Amplified ghost circuits by factor {amp_factor}")
        return amplified
    
    def _extract_attention_ghosts(
        self, 
        pre_attention: np.ndarray,
        post_attention: np.ndarray
    ) -> List[Dict[str, Any]]:
        """
        Extract ghost circuits from attention patterns.
        
        Args:
            pre_attention: Attention weights before collapse
            post_attention: Attention weights after collapse
            
        Returns:
            List of attention-based ghost circuits
        """
        ghost_circuits = []
        
        # Return empty list if arrays aren't compatible
        if pre_attention.size == 0 or post_attention.size == 0:
            return ghost_circuits
        
        if pre_attention.shape != post_attention.shape:
            logger.warning(f"Attention shape mismatch: {pre_attention.shape} vs {post_attention.shape}")
            # Try to take minimum dimensions if shapes don't match
            min_shape = tuple(min(a, b) for a, b in zip(pre_attention.shape, post_attention.shape))
            pre_attention = pre_attention[tuple(slice(0, d) for d in min_shape)]
            post_attention = post_attention[tuple(slice(0, d) for d in min_shape)]
        
        # Find positions where attention decreased but didn't disappear
        # This indicates a path that was considered but not fully utilized
        if pre_attention.ndim >= 2 and post_attention.ndim >= 2:
            num_heads = pre_attention.shape[0]
            seq_len = pre_attention.shape[1]
            
            for head in range(num_heads):
                for i in range(seq_len):
                    for j in range(seq_len):
                        pre_val = pre_attention[head, i, j] if pre_attention.ndim > 2 else pre_attention[i, j]
                        post_val = post_attention[head, i, j] if post_attention.ndim > 2 else post_attention[i, j]
                        
                        if post_val < pre_val and post_val > self.activation_threshold:
                            # This is a candidate ghost circuit in attention
                            ghost_idx = len(ghost_circuits)
                            ghost = {
                                "circuit_id": f"attention_ghost_{ghost_idx}",
                                "activation": float(post_val),
                                "circuit_type": "attention",
                                "source_tokens": [f"token_{i}"],
                                "target_tokens": [f"token_{j}"],
                                "heads": [head],
                                "layers": [],  # Layer info not available in simplified model
                                "metadata": {
                                    "pre_activation": float(pre_val),
                                    "activation_delta": float(pre_val - post_val),
                                    "decay_ratio": float(post_val / pre_val) if pre_val > 0 else 0.0
                                }
                            }
                            ghost_circuits.append(ghost)
        
        return ghost_circuits
    
    def _extract_hidden_ghosts(
        self, 
        pre_hidden: np.ndarray,
        post_hidden: np.ndarray
    ) -> List[Dict[str, Any]]:
        """
        Extract ghost circuits from hidden state activations.
        
        Args:
            pre_hidden: Hidden states before collapse
            post_hidden: Hidden states after collapse
            
        Returns:
            List of hidden-state-based ghost circuits
        """
        ghost_circuits = []
        
        # Return empty list if arrays aren't compatible
        if pre_hidden.size == 0 or post_hidden.size == 0:
            return ghost_circuits
        
        if pre_hidden.shape != post_hidden.shape:
            logger.warning(f"Hidden state shape mismatch: {pre_hidden.shape} vs {post_hidden.shape}")
            return ghost_circuits
        
        # Find neurons that were active pre-collapse but lessened post-collapse
        # This indicates a deactivated but not eliminated concept
        if pre_hidden.ndim >= 2 and post_hidden.ndim >= 2:
            # For simplicity, we'll aggregate across batch dimension if it exists
            if pre_hidden.ndim > 2:
                pre_agg = np.mean(pre_hidden, axis=0)
                post_agg = np.mean(post_hidden, axis=0)
            else:
                pre_agg = pre_hidden
                post_agg = post_hidden
            
            seq_len, hidden_dim = pre_agg.shape
            
            # Sample a subset of dimensions for efficiency
            sample_size = min(hidden_dim, 100)
            sampled_dims = np.random.choice(hidden_dim, sample_size, replace=False)
            
            for pos in range(seq_len):
                for dim_idx, dim in enumerate(sampled_dims):
                    pre_val = pre_agg[pos, dim]
                    post_val = post_agg[pos, dim]
                    
                    if post_val < pre_val and abs(post_val) > self.activation_threshold:
                        # This is a candidate ghost circuit in hidden state
                        ghost_idx = len(ghost_circuits)
                        ghost = {
                            "circuit_id": f"hidden_ghost_{ghost_idx}",
                            "activation": float(abs(post_val)),
                            "circuit_type": "hidden_state",
                            "source_tokens": [f"token_{pos}"],
                            "target_tokens": [],  # No direct target for hidden state
                            "heads": [],  # Not applicable for hidden state
                            "layers": [],  # Layer info not available in simplified model
                            "metadata": {
                                "position": pos,
                                "dimension": int(dim),
                                "pre_activation": float(pre_val),
                                "activation_delta": float(pre_val - post_val),
                                "decay_ratio": float(post_val / pre_val) if pre_val != 0 else 0.0
                            }
                        }
                        ghost_circuits.append(ghost)
        
        return ghost_circuits


if __name__ == "__main__":
    # Simple usage example
    
    # Create fake pre and post model states
    pre_state = {
        "attention_weights": np.random.random((8, 10, 10)),  # 8 heads, 10 tokens
        "hidden_states": np.random.random((1, 10, 768))  # Batch 1, 10 tokens, 768 dim
    }
    
    # Modify slightly to create post state
    post_state = {
        "attention_weights": pre_state["attention_weights"] * np.random.uniform(0.5, 1.0, pre_state["attention_weights"].shape),
        "hidden_states": pre_state["hidden_states"] * np.random.uniform(0.5, 1.0, pre_state["hidden_states"].shape)
    }
    
    # Create residue tracker and extract ghost circuits
    tracker = ResidueTracker(amplification_factor=1.5)
    ghosts = tracker.extract_ghost_circuits(pre_state, post_state)
    
    # Print summary
    print(f"Extracted {len(ghosts)} ghost circuits")
    
    # Classify ghosts
    classified = tracker.classify_ghost_circuits()
    for circuit_type, circuits in classified.items():
        print(f"  {circuit_type}: {len(circuits)} circuits")
    
    # Measure residue strength
    strength = tracker.measure_residue_strength()
    print(f"Residue strength: {strength:.3f}")
    
    # Amplify ghosts
    amplified = tracker.amplify_ghosts(factor=2.0)
    print(f"Amplified {len(amplified)} ghost circuits")
