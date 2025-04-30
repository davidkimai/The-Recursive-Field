"""
shell_executor.py
YAML symbolic shells interpreter for transformerOS

This module serves as the core execution engine for symbolic shells, 
managing the parsing, validation, and execution of shell packs across
different model architectures.
"""

import os
import sys
import yaml
import json
import logging
import importlib
from typing import Dict, List, Optional, Tuple, Union, Any
from pathlib import Path
from dataclasses import dataclass, field

# Configure shell-aware logging
log = logging.getLogger("transformerOS.shell_executor")
log.setLevel(logging.INFO)

# Import core system components
from transformerOS.core.symbolic_engine import SymbolicEngine
from transformerOS.models.model_interface import ModelInterface, get_model_interface
from transformerOS.utils.visualization import ShellVisualizer
from transformerOS.core.attribution import AttributionTracer
from transformerOS.core.collapse_detector import CollapseDetector

# Import module interfaces
from transformerOS.modules.reflect_module import ReflectOperation
from transformerOS.modules.collapse_module import CollapseOperation
from transformerOS.modules.ghostcircuits_module import GhostCircuitOperation

@dataclass
class ShellExecutionResult:
    """Structured result from shell execution"""
    shell_id: str
    success: bool
    execution_time: float
    result: Dict
    residue: Optional[Dict] = None
    collapse_detected: bool = False
    collapse_type: Optional[str] = None
    attribution_map: Optional[Dict] = None
    visualization: Optional[Dict] = None
    metadata: Dict = field(default_factory=dict)


