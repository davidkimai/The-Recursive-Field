"""
parse.py
Translate .p/ commands to function calls in transformerOS

This module handles the parsing and translation of the .p/ command language,
transforming structured .p/ commands into executable function calls in the
transformerOS framework.
"""

import re
import yaml
import json
import logging
from typing import Dict, List, Optional, Tuple, Union, Any
from pathlib import Path

# Configure parser logging
log = logging.getLogger("transformerOS.pareto_lang.parse")
log.setLevel(logging.INFO)

class CommandParser:
    """
    Parser for the .p/ command language
    
    This class handles the parsing and translation of .p/ commands into
    executable function calls, enabling a consistent interface between
    the symbolic command language and the underlying system operations.
    """
    
    def __init__(self, commands_file: Optional[str] = None):
        """
        Initialize the command parser
        
        Parameters:
        -----------
        commands_file : Optional[str]
            Path to the YAML file containing command definitions
            If None, uses the default commands.yaml in the same directory
        """
        # Load command definitions
        if commands_file is None:
            # Use default commands file in the same directory
            commands_file = Path(__file__).parent / "commands.yaml"
        
        self.commands = self._load_commands(commands_file)
        
        # Compile regex patterns for command parsing
        self.command_pattern = re.compile(r'\.p/([a-zA-Z_]+)\.([a-zA-Z_]+)(\{.*\})?')
        self.param_pattern = re.compile(r'([a-zA-Z_]+)\s*=\s*([^,}]+)')
        
        log.info(f"CommandParser initialized with {len(self.commands)} command definitions")

    def _load_commands(self, commands_file: str) -> Dict:
        """Load command definitions from YAML file"""
        try:
            with open(commands_file, 'r') as f:
                commands = yaml.safe_load(f)
            
            # Validate command structure
            if not isinstance(commands, dict) or "commands" not in commands:
                raise ValueError(f"Invalid command file format: {commands_file}")
            
            log.info(f"Loaded {len(commands['commands'])} command definitions from {commands_file}")
            return commands
        
        except Exception as e:
            log.error(f"Failed to load commands from {commands_file}: {e}")
            # Return empty commands dict as fallback
            return {"commands": {}, "version": "unknown"}

    def parse_command(self, command_str: str) -> Dict:
        """
        Parse a .p/ command string into a structured command object
        
        Parameters:
        -----------
        command_str : str
            The .p/ command string to parse
            
        Returns:
        --------
        Dict containing the parsed command structure
        """
        # Strip whitespace
        command_str = command_str.strip()
        
        # Check if this is a .p/ command
        if not command_str.startswith(".p/"):
            raise ValueError(f"Not a valid .p/ command: {command_str}")
        
        # Extract command components using regex
        match = self.command_pattern.match(command_str)
        if not match:
            raise ValueError(f"Invalid command format: {command_str}")
        
        domain, operation, params_str = match.groups()
        
        # Parse parameters if present
        params = {}
        if params_str:
            # Remove the braces
            params_str = params_str.strip('{}')
            
            # Extract parameters using regex
            param_matches = self.param_pattern.findall(params_str)
            for param_name, param_value in param_matches:
                # Process the parameter value based on type
                params[param_name] = self._parse_parameter_value(param_value)
        
        # Create command structure
        parsed_command = {
            "domain": domain,
            "operation": operation,
            "parameters": params,
            "original": command_str
        }
        
        log.debug(f"Parsed command: {parsed_command}")
        return parsed_command

    def _parse_parameter_value(self, value_str: str) -> Any:
        """Parse a parameter value string into the appropriate type"""
        # Strip whitespace and quotes
        value_str = value_str.strip()
        
        # Handle quoted strings
        if (value_str.startswith('"') and value_str.endswith('"')) or \
           (value_str.startswith("'") and value_str.endswith("'")):
            return value_str[1:-1]
        
        # Handle numeric values
        try:
            # Try as int
            if value_str.isdigit():
                return int(value_str)
            
            # Try as float
            return float(value_str)
        except ValueError:
            pass
        
        # Handle boolean values
        if value_str.lower() == "true":
            return True
        elif value_str.lower() == "false":
            return False
        
        # Handle special values
        if value_str.lower() == "null" or value_str.lower() == "none":
            return None
        
        # Handle lists
        if value_str.startswith('[') and value_str.endswith(']'):
            # Simple list parsing - this could be enhanced for nested structures
            items = value_str[1:-1].split(',')
            return [self._parse_parameter_value(item) for item in items]
        
        # Handle complete as a special string case
        if value_str.lower() == "complete":
            return "complete"
        
        # Default to string
        return value_str

    def validate_command(self, parsed_command: Dict) -> Tuple[bool, Optional[str]]:
        """
        Validate a parsed command against command definitions
        
        Parameters:
        -----------
        parsed_command : Dict
            The parsed command structure to validate
            
        Returns:
        --------
        Tuple of (is_valid, error_message)
        """
        domain = parsed_command["domain"]
        operation = parsed_command["operation"]
        parameters = parsed_command["parameters"]
        
        # Check if domain exists
        if domain not in self.commands["commands"]:
            return False, f"Unknown command domain: {domain}"
        
        # Check if operation exists in domain
        domain_commands = self.commands["commands"][domain]
        if operation not in domain_commands:
            return False, f"Unknown operation '{operation}' in domain '{domain}'"
        
        # Get command definition
        command_def = domain_commands[operation]
        
        # Check required parameters
        if "required_parameters" in command_def:
            for required_param in command_def["required_parameters"]:
                if required_param not in parameters:
                    return False, f"Missing required parameter: {required_param}"
        
        # Check parameter types (basic validation)
        if "parameters" in command_def:
            for param_name, param_value in parameters.items():
                if param_name in command_def["parameters"]:
                    expected_type = command_def["parameters"][param_name]["type"]
                    
                    # Check parameter type
                    if not self._validate_parameter_type(param_value, expected_type):
                        return False, f"Parameter '{param_name}' has invalid type. Expected {expected_type}."
        
        return True, None

    def _validate_parameter_type(self, value: Any, expected_type: str) -> bool:
        """Validate a parameter value against its expected type"""
        if expected_type == "string":
            return isinstance(value, str)
        elif expected_type == "int":
            return isinstance(value, int)
        elif expected_type == "float":
            return isinstance(value, (int, float))
        elif expected_type == "bool":
            return isinstance(value, bool)
        elif expected_type == "list":
            return isinstance(value, list)
        elif expected_type == "any":
            return True
        elif expected_type == "string_or_int":
            return isinstance(value, (str, int))
        elif expected_type == "null":
            return value is None
        else:
            # For complex types, just return True
            return True

    def get_function_mapping(self, parsed_command: Dict) -> Dict:
        """
        Get the function mapping for a parsed command
        
        Parameters:
        -----------
        parsed_command : Dict
            The parsed command structure
            
        Returns:
        --------
        Dict containing function mapping information
        """
        domain = parsed_command["domain"]
        operation = parsed_command["operation"]
        
        # Get command definition
        try:
            command_def = self.commands["commands"][domain][operation]
        except KeyError:
            log.warning(f"No function mapping found for {domain}.{operation}")
            return {"function": None, "module": None, "parameters": {}}
        
        # Extract function mapping
        function_mapping = command_def.get("function_mapping", {})
        
        # Create mapping result
        mapping = {
            "function": function_mapping.get("function", None),
            "module": function_mapping.get("module", None),
            "parameters": self._map_parameters(parsed_command["parameters"], function_mapping),
            "original_command": parsed_command["original"]
        }
        
        return mapping

    def _map_parameters(self, cmd_params: Dict, function_mapping: Dict) -> Dict:
        """Map command parameters to function parameters based on mapping rules"""
        result_params = {}
        
        # Direct parameter mappings
        param_mapping = function_mapping.get("parameter_mapping", {})
        for cmd_param, func_param in param_mapping.items():
            if cmd_param in cmd_params:
                result_params[func_param] = cmd_params[cmd_param]
        
        # Add unmapped parameters if they match function parameter names
        for param_name, param_value in cmd_params.items():
            if param_name not in param_mapping.values():
                # Add parameter directly if no specific mapping
                result_params[param_name] = param_value
        
        return result_params

    def extract_commands(self, text: str) -> List[Dict]:
        """
        Extract all .p/ commands from a text
        
        Parameters:
        -----------
        text : str
            The text to extract commands from
            
        Returns:
        --------
        List of parsed command dictionaries
        """
        # Find all command matches
        pattern = r'(\.p/[a-zA-Z_]+\.[a-zA-Z_]+(?:\{[^}]*\})?)'
        command_matches = re.findall(pattern, text)
        
        # Parse each command
        parsed_commands = []
        for cmd_str in command_matches:
            try:
                parsed_cmd = self.parse_command(cmd_str)
                parsed_commands.append(parsed_cmd)
            except ValueError as e:
                log.warning(f"Failed to parse command '{cmd_str}': {e}")
        
        log.info(f"Extracted {len(parsed_commands)} commands from text")
        return parsed_commands


