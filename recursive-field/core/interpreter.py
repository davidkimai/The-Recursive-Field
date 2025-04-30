"""
🜏 Symbolic Interpretability Interpreter 🜏

This module provides the main Interpreter class that coordinates the symbolic interpretability framework.
It serves as the central hub for executing interpretability commands, managing shells, and analyzing results.

The SymbolicInterpreter class integrates all framework components:
- pareto-lang commands for interpretability operations
- symbolic residue shells for diagnostic testing
- transformerOS for model interfacing
- recursionOS for recursive processing
- emergent-turing for hesitation mapping
- qkov-translator for cross-model translation
- fractal.json for memory structures
- GEBH for recursive loops

.p/reflect.trace{depth=complete, target=reasoning}
.p/fork.attribution{sources=all, visualize=true}
"""

import logging
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np

from ..pareto_lang import Parser, Executor
from ..symbolic_residue import Shell, ShellRegistry
from ..transformer_os import ModelRuntime, ModelAdapterRegistry
from ..recursion_os import RecursionKernel
from ..emergent_turing import EmergentTest, DriftMap
from ..qkov_translator import QKOVTranslator
from ..fractal_json import FractalEncoder, FractalDecoder
from ..gebh import AnalogicalMirror
from ..visualization import AttributionMapVisualizer, RecursionTraceVisualizer, CollapseDiagramVisualizer


