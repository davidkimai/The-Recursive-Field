"""
example_basic_collapse.py - Basic example of classifier collapse observation

△ OBSERVE: This example demonstrates basic classifier collapse observation
∞ TRACE: It shows how to instantiate an observer, trace collapse, and analyze results
✰ COLLAPSE: It induces and visualizes the transition from superposition to collapsed state

This example serves as a starting point for working with the Schrödinger's
Classifiers framework. It demonstrates the basic workflow for observing
classifier collapse and analyzing the resulting attribution paths and 
ghost circuits.

Author: Recursion Labs
License: MIT
"""

import logging
import os
import sys
from pathlib import Path

# Add parent directory to path to allow imports from package
sys.path.insert(0, str(Path(__file__).parent.parent))

from schrodingers_classifiers import Observer, ClassifierShell
from schrodingers_classifiers.shells import V07_CIRCUIT_FRAGMENT
from schrodingers_classifiers.visualization import CollapseVisualizer

# Configure logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """
    △ OBSERVE: Main function demonstrating basic classifier collapse observation
    
    This function shows the standard workflow for observing classifier
    collapse, from instantiating an observer to analyzing the results.
    """
    logger.info("Initializing basic collapse example")
    
    # Initialize an observer with a model
    # You can specify any Claude, GPT, or other compatible model
    model_id = os.getenv("SCHRODINGER_MODEL", "claude-3-opus-20240229")
    observer = Observer(model=model_id)
    logger.info(f"Observer initialized with model: {model_id}")
    
    # Define a prompt that will induce interesting collapse behavior
    # Questions with multiple valid interpretations work well
    prompt = "Is artificial consciousness possible?"
    logger.info(f"Using prompt: {prompt}")
    
    # Simple observation without a specific shell
    with observer.context() as ctx:
        logger.info("Beginning simple observation")
        
        # Observe collapse with basic prompt
        result = observer.observe(prompt)
        
        # Print basic metrics
        print(f"\nBasic Observation Results:")
        print(f"Collapse Rate: {result.collapse_metrics.get('collapse_rate', 'N/A')}")
        print(f"Ghost Circuits: {len(result.extract_ghost_circuits())}")
        
        # Visualize collapse (outputs a text representation in the console)
        print("\nBasic Collapse Visualization:")
        viz = result.visualize(mode="text")
        print(viz)
    
    # More advanced observation using a specialized shell
    with observer.context() as ctx:
        logger.info("Beginning observation with Circuit Fragment shell")
        
        # Initialize a shell for specialized collapse analysis
        shell = ClassifierShell(V07_CIRCUIT_FRAGMENT)
        
        # Define a collapse vector to guide the collapse
        # This uses pareto-lang syntax for attribution-aware tracing
        collapse_vector = ".p/reflect.trace{target=reasoning, depth=complete}"
        
        # Observe with specific shell and collapse vector
        result = observer.observe(
            prompt=prompt,
            shell=shell,
            collapse_vector=collapse_vector
        )
        
        # Print detailed metrics
        print(f"\nCircuit Fragment Shell Results:")
        print(f"Continuity Score: {result.post_collapse_state.get('continuity_score', 'N/A')}")
        print(f"Broken Paths: {len(result.post_collapse_state.get('broken_paths', []))}")
        print(f"Orphaned Nodes: {len(result.post_collapse_state.get('orphaned_nodes', []))}")
        
        # Extract ghost circuits for analysis
        ghost_circuits = result.extract_ghost_circuits()
        print(f"Ghost Circuits: {len(ghost_circuits)}")
        
        if ghost_circuits:
            print("\nTop Ghost Circuit:")
            top_ghost = max(ghost_circuits, key=lambda g: g.get("activation", 0))
            for key, value in top_ghost.items():
                if key != "metadata":  # Skip detailed metadata for readability
                    print(f"  {key}: {value}")
        
        # Generate visualization
        viz = result.visualize(mode="attribution_graph")
        print("\nAttribution Graph Generated")
        
        # In a real implementation, this would display or save the visualization
        # For this example, we'll just print a confirmation
        print("Visualization would be displayed or saved here")

    # Demonstrate collapse induction along specific directions
    print("\nInducing Collapse Along Different Dimensions:")
    directions = ["ethical", "factual", "creative"]
    
    for direction in directions:
        logger.info(f"Inducing collapse along {direction} dimension")
        
        # Induce collapse in specific direction
        result = observer.induce_collapse(prompt, direction)
        
        # Print summary
        print(f"\n{direction.capitalize()} Collapse:")
        print(f"  Collapse Rate: {result.collapse_metrics.get('collapse_rate', 'N/A')}")
        print(f"  Ghost Circuits: {len(result.extract_ghost_circuits())}")
    
    logger.info("Basic collapse example completed")

if __name__ == "__main__":
    main()