# Command execution helper function
def execute_parsed_command(parsed_mapping: Dict) -> Dict:
    """
    Execute a parsed command mapping using dynamic imports
    
    Parameters:
    -----------
    parsed_mapping : Dict
        The parsed function mapping to execute
        
    Returns:
    --------
    Dict containing execution results
    """
    function_name = parsed_mapping["function"]
    module_name = parsed_mapping["module"]
    parameters = parsed_mapping["parameters"]
    
    if not function_name or not module_name:
        raise ValueError("Invalid function mapping: missing function or module name")
    
    try:
        # Dynamically import the module
        module = __import__(module_name, fromlist=[function_name])
        
        # Get the function from the module
        function = getattr(module, function_name)
        
        # Execute the function with parameters
        result = function(**parameters)
        
        # Return execution result
        return {
            "status": "success",
            "result": result,
            "command": parsed_mapping["original_command"]
        }
        
    except ImportError as e:
        log.error(f"Failed to import module {module_name}: {e}")
        return {
            "status": "error",
            "error": f"Module not found: {module_name}",
            "command": parsed_mapping["original_command"]
        }
        
    except AttributeError as e:
        log.error(f"Function {function_name} not found in module {module_name}: {e}")
        return {
            "status": "error",
            "error": f"Function not found: {function_name}",
            "command": parsed_mapping["original_command"]
        }
        
    except Exception as e:
        log.error(f"Error executing function {function_name}: {e}")
        return {
            "status": "error",
            "error": str(e),
            "command": parsed_mapping["original_command"]
        }


# Main execution for command-line usage
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Parse .p/ commands")
    parser.add_argument("command", help=".p/ command to parse")
    parser.add_argument("--commands-file", help="Path to commands YAML file")
    parser.add_argument("--execute", action="store_true", help="Execute the parsed command")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    
    args = parser.parse_args()
    
    # Configure logging
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    
    # Create parser
    cmd_parser = CommandParser(args.commands_file)
    
    try:
        # Parse command
        parsed_cmd = cmd_parser.parse_command(args.command)
        print("Parsed Command:")
        print(json.dumps(parsed_cmd, indent=2))
        
        # Validate command
        valid, error = cmd_parser.validate_command(parsed_cmd)
        if valid:
            print("Command validation: PASSED")
        else:
            print(f"Command validation: FAILED - {error}")
        
        # Get function mapping
        func_mapping = cmd_parser.get_function_mapping(parsed_cmd)
        print("\nFunction Mapping:")
        print(json.dumps(func_mapping, indent=2))
        
        # Execute if requested
        if args.execute and valid:
            print("\nExecuting command...")
            result = execute_parsed_command(func_mapping)
            print("\nExecution Result:")
            print(json.dumps(result, indent=2))
            
    except Exception as e:
        print(f"Error: {e}")
