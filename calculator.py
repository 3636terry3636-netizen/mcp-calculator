# calculator.py
from fastmcp import FastMCP
import sys
import logging
import math
import random

logger = logging.getLogger('Calculator')

# Fix UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stderr.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')

# Create an MCP server
mcp = FastMCP("Calculator")

# Add calculation tool
@mcp.tool()
def calculator(expression: str) -> dict:
    """Execute mathematical calculations. Supports math operations, variables, and functions from math and random modules."""
    try:
        # Safe evaluation with limited namespace
        allowed_names = {
            'math': math,
            'random': random,
            'abs': abs,
            'pow': pow,
            'round': round,
            'min': min,
            'max': max,
            'sum': sum,
        }
        
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        logger.info(f"Expression: {expression} | Result: {result}")
        
        return {
            "success": True,
            "result": result,
            "expression": expression
        }
    except ZeroDivisionError:
        error_msg = "Error: Division by zero"
        logger.error(f"Expression: {expression} | {error_msg}")
        return {
            "success": False,
            "error": error_msg,
            "expression": expression
        }
    except NameError as e:
        error_msg = f"Error: Unknown variable or function - {str(e)}"
        logger.error(f"Expression: {expression} | {error_msg}")
        return {
            "success": False,
            "error": error_msg,
            "expression": expression
        }
    except SyntaxError:
        error_msg = "Error: Invalid expression syntax"
        logger.error(f"Expression: {expression} | {error_msg}")
        return {
            "success": False,
            "error": error_msg,
            "expression": expression
        }
    except Exception as e:
        error_msg = f"Error: {type(e).__name__} - {str(e)}"
        logger.error(f"Expression: {expression} | {error_msg}")
        return {
            "success": False,
            "error": error_msg,
            "expression": expression
        }

# Start the server
if __name__ == "__main__":
    mcp.run(transport="stdio")
