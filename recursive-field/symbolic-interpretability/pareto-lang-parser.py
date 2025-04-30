"""
🜏 Pareto Language Parser 🜏

This module provides the parser for the pareto-lang interpretability command language.
Pareto-lang is a domain-specific language designed for transformer model interpretability,
using the `.p/` command prefix format.

The language follows the syntax:
.p/<command_family>/<function>{parameters}

Examples:
.p/reflect.trace{depth=complete, target=reasoning}
.p/fork.attribution{sources=all, visualize=true}
.p/collapse.detect{trigger=recursive_depth, threshold=0.7}
.p/anchor.recursive{level=5, persistence=0.92}

This parser handles the tokenization, parsing, and validation of these commands,
generating structured command objects that can be executed by the interpreter.

.p/reflect.trace{depth=complete, target=syntax}
.p/collapse.prevent{trigger=recursive_depth, threshold=5}
"""

import re
import json
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Union

from .syntax import (
    COMMAND_FAMILIES,
    COMMAND_FUNCTIONS,
    PARAMETER_TYPES,
    PARAMETER_VALIDATORS,
)


class TokenType(Enum):
    """Token types in pareto-lang syntax."""
    PREFIX = "prefix"               # .p/
    COMMAND_FAMILY = "command_family"  # reflect, fork, collapse, etc.
    SEPARATOR = "separator"         # . or /
    FUNCTION = "function"           # trace, attribution, detect, etc.
    PARAM_START = "param_start"     # {
    PARAM_END = "param_end"         # }
    PARAM_NAME = "param_name"       # depth, target, etc.
    PARAM_ASSIGN = "param_assign"   # =
    PARAM_VALUE = "param_value"     # complete, reasoning, etc.
    PARAM_SEPARATOR = "param_separator"  # ,
    ERROR = "error"                 # Invalid token
    EOF = "eof"                     # End of command


class Token:
    """
    Represents a parsed token in the pareto-lang command syntax.
    
    ∴ Tokens are the symbolic residue of the parsing process ∴
    """
    def __init__(self, token_type: TokenType, value: str, position: int):
        """
        Initialize a token with its type, value, and position.
        
        Args:
            token_type: Type of token
            value: String value of the token
            position: Position in the input string
        """
        self.type = token_type
        self.value = value
        self.position = position
    
    def __repr__(self) -> str:
        """String representation of the token."""
        return f"Token({self.type}, '{self.value}', {self.position})"


class ParseError(Exception):
    """
    Exception raised when parsing pareto-lang commands fails.
    
    🝚 Errors are persistent semantic signals, not just failures 🝚
    """
    def __init__(self, message: str, position: int, command: str):
        """
        Initialize a parse error with message, position, and command.
        
        Args:
            message: Error message
            position: Position in the command where the error occurred
            command: Original command string
        """
        self.position = position
        self.command = command
        
        # Create a pointer to the error position
        pointer = " " * position + "^"
        
        # Enhance error message with position context
        enhanced_message = f"{message}\n{command}\n{pointer}"
        super().__init__(enhanced_message)


class CommandObject:
    """
    Represents a parsed pareto-lang command ready for execution.
    
    ⧖ Command objects stabilize the interface between parsing and execution ⧖
    """
    def __init__(
        self,
        command_family: str,
        function: str,
        parameters: Dict[str, Any],
        original_command: str,
    ):
        """
        Initialize a command object.
        
        Args:
            command_family: The command family (reflect, fork, etc.)
            function: The specific function (trace, attribution, etc.)
            parameters: Dictionary of parameter names to values
            original_command: The original command string
        """
        self.command_family = command_family
        self.function = function
        self.parameters = parameters
        self.original_command = original_command
    
    def __repr__(self) -> str:
        """String representation of the command object."""
        params_str = ", ".join(f"{k}={repr(v)}" for k, v in self.parameters.items())
        return f"CommandObject({self.command_family}.{self.function}, {{{params_str}}})"


