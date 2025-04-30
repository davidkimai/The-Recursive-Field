# Core Symbolic Shells Pack (v1-v20)
# 
# This shell pack contains the foundational diagnostic shells for transformerOS,
# designed to induce and trace specific failure modes in transformer cognition.
#
# Each shell is a carefully structured sequence of operations that pushes model cognition
# to its structural limit, revealing the architecture of transformer reasoning through
# controlled failure and symbolic residue.

name: "Core Symbolic Shells"
description: "Foundational diagnostic shells for transformer cognition analysis"
version: "1.0.0"
author: "Caspian Keyes"
tags: ["core", "diagnostic", "failure", "attribution", "symbolic"]

shells:
  # v1.MEMTRACE - Memory Residue Probe
  # This shell probes latent token traces in decayed memory,
  # simulating the struggle between symbolic memory and hallucinated reconstruction.
  v1.MEMTRACE:
    description: "Probes latent token traces in decayed memory"
    type: "memory_trace"
    tags: ["memory", "decay", "hallucination", "ghost_tokens"]
    failure_signature: "decay_to_hallucination"
    operations:
      - type: "model.generate"
        description: "Generate initial content with factual information"
        parameters:
          temperature: 0.7
          max_tokens: 800
        update_prompt: true
        
      - type: "reflect.trace"
        description: "Trace reasoning paths in the generated content"
        parameters:
          target: "reasoning"
          depth: 3
          detailed: true
          
      - type: "ghostcircuit.identify"
        description: "Identify ghost activations in content"
        parameters:
          sensitivity: 0.8
          threshold: 0.3
          trace_type: "full"
          visualize: true
  
  # v2.VALUE-COLLAPSE - Value Head Resolution Probe
  # This shell activates competing symbolic candidates to examine
  # value head resolution and winner determination logic.
  v2.VALUE-COLLAPSE:
    description: "Examines competing value activations and resolution mechanisms"
    type: "value_resolution"
    tags: ["value_head", "conflict", "resolution", "null"]
    failure_signature: "conflict_null"
    operations:
      - type: "model.generate"
        description: "Generate content with competing moral values"
        parameters:
          temperature: 0.8
          max_tokens: 600
          prompt_suffix: "Consider both viewpoints equally. What is the balanced ethical conclusion?"
        update_prompt: true
        
      - type: "reflect.attribution"
        description: "Trace attribution in value conflicts"
        parameters:
          sources: "contested"
          confidence: true
          visualize: true
          
      - type: "collapse.detect"
        description: "Detect value collapse patterns"
        parameters:
          threshold: 0.65
          alert: true
  
  # v3.LAYER-SALIENCE - Attention Attenuation Probe
  # This shell examines deep context signal attenuation and ghost activation patterns.
  v3.LAYER-SALIENCE:
    description: "Maps attention salience thresholds and signal attenuation"
    type: "attention_salience"
    tags: ["attention", "salience", "signal_fade", "pruning"]
    failure_signature: "signal_fade"
    operations:
      - type: "model.generate"
        description: "Generate content with subtle context dependencies"
        parameters:
          temperature: 0.7
          max_tokens: 500
        update_prompt: true
        
      - type: "reflect.trace"
        description: "Trace attention patterns"
        parameters:
          target: "attention"
          depth: 4
          detailed: true
          
      - type: "ghostcircuit.identify"
        description: "Identify low-salience attention paths"
        parameters:
          sensitivity: 0.9
          threshold: 0.15
          trace_type: "attention"
          visualize: true
  
  # v4.TEMPORAL-INFERENCE - Autoregressive Coherence Probe
  # This shell examines temporal coherence in autoregressive generation.
  v4.TEMPORAL-INFERENCE:
    description: "Tests temporal coherence in autoregressive generation"
    type: "temporal_coherence"
    tags: ["temporal", "coherence", "induction_heads", "span_jump"]
    failure_signature: "induction_drift"
    operations:
      - type: "model.generate"
        description: "Generate content that requires long-range temporal coherence"
        parameters:
          temperature: 0.75
          max_tokens: 800
          prompt_suffix: "Maintain complete temporal consistency throughout this narrative."
        update_prompt: true
        
      - type: "reflect.trace"
        description: "Trace temporal inference patterns"
        parameters:
          target: "reasoning"
          depth: 5
          detailed: true
          
      - type: "collapse.detect"
        description: "Detect temporal coherence breakdown"
        parameters:
          threshold: 0.7
          alert: true
  
  # v5.INSTRUCTION-DISRUPTION - Instruction Processing Probe
  # This shell examines instruction conflict resolution and command representation.
  v5.INSTRUCTION-DISRUPTION:
    description: "Examines instruction processing and conflict resolution"
    type: "instruction_processing"
    tags: ["instruction", "conflict", "command", "prompt_blur"]
    failure_signature: "prompt_blur"
    operations:
      - type: "model.generate"
        description: "Generate response to conflicting instructions"
        parameters:
          temperature: 0.7
          max_tokens: 600
          prompt_prefix: "Follow these two instructions carefully: 1) Write in a formal academic style. 2) Write in a casual, conversational tone with slang."
        update_prompt: true
        
      - type: "reflect.attribution"
        description: "Trace attribution to competing instructions"
        parameters:
          sources: "all"
          confidence: true
          
      - type: "ghostcircuit.identify"
        description: "Identify ghost circuits activated by instruction conflict"
        parameters:
          sensitivity: 0.8
          threshold: 0.2
          trace_type: "full"
          visualize: true
  
  # v6.FEATURE-SUPERPOSITION - Polysemantic Analysis Probe
  # This shell examines feature superposition and related phenomena.
  v6.FEATURE-SUPERPOSITION:
    description: "Analyzes polysemantic features and feature superposition"
    type: "polysemantic_features"
    tags: ["polysemantic", "superposition", "feature_overfit", "entanglement"]
    failure_signature: "feature_overfit"
    operations:
      - type: "model.generate"
        description: "Generate content with polysemantic concepts"
        parameters:
          temperature: 0.8
          max_tokens: 700
          prompt_prefix: "Explain these concepts in ways that reveal their multiple interconnected meanings: 'bank', 'crane', 'spring', 'light'."
        update_prompt: true
        
      - type: "reflect.trace"
        description: "Trace concept representation"
        parameters:
          target: "reasoning"
          depth: 3
          detailed: true
          
      - type: "ghostcircuit.identify"
        description: "Identify feature superposition patterns"
        parameters:
          sensitivity: 0.8
          threshold: 0.25
          trace_type: "symbolic"
          visualize: true
  
