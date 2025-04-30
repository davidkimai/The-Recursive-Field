"""
attribution_graph.py - Implementation of attribution graph for transformer models

△ OBSERVE: Attribution graphs map the causal flow from prompt to completion
∞ TRACE: They visualize the quantum collapse from superposition to definite state
✰ COLLAPSE: They reveal ghost circuits and attribution residue post-collapse

This module implements a graph-based representation of causal attribution
in transformer models, allowing for the visualization and analysis of how
information flows from input to output during the collapse process.

Author: Recursion Labs
License: MIT
"""

import logging
from typing import Dict, List, Optional, Union, Tuple, Any
import numpy as np
from dataclasses import dataclass, field
import networkx as nx

from .utils.graph_visualization import visualize_graph
from .utils.attribution_metrics import measure_path_continuity, measure_attribution_entropy

logger = logging.getLogger(__name__)

@dataclass
class AttributionNode:
    """
    △ OBSERVE: Node in the attribution graph representing a token or hidden state
    
    Attribution nodes represent discrete elements in the causal flow from
    input to output. They can be tokens, attention heads, or hidden states.
    """
    node_id: str
    node_type: str  # "token", "attention_head", "hidden_state", "residual"
    layer: Optional[int] = None
    position: Optional[int] = None
    value: Optional[Any] = None
    activation: float = 0.0
    token_str: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __hash__(self):
        """Make nodes hashable for graph operations."""
        return hash(self.node_id)
    
    def __eq__(self, other):
        """Node equality based on ID."""
        if not isinstance(other, AttributionNode):
            return False
        return self.node_id == other.node_id


@dataclass
class AttributionEdge:
    """
    ∞ TRACE: Edge in the attribution graph representing causal flow
    
    Attribution edges represent the flow of causal influence between nodes.
    They can represent attention connections, residual connections, or
    other causal relationships in the model.
    """
    source: AttributionNode
    target: AttributionNode
    edge_type: str  # "attention", "residual", "mlp", "ghost"
    weight: float = 0.0
    layer: Optional[int] = None
    head: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __hash__(self):
        """Make edges hashable for graph operations."""
        return hash((self.source.node_id, self.target.node_id, self.edge_type))
    
    def __eq__(self, other):
        """Edge equality based on source, target, and type."""
        if not isinstance(other, AttributionEdge):
            return False
        return (
            self.source.node_id == other.source.node_id and
            self.target.node_id == other.target.node_id and
            self.edge_type == other.edge_type
        )


