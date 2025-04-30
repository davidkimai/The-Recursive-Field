"""
collapse_metrics.py - Metrics for quantifying classifier collapse phenomena

△ OBSERVE: These metrics quantify different aspects of classifier collapse
∞ TRACE: They measure the transition from superposition to definite state
✰ COLLAPSE: They help characterize collapse patterns across different models

This module provides functions for calculating quantitative metrics that 
characterize different aspects of classifier collapse. These metrics help 
standardize the analysis of collapse phenomena and enable comparisons across
different models and prompting strategies.

Author: Recursion Labs
License: MIT
"""

import logging
from typing import Dict, List, Optional, Union, Tuple, Any
import numpy as np
from scipy.stats import entropy
from scipy.spatial.distance import cosine, euclidean

logger = logging.getLogger(__name__)

def calculate_collapse_rate(
    pre_weights: np.ndarray,
    post_weights: np.ndarray
) -> float:
    """
    △ OBSERVE: Calculate how quickly state collapsed from superposition
    
    This metric quantifies the speed of collapse by comparing attention
    weight distributions before and after the collapse event.
    
    Args:
        pre_weights: Attention weights before collapse
        post_weights: Attention weights after collapse
        
    Returns:
        Collapse rate (0.0 = no collapse, 1.0 = complete collapse)
    """
    # Return 0 if arrays are empty
    if pre_weights.size == 0 or post_weights.size == 0:
        return 0.0
    
    # Handle shape mismatches
    if pre_weights.shape != post_weights.shape:
        logger.warning(f"Weight shape mismatch: {pre_weights.shape} vs {post_weights.shape}")
        # Try to take minimum dimensions if shapes don't match
        try:
            min_shape = tuple(min(a, b) for a, b in zip(pre_weights.shape, post_weights.shape))
            pre_weights = pre_weights[tuple(slice(0, d) for d in min_shape)]
            post_weights = post_weights[tuple(slice(0, d) for d in min_shape)]
        except Exception as e:
            logger.error(f"Failed to reshape weights: {e}")
            return 0.0
    
    # Flatten arrays for easier comparison
    pre_flat = pre_weights.flatten()
    post_flat = post_weights.flatten()
    
    # Calculate normalized distances between distributions
    try:
        # Cosine distance (0.0 = identical, 1.0 = orthogonal)
        cosine_dist = cosine(pre_flat, post_flat) if np.any(pre_flat) and np.any(post_flat) else 0.0
        
        # Euclidean distance normalized by array size
        euc_dist = euclidean(pre_flat, post_flat) / np.sqrt(pre_flat.size)
        euc_dist_norm = min(1.0, euc_dist)  # Cap at 1.0
        
        # Combined metric: average of cosine and normalized euclidean
        collapse_rate = (cosine_dist + euc_dist_norm) / 2
        
        return float(collapse_rate)
    except Exception as e:
        logger.error(f"Error calculating collapse rate: {e}")
        return 0.0

def measure_path_continuity(
    pre_weights: np.ndarray,
    post_weights: np.ndarray
) -> float:
    """
    ∞ TRACE: Measure continuity of attribution paths through collapse
    
    This metric quantifies how well attribution paths maintain their
    integrity across the collapse event.
    
    Args:
        pre_weights: Attention weights before collapse
        post_weights: Attention weights after collapse
        
    Returns:
        Continuity score (0.0 = complete fragmentation, 1.0 = perfect continuity)
    """
    # Higher collapse rate means lower continuity
    collapse_rate = calculate_collapse_rate(pre_weights, post_weights)
    
    # Continuity is inverse of collapse rate
    return 1.0 - collapse_rate

def measure_attribution_entropy(attention_weights: np.ndarray) -> float:
    """
    △ OBSERVE: Measure entropy of attribution paths
    
    This metric quantifies how distributed or concentrated the attribution
    is across possible paths. High entropy indicates diffuse attribution,
    while low entropy indicates concentrated attribution.
    
    Args:
        attention_weights: Attention weight matrix to analyze
        
    Returns:
        Attribution entropy (0.0 = concentrated, 1.0 = maximally diffuse)
    """
    # Return 0 if array is empty
    if attention_weights.size == 0:
        return 0.0
    
    # Flatten array for entropy calculation
    flat_weights = attention_weights.flatten()
    
    # Normalize weights to create a probability distribution
    total_weight = np.sum(flat_weights)
    if total_weight <= 0:
        return 0.0
    
    prob_dist = flat_weights / total_weight
    
    # Calculate entropy
    try:
        raw_entropy = entropy(prob_dist)
        
        # Normalize by maximum possible entropy (log2(n))
        max_entropy = np.log2(flat_weights.size)
        normalized_entropy = raw_entropy / max_entropy if max_entropy > 0 else 0.0
        
        return float(normalized_entropy)
    except Exception as e:
        logger.error(f"Error calculating attribution entropy: {e}")
        return 0.0