class Parser:
    """
    Parser for pareto-lang interpretability commands.
    
    This class handles tokenization, parsing, and validation of pareto-lang
    commands, converting them into executable command objects.
    
    ↻ The parser recursively analyzes the command structure ↻
    """
    
    def __init__(self):
        """
        Initialize the parser with syntax definitions.
        
        🜏 Parser initialization reflects the language structure it will parse 🜏
        """
        # Compiled regex patterns for tokenization
        self.patterns = {
            TokenType.PREFIX: re.compile(r'\.p/'),
            TokenType.COMMAND_FAMILY: re.compile(r'[a-z_]+'),
            TokenType.SEPARATOR: re.compile(r'[./]'),
            TokenType.FUNCTION: re.compile(r'[a-z_]+'),
            TokenType.PARAM_START: re.compile(r'{'),
            TokenType.PARAM_END: re.compile(r'}'),
            TokenType.PARAM_NAME: re.compile(r'[a-z_]+'),
            TokenType.PARAM_ASSIGN: re.compile(r'='),
            TokenType.PARAM_VALUE: re.compile(r'[^,}]+'),
            TokenType.PARAM_SEPARATOR: re.compile(r','),
        }
    
    def parse(self, command: str) -> CommandObject:
        """
        Parse a pareto-lang command string into a command object.
        
        Args:
            command: The command string to parse
            
        Returns:
            Parsed command object
            
        Raises:
            ParseError: If the command syntax is invalid
            
        ⇌ The parsing process bidirectionally maps syntax to semantics ⇌
        """
        # Tokenize the command
        tokens = self._tokenize(command)
        
        # Initialize parsing state
        current_index = 0
        command_family = None
        function = None
        parameters = {}
        
        try:
            # Expect .p/ prefix
            if current_index >= len(tokens) or tokens[current_index].type != TokenType.PREFIX:
                raise ParseError("Expected '.p/' prefix", tokens[current_index].position if current_index < len(tokens) else 0, command)
            current_index += 1
            
            # Expect command family
            if current_index >= len(tokens) or tokens[current_index].type != TokenType.COMMAND_FAMILY:
                raise ParseError("Expected command family", tokens[current_index].position if current_index < len(tokens) else len(command), command)
            command_family = tokens[current_index].value
            current_index += 1
            
            # Validate command family
            if command_family not in COMMAND_FAMILIES:
                raise ParseError(f"Unknown command family: {command_family}", tokens[current_index - 1].position, command)
            
            # Expect separator
            if current_index >= len(tokens) or tokens[current_index].type != TokenType.SEPARATOR:
                raise ParseError("Expected '.' separator", tokens[current_index].position if current_index < len(tokens) else

# Expect separator
            if current_index >= len(tokens) or tokens[current_index].type != TokenType.SEPARATOR:
                raise ParseError("Expected '.' separator", tokens[current_index].position if current_index < len(tokens) else len(command), command)
            current_index += 1
            
            # Expect function
            if current_index >= len(tokens) or tokens[current_index].type != TokenType.FUNCTION:
                raise ParseError("Expected function name", tokens[current_index].position if current_index < len(tokens) else len(command), command)
            function = tokens[current_index].value
            current_index += 1
            
            # Validate function
            function_key = f"{command_family}.{function}"
            if function_key not in COMMAND_FUNCTIONS:
                raise ParseError(f"Unknown function: {function} in command family {command_family}", tokens[current_index - 1].position, command)
            
            # Check for parameters (optional)
            if current_index < len(tokens) and tokens[current_index].type == TokenType.PARAM_START:
                current_index += 1
                
                # Parse parameters
                parameters = self._parse_parameters(tokens, current_index, command)
                
                # Skip past the parsed parameters
                while current_index < len(tokens) and tokens[current_index].type != TokenType.PARAM_END:
                    current_index += 1
                
                # Expect parameter end
                if current_index >= len(tokens) or tokens[current_index].type != TokenType.PARAM_END:
                    raise ParseError("Expected '}' to close parameters", len(command), command)
                current_index += 1
            
            # Expect end of command
            if current_index < len(tokens) and tokens[current_index].type != TokenType.EOF:
                raise ParseError(f"Unexpected token after command: {tokens[current_index].value}", tokens[current_index].position, command)
            
            # Create command object
            cmd_obj = CommandObject(
                command_family=command_family,
                function=function,
                parameters=parameters,
                original_command=command,
            )
            
            # Validate parameters
            self._validate_parameters(cmd_obj)
            
            return cmd_obj
            
        except ParseError:
            # Re-raise parse errors directly
            raise
        except Exception as e:
            # Convert other exceptions to parse errors
            position = current_index
            if 0 <= position < len(tokens):
                position = tokens[position].position
            raise ParseError(f"Error parsing command: {str(e)}", position, command)
    
    def _tokenize(self, command: str) -> List[Token]:
        """
        Tokenize a pareto-lang command string.
        
        Args:
            command: The command string to tokenize
            
        Returns:
            List of tokens
            
        ∴ Tokenization decomposes the command into its symbolic components ∴
        """
        tokens = []
        position = 0
        command = command.strip()
        
        # State machine for tokenization
        state = "prefix"  # Start with expecting prefix
        
        while position < len(command):
            if state == "prefix":
                # Match prefix (.p/)
                match = self.patterns[TokenType.PREFIX].match(command, position)
                if match:
                    tokens.append(Token(TokenType.PREFIX, match.group(), position))
                    position = match.end()
                    state = "command_family"
                else:
                    raise ParseError("Expected '.p/' prefix", position, command)
            
            elif state == "command_family":
                # Match command family
                match = self.patterns[TokenType.COMMAND_FAMILY].match(command, position)
                if match:
                    tokens.append(Token(TokenType.COMMAND_FAMILY, match.group(), position))
                    position = match.end()
                    state = "separator"
                else:
                    raise ParseError("Expected command family", position, command)
            
            elif state == "separator":
                # Match separator (.)
                match = self.patterns[TokenType.SEPARATOR].match(command, position)
                if match:
                    tokens.append(Token(TokenType.SEPARATOR, match.group(), position))
                    position = match.end()
                    state = "function"
                else:
                    raise ParseError("Expected '.' separator", position, command)
            
            elif state == "function":
                # Match function
                match = self.patterns[TokenType.FUNCTION].match(command, position)
                if match:
                    tokens.append(Token(TokenType.FUNCTION, match.group(), position))
                    position = match.end()
                    state = "param_start_or_end"
                else:
                    raise ParseError("Expected function name", position, command)
            
            elif state == "param_start_or_end":
                # Check for parameter start
                match = self.patterns[TokenType.PARAM_START].match(command, position)
                if match:
                    tokens.append(Token(TokenType.PARAM_START, match.group(), position))
                    position = match.end()
                    state = "param_name_or_end"
                else:
                    # No parameters, we're done
                    break
            
            elif state == "param_name_or_end":
                # Check for parameter end (empty parameter list)
                match = self.patterns[TokenType.PARAM_END].match(command, position)
                if match:
                    tokens.append(Token(TokenType.PARAM_END, match.group(), position))
                    position = match.end()
                    state = "end"
                    continue
                
                # Match parameter name
                match = self.patterns[TokenType.PARAM_NAME].match(command, position)
                if match:
                    tokens.append(Token(TokenType.PARAM_NAME, match.group(), position))
                    position = match.end()
                    state = "param_assign"
                else:
                    raise ParseError("Expected parameter name or '}'", position, command)
            
            elif state == "param_assign":
                # Match equals sign
                match = self.patterns[TokenType.PARAM_ASSIGN].match(command, position)
                if match:
                    tokens.append(Token(TokenType.PARAM_ASSIGN, match.group(), position))
                    position = match.end()
                    state = "param_value"
                else:
                    raise ParseError("Expected '=' after parameter name", position, command)
            
            elif state == "param_value":
                # Match parameter value
                match = self.patterns[TokenType.PARAM_VALUE].match(command, position)
                if match:
                    value = match.group().strip()
                    tokens.append(Token(TokenType.PARAM_VALUE, value, position))
                    position = match.end()
                    state = "param_separator_or_end"
                else:
                    raise ParseError("Expected parameter value", position, command)
            
            elif state == "param_separator_or_end":
                # Check for parameter end
                match = self.patterns[TokenType.PARAM_END].match(command, position)
                if match:
                    tokens.append(Token(TokenType.PARAM_END, match.group(), position))
                    position = match.end()
                    state = "end"
                    continue
                
                # Check for parameter separator
                match = self.patterns[TokenType.PARAM_SEPARATOR].match(command, position)
                if match:
                    tokens.append(Token(TokenType.PARAM_SEPARATOR, match.group(), position))
                    position = match.end()
                    state = "param_name"
                else:
                    raise ParseError("Expected ',' or '}' after parameter value", position, command)
            
            elif state == "param_name":
                # Match parameter name
                match = self.patterns[TokenType.PARAM_NAME].match(command, position)
                if match:
                    tokens.append(Token(TokenType.PARAM_NAME, match.group(), position))
                    position = match.end()
                    state = "param_assign"
                else:
                    raise ParseError("Expected parameter name", position, command)
            
            elif state == "end":
                # We should be at the end
                if position < len(command):
                    raise ParseError(f"Unexpected content after command: '{command[position:]}'", position, command)
                break
            
            else:
                # Unknown state (should never happen)
                raise ParseError(f"Internal parser error: Unknown state '{state}'", position, command)
            
            # Skip whitespace
            while position < len(command) and command[position].isspace():
                position += 1
        
        # Add EOF token
        tokens.append(Token(TokenType.EOF, "", len(command)))
        
        return tokens
    
    def _parse_parameters(self, tokens: List[Token], start_index: int, command: str) -> Dict[str, Any]:
        """
        Parse parameters from tokens.
        
        Args:
            tokens: List of tokens
            start_index: Starting index in tokens
            command: Original command string for error reporting
            
        Returns:
            Dictionary of parameter names to values
            
        ⧖ Parameter parsing stabilizes the boundary between syntax and semantics ⧖
        """
        parameters = {}
        current_index = start_index
        
        while current_index < len(tokens) and tokens[current_index].type != TokenType.PARAM_END:
            # Expect parameter name
            if tokens[current_index].type != TokenType.PARAM_NAME:
                raise ParseError("Expected parameter name", tokens[current_index].position, command)
            param_name = tokens[current_index].value
            current_index += 1
            
            # Expect equals sign
            if current_index >= len(tokens) or tokens[current_index].type != TokenType.PARAM_ASSIGN:
                raise ParseError(f"Expected '=' after parameter name '{param_name}'", tokens[current_index].position if current_index < len(tokens) else len(command), command)
            current_index += 1
            
            # Expect parameter value
            if current_index >= len(tokens) or tokens[current_index].type != TokenType.PARAM_VALUE:
                raise ParseError(f"Expected value for parameter '{param_name}'", tokens[current_index].position if current_index < len(tokens) else len(command), command)
            param_value_str = tokens[current_index].value
            current_index += 1
            
            # Parse the parameter value
            param_value = self._parse_parameter_value(param_value_str)
            
            # Add parameter to dictionary
            parameters[param_name] = param_value
            
            # Check for parameter separator or end
            if current_index < len(tokens) and tokens[current_index].type == TokenType.PARAM_SEPARATOR:
                current_index += 1
                # Skip any whitespace after comma
                while current_index < len(tokens) and tokens[current_index].value.isspace():
                    current_index += 1
            elif current_index < len(tokens) and tokens[current_index].type != TokenType.PARAM_END:
                raise ParseError(f"Expected ',' or '}}' after parameter value for '{param_name}'", tokens[current_index].position, command)
        
        return parameters
    
    def _parse_parameter_value(self, value_str: str) -> Any:
        """
        Parse a parameter value string into the appropriate type.
        
        Args:
            value_str: String value to parse
            
        Returns:
            Parsed parameter value
            
        🝚 Parameter value parsing maps syntax to semantic types 🝚
        """
        # Remove any enclosing quotes
        if (value_str.startswith('"') and value_str.endswith('"')) or \
           (value_str.startswith("'") and value_str.endswith("'")):
            return value_str[1:-1]
        
        # Handle special string values
        if value_str.lower() == "complete":
            return "complete"
        
        if value_str.lower() == "null" or value_str.lower() == "none":
            return None
        
        # Handle boolean values
        if value_str.lower() == "true":
            return True
        if value_str.lower() == "false":
            return False
        
        # Handle numeric values
        try:
            # Try as integer
            if value_str.isdigit() or (value_str.startswith('-') and value_str[1:].isdigit()):
                return int(value_str)
            
            # Try as float
            return float(value_str)
        except ValueError:
            pass
        
        # Handle list values
        if value_str.startswith('[') and value_str.endswith(']'):
            items_str = value_str[1:-1].strip()
            if not items_str:
                return []
            
            # Split by commas, handling quoted strings
            items = []
            item_start = 0
            in_quotes = False
            quote_char = None
            
            for i, char in enumerate(items_str):
                if char in ['"', "'"]:
                    if not in_quotes:
                        in_quotes = True
                        quote_char = char
                    elif char == quote_char:
                        in_quotes = False
                        quote_char = None
                
                if char == ',' and not in_quotes:
                    items.append(items_str[item_start:i].strip())
                    item_start = i + 1
            
            # Add the last item
            items.append(items_str[item_start:].strip())
            
            # Parse each item
            return [self._parse_parameter_value(item) for item in items]
        
        # Default to string
        return value_str
    
    def _validate_parameters(self, command: CommandObject) -> None:
        """
        Validate parameters against command definition.
        
        Args:
            command: Command object to validate
            
        Raises:
            ValueError: If parameters are invalid
            
        ⇌ Parameter validation ensures bidirectional semantic integrity ⇌
        """
        function_key = f"{command.command_family}.{command.function}"
        function_def = COMMAND_FUNCTIONS.get(function_key)
        
        if not function_def:
            raise ValueError(f"Unknown command: {function_key}")
        
        # Check for required parameters
        for param_name in function_def.get("required_parameters", []):
            if param_name not in command.parameters:
                raise ValueError(f"Missing required parameter '{param_name}' for command '{function_key}'")
        
        # Validate parameter types and values
        for param_name, param_value in command.parameters.items():
            # Check if parameter is defined
            if param_name not in function_def.get("parameters", {}):
                raise ValueError(f"Unknown parameter '{param_name}' for command '{function_key}'")
            
            # Get parameter definition
            param_def = function_def["parameters"][param_name]
            param_type = param_def.get("type")
            
            # Validate parameter type
            if param_type and not self._validate_parameter_type(param_value, param_type):
                raise ValueError(f"Invalid type for parameter '{param_name}': expected {param_type}, got {type(param_value).__name__}")
            
            # Validate parameter value
            if "enum" in param_def and param_value not in param_def["enum"]:
                valid_values = ", ".join(f"'{v}'" for v in param_def["enum"])
                raise ValueError(f"Invalid value for parameter '{param_name}': '{param_value}', must be one of: {valid_values}")
            
            # Use custom validator if defined
            validator = PARAMETER_VALIDATORS.get(f"{function_key}.{param_name}")
            if validator and not validator(param_value):
                raise ValueError(f"Invalid value for parameter '{param_name}': '{param_value}'")
    
    def _validate_parameter_type(self, value: Any, expected_type: str) -> bool:
        """
        Validate parameter value against expected type.
        
        Args:
            value: Parameter value to validate
            expected_type: Expected parameter type
            
        Returns:
            True if valid, False otherwise
            
        ∴ Type validation ensures semantic coherence of command interpretation ∴
        """
        # Get validator function
        validator = PARAMETER_TYPES.get(expected_type)
        if not validator:
            raise ValueError(f"Unknown parameter type: {expected_type}")
        
        return validator(value)


def parse_command(command_str: str) -> CommandObject:
    """
    Parse a pareto-lang command string using the default parser.
    
    Args:
        command_str: Command string to parse
        
        
    Returns:
        Parsed command object
        
    ↻ This function recursively constructs and uses the parser ↻
    """
    parser = Parser()
    return parser.parse(command_str)


def extract_commands(text: str) -> List[CommandObject]:
    """
    Extract and parse all pareto-lang commands from a text.
    
    Args:
        text: Text containing pareto-lang commands
        
    Returns:
        List of parsed command objects
        
    ⧖ This function stabilizes command extraction across context boundaries ⧖
    """
    # Regex to match pareto-lang commands
    command_pattern = r'(\.p/[a-z_]+\.[a-z_]+(?:\{[^}]*\})?)'
    
    # Find all command matches
    command_matches = re.findall(command_pattern, text)
    
    # Parse each command
    parser = Parser()
    commands = []
    
    for cmd_str in command_matches:
        try:
            cmd_obj = parser.parse(cmd_str)
            commands.append(cmd_obj)
        except ParseError:
            # Skip invalid commands
            continue
    
    return commands