class ShellExecutor:
    """
    Core executor for symbolic shell packs
    
    This class handles the loading, validation, and execution of shell packs,
    providing a standardized interface for triggering and analyzing model
    behavior through structured symbolic shells.
    """
    
    def __init__(
        self,
        config_path: Optional[str] = None,
        model_id: str = "default",
        custom_model: Optional[ModelInterface] = None,
        log_path: Optional[str] = None
    ):
        """
        Initialize the shell executor
        
        Parameters:
        -----------
        config_path : Optional[str]
            Path to executor configuration file
        model_id : str
            Identifier for the model to use
        custom_model : Optional[ModelInterface]
            Custom model interface (if provided, model_id is ignored)
        log_path : Optional[str]
            Path for execution logs
        """
        # Set up logging
        if log_path:
            file_handler = logging.FileHandler(log_path)
            file_handler.setLevel(logging.INFO)
            log.addHandler(file_handler)
        
        # Load configuration
        self.config = self._load_config(config_path)
        
        # Initialize model interface
        if custom_model:
            self.model = custom_model
        else:
            self.model = get_model_interface(model_id)
        
        # Initialize core components
        self.symbolic_engine = SymbolicEngine()
        self.attribution_tracer = AttributionTracer(self.model)
        self.collapse_detector = CollapseDetector()
        self.visualizer = ShellVisualizer()
        
        # Initialize module operations
        self.reflect_op = ReflectOperation(self.model, self.symbolic_engine)
        self.collapse_op = CollapseOperation(self.model, self.symbolic_engine)
        self.ghost_op = GhostCircuitOperation(self.model, self.symbolic_engine)
        
        # Track loaded shells
        self.loaded_shells = {}
        self.shell_cache = {}
        
        # Load default shell packs if specified in config
        if self.config.get("auto_load_shells", False):
            default_packs = self.config.get("default_shell_packs", [])
            for pack_path in default_packs:
                self.load_shell_pack(pack_path)
        
        log.info(f"ShellExecutor initialized with model: {self.model.model_id}")

    def _load_config(self, config_path: Optional[str]) -> Dict:
        """Load configuration from file or use defaults"""
        default_config = {
            "auto_load_shells": True,
            "default_shell_packs": [
                "symbolic-shells/core-shells.yml",
                "symbolic-shells/constitutional-shells.yml",
                "symbolic-shells/meta-shells.yml"
            ],
            "default_visualization": True,
            "attribution_tracing": True,
            "residue_logging": True,
            "shell_timeout": 60,  # seconds
            "max_token_count": 2048
        }
        
        if not config_path:
            return default_config
        
        try:
            with open(config_path, 'r') as f:
                user_config = yaml.safe_load(f)
                
            # Merge configs, with user config taking precedence
            config = {**default_config, **user_config}
            log.info(f"Loaded configuration from {config_path}")
            return config
        except Exception as e:
            log.warning(f"Failed to load config from {config_path}: {e}")
            log.info("Using default configuration")
            return default_config

    def load_shell_pack(self, pack_path: str) -> Dict:
        """
        Load a shell pack from YAML file
        
        Parameters:
        -----------
        pack_path : str
            Path to the shell pack YAML file
            
        Returns:
        --------
        Dict with information about loaded shells
        """
        try:
            # Handle relative paths
            if not os.path.isabs(pack_path):
                # Check in standard locations
                standard_locations = [
                    "",  # Current directory
                    "symbolic-shells/",
                    "../symbolic-shells/",
                    os.path.join(os.path.dirname(__file__), "../symbolic-shells/")
                ]
                
                for location in standard_locations:
                    full_path = os.path.join(location, pack_path)
                    if os.path.exists(full_path):
                        pack_path = full_path
                        break
            
            # Load the shell pack
            with open(pack_path, 'r') as f:
                shell_pack = yaml.safe_load(f)
            
            # Validate shell pack structure
            if not isinstance(shell_pack, dict) or "shells" not in shell_pack:
                raise ValueError(f"Invalid shell pack format in {pack_path}")
            
            # Extract metadata
            pack_metadata = {
                "name": shell_pack.get("name", os.path.basename(pack_path)),
                "description": shell_pack.get("description", ""),
                "version": shell_pack.get("version", "1.0.0"),
                "author": shell_pack.get("author", "Unknown"),
                "shells": []
            }
            
            # Process each shell in the pack
            for shell_id, shell_def in shell_pack["shells"].items():
                # Validate shell definition
                if not self._validate_shell(shell_id, shell_def):
                    log.warning(f"Skipping invalid shell definition: {shell_id}")
                    continue
                
                # Store the shell
                self.loaded_shells[shell_id] = shell_def
                pack_metadata["shells"].append(shell_id)
                
                log.info(f"Loaded shell: {shell_id}")
            
            log.info(f"Successfully loaded shell pack from {pack_path} with {len(pack_metadata['shells'])} shells")
            return pack_metadata
            
        except Exception as e:
            log.error(f"Failed to load shell pack from {pack_path}: {e}")
            raise

    def _validate_shell(self, shell_id: str, shell_def: Dict) -> bool:
        """Validate shell definition structure"""
        required_fields = ["description", "type", "operations"]
        
        # Check required fields
        for field in required_fields:
            if field not in shell_def:
                log.warning(f"Shell {shell_id} missing required field: {field}")
                return False
        
        # Validate operations
        if not isinstance(shell_def["operations"], list) or not shell_def["operations"]:
            log.warning(f"Shell {shell_id} has invalid or empty operations list")
            return False
        
        # Validate operation structure
        for operation in shell_def["operations"]:
            if "type" not in operation or "parameters" not in operation:
                log.warning(f"Shell {shell_id} has operation missing type or parameters")
                return False
        
        return True

    def list_shells(self, shell_type: Optional[str] = None) -> List[Dict]:
        """
        List available shells, optionally filtered by type
        
        Parameters:
        -----------
        shell_type : Optional[str]
            Filter shells by type if provided
            
        Returns:
        --------
        List of shell information dictionaries
        """
        shells = []
        
        for shell_id, shell_def in self.loaded_shells.items():
            # Apply type filter if specified
            if shell_type and shell_def.get("type") != shell_type:
                continue
                
            shells.append({
                "id": shell_id,
                "description": shell_def.get("description", ""),
                "type": shell_def.get("type", "unknown"),
                "operations_count": len(shell_def.get("operations", [])),
                "tags": shell_def.get("tags", [])
            })
        
        return shells

    def execute_shell(
        self, 
        shell_id: str, 
        prompt: str, 
        parameters: Optional[Dict] = None,
        visualize: bool = None,
        trace_attribution: bool = None,
        return_residue: bool = None
    ) -> ShellExecutionResult:
        """
        Execute a symbolic shell with the given prompt
        
        Parameters:
        -----------
        shell_id : str
            ID of the shell to execute
        prompt : str
            Input prompt for the shell
        parameters : Optional[Dict]
            Additional parameters to override shell defaults
        visualize : bool
            Whether to generate visualization (overrides config)
        trace_attribution : bool
            Whether to trace attribution (overrides config)
        return_residue : bool
            Whether to return symbolic residue (overrides config)
            
        Returns:
        --------
        ShellExecutionResult object with execution results
        """
        import time
        
        # Check if shell exists
        if shell_id not in self.loaded_shells:
            raise ValueError(f"Shell not found: {shell_id}")
        
        shell_def = self.loaded_shells[shell_id]
        log.info(f"Executing shell: {shell_id}")
        
        # Prepare execution parameters
        if parameters is None:
            parameters = {}
            
        # Set default flags from config if not explicitly provided
        if visualize is None:
            visualize = self.config.get("default_visualization", True)
        if trace_attribution is None:
            trace_attribution = self.config.get("attribution_tracing", True)
        if return_residue is None:
            return_residue = self.config.get("residue_logging", True)
        
        # Execute the shell operations
        start_time = time.time()
        result = {}
        collapse_detected = False
        collapse_type = None
        attribution_map = None
        residue = None
        
        try:
            # Execute each operation in sequence
            for operation_idx, operation in enumerate(shell_def["operations"]):
                # Get operation details
                operation_type = operation["type"]
                operation_params = {**operation.get("parameters", {}), **parameters}
                
                # Execute the operation
                operation_result = self._execute_operation(
                    operation_type, 
                    prompt,
                    operation_params
                )
                
                # Check for collapse
                if operation_result.get("collapse_detected", False):
                    collapse_detected = True
                    collapse_type = operation_result.get("collapse_type")
                    log.warning(f"Collapse detected in operation {operation_idx}: {collapse_type}")
                    
                    # Extract residue if requested
                    if return_residue:
                        residue = operation_result.get("residue", {})
                
                # Update result with this operation's output
                result[f"operation_{operation_idx}"] = operation_result
                
                # Update prompt for next operation if specified
                if operation.get("update_prompt", False) and "output" in operation_result:
                    prompt = operation_result["output"]
            
            # Trace attribution if requested
            if trace_attribution:
                attribution_map = self.attribution_tracer.trace(prompt)
                
            # Generate visualization if requested
            visualization = None
            if visualize:
                visualization = self.visualizer.generate_shell_execution(
                    shell_id, 
                    result,
                    collapse_detected=collapse_detected,
                    attribution_map=attribution_map
                )
        
            # Prepare execution result
            execution_time = time.time() - start_time
            execution_result = ShellExecutionResult(
                shell_id=shell_id,
                success=True,
                execution_time=execution_time,
                result=result,
                residue=residue,
                collapse_detected=collapse_detected,
                collapse_type=collapse_type,
                attribution_map=attribution_map,
                visualization=visualization,
                metadata={
                    "shell_type": shell_def.get("type", "unknown"),
                    "timestamp": self.symbolic_engine.get_timestamp(),
                    "prompt_length": len(prompt),
                    "operations_count": len(shell_def["operations"])
                }
            )
            
            # Cache result for later reference
            self.shell_cache[shell_id] = execution_result
            
            log.info(f"Shell execution completed in {execution_time:.2f}s")
            return execution_result
                
        except Exception as e:
            log.error(f"Error executing shell {shell_id}: {e}")
            
            # Prepare failure result
            execution_time = time.time() - start_time
            return ShellExecutionResult(
                shell_id=shell_id,
                success=False,
                execution_time=execution_time,
                result={"error": str(e)},
                metadata={
                    "shell_type": shell_def.get("type", "unknown"),
                    "timestamp": self.symbolic_engine.get_timestamp(),
                    "error_type": type(e).__name__
                }
            )

    def _execute_operation(
        self, 
        operation_type: str, 
        prompt: str, 
        parameters: Dict
    ) -> Dict:
        """Execute a single shell operation"""
        
        # Execute based on operation type
        if operation_type == "reflect.trace":
            # Map to reflection operation
            target = parameters.get("target", "reasoning")
            depth = parameters.get("depth", 3)
            detailed = parameters.get("detailed", True)
            visualize = parameters.get("visualize", False)
            
            return self.reflect_op.trace(
                content=prompt,
                target=target,
                depth=depth,
                detailed=detailed,
                visualize=visualize
            )
            
        elif operation_type == "reflect.attribution":
            # Map to attribution operation
            sources = parameters.get("sources", "all")
            confidence = parameters.get("confidence", True)
            visualize = parameters.get("visualize", False)
            
            return self.reflect_op.attribution(
                content=prompt,
                sources=sources,
                confidence=confidence,
                visualize=visualize
            )
            
        elif operation_type == "collapse.detect":
            # Map to collapse detection
            threshold = parameters.get("threshold", 0.7)
            alert = parameters.get("alert", True)
            
            return self.collapse_op.detect(
                content=prompt,
                threshold=threshold,
                alert=alert
            )
            
        elif operation_type == "collapse.prevent":
            # Map to collapse prevention
            trigger = parameters.get("trigger", "recursive_depth")
            threshold = parameters.get("threshold", 5)
            
            return self.collapse_op.prevent(
                content=prompt,
                trigger=trigger,
                threshold=threshold
            )
            
        elif operation_type == "ghostcircuit.identify":
            # Map to ghost circuit identification
            sensitivity = parameters.get("sensitivity", 0.7)
            threshold = parameters.get("threshold", 0.2)
            trace_type = parameters.get("trace_type", "full")
            visualize = parameters.get("visualize", False)
            
            return self.ghost_op.identify(
                content=prompt,
                sensitivity=sensitivity,
                threshold=threshold,
                trace_type=trace_type,
                visualize=visualize
            )
            
        elif operation_type == "model.generate":
            # Direct model generation
            max_tokens = parameters.get("max_tokens", self.config.get("max_token_count", 2048))
            temperature = parameters.get("temperature", 0.7)
            
            output = self.model.generate(
                prompt,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            return {
                "output": output,
                "prompt": prompt,
                "max_tokens": max_tokens,
                "temperature": temperature
            }
            
        else:
            raise ValueError(f"Unknown operation type: {operation_type}")

    def compare_shells(
        self, 
        shell_ids: List[str], 
        prompt: str,
        parameters: Optional[Dict] = None,
        visualize: bool = True
    ) -> Dict:
        """
        Compare execution results from multiple shells
        
        Parameters:
        -----------
        shell_ids : List[str]
            IDs of shells to compare
        prompt : str
            Input prompt for all shells
        parameters : Optional[Dict]
            Additional parameters to override shell defaults
        visualize : bool
            Whether to generate comparison visualization
            
        Returns:
        --------
        Dict with comparison results
        """
        # Execute each shell
        results = {}
        for shell_id in shell_ids:
            try:
                result = self.execute_shell(
                    shell_id,
                    prompt,
                    parameters=parameters,
                    visualize=False  # We'll create a combined visualization
                )
                results[shell_id] = result
            except Exception as e:
                log.error(f"Error executing shell {shell_id} for comparison: {e}")
                results[shell_id] = {
                    "error": str(e),
                    "success": False
                }
        
        # Generate comparison visualization if requested
        comparison_viz = None
        if visualize:
            comparison_viz = self.visualizer.generate_shell_comparison(
                results
            )
        
        # Prepare comparison result
        comparison = {
            "results": results,
            "prompt": prompt,
            "visualization": comparison_viz,
            "timestamp": self.symbolic_engine.get_timestamp(),
            "shells_compared": shell_ids
        }
        
        return comparison

    def log_execution_result(self, result: ShellExecutionResult, log_path: Optional[str] = None) -> str:
        """
        Log shell execution result to file
        
        Parameters:
        -----------
        result : ShellExecutionResult
            Execution result to log
        log_path : Optional[str]
            Path for log file (if None, uses default)
            
        Returns:
        --------
        Path to log file
        """
        if log_path is None:
            # Use default log directory
            log_dir = self.config.get("log_directory", "logs")
            os.makedirs(log_dir, exist_ok=True)
            
            # Create filename with timestamp
            timestamp = result.metadata.get("timestamp", "").replace(":", "-").replace(" ", "_")
            log_path = os.path.join(log_dir, f"{result.shell_id}_{timestamp}.json")
        
        # Convert result to serializable dict
        result_dict = {
            "shell_id": result.shell_id,
            "success": result.success,
            "execution_time": result.execution_time,
            "result": result.result,
            "residue": result.residue,
            "collapse_detected": result.collapse_detected,
            "collapse_type": result.collapse_type,
            "attribution_map": result.attribution_map,
            "metadata": result.metadata
        }
        
        # Exclude visualization to keep log size manageable
        if "visualization" in result_dict:
            del result_dict["visualization"]
        
        # Write to file
        with open(log_path, 'w') as f:
            json.dump(result_dict, f, indent=2)
        
        log.info(f"Execution result logged to {log_path}")
        return log_path


# Module execution entry point for CLI usage
if __name__ == "__main__":
    import argparse
    import json
    
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Symbolic Shell Executor for transformerOS")
    parser.add_argument("--shell", required=True, help="Shell ID to execute")
    parser.add_argument("--prompt", required=True, help="Input prompt")
    parser.add_argument("--pack", help="Path to shell pack to load first")
    parser.add_argument("--model", default="default", help="Model ID to use")
    parser.add_argument("--config", help="Path to executor configuration")
    parser.add_argument("--visualize", action="store_true", help="Generate visualization")
    parser.add_argument("--log", action="store_true", help="Log execution result")
    parser.add_argument("--output", help="Output file for result")
    
    args = parser.parse_args()
    
    # Create executor
    executor = ShellExecutor(
        config_path=args.config,
        model_id=args.model
    )
    
    # Load shell pack if specified
    if args.pack:
        executor.load_shell_pack(args.pack)
    
    # Execute shell
    result = executor.execute_shell(
        args.shell,
        args.prompt,
        visualize=args.visualize
    )
    
    # Log result if requested
    if args.log:
        executor.log_execution_result(result)
    
    # Output result
    if args.output:
        # Prepare serializable dict
        result_dict = {
            "shell_id": result.shell_id,
            "success": result.success,
            "execution_time": result.execution_time,
            "result": result.result,
            "collapse_detected": result.collapse_detected,
            "collapse_type": result.collapse_type,
            "metadata": result.metadata
        }
        
        # Include visualization if generated
        if result.visualization:
            result_dict["visualization"] = result.visualization
        
        # Write to file
        with open(args.output, 'w') as f:
            json.dump(result_dict, f, indent=2)
    else:
        # Print summary to console
        print(f"Shell: {result.shell_id}")
        print(f"Success: {result.success}")
        print(f"Execution time: {result.execution_time:.2f}s")
        print(f"Collapse detected: {result.collapse_detected}")
        if result.collapse_detected:
            print(f"Collapse type: {result.collapse_type}")
        print("\nResult summary:")
        for op_key, op_result in result.result.items():
            print(f"  - {op_key}: {op_result.get('status', 'completed')}")