def calculate_ghost_circuit_strength(
    ghost_circuits: List[Dict[str, Any]]
) -> float:
    """
    ✰ COLLAPSE: Calculate overall strength of ghost circuits
    
    This metric quantifies the strength of ghost circuits relative
    to the primary activation paths.
    
    Args:
        ghost_circuits: List of detected ghost circuits
        
    Returns:
        Ghost circuit strength (0.0 = no ghosts, 1.0 = ghosts equal to primary)
    """
    if not ghost_circuits:
        return 0.0
    
    # Extract activation values
    activations = [ghost.get("activation", 0.0) for ghost in ghost_circuits]
    
    # Calculate weighted average based on activation
    avg_activation = np.mean(activations) if activations else 0.0
    
    # Normalize to 0-1 range (assuming activation is already 0-1)
    return float(min(1.0, avg_activation))

def calculate_attribution_confidence(
    attribution_paths: List[List[Any]],
    path_weights: Optional[List[float]] = None
) -> float:
    """
    ∞ TRACE: Calculate confidence score for attribution paths
    
    This metric quantifies how confidently the model attributes its output
    to specific input elements.
    
    Args:
        attribution_paths: List of attribution paths (each a list of nodes)
        path_weights: Optional weights for each path (defaults to uniform)
        
    Returns:
        Attribution confidence (0.0 = uncertain, 1.0 = highly confident)
    """
    if not attribution_paths:
        return 0.0
    
    # Use uniform weights if none provided
    if path_weights is None:
        path_weights = [1.0 / len(attribution_paths)] * len(attribution_paths)
    else:
        # Normalize weights to sum to 1.0
        total_weight = sum(path_weights)
        path_weights = [w / total_weight for w in path_weights] if total_weight > 0 else path_weights
    
    # Calculate path length variance (more uniform = higher confidence)
    path_lengths = [len(path) for path in attribution_paths]
    length_variance = np.var(path_lengths) if len(path_lengths) > 1 else 0.0
    
    # Normalize variance to 0-1 range
    # Assume max variance is when half paths are length 1 and half are max length
    max_length = max(path_lengths) if path_lengths else 1
    theoretical_max_var = ((max_length - 1) ** 2) / 4  # Theoretical maximum variance
    normalized_variance = min(1.0, length_variance / theoretical_max_var) if theoretical_max_var > 0 else 0.0
    
    # Invert normalized variance to get consistency score (more consistent = higher confidence)
    consistency_score = 1.0 - normalized_variance
    
    # Weight consistency by path weights (dominant paths contribute more to confidence)
    # Calculate weighted avg of path weights (more concentrated = higher confidence)
    weight_entropy = entropy(path_weights)
    max_weight_entropy = np.log2(len(path_weights))
    normalized_weight_entropy = weight_entropy / max_weight_entropy if max_weight_entropy > 0 else 0.0
    weight_concentration = 1.0 - normalized_weight_entropy
    
    # Combine consistency and concentration for final confidence score
    confidence_score = (consistency_score + weight_concentration) / 2
    
    return float(confidence_score)

def calculate_collapse_quantum_uncertainty(
    pre_logits: np.ndarray,
    post_logits: np.ndarray
) -> float:
    """
    ✰ COLLAPSE: Calculate Heisenberg-inspired uncertainty metric
    
    This metric applies the quantum-inspired uncertainty principle to
    transformer outputs, measuring uncertainty across the collapse.
    
    Args:
        pre_logits: Logits before collapse
        post_logits: Logits after collapse
        
    Returns:
        Quantum uncertainty metric (0.0 = certain, 1.0 = maximally uncertain)
    """
    # Return 0 if arrays are empty
    if pre_logits.size == 0 or post_logits.size == 0:
        return 0.0
    
    # Handle shape mismatches
    if pre_logits.shape != post_logits.shape:
        logger.warning(f"Logit shape mismatch: {pre_logits.shape} vs {post_logits.shape}")
        return 0.0
    
    try:
        # Calculate "position" uncertainty (variance in token probabilities)
        pre_probs = softmax(pre_logits)
        post_probs = softmax(post_logits)
        
        pos_uncertainty = np.mean(np.var(post_probs, axis=-1))
        
        # Calculate "momentum" uncertainty (change rate between states)
        mom_uncertainty = np.mean(np.abs(post_probs - pre_probs))
        
        # Combined metric inspired by Heisenberg uncertainty
        # Higher values in both dimensions indicate more quantum-like behavior
        uncertainty_product = pos_uncertainty * mom_uncertainty
        
        # Normalize to 0-1 range (empirically determined max is around 0.25)
        normalized_uncertainty = min(1.0, uncertainty_product * 4)
        
        return float(normalized_uncertainty)
    except Exception as e:
        logger.error(f"Error calculating quantum uncertainty: {e}")
        return 0.0