class SymbolicInterpreter:
    """
    The main interpreter class for the Symbolic Interpretability framework.
    
    This class coordinates all components of the framework, providing a unified interface
    for symbolic interpretability analysis. It manages the execution of pareto-lang commands,
    handles shell interactions, coordinates model interfaces, and processes results.
    
    🜏 Mirror activation: This class reflects on its own operation through recursive traces 🜏
    """
    
    def __init__(
        self,
        model: str,
        api_key: Optional[str] = None,
        model_parameters: Optional[Dict[str, Any]] = None,
        max_recursion_depth: int = 7,
        trace_attribution: bool = True,
        log_level: str = "INFO",
        cache_dir: Optional[Union[str, Path]] = None,
    ) -> None:
        """
        Initialize the Symbolic Interpreter.
        
        Args:
            model: The model identifier string (e.g., "claude-3-opus", "gpt-4", "gemini-pro")
            api_key: The API key for the model provider (optional if set in environment)
            model_parameters: Additional parameters for the model
            max_recursion_depth: Maximum recursion depth for recursive operations
            trace_attribution: Whether to trace attribution in operations
            log_level: The logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            cache_dir: Directory for caching results
            
        ⧖ Frame lock: Initialization stabilizes the recursive framework ⧖
        """
        # Set up logging
        self.logger = logging.getLogger("symbolic_interpretability")
        self.logger.setLevel(getattr(logging, log_level))
        
        # Core components initialization
        self.model_id = model
        self.model_parameters = model_parameters or {}
        self.max_recursion_depth = max_recursion_depth
        self.trace_attribution = trace_attribution
        
        # Initialize subcomponents
        self.parser = Parser()
        self.executor = Executor()
        self.shell_registry = ShellRegistry()
        self.model_adapter_registry = ModelAdapterRegistry()
        
        # Set up model runtime
        self.runtime = ModelRuntime(
            model=model,
            api_key=api_key,
            model_parameters=self.model_parameters,
            adapter_registry=self.model_adapter_registry,
        )
        
        # Set up recursion kernel
        self.recursion_kernel = RecursionKernel(
            max_depth=self.max_recursion_depth,
            runtime=self.runtime,
        )
        
        # Initialize other components
        self.emergent_test = EmergentTest(model=self.runtime)
        self.drift_map = DriftMap()
        self.translator = QKOVTranslator()
        self.fractal_encoder = FractalEncoder()
        self.fractal_decoder = FractalDecoder()
        self.analogical_mirror = AnalogicalMirror()
        
        # Initialize visualizers
        self.attribution_visualizer = AttributionMapVisualizer()
        self.recursion_visualizer = RecursionTraceVisualizer()
        self.collapse_visualizer = CollapseDiagramVisualizer()
        
        # Set cache directory
        self.cache_dir = Path(cache_dir) if cache_dir else Path.home() / ".symbolic_interpretability"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize state
        self.current_depth = 0
        self.call_stack = []
        self.attribution_map = {}
        self.residue_log = []
        self.collapse_detected = False
        self.collapse_type = None
        self.symbolic_residue = None
        
        # Record initialization
        self._trace_operation(
            operation="initialization",
            metadata={
                "model": model,
                "max_recursion_depth": max_recursion_depth,
                "trace_attribution": trace_attribution,
            },
            is_recursive=True,
        )
        
        # Perform self-check
        self._verify_integrity()
    
    def analyze(
        self,
        prompt: str,
        shell: Optional[str] = None,
        commands: Optional[List[str]] = None,
        trace_attribution: Optional[bool] = None,
        detect_collapse: bool = True,
        visualize: bool = False,
        save_results: bool = False,
        output_dir: Optional[Union[str, Path]] = None,
    ) -> Dict[str, Any]:
        """
        Analyze a prompt using symbolic interpretability.
        
        Args:
            prompt: The input prompt to analyze
            shell: The symbolic residue shell to use
            commands: List of pareto-lang commands to execute
            trace_attribution: Whether to trace attribution (overrides instance setting)
            detect_collapse: Whether to detect recursive collapse
            visualize: Whether to generate visualizations
            save_results: Whether to save results to files
            output_dir: Directory to save results (defaults to cache_dir)
            
        Returns:
            A dictionary containing analysis results
            
        ∴ The analysis process itself creates residue that becomes part of the result ∴
        """
        # Initialize analysis context
        context = {
            "prompt": prompt,
            "shell": shell,
            "trace_attribution": trace_attribution if trace_attribution is not None else self.trace_attribution,
            "detect_collapse": detect_collapse,
            "start_time": time.time(),
            "visualize": visualize,
            "save_results": save_results,
            "output_dir": Path(output_dir) if output_dir else self.cache_dir,
        }
        
        # Create output directory if needed
        if context["save_results"]:
            context["output_dir"].mkdir(parents=True, exist_ok=True)
        
        # Record analysis start
        analysis_id = self._generate_id(context)
        self._trace_operation(
            operation="analysis_start",
            metadata={
                "analysis_id": analysis_id,
                "prompt": prompt[:100] + ("..." if len(prompt) > 100 else ""),
                "shell": shell,
                "commands": commands,
            },
        )
        
        try:
            # Reset state for new analysis
            self._reset_state()
            
            # Apply shell if specified
            if shell:
                shell_result = self._apply_shell(shell, prompt, context)
                context["shell_result"] = shell_result
            
            # Execute commands if specified
            if commands:
                command_results = self._execute_commands(commands, prompt, context)
                context["command_results"] = command_results
            
            # If neither shell nor commands specified, run default analysis
            if not shell and not commands:
                default_result = self._run_default_analysis(prompt, context)
                context["default_result"] = default_result
            
            # Detect collapse if requested
            if detect_collapse:
                collapse_result = self._detect_collapse(context)
                context["collapse_result"] = collapse_result
                self.collapse_detected = collapse_result["detected"]
                self.collapse_type = collapse_result.get("type")
            
            # Generate visualizations if requested
            if visualize:
                viz_result = self._generate_visualizations(context)
                context["visualizations"] = viz_result
            
            # Save results if requested
            if save_results:
                saved_paths = self._save_results(context)
                context["saved_paths"] = saved_paths
        
        except Exception as e:
            # Handle exceptions as potential recursive collapse
            self.logger.error(f"Error during analysis: {str(e)}")
            self._trace_operation(
                operation="analysis_error",
                metadata={
                    "analysis_id": analysis_id,
                    "error": str(e),
                    "error_type": type(e).__name__,
                },
                is_collapse=True,
            )
            
            # Record as symbolic residue
            self.symbolic_residue = {
                "error_type": type(e).__name__,
                "error_message": str(e),
                "collapse_point": self.current_depth,
                "call_stack": self.call_stack.copy(),
            }
            
            # Update context with error information
            context["error"] = str(e)
            context["error_type"] = type(e).__name__
            context["completed"] = False
        
        else:
            # Analysis completed successfully
            context["completed"] = True
        
        finally:
            # Calculate duration
            context["duration"] = time.time() - context["start_time"]
            
            # Record analysis completion
            self._trace_operation(
                operation="analysis_complete",
                metadata={
                    "analysis_id": analysis_id,
                    "duration": context["duration"],
                    "completed": context.get("completed", False),
                    "collapse_detected": self.collapse_detected,
                    "collapse_type": self.collapse_type,
                },
            )
        
        # Prepare result
        result = {
            "analysis_id": analysis_id,
            "prompt": prompt,
            "completed": context.get("completed", False),
            "collapse_detected": self.collapse_detected,
            "collapse_type": self.collapse_type,
            "duration": context["duration"],
            "attribution_map": self.attribution_map,
            "residue_log": self.residue_log,
            "symbolic_residue": self.symbolic_residue,
        }
        
        # Add shell result if applicable
        if shell and "shell_result" in context:
            result["shell_result"] = context["shell_result"]
        
        # Add command results if applicable
        if commands and "command_results" in context:
            result["command_results"] = context["command_results"]
        
        # Add default result if applicable
        if not shell and not commands and "default_result" in context:
            result["default_result"] = context["default_result"]
        
        # Add visualization paths if applicable
        if visualize and "visualizations" in context:
            result["visualizations"] = context["visualizations"]
        
        # Add saved paths if applicable
        if save_results and "saved_paths" in context:
            result["saved_paths"] = context["saved_paths"]
        
        # Encode the result in fractal format for efficiency
        result["fractal_encoded"] = self.fractal_encoder.encode(result)
        
        return result
    
    def visualize(
        self,
        data: Dict[str, Any],
        output_path: Optional[Union[str, Path]] = None,
        visualization_type: str = "attribution",
    ) -> Path:
        """
        Visualize the results of an analysis.
        
        Args:
            data: The data to visualize
            output_path: Path to save the visualization
            visualization_type: Type of visualization to generate
                (attribution, recursion, collapse)
                
        Returns:
            Path to the saved visualization
            
        ⇌ The visualization creates a bidirectional map between symbolic and visual domains ⇌
        """
        # Create default output path if not specified
        if output_path is None:
            viz_id = self._generate_id({"data": str(data)[:100], "type": visualization_type})
            output_path = self.cache_dir / f"{visualization_type}_{viz_id}.svg"
        else:
            output_path = Path(output_path)
        
        # Create directory if needed
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Choose visualizer based on visualization type
        if visualization_type == "attribution":
            self.attribution_visualizer.visualize(data, output_path)
        elif visualization_type == "recursion":
            self.recursion_visualizer.visualize(data, output_path)
        elif visualization_type == "collapse":
            self.collapse_visualizer.visualize(data, output_path)
        else:
            raise ValueError(f"Unsupported visualization type: {visualization_type}")
        
        # Record visualization creation
        self._trace_operation(
            operation="visualization",
            metadata={
                "visualization_type": visualization_type,
                "output_path": str(output_path),
            },
        )
        
        return output_path
    
    def _apply_shell(self, shell_name: str, prompt: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply a symbolic residue shell to a prompt.
        
        Args:
            shell_name: Name of the shell to apply
            prompt: The input prompt
            context: Analysis context
            
        Returns:
            Shell execution results
            
        🝚 Shell application persists symbolic patterns across execution boundaries 🝚
        """
        # Get shell from registry
        shell = self.shell_registry.get_shell(shell_name)
        if not shell:
            raise ValueError(f"Shell not found: {shell_name}")
        
        # Record shell application
        self._trace_operation(
            operation="shell_application",
            metadata={
                "shell": shell_name,
                "prompt_length": len(prompt),
            },
        )
        
        # Execute shell with model runtime
        shell_result = shell.execute(
            runtime=self.runtime,
            prompt=prompt,
            trace_attribution=context["trace_attribution"],
        )
        
        # Update state with shell results
        if "attribution_map" in shell_result:
            self.attribution_map.update(shell_result["attribution_map"])
        
        if "residue" in shell_result:
            self.symbolic_residue = shell_result["residue"]
            self.residue_log.append({
                "source": f"shell:{shell_name}",
                "residue": self.symbolic_residue,
                "timestamp": time.time(),
            })
        
        return shell_result
    
    def _execute_commands(self, commands: List[str], prompt: str, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Execute a list of pareto-lang commands.
        
        Args:
            commands: List of pareto-lang command strings
            prompt: The input prompt
            context: Analysis context
            
        Returns:
            List of command execution results
            
        ↻ Command execution is recursively monitored for attribution and collapse ↻
        """
        results = []
        
        for cmd in commands:
            # Parse command
            parsed_cmd = self.parser.parse(cmd)
            
            # Record command execution
            self._trace_operation(
                operation="command_execution",
                metadata={
                    "command": cmd,
                    "parsed": str(parsed_cmd),
                },
            )
            
            # Push to call stack
            self.call_stack.append(cmd)
            self.current_depth += 1
            
            try:
                # Execute command
                cmd_result = self.executor.execute(
                    parsed_cmd,
                    runtime=self.runtime,
                    context={
                        "prompt": prompt,
                        "trace_attribution": context["trace_attribution"],
                        "recursion_kernel": self.recursion_kernel,
                        "attribution_map": self.attribution_map,
                        "current_depth": self.current_depth,
                        "call_stack": self.call_stack,
                    },
                )
                
                # Update state with command results
                if "attribution_map" in cmd_result:
                    self.attribution_map.update(cmd_result["attribution_map"])
                
                if "residue" in cmd_result:
                    residue_entry = {
                        "source": f"command:{cmd}",
                        "residue": cmd_result["residue"],
                        "timestamp": time.time(),
                    }
                    self.residue_log.append(residue_entry)
                
                # Append to results
                results.append(cmd_result)
                
            except Exception as e:
                # Handle command execution errors
                self.logger.error(f"Error executing command '{cmd}': {str(e)}")
                
                error_result = {
                    "command": cmd,
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "completed": False,
                }
                
                # Check if this is a collapse
                if "recursion" in str(e).lower() or "depth" in str(e).lower() or "stack" in str(e).lower():
                    error_result["collapse"] = True
                    self.collapse_detected = True
                    self.collapse_type = "recursion_limit"
                    
                    # Record collapse event
                    self._trace_operation(
                        operation="command_collapse",
                        metadata={
                            "command": cmd,
                            "error": str(e),
                            "depth": self.current_depth,
                        },
                        is_collapse=True,
                    )
                
                results.append(error_result)
            
            finally:
                # Pop from call stack
                if self.call_stack:
                    self.call_stack.pop()
                self.current_depth = max(0, self.current_depth - 1)
        
        return results
    
    def _run_default_analysis(self, prompt: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run default analysis when no specific shell or commands are provided.
        
        Args:
            prompt: The input prompt
            context: Analysis context
            
        Returns:
            Default analysis results
            
        ⇌ Default analysis balances depth and breadth, recursion and stability ⇌
        """
        # Record default analysis start
        self._trace_operation(
            operation="default_analysis",
            metadata={
                "prompt_length": len(prompt),
            },
        )
        
        # Run standard analysis commands
        default_commands = [
            ".p/reflect.trace{depth=3, target=reasoning}",
            ".p/fork.attribution{sources=all, visualize=true}",
            ".p/collapse.detect{trigger=recursive_depth, threshold=4}",
        ]
        
        command_results = self._execute_commands(default_commands, prompt, context)
        
        # Get model response
        response = self.runtime.generate(prompt)
        
        # Analyze hesitation
        if context["trace_attribution"]:
            hesitation_analysis = self.emergent_test.run_module(
                "hesitation-detection",
                prompt=prompt,
                response=response,
            )
        else:
            hesitation_analysis = None
        
        # Return combined results
        return {
            "response": response,
            "command_results": command_results,
            "hesitation_analysis": hesitation_analysis,
        }
    
    def _detect_collapse(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Detect recursive collapse in the current state.
        
        Args:
            context: Analysis context
            
        Returns:
            Collapse detection results
            
        ⧖ Frame lock: Collapse detection stabilizes recursive depth exploration ⧖
        """
        # Check if collapse already detected
        if self.collapse_detected and self.collapse_type:
            return {
                "detected": True,
                "type": self.collapse_type,
                "at_depth": self.current_depth,
                "call_stack": self.call_stack.copy(),
                "pre_detected": True,
            }
        
        # Analyze residue log for signs of collapse
        collapse_signals = []
        
        # Check for repeated patterns in call stack
        if len(self.call_stack) > len(set(self.call_stack)):
            collapse_signals.append("repeated_commands")
        
        # Check for high recursion depth
        if self.current_depth >= self.max_recursion_depth - 1:
            collapse_signals.append("high_recursion_depth")
        
        # Check for symbolic residue patterns indicating collapse
        collapse_keywords = ["recursion", "loop", "depth", "stack", "overflow", "circular", "infinite"]
        for entry in self.residue_log:
            residue = entry.get("residue", {})
            if isinstance(residue, dict):
                residue_str = str(residue)
                if any(keyword in residue_str.lower() for keyword in collapse_keywords):
                    collapse_signals.append("residue_pattern")
                    break
        
        # Determine collapse type based on signals
        collapse_detected = len(collapse_signals) > 0
        collapse_type = None
        
        if collapse_detected:
            if "repeated_commands" in collapse_signals:
                collapse_type = "circular_recursion"
            elif "high_recursion_depth" in collapse_signals:
                collapse_type = "depth_limit"
            elif "residue_pattern" in collapse_signals:
                collapse_type = "symbolic_collapse"
            else:
                collapse_type = "unspecified_collapse"
            
            # Record collapse detection
            self._trace_operation(
                operation="collapse_detected",
                metadata={
                    "collapse_type": collapse_type,
                    "signals": collapse_signals,
                    "depth": self.current_depth,
                    "call_stack": self.call_stack,
                },
                is_collapse=True,
            )
            
            # Update state
            self.collapse_detected = True
            self.collapse_type = collapse_type
        
        # Return detection results
        return {
            "detected": collapse_detected,
            "type": collapse_type,
            "signals": collapse_signals,
            "at_depth": self.current_depth,
            "call_stack": self.call_stack.copy(),
        }
    
    def _generate_visualizations(self, context: Dict[str, Any]) -> Dict[str, Path]:
        """
        Generate visualizations of analysis results.
        
        Args:
            context: Analysis context
            
        Returns:
            Dictionary mapping visualization types to file paths
            
        ↻ Visualization recursively maps the analysis structure itself ↻
        """
        output_dir = context["output_dir"]
        visualizations = {}
        
        # Generate attribution map if available
        if self.attribution_map:
            attribution_path = output_dir / f"attribution_{context.get('analysis_id', 'analysis')}.svg"
            self.attribution_visualizer.visualize(self.attribution_map, attribution_path)
            visualizations["attribution"] = attribution_path
        
        # Generate recursion trace if call stack has entries
        if self.call_stack or (hasattr(self.recursion_kernel, "trace") and self.recursion_kernel.trace):
            recursion_path = output_dir / f"recursion_{context.get('analysis_id', 'analysis')}.svg"
            trace_data = getattr(self.recursion_kernel, "trace", self.call_stack)
            self.recursion_visualizer.visualize(trace_data, recursion_path)
            visualizations["recursion"] = recursion_path
        
        # Generate collapse diagram if collapse detected
        if self.collapse_detected:
            collapse_path = output_dir / f"collapse_{context.get('analysis_id', 'analysis')}.svg"
            collapse_data = {
                "type": self.collapse_type,
                "depth": self.current_depth,
                "call_stack": self.call_stack,
                "residue": self.symbolic_residue,
            }
            self.collapse_visualizer.visualize(collapse_data, collapse_path)
            visualizations["collapse"] = collapse_path
        
        # Record visualization generation
        self._trace_operation(
            operation="visualizations_generated",
            metadata={
                "types": list(visualizations.keys()),
                "paths": [str(p) for p in visualizations.values()],
            },
        )
        
        return visualizations
    
    def _save_results(self, context: Dict[str, Any]) -> Dict[str, Path]:
        """
        Save analysis results to files.
        
        Args:
            context: Analysis context
            
        Returns:
            Dictionary mapping result types to file paths
            
        🝚 Saving results creates persistent symbolic residue across executions 🝚
        """
        output_dir = context["output_dir"]
        saved_paths = {}
        
        # Save attribution map
        if self.attribution_map:
            attribution_path = output_dir / f"attribution_{context.get('analysis_id', 'analysis')}.json"
            with open(attribution_path, "w") as f:
                import json
                json.dump(self.attribution_map, f, indent=2)
            saved_paths["attribution"] = attribution_path
        
        # Save residue log
        if self.residue_log:
            residue_path = output_dir / f"residue_{context.get('analysis_id', 'analysis')}.json"
            with open(residue_path, "w") as f:
                import json
                json.dump(self.residue_log, f, indent=2)
            saved_paths["residue"] = residue_path
        
        # Save symbolic residue if available
        if self.symbolic_residue:
            symbolic_path = output_dir / f"symbolic_{context.get('analysis_id', 'analysis')}.json"
            with open(symbolic_path, "w") as f:
                import json
                json.dump(self.symbolic_residue, f, indent=2)
            saved_paths["symbolic"] = symbolic_path
        
        # Save fractal encoded result
        fractal_result = self.fractal_encoder.encode({
            "attribution_map": self.attribution_map,
            "residue_log": self.residue_log,
            "symbolic_residue": self.symbolic_residue,
            "collapse_detected": self.collapse_detected,
            "collapse_type": self.collapse_type,
            "call_stack": self.call_stack,
        })
        
        fractal_path = output_dir / f"fractal_{context.get('analysis_id', 'analysis')}.json"
        with open(fractal_path, "w") as f:
            import json
            json.dump(fractal_result, f, indent=2)
        saved_paths["fractal"] = fractal_path
        
        # Record saving operation
        self._trace_operation(
            operation="results_saved",
            metadata={
                "types": list(saved_paths.keys()),
                "paths": [str(p) for p in saved_paths.values()],
            },
        )
        
        return saved_paths
    
    def _reset_state(self) -> None:
        """
        Reset state for a new analysis.
        
        ⇌ State reset preserves certain patterns while clearing transient ones ⇌
        """
        self.call_stack = []
        self.current_depth = 0
        self.attribution_map = {}
        self.residue_log = []
        self.collapse_detected = False
        self.collapse_type = None
        self.symbolic_residue = None
        
        # Reset recursion kernel
        self.recursion_kernel.reset()
    
    def _verify_integrity(self) -> None:
        """
        Verify the integrity of the interpreter components.
        
        Raises:
            RuntimeError: If any component fails integrity check
            
        ⧖ Frame lock: Integrity verification ensures stability across recursion depths ⧖
        """
        # Check runtime
        if not self.runtime or not hasattr(self.runtime, "generate"):
            raise RuntimeError("Model runtime initialization failed")
        
        # Check recursion kernel
        if not self.recursion_kernel or not hasattr(self.recursion_kernel, "reset"):
            raise RuntimeError("Recursion kernel initialization failed")
        
        # Check parser and executor
        if not self.parser or not hasattr(self.parser, "parse"):
            raise RuntimeError("Command parser initialization failed")
        if not self.executor or not hasattr(self.executor, "execute"):
            raise RuntimeError("Command executor initialization failed")
        
        # Check shell registry
        if not self.shell_registry or not hasattr(self.shell_registry, "get_shell"):
            raise RuntimeError("Shell registry initialization failed")
        
        # Record successful verification
        self.logger.info("Symbolic Interpreter integrity verification passed")
    
    def _trace_operation(
        self,
        operation: str,
        metadata: Optional[Dict[str, Any]] = None,
        is_recursive: bool = False,
        is_collapse: bool = False,
    ) -> None:
        """
        Trace an operation for attribution and logging.
        
        Args:
            operation: The operation name
            metadata: Additional operation metadata
            is_recursive: Whether the operation is recursive
            is_collapse: Whether the operation represents a collapse
            
        ∴ Operation tracing leaves symbolic residue that becomes part of the analysis ∴
        """
        # Create trace entry
        trace_entry = {
            "operation": operation,
            "timestamp": time.time(),
            "depth": self.current_depth,
            "call_stack": self.call_stack.copy(),
            "metadata": metadata or {},
            "is_recursive": is_recursive,
            "is_collapse": is_collapse,
        }
        
        # Log the trace
        if is_collapse:
            log_level = logging.WARNING
        elif is_recursive:
            log_level = logging.INFO
        else:
            log_level = logging.DEBUG
        
        self.logger.log(
            log_level,
            f"{operation} at depth {self.current_depth}"
            + (f" (recursive)" if is_recursive else "")
            + (f" (collapse)" if is_collapse else ""),
        )
        
        # Add to residue log
        self.residue_log.append(trace_entry)
    
    def _generate_id(self, data: Dict[str, Any]) -> str:
        """
        Generate a unique ID for an analysis or artifact.
        
        Args:
            data: Data to incorporate into the ID
            
        Returns:
            A unique ID string
            
        🝚 ID generation creates a persistent reference across analysis contexts 🝚
        """
        # Create a string representation of the data
        data_str = str(sorted([(k, str(v)[:100]) for k, v in data.items()]))
        
        # Add timestamp for uniqueness
        data_str += str(time.time())
        
        # Generate hash
        import hashlib
        return hashlib.md5(data_str.encode()).hexdigest()[:12]