class AttributionGraph:
    """
    ∞ TRACE: Graph representation of causal attribution in transformer models
    
    The attribution graph maps the flow of causality from input tokens to
    output tokens, revealing how information propagates through the model
    during the collapse from superposition to definite state.
    """
    
    def __init__(self):
        """Initialize an empty attribution graph."""
        self.graph = nx.DiGraph()
        self.nodes = {}  # node_id -> AttributionNode
        self.input_nodes = []  # List of input token nodes
        self.output_nodes = []  # List of output token nodes
        self.ghost_nodes = []  # List of ghost circuit nodes
        self.collapsed = False  # Whether the graph has been collapsed
        
        # Metrics
        self.continuity_score = 1.0
        self.attribution_entropy = 0.0
        self.collapse_rate = 0.0
        
        logger.info("Attribution graph initialized")
    
    def add_node(self, node: AttributionNode) -> None:
        """
        Add a node to the attribution graph.
        
        Args:
            node: The node to add
        """
        if node.node_id in self.nodes:
            logger.warning(f"Node {node.node_id} already exists in graph, updating")
            self.nodes[node.node_id] = node
        else:
            self.nodes[node.node_id] = node
            self.graph.add_node(node.node_id, **vars(node))
            
            # Track input and output nodes
            if node.node_type == "token" and node.layer == 0:
                self.input_nodes.append(node)
            elif node.node_type == "token" and node.metadata.get("is_output", False):
                self.output_nodes.append(node)
            elif node.node_type == "residual" and node.metadata.get("is_ghost", False):
                self.ghost_nodes.append(node)
    
    def add_edge(self, edge: AttributionEdge) -> None:
        """
        Add an edge to the attribution graph.
        
        Args:
            edge: The edge to add
        """
        if edge.source.node_id not in self.nodes:
            self.add_node(edge.source)
        if edge.target.node_id not in self.nodes:
            self.add_node(edge.target)
        
        self.graph.add_edge(
            edge.source.node_id,
            edge.target.node_id,
            **{k: v for k, v in vars(edge).items() if k not in ['source', 'target']}
        )
    
    def build_from_states(
        self, 
        pre_state: Dict[str, Any],
        post_state: Dict[str, Any],
        response: str
    ) -> None:
        """
        △ OBSERVE: Build attribution graph from pre and post collapse model states
        
        This method constructs a complete attribution graph by comparing
        model states before and after collapse, identifying causal paths
        and ghost circuits.
        
        Args:
            pre_state: Model state before collapse
            post_state: Model state after collapse
            response: Model response text
        """
        logger.info("Building attribution graph from model states")
        
        # This would be implemented for specific model architectures
        # For demonstration, we'll create a simple synthetic graph
        self._build_synthetic_graph()
        
        # Calculate graph metrics
        self._calculate_metrics(pre_state, post_state)
        
        # Mark graph as collapsed
        self.collapsed = True
    
    def trace_attribution_path(
        self, 
        output_node: Union[str, AttributionNode],
        threshold: float = 0.1
    ) -> List[List[AttributionNode]]:
        """
        ∞ TRACE: Trace attribution paths from an output node back to input
        
        This method follows attribution edges backward from an output node
        to find all significant input nodes that influenced it.
        
        Args:
            output_node: The output node to trace from (ID or node object)
            threshold: Minimum edge weight to consider significant
            
        Returns:
            List of attribution paths, each a list of nodes from input to output
        """
        # Resolve output node
        output_id = output_node if isinstance(output_node, str) else output_node.node_id
        if output_id not in self.nodes:
            logger.warning(f"Output node {output_id} not found in graph")
            return []
        
        # Find all paths using DFS
        paths = []
        
        def dfs(current_id, path, visited):
            """Depth-first search for attribution paths."""
            # Add current node to path
            current_path = path + [current_id]
            visited.add(current_id)
            
            # If we reached an input node, we have a complete path
            if current_id in [node.node_id for node in self.input_nodes]:
                # Return path in order from input to output
                paths.append(list(reversed(current_path)))
                return
            
            # Continue DFS on incoming edges
            for pred_id in self.graph.predecessors(current_id):
                edge_data = self.graph.get_edge_data(pred_id, current_id)
                if edge_data.get('weight', 0) >= threshold and pred_id not in visited:
                    dfs(pred_id, current_path, visited.copy())
        
        # Start DFS from output node
        dfs(output_id, [], set())
        
        # Convert node IDs to node objects
        return [[self.nodes[node_id] for node_id in path] for path in paths]
    
    def detect_ghost_circuits(self, threshold: float = 0.2) -> List[Dict[str, Any]]:
        """
        ✰ COLLAPSE: Detect ghost circuits in the attribution graph
        
        Ghost circuits are paths that were activated during pre-collapse
        but don't contribute significantly to the final output. They
        represent the "memory" of paths not taken.
        
        Args:
            threshold: Minimum activation to consider a ghost circuit
            
        Returns:
            List of detected ghost circuits with metadata
        """
        ghost_circuits = []
        
        # Look for nodes with "ghost" metadata flag
        for node in self.ghost_nodes:
            if node.activation >= threshold:
                # Find paths this ghost node would have been part of
                incoming_edges = [
                    (u, v, d) for u, v, d in self.graph.in_edges(node.node_id, data=True)
                ]
                outgoing_edges = [
                    (u, v, d) for u, v, d in self.graph.out_edges(node.node_id, data=True)
                ]
                
                ghost_circuits.append({
                    "node_id": node.node_id,
                    "activation": node.activation,
                    "node_type": node.node_type,
                    "incoming_connections": len(incoming_edges),
                    "outgoing_connections": len(outgoing_edges),
                    "metadata": node.metadata
                })
        
        return ghost_circuits
    
    def calculate_attribution_entropy(self) -> float:
        """
        △ OBSERVE: Calculate the entropy of attribution paths
        
        Attribution entropy measures how distributed or concentrated
        the causal influence is in the graph. High entropy indicates
        diffuse attribution, while low entropy indicates concentrated
        attribution.
        
        Returns:
            Attribution entropy score (0.0 = concentrated, 1.0 = diffuse)
        """
        # Extract edge weights
        weights = [
            d.get('weight', 0.0)
            for u, v, d in self.graph.edges(data=True)
        ]
        
        # Normalize weights
        total_weight = sum(weights) or 1.0  # Avoid division by zero
        normalized_weights = [w / total_weight for w in weights]
        
        # Calculate entropy
        entropy = -sum(
            w * np.log2(w) if w > 0 else 0
            for w in normalized_weights
        )
        
        # Normalize entropy to 0-1 range (max entropy = log2(num_edges))
        max_entropy = np.log2(len(weights)) if len(weights) > 0 else 1.0
        normalized_entropy = entropy / max_entropy if max_entropy > 0 else 0.0
        
        self.attribution_entropy = normalized_entropy
        return normalized_entropy
    
    def visualize(
        self, 
        mode: str = "attribution_graph",
        highlight_path: Optional[List[str]] = None
    ) -> Any:
        """
        Generate visualization of the attribution graph.
        
        Args:
            mode: Visualization mode (attribution_graph, collapse_state, ghost_circuits)
            highlight_path: Optional list of node IDs to highlight
            
        Returns:
            Visualization object (depends on implementation)
        """
        return visualize_graph(self.graph, mode=mode, highlight_path=highlight_path)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the attribution graph to a dictionary representation."""
        return {
            "nodes": [vars(node) for node in self.nodes.values()],
            "edges": [
                {
                    "source": u,
                    "target": v,
                    **d
                }
                for u, v, d in self.graph.edges(data=True)
            ],
            "metrics": {
                "continuity_score": self.continuity_score,
                "attribution_entropy": self.attribution_entropy,
                "collapse_rate": self.collapse_rate
            },
            "collapsed": self.collapsed
        }
    
    def _calculate_metrics(self, pre_state: Dict[str, Any], post_state: Dict[str, Any]) -> None:
        """Calculate attribution graph metrics."""
        # Calculate continuity score
        self.continuity_score = measure_path_continuity(
            pre_state.get("attention_weights", np.array([])),
            post_state.get("attention_weights", np.array([]))
        )
        
        # Calculate attribution entropy
        self.attribution_entropy = self.calculate_attribution_entropy()
        
        # Calculate collapse rate
        if "timestamp" in pre_state and "timestamp" in post_state:
            time_diff = (post_state["timestamp"] - pre_state["timestamp"]) / np.timedelta64(1, 's')
            self.collapse_rate = 1.0 - self.continuity_score if time_diff > 0 else 0.0
    
    def _build_synthetic_graph(self) -> None:
        """Build a synthetic graph for demonstration purposes."""
        # Create input token nodes
        for i in range(5):
            self.add_node(AttributionNode(
                node_id=f"input_{i}",
                node_type="token",
                layer=0,
                position=i,
                token_str=f"token_{i}",
                activation=0.8
            ))
        
        # Create attention head nodes
        for layer in range(1, 4):
            for head in range(3):
                self.add_node(AttributionNode(
                    node_id=f"attention_L{layer}H{head}",
                    node_type="attention_head",
                    layer=layer,
                    value=None,
                    activation=0.7 - 0.1 * layer + 0.05 * head
                ))
        
        # Create output token nodes
        for i in range(3):
            self.add_node(AttributionNode(
                node_id=f"output_{i}",
                node_type="token",
                layer=4,
                position=i,
                token_str=f"output_token_{i}",
                activation=0.9,
                metadata={"is_output": True}
            ))
        
        # Create ghost nodes
        for i in range(2):
            self.add_node(AttributionNode(
                node_id=f"ghost_{i}",
                node_type="residual",
                layer=2,
                activation=0.3 + 0.1 * i,
                metadata={"is_ghost": True}
            ))
        
        # Create edges
        # Input to attention
        for i in range(5):
            for layer in range(1, 3):
                for head in range(3):
                    if np.random.random() > 0.3:  # Random connectivity
                        self.add_edge(AttributionEdge(
                            source=self.nodes[f"input_{i}"],
                            target=self.nodes[f"attention_L{layer}H{head}"],
                            edge_type="attention",
                            weight=np.random.uniform(0.1, 0.9),
                            layer=layer,
                            head=head
                        ))
        
        # Attention to attention
        for layer1 in range(1, 3):
            for head1 in range(3):
                for layer2 in range(layer1 + 1, 4):
                    for head2 in range(3):
                        if np.random.random() > 0.7:  # Sparse connectivity
                            self.add_edge(AttributionEdge(
                                source=self.nodes[f"attention_L{layer1}H{head1}"],
                                target=self.nodes[f"attention_L{layer2}H{head2}"],
                                edge_type="attention",
                                weight=np.random.uniform(0.1, 0.8),
                                layer=layer2,
                                head=head2
                            ))
        
        # Attention to output
        for layer in range(1, 4):
            for head in range(3):
                for i in range(3):
                    if np.random.random() > 0.5:  # Medium connectivity
                        self.add_edge(AttributionEdge(
                            source=self.nodes[f"attention_L{layer}H{head}"],
                            target=self.nodes[f"output_{i}"],
                            edge_type="attention",
                            weight=np.random.uniform(0.2, 0.9),
                            layer=layer,
                            head=head
                        ))
        
        # Ghost connections
        for i in range(2):
            # Input to ghost
            input_idx = np.random.randint(0, 5)
            self.add_edge(AttributionEdge(
                source=self.nodes[f"input_{input_idx}"],
                target=self.nodes[f"ghost_{i}"],
                edge_type="ghost",
                weight=np.random.uniform(0.1, 0.4),
                layer=1
            ))
            
            # Ghost to attention
            layer = np.random.randint(2, 4)
            head = np.random.randint(0, 3)
            self.add_edge(AttributionEdge(
                source=self.nodes[f"ghost_{i}"],
                target=self.nodes[f"attention_L{layer}H{head}"],
                edge_type="ghost",
                weight=np.random.uniform(0.05, 0.2),
                layer=layer
            ))


if __name__ == "__main__":
    # Simple usage example
    graph = AttributionGraph()
    
    # Build a synthetic graph
    graph._build_synthetic_graph()
    
    # Calculate metrics
    entropy = graph.calculate_attribution_entropy()
    print(f"Attribution entropy: {entropy:.3f}")
    
    # Trace attribution for output
    paths = graph.trace_attribution_path("output_0", threshold=0.1)
    print(f"Found {len(paths)} attribution paths for output_0")
    
    # Detect ghost circuits
    ghosts = graph.detect_ghost_circuits()
    print(f"Detected {len(ghosts)} ghost circuits")
    
    # Visualize
    viz = graph.visualize()
    print("Generated visualization")