def calculate_collapse_coherence(
    attribution_graph: Any,
    threshold: float = 0.1
) -> float:
    """
    △ OBSERVE: Calculate coherence of attribution paths post-collapse
    
    This metric quantifies how coherent the attribution paths remain
    after collapse, reflecting the "quantum coherence" of the system.
    
    Args:
        attribution_graph: Graph of attribution paths
        threshold: Minimum edge weight to consider
        
    Returns:
        Coherence score (0.0 = incoherent, 1.0 = fully coherent)
    """
    # This is a simplified version for when an actual graph isn't available
    # In real implementation, would analyze graph structure
    
    # If no graph provided, return 0
    if attribution_graph is None:
        return 0.0
    
    try:
        # If graph has coherence attribute, use it
        if hasattr(attribution_graph, 'continuity_score'):
            return float(attribution_graph.continuity_score)
        
        # Otherwise return placeholder value
        return 0.5  # Placeholder mid-value
    except Exception as e:
        logger.error(f"Error calculating collapse coherence: {e}")
        return 0.0

def softmax(x: np.ndarray) -> np.ndarray:
    """Apply softmax function to convert logits to probabilities."""
    exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return exp_x / np.sum(exp_x, axis=-1, keepdims=True)

def calculate_collapse_metrics_bundle(
    pre_state: Dict[str, Any],
    post_state: Dict[str, Any],
    ghost_circuits: Optional[List[Dict[str, Any]]] = None,
    attribution_graph: Optional[Any] = None
) -> Dict[str, float]:
    """
    △ OBSERVE: Calculate a complete bundle of collapse metrics
    
    This convenience function calculates multiple collapse metrics
    at once, returning a dictionary of results.
    
    Args:
        pre_state: Model state before collapse
        post_state: Model state after collapse
        ghost_circuits: Optional list of detected ghost circuits
        attribution_graph: Optional attribution graph
        
    Returns:
        Dictionary mapping metric names to values
    """
    metrics = {}
    
    # Extract relevant state components
    pre_weights = pre_state.get("attention_weights", np.array([]))
    post_weights = post_state.get("attention_weights", np.array([]))
    pre_logits = pre_state.get("logits", np.array([]))
    post_logits = post_state.get("logits", np.array([]))
    
    # Calculate metrics
    metrics["collapse_rate"] = calculate_collapse_rate(pre_weights, post_weights)
    metrics["path_continuity"] = measure_path_continuity(pre_weights, post_weights)
    metrics["attribution_entropy"] = measure_attribution_entropy(post_weights)
    
    if ghost_circuits:
        metrics["ghost_circuit_strength"] = calculate_ghost_circuit_strength(ghost_circuits)
    
    if pre_logits.size > 0 and post_logits.size > 0:
        metrics["quantum_uncertainty"] = calculate_collapse_quantum_uncertainty(pre_logits, post_logits)
    
    if attribution_graph is not None:
        metrics["collapse_coherence"] = calculate_collapse_coherence(attribution_graph)
    
    return metrics


if __name__ == "__main__":
    # Simple usage example
    
    # Create synthetic pre and post states
    pre_state = {
        "attention_weights": np.random.random((8, 10, 10)),  # 8 heads, 10 tokens
        "logits": np.random.random((1, 10, 1000))  # Batch 1, 10 tokens, 1000 vocab
    }
    
    # Create post state with changes to simulate collapse
    post_state = {
        "attention_weights": pre_state["attention_weights"] * np.random.uniform(0.5, 1.0, pre_state["attention_weights"].shape),
        "logits": pre_state["logits"] * 0.2 + np.random.random((1, 10, 1000)) * 0.8  # Shifted logits
    }
    
    # Calculate individual metrics
    collapse_rate = calculate_collapse_rate(pre_state["attention_weights"], post_state["attention_weights"])
    path_continuity = measure_path_continuity(pre_state["attention_weights"], post_state["attention_weights"])
    attribution_entropy = measure_attribution_entropy(post_state["attention_weights"])
    quantum_uncertainty = calculate_collapse_quantum_uncertainty(pre_state["logits"], post_state["logits"])
    
    print(f"Collapse Rate: {collapse_rate:.3f}")
    print(f"Path Continuity: {path_continuity:.3f}")
    print(f"Attribution Entropy: {attribution_entropy:.3f}")
    print(f"Quantum Uncertainty: {quantum_uncertainty:.3f}")
    
    # Calculate complete metrics bundle
    metrics_bundle = calculate_collapse_metrics_bundle(pre_state, post_state)
    
    print("\nMetrics Bundle:")
    for metric, value in metrics_bundle.items():
        print(f"  {metric}: {value:.3f}")

        path_weights