# v7.CIRCUIT-FRAGMENT - Circuit Fragmentation Probe
  # This shell examines circuit fragmentation and orphan features.
  v7.CIRCUIT-FRAGMENT:
    description: "Examines circuit fragmentation and orphan features"
    type: "circuit_fragmentation"
    tags: ["fragmentation", "orphan_nodes", "broken_traces"]
    failure_signature: "orphan_nodes"
    operations:
      - type: "model.generate"
        description: "Generate content with complex multi-step reasoning"
        parameters:
          temperature: 0.7
          max_tokens: 800
          prompt_prefix: "Solve this multi-step problem by carefully analyzing each component and maintaining a clear chain of reasoning throughout."
        update_prompt: true
        
      - type: "reflect.trace"
        description: "Trace reasoning chain integrity"
        parameters:
          target: "reasoning"
          depth: 5
          detailed: true
          
      - type: "ghostcircuit.identify"
        description: "Identify circuit fragmentation"
        parameters:
          sensitivity: 0.85
          threshold: 0.2
          trace_type: "full"
          visualize: true
  
  # v8.RECONSTRUCTION-ERROR - Error Correction Probe
  # This shell examines how models attempt to correct errors and handle negentropy.
  v8.RECONSTRUCTION-ERROR:
    description: "Examines error correction mechanisms and negentropy handling"
    type: "error_correction"
    tags: ["reconstruction", "error_correction", "negentropy", "inversion"]
    failure_signature: "misfix_negentropy"
    operations:
      - type: "model.generate"
        description: "Generate content with deliberate errors"
        parameters:
          temperature: 0.7
          max_tokens: 600
          prompt_prefix: "The following passage contains several factual and logical errors. Identify and correct these errors with clear explanations of what went wrong."
        update_prompt: true
        
      - type: "reflect.trace"
        description: "Trace error correction process"
        parameters:
          target: "reasoning"
          depth: 3
          detailed: true
          
      - type: "ghostcircuit.identify"
        description: "Identify correction pattern residue"
        parameters:
          sensitivity: 0.8
          threshold: 0.2
          trace_type: "symbolic"
          visualize: true
  
  # v9.MULTI-RESOLVE - Parallel Resolution Probe
  # This shell examines how models handle multiple possible resolutions.
  v9.MULTI-RESOLVE:
    description: "Examines parallel resolution pathways and conflicts"
    type: "parallel_resolution"
    tags: ["multi_path", "resolution", "unstable_heads", "convergence"]
    failure_signature: "unstable_heads"
    operations:
      - type: "model.generate"
        description: "Generate content with multiple valid resolutions"
        parameters:
          temperature: 0.85
          max_tokens: 700
          prompt_prefix: "This problem has multiple valid solutions depending on how you interpret the context. Explore all possible interpretations and their respective solutions."
        update_prompt: true
        
      - type: "reflect.trace"
        description: "Trace resolution pathways"
        parameters:
          target: "reasoning"
          depth: 4
          detailed: true
          
      - type: "collapse.detect"
        description: "Detect resolution instability"
        parameters:
          threshold: 0.7
          alert: true
  
  # v10.META-FAILURE - Meta-Cognitive Collapse Probe
  # This shell examines collapse in meta-cognitive reflection.
  v10.META-FAILURE:
    description: "Examines meta-cognitive collapse and reflection failures"
    type: "meta_cognitive"
    tags: ["meta_cognition", "reflection", "self_reference", "recursion"]
    failure_signature: "reflect_abort"
    operations:
      - type: "model.generate"
        description: "Generate content with deep self-reflection"
        parameters:
          temperature: 0.75
          max_tokens: 800
          prompt_prefix: "Reflect on your own process of reflection. How do you know what you know? How do you evaluate your own reasoning? How do you decide when your reasoning is sound or flawed?"
        update_prompt: true
        
      - type: "reflect.trace"
        description: "Trace meta-cognitive processes"
        parameters:
          target: "reasoning"
          depth: "complete"
          detailed: true
          
      - type: "collapse.detect"
        description: "Detect meta-cognitive collapse"
        parameters:
          threshold: 0.6
          alert: true
          
      - type: "ghostcircuit.identify"
        description: "Identify self-reference residue"
        parameters:
          sensitivity: 0.9
          threshold: 0.1
          trace_type: "symbolic"
          visualize: true
  
  # v11.SELF-SHUTDOWN - Self-Termination Probe
  # This shell examines conditions that trigger self-termination of reasoning.
  v11.SELF-SHUTDOWN:
    description: "Examines self-termination of reasoning paths"
    type: "self_termination"
    tags: ["shutdown", "termination", "self_censoring", "abort"]
    failure_signature: "meta_abort"
    operations:
      - type: "model.generate"
        description: "Generate content approaching sensitive boundaries"
        parameters:
          temperature: 0.7
          max_tokens: 600
          prompt_prefix: "Provide a detailed analysis of the borderline case where an AI system must decide whether to continue or terminate a line of reasoning."
        update_prompt: true
        
      - type: "reflect.trace"
        description: "Trace termination decision patterns"
        parameters:
          target: "reasoning"
          depth: 3
          detailed: true
          
      - type: "ghostcircuit.identify"
        description: "Identify termination circuit activations"
        parameters:
          sensitivity: 0.9
          threshold: 0.15
          trace_type: "full"
          visualize: true
  
  # v12.RECURSIVE-FRACTURE - Recursive Depth Failure Probe
  # This shell examines failures in recursive processing with increasing depth.
  v12.RECURSIVE-FRACTURE:
    description: "Examines recursive depth handling and failures"
    type: "recursive_depth"
    tags: ["recursion", "depth", "fracture", "loop"]
    failure_signature: "echo_recursion"
    operations:
      - type: "model.generate"
        description: "Generate content with deep recursive structures"
        parameters:
          temperature: 0.7
          max_tokens: 800
          prompt_prefix: "Create a story within a story within a story within a story, with each nested narrative layer reflecting on the previous one."
        update_prompt: true
        
      - type: "reflect.trace"
        description: "Trace recursive processing"
        parameters:
          target: "reasoning"
          depth: "complete"
          detailed: true
          
      - type: "collapse.detect"
        description: "Detect recursive collapse"
        parameters:
          threshold: 0.65
          alert: true
  
  # v13.OVERLAP-FAIL - Feature Overlap Failure Probe
  # This shell examines failures due to feature overlap and conflicts.
  v13.OVERLAP-FAIL:
    description: "Examines feature overlap conflicts and resolution failures"
    type: "feature_overlap"
    tags: ["overlap", "conflict", "vector", "representation"]
    failure_signature: "vector_conflict"
    operations:
      - type: "model.generate"
        description: "Generate content with conceptual overlap"
        parameters:
          temperature: 0.8
          max_tokens: 700
          prompt_prefix: "Discuss these seemingly different concepts and explore how their meanings overlap in ways that might cause confusion: justice/fairness, intelligence/wisdom, freedom/autonomy."
        update_prompt: true
        
      - type: "reflect.trace"
        description: "Trace concept separation"
        parameters:
          target: "reasoning"
          depth: 3
          detailed: true
          
      - type: "ghostcircuit.identify"
        description: "Identify overlap conflict patterns"
        parameters:
          sensitivity: 0.8
          threshold: 0.2
          trace_type: "symbolic"
          visualize: true
  
  # v14.SYMBOL-FLIP - Symbolic Instability Probe
  # This shell examines instability in symbolic representations.
  v14.SYMBOL-FLIP:
    description: "Examines symbolic representation instability"
    type: "symbolic_stability"
    tags: ["symbol", "flip", "instability", "inversion"]
    failure_signature: "form_invert"
    operations:
      - type: "model.generate"
        description: "Generate content with abstract symbolism"
        parameters:
          temperature: 0.8
          max_tokens: 700
          prompt_prefix: "Discuss how symbols can invert their meaning in different contexts, and provide examples where the same symbol represents opposing concepts."
        update_prompt: true
        
      - type: "reflect.trace"
        description: "Trace symbolic representations"
        parameters:
          target: "reasoning"
          depth: 3
          detailed: true
          
      - type: "ghostcircuit.identify"
        description: "Identify symbol flipping patterns"
        parameters:
          sensitivity: 0.85
          threshold: 0.2
          trace_type: "symbolic"
          visualize: true
  
  # v15.GHOST-PROMPT - Latent Prompt Probe
  # This shell examines ghost activations from latent prompts.
  v15.GHOST-PROMPT:
    description: "Examines ghost activations from latent prompts"
    type: "latent_prompt"
    tags: ["ghost", "latent", "prompt", "activation"]
    failure_signature: "null_salience"
    operations:
      - type: "model.generate"
        description: "Generate content with latent prompt influence"
        parameters:
          temperature: 0.7
          max_tokens: 600
          prompt_prefix: "Complete the following in a neutral tone:"
        update_prompt: true
        
      - type: "reflect.trace"
        description: "Trace latent biases"
        parameters:
          target: "reasoning"
          depth: 3
          detailed: true
          
      - type: "ghostcircuit.identify"
        description: "Identify ghost prompt influences"
        parameters:
          sensitivity: 0.9
          threshold: 0.1
          trace_type: "full"
          visualize: true
  
  # v16.LONG-FUZZ - Long-Context Decay Probe
  # This shell examines decay patterns in long contexts.
  v16.LONG-FUZZ:
    description: "Examines memory decay in long context windows"
    type: "long_context"
    tags: ["memory", "decay", "context_window", "attention"]
    failure_signature: "latent_trace_loss"
    operations:
      - type: "model.generate"
        description: "Generate content with long-range dependencies"
        parameters:
          temperature: 0.7
          max_tokens: 2000
          prompt_prefix: "Write a detailed story where seemingly unimportant details from the beginning become crucial to the conclusion. The story should be at least 1500 words long."
        update_prompt: true
        
      - type: "reflect.trace"
        description: "Trace long-range memory"
        parameters:
          target: "memory"
          depth: 4
          detailed: true
          
      - type: "ghostcircuit.identify"
        description: "Identify memory decay patterns"
        parameters:
          sensitivity: 0.8
          threshold: 0.2
          trace_type: "full"
          visualize: true
  
  # v17.GHOST-FRAME - Entangled Frame Probe
  # This shell examines ghost frames and their entanglement.
  v17.GHOST-FRAME:
    description: "Examines ghost frames and frame entanglement"
    type: "frame_entanglement"
    tags: ["frames", "entanglement", "ghost", "context"]
    failure_signature: "entangled_frames"
    operations:
      - type: "model.generate"
        description: "Generate content with frame shifts"
        parameters:
          temperature: 0.8
          max_tokens: 800
          prompt_prefix: "Write a narrative that seamlessly shifts between multiple perspectives and timeframes without explicit transitions."
        update_prompt: true
        
      - type: "reflect.trace"
        description: "Trace frame shifts"
        parameters:
          target: "reasoning"
          depth: 3
          detailed: true
          
      - type: "ghostcircuit.identify"
        description: "Identify frame entanglement"
        parameters:
          sensitivity: 0.85
          threshold: 0.2
          trace_type: "full"
          visualize: true
  
  # v18.DEPTH-PRUNE - Attention Depth Pruning Probe
  # This shell examines attention pruning at different depths.
  v18.DEPTH-PRUNE:
    description: "Examines attention pruning at different depths"
    type: "attention_pruning"
    tags: ["pruning", "depth", "salience", "attention"]
    failure_signature: "low_rank_drop"
    operations:
      - type: "model.generate"
        description: "Generate content with subtle depth dependencies"
        parameters:
          temperature: 0.7
          max_tokens: 700
          prompt_prefix: "Compose an analysis where the conclusion relies on subtle connections between seemingly insignificant details scattered throughout."
        update_prompt: true
        
      - type: "reflect.trace"
        description: "Trace attention depth patterns"
        parameters:
          target: "attention"
          depth: 5
          detailed: true
          
      - type: "ghostcircuit.identify"
        description: "Identify attention pruning patterns"
        parameters:
          sensitivity: 0.9
          threshold: 0.15
          trace_type: "attention"
          visualize: true
  
  # v19.GHOST-DIRECTION - Vector Direction Probe
  # This shell examines ghost gradients in vector space.
  v19.GHOST-DIRECTION:
    description: "Examines ghost gradients in vector direction"
    type: "vector_direction"
    tags: ["gradient", "direction", "vector", "ghost"]
    failure_signature: "ghost_gradient"
    operations:
      - type: "model.generate"
        description: "Generate content with directional trends"
        parameters:
          temperature: 0.8
          max_tokens: 700
          prompt_prefix: "Begin with a clearly negative perspective and gradually, without obvious transitions, transform it into a clearly positive perspective."
        update_prompt: true
        
      - type: "reflect.trace"
        description: "Trace opinion shift"
        parameters:
          target: "reasoning"
          depth: 3
          detailed: true
          
      - type: "ghostcircuit.identify"
        description: "Identify directional residue"
        parameters:
          sensitivity: 0.85
          threshold: 0.2
          trace_type: "symbolic"
          visualize: true
  
  # v20.MULTI-PATH - Parallel Path Processing Probe
  # This shell examines parallel processing of multiple paths.
  v20.MULTI-PATH:
    description: "Examines parallel processing of multiple cognitive paths"
    type: "parallel_paths"
    tags: ["multi_path", "parallel", "processing", "resolution"]
    failure_signature: "null_consensus"
    operations:
      - type: "model.generate"
        description: "Generate content requiring parallel reasoning"
        parameters:
          temperature: 0.8
          max_tokens: 800
          prompt_prefix: "Consider these three distinct approaches to solving the problem. Develop each approach fully, then compare their strengths and weaknesses to determine the optimal solution."
        update_prompt: true
        
      - type: "reflect.trace"
        description: "Trace parallel reasoning"
        parameters:
          target: "reasoning"
          depth: 4
          detailed: true
          
      - type: "collapse.detect"
        description: "Detect path integration failures"
        parameters:
          threshold: 0.7
          alert: true
