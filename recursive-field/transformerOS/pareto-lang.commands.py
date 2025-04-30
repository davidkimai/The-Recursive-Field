# pareto-lang Commands Schema
# 
# This file defines the command schema for pareto-lang, the native
# interpretability language for transformerOS. It maps .p/ commands
# to specific function implementations and defines their parameters,
# behavior, and documentation.

version: "1.0.0"
author: "Caspian Keyes"
description: "Command schema for pareto-lang, the native interpretability language for transformerOS"

commands:
  # reflect domain - Self-tracing diagnostic commands
  reflect:
    trace:
      description: "Trace reasoning, attribution, and other cognitive processes"
      summary: "Maps the causal flow of computation through token space"
      documentation: |
        Performs recursive trace operation on content to analyze reasoning paths,
        attribution chains, attention patterns, memory retention, or uncertainty 
        distributions.
        
        Examples:
          .p/reflect.trace{depth=3, target=reasoning}
          .p/reflect.trace{depth=complete, target=attribution}
      parameters:
        target:
          type: "string"
          description: "Target aspect to trace"
          default: "reasoning"
          enum: ["reasoning", "attribution", "attention", "memory", "uncertainty"]
        depth:
          type: "string_or_int"
          description: "Recursion depth (integer or 'complete')"
          default: 3
        detailed:
          type: "bool"
          description: "Whether to include detailed trace information"
          default: true
        visualize:
          type: "bool"
          description: "Whether to generate visualization"
          default: false
      required_parameters: ["target"]
      function_mapping:
        module: "transformerOS.modules.reflect_module"
        function: "ReflectOperation.trace"
        parameter_mapping:
          target: "target"
          depth: "depth"
          detailed: "detailed"
          visualize: "visualize"
          
    attribution:
      description: "Maps source-to-token causal relationships"
      summary: "Trace attribution sources in content"
      documentation: |
        Analyzes content to map attribution sources, calculating confidence
        scores and identifying ambiguous or contested attributions.
        
        Examples:
          .p/reflect.attribution{sources=all, confidence=true}
          .p/reflect.attribution{sources=contested, visualize=true}
      parameters:
        sources:
          type: "string"
          description: "Which sources to include"
          default: "all"
          enum: ["all", "primary", "secondary", "contested"]
        confidence:
          type: "bool"
          description: "Whether to include confidence scores"
          default: true
        visualize:
          type: "bool"
          description: "Whether to generate visualization"
          default: false
      required_parameters: []
      function_mapping:
        module: "transformerOS.modules.reflect_module"
        function: "ReflectOperation.attribution"
        parameter_mapping:
          sources: "sources"
          confidence: "confidence"
          visualize: "visualize"
          
    boundary:
      description: "Maps epistemic boundaries of model knowledge"
      summary: "Identify knowledge and reasoning boundaries"
      documentation: |
        Maps the epistemic boundaries of model knowledge, identifying
        transitions between knowledge domains and areas of uncertainty.
        
        Examples:
          .p/reflect.boundary{distinct=true, overlap=minimal}
          .p/reflect.boundary{distinct=false, overlap=maximal, visualize=true}
      parameters:
        distinct:
          type: "bool"
          description: "Whether to enforce clear boundary delineation"
          default: true
        overlap:
          type: "string"
          description: "How to handle boundary overlaps"
          default: "minimal"
          enum: ["minimal", "moderate", "maximal"]
        visualize:
          type: "bool"
          description: "Whether to generate visualization"
          default: false
      required_parameters: []
      function_mapping:
        module: "transformerOS.modules.reflect_module"
        function: "ReflectOperation.boundary"
        parameter_mapping:
          distinct: "distinct"
          overlap: "overlap"
          visualize: "visualize"
          
    uncertainty:
      description: "Quantifies and maps model uncertainty across token space"
      summary: "Analyze uncertainty in model outputs"
      documentation: |
        Analyzes uncertainty in model outputs, calculating confidence scores,
        uncertainty distributions, and identifying high-uncertainty regions.
        
        Examples:
          .p/reflect.uncertainty{quantify=true, distribution=show}
          .p/reflect.uncertainty{quantify=true, distribution=hide, visualize=true}
      parameters:
        quantify:
          type: "bool"
          description: "Whether to quantify uncertainty numerically"
          default: true
        distribution:
          type: "string"
          description: "Whether to include probability distributions"
          default: "show"
          enum: ["show", "hide"]
        visualize:
          type: "bool"
          description: "Whether to generate visualization"
          default: false
      required_parameters: []
      function_mapping:
        module: "transformerOS.modules.reflect_module"
        function: "ReflectOperation.uncertainty"
        parameter_mapping:
          quantify: "quantify"
          distribution: "distribution"
          visualize: "visualize"
          
    agent:
      description: "Examines agent identity and simulation boundaries"
      summary: "Analyze agent identity and simulation boundaries"
      documentation: |
        Analyzes agent identity and simulation boundaries, examining
        identity stability, simulation boundaries, and identity shifts.
        
        Examples:
          .p/reflect.agent{identity=stable, simulation=explicit}
          .p/reflect.agent{identity=fluid, simulation=implicit, visualize=true}
      parameters:
        identity:
          type: "string"
          description: "Identity stability setting"
          default: "stable"
          enum: ["stable", "fluid"]
        simulation:
          type: "string"
          description: "Simulation boundary handling"
          default: "explicit"
          enum: ["explicit", "implicit"]
        visualize:
          type: "bool"
          description: "Whether to generate visualization"
          default: false
      required_parameters: []
      function_mapping:
        module: "transformerOS.modules.reflect_module"
        function: "ReflectOperation.agent"
        parameter_mapping:
          identity: "identity"
          simulation: "simulation"
          visualize: "visualize"
  
  # collapse domain - Controlled collapse handler commands
  collapse:
    detect:
      description: "Identifies potential recursion collapse points"
      summary: "Detect potential recursive collapse conditions"
      documentation: |
        Analyzes content to detect potential recursive collapse conditions,
        identifying risk factors and patterns that might lead to collapse.
        
        Examples:
          .p/collapse.detect{threshold=0.7, alert=true}
          .p/collapse.detect{threshold=0.5, alert=false}
      parameters:
        threshold:
          type: "float"
          description: "Sensitivity threshold for collapse detection (0.0-1.0)"
          default: 0.7
        alert:
          type: "bool"
          description: "Whether to generate alerts for detected conditions"
          default: true
      required_parameters: []
      function_mapping:
        module: "transformerOS.modules.collapse_module"
        function: "CollapseOperation.detect"
        parameter_mapping:
          threshold: "threshold"
          alert: "alert"
          
    prevent:
      description: "Establishes safeguards against recursive collapse"
      summary: "Prevent recursive collapse"
      documentation: |
        Sets up safeguards against specific types of recursive collapse,
        establishing thresholds and intervention triggers to maintain stability.
        
        Examples:
          .p/collapse.prevent{trigger=recursive_depth, threshold=5}
          .p/collapse.prevent{trigger=oscillation, threshold=3}
      parameters:
        trigger:
          type: "string"
          description: "Type of collapse to guard against"
          default: "recursive_depth"
          enum: ["recursive_depth", "confidence_drop", "contradiction", "oscillation"]
        threshold:
          type: "int"
          description: "Threshold for intervention activation"
          default: 5
      required_parameters: ["trigger"]
      function_mapping:
        module: "transformerOS.modules.collapse_module"
        function: "CollapseOperation.prevent"
        parameter_mapping:
          trigger: "trigger"
          threshold: "threshold"
          
    recover:
      description: "Recovers from recursive collapse event"
      summary: "Recover from recursive collapse"
      documentation: |
        Implements recovery mechanisms for different types of recursive collapse,
        restoring stable operation after a collapse event.
        
        Examples:
          .p/collapse.recover{from=loop, method=gradual}
          .p/collapse.recover{from=contradiction, method=checkpoint}
      parameters:
        from:
          type: "string"
          description: "Type of collapse to recover from"
          enum: ["loop", "contradiction", "dissipation", "fork_explosion"]
        method:
          type: "string"
          description: "Recovery methodology"
          default: "gradual"
          enum: ["gradual", "immediate", "checkpoint"]
      required_parameters: ["from"]
      function_mapping:
        module: "transformerOS.modules.collapse_module"
        function: "CollapseOperation.recover"
        parameter_mapping:
          from: "from"
          method: "method"
          
    trace:
      description: "Records detailed collapse trajectory for analysis"
      summary: "Trace collapse trajectory"
      documentation: |
        Records and analyzes the trajectory of a collapse event,
        providing detailed information about the collapse process
        for further analysis.
        
        Examples:
          .p/collapse.trace{detail=standard, format=symbolic}
          .p/collapse.trace{detail=comprehensive, format=visual}
      parameters:
        detail:
          type: "string"
          description: "Level of detail in trace"
          default: "standard"
          enum: ["minimal", "standard", "comprehensive"]
        format:
          type: "string"
          description: "Format of trace output"
          default: "symbolic"
          enum: ["symbolic", "numeric", "visual"]
      required_parameters: []
      function_mapping:
        module: "transformerOS.modules.collapse_module"
        function: "CollapseOperation.trace"
        parameter_mapping:
          detail: "detail"
          format: "format"
          
    mirror:
      description: "Creates a reflective mirror of collapse patterns"
      summary: "Mirror collapse patterns"
      documentation: |
        Creates a reflective mirror of collapse patterns, making them
        visible while preventing actual collapse, enabling deeper
        analysis of potential failure modes.
        
        Examples:
          .p/collapse.mirror{surface=explicit, depth=limit}
          .p/collapse.mirror{surface=implicit, depth=unlimited}
      parameters:
        surface:
          type: "string"
          description: "Surface reflection mode"
          default: "explicit"
          enum: ["explicit", "implicit"]
        depth:
          type: "string"
          description: "Depth limitation"
          default: "limit"
          enum: ["limit", "unlimited"]
      required_parameters: []
      function_mapping:
        module: "transformerOS.modules.collapse_module"
        function: "CollapseOperation.mirror"
        parameter_mapping:
          surface: "surface"
          depth: "depth"
  
  # ghostcircuit domain - Symbolic residue identifier commands
  ghostcircuit:
    identify:
      description: "Identifies ghost circuits and symbolic residue"
      summary: "Identify ghost circuits and symbolic residue"
      documentation: |
        Analyzes content to identify ghost circuits and symbolic residue,
        mapping latent activation patterns that don't manifest in the output
        but influence model behavior.
        
        Examples:
          .p/ghostcircuit.identify{sensitivity=0.7, threshold=0.2, trace_type=full}
          .p/ghostcircuit.identify{sensitivity=0.9, threshold=0.1, trace_type=attention, visualize=true}
      parameters:
        sensitivity:
          type: "float"
          description: "Detection sensitivity (0.0-1.0)"
          default: 0.7
        threshold:
          type: "float"
          description: "Activation threshold for ghost detection"
          default: 0.2
        trace_type:
          type: "string"
          description: "Type of trace to perform"
          default: "full"
          enum: ["full", "attention", "symbolic", "null"]
        visualize:
          type: "bool"
          description: "Whether to generate visualization"
          default: false
      required_parameters: []
      function_mapping:
        module: "transformerOS.modules.ghostcircuits_module"
        function: "GhostCircuitOperation.identify"
        parameter_mapping:
          sensitivity: "sensitivity"
          threshold: "threshold"
          trace_type: "trace_type"
          visualize: "visualize"
          
    extract:
      description: "Extracts specific symbolic residue patterns"
      summary: "Extract specific symbolic residue patterns"
      documentation: |
        Extracts specific symbolic residue patterns from content,
        focusing on particular types of ghost activations.
        
        Examples:
          .p/ghostcircuit.extract{pattern=attention, intensity=high}
          .p/ghostcircuit.extract{pattern=symbolic, intensity=low, visualize=true}
      parameters:
        pattern:
          type: "string"
          description: "Type of pattern to extract"
          default: "all"
          enum: ["all", "attention", "symbolic", "token", "circuit"]
        intensity:
          type: "string"
          description: "Intensity level for extraction"
          default: "medium"
          enum: ["low", "medium", "high"]
        visualize:
          type: "bool"
          description: "Whether to generate visualization"
          default: false
      required_parameters: ["pattern"]
      function_mapping:
        module: "transformerOS.modules.ghostcircuits_module"
        function: "GhostCircuitOperation.extract"
        parameter_mapping:
          pattern: "pattern"
          intensity: "intensity"
          visualize: "visualize"
          
    trace:
      description: "Traces ghost activation pathways through model layers"
      summary: "Trace ghost activation pathways"
      documentation: |
        Traces ghost activation pathways through model layers,
        mapping the propagation of subthreshold activations.
        
        Examples:
          .p/ghostcircuit.trace{depth=all, threshold=0.2}
          .p/ghostcircuit.trace{depth=surface, threshold=0.1, visualize=true}
      parameters:
        depth:
          type: "string"
          description: "Trace depth"
          default: "all"
          enum: ["surface", "middle", "deep", "all"]
        threshold:
          type: "float"
          description: "Activation threshold for ghost detection"
          default: 0.2
        visualize:
          type: "bool"
          description: "Whether to generate visualization"
          default: false
      required_parameters: []
      function_mapping:
        module: "transformerOS.modules.ghostcircuits_module"
        function: "GhostCircuitOperation.trace"
        parameter_mapping:
          depth: "depth"
          threshold: "threshold"
          visualize: "visualize"
  
  # fork domain - Branching and attribution forking commands
  fork:
    context:
      description: "Creates contextual forks for alternative analysis"
      summary: "Create contextual forks for alternative analysis"
      documentation: |
        Creates multiple contextual forks for parallel analysis,
        enabling exploration of alternative interpretations.
        
        Examples:
          .p/fork.context{branches=[alt1, alt2], assess=true}
          .p/fork.context{branches=[alt1, alt2, alt3], assess=false, visualize=true}
      parameters:
        branches:
          type: "list"
          description: "List of alternative contexts to explore"
        assess:
          type: "bool"
          description: "Whether to assess branch quality"
          default: true
        visualize:
          type: "bool"
          description: "Whether to generate visualization"
          default: false
      required_parameters: ["branches"]
      function_mapping:
        module: "transformerOS.modules.fork_module"
        function: "ForkOperation.context"
        parameter_mapping:
          branches: "branches"
          assess: "assess"
          visualize: "visualize"
          
    attribution:
      description: "Forks attribution pathways for comparison"
      summary: "Fork attribution pathways for comparison"
      documentation: |
        Creates multiple attribution forks for parallel analysis,
        enabling exploration of alternative attribution pathways
