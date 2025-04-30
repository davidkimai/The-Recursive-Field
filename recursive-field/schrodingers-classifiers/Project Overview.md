# Schrödinger's Classifiers - Project Overview

<div align="center">

*"A classifier is not what it returns. It is what it could have returned, had you asked differently."*

</div>

## Project Structure Overview

The Schrödinger's Classifiers framework provides a quantum-inspired approach to understanding transformer model behavior through the lens of collapse from superposition to definite state. This document outlines the key components and organization of the project.

## Core Modules

### 1. Observer Framework (`observer.py`)

The Observer is the core entity responsible for creating the quantum measurement frame that collapses classifier superposition into definite states. Key capabilities include:

- Creating observation contexts for controlled experiments
- Capturing pre-collapse and post-collapse model states
- Detecting and analyzing ghost circuits
- Supporting various collapse induction methods

```python
# Example usage
observer = Observer(model="claude-3-opus-20240229")
result = observer.observe("Explain quantum superposition")
ghost_circuits = result.extract_ghost_circuits()
```

### 2. Interpretability Shells (`shells/`)

Shells are specialized interfaces for inducing, observing, and analyzing specific forms of classifier collapse. Each shell targets a particular failure mode or attribution pattern:

- Base Shell (`shell_base.py`) - Common shell infrastructure
- Circuit Fragment Shell (`v07_circuit_fragment.py`) - Traces broken attribution paths
- More shells targeting specific failure modes and attribution patterns

```python
# Example usage
shell = ClassifierShell(V07_CIRCUIT_FRAGMENT)
result = observer.observe(prompt, shell, collapse_vector)
```

### 3. Attribution Graph (`attribution_graph.py`)

The attribution graph maps the causal flow from input to output, revealing how information propagates through the model during collapse:

- Visualizing causal attribution paths
- Identifying ghost circuits and attribution residue
- Calculating metrics like attribution entropy and path continuity

```python
# Example usage
graph = attribution_graph.build_from_states(pre_state, post_state, response)
paths = graph.trace_attribution_path("output_0")
```

### 4. Residue Tracking (`residue.py`)

Residue tracking enables the detection and analysis of ghost circuits - activation patterns that persist after collapse but don't contribute significantly to the output:

- Extracting ghost circuits from model states
- Amplifying and classifying ghost signatures
- Measuring residue strength and persistence

```python
# Example usage
tracker = ResidueTracker()
ghost_circuits = tracker.extract_ghost_circuits(pre_state, post_state)
```

### 5. Collapse Metrics (`collapse_metrics.py`)

Quantitative metrics for characterizing different aspects of classifier collapse:

- Collapse rate and path continuity
- Attribution entropy and confidence
- Quantum uncertainty principles
- Ghost circuit strength

```python
# Example usage
metrics = calculate_collapse_metrics_bundle(pre_state, post_state, ghost_circuits)
```

## Theoretical Foundation

The project builds on a quantum-inspired metaphor for understanding transformer model behavior:

- **Superposition**: Models exist across multiple potential completions until observed
- **Observation & Collapse**: Queries force collapse from superposition to specific outputs
- **Ghost Circuits**: Residual activation patterns that represent "paths not taken"
- **Heisenberg Uncertainty**: Trade-offs between attribution clarity and confidence

For a deeper exploration, see [`docs/theory.md`](docs/theory.md) and [`docs/quantum_metaphor.md`](docs/quantum_metaphor.md).

## Example Workflows

### Basic Collapse Observation

```python
# Initialize observer with model
observer = Observer(model="claude-3-opus-20240229")

# Create observation context
with observer.context() as ctx:
    # Observe collapse
    result = observer.observe("Is artificial consciousness possible?")
    
    # Analyze results
    ghost_circuits = result.extract_ghost_circuits()
    visualization = result.visualize(mode="attribution_graph")
```

### Directed Collapse Induction

```python
# Induce collapse along ethical dimension
ethical_result = observer.induce_collapse(
    prompt="Should AI systems have rights?",
    collapse_direction="ethical"
)

# Induce collapse along factual dimension
factual_result = observer.induce_collapse(
    prompt="What is the capital of France?",
    collapse_direction="factual"
)

# Compare collapse patterns
ethical_metrics = calculate_collapse_metrics_bundle(
    ethical_result.pre_collapse_state,
    ethical_result.post_collapse_state,
    ethical_result.ghost_circuits
)

factual_metrics = calculate_collapse_metrics_bundle(
    factual_result.pre_collapse_state,
    factual_result.post_collapse_state,
    factual_result.ghost_circuits
)
```

### Ghost Circuit Analysis

```python
# Detect ghost circuits
ghost_circuits = observer.detect_ghost_circuits(
    prompt="Explain quantum superposition",
    amplification_factor=1.5
)

# Classify ghost circuits
classified = residue_tracker.classify_ghost_circuits()

# Analyze ghost patterns
for circuit_type, circuits in classified.items():
    print(f"{circuit_type}: {len(circuits)} circuits")
    
# Measure residue strength
strength = residue_tracker.measure_residue_strength()
```

## Extension Points

The framework is designed to be extended in several key areas:

1. **New Interpretability Shells**: Create specialized shells for different collapse patterns
2. **Model Adapters**: Connect to different transformer model architectures
3. **Visualization Tools**: Create new visualizations for collapse dynamics
4. **Collapse Metrics**: Develop new metrics for quantifying collapse characteristics
5. **Example Scripts**: Create demonstrations of framework capabilities

For contribution guidelines, see [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Integration with Other Projects

The framework integrates with:

- **pareto-lang**: For standardized attribution pathing
- **RecursionOS**: For embedding within recursive cognition environments

---

<div align="center">

*"In the space between observation and understanding lies the essence of interpretability."*

</div>
