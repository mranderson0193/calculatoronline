from flask import Flask, render_template, request, jsonify
import math
import logging
from datetime import datetime
import os

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('calculator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Security: Define allowed safe functions and constants
SAFE_MATH_DICT = {
    'math': math,
    '__builtins__': {},
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'asin': math.asin,
    'acos': math.acos,
    'atan': math.atan,
    'log': math.log10,
    'log10': math.log10,
    'log2': math.log2,
    'ln': math.log,
    'sqrt': math.sqrt,
    'exp': math.exp,
    'factorial': math.factorial,
    'degrees': math.degrees,
    'radians': math.radians,
    'pi': math.pi,
    'e': math.e,
    'tau': math.tau,
    'inf': math.inf,
}

@app.route('/')
def index():
    logger.info('Home page accessed')
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    """Handle calculator expression evaluation with security validations."""
    try:
        expression = request.form.get('expression', '').strip()
        
        # Validate expression is not empty
        if not expression or expression == '0':
            logger.warning('Empty or invalid expression submitted')
            return render_template('index.html', error='Please enter a valid expression', expression=expression)
        
        # Final validation: check for incomplete expressions
        if expression[-1] in '+-*/.':
            logger.warning(f'Incomplete expression: {expression}')
            return render_template('index.html', error='Expression cannot end with an operator or decimal', expression=expression)
        
        # Validate expression length to prevent abuse
        if len(expression) > 500:
            logger.warning(f'Expression too long: {len(expression)} characters')
            return render_template('index.html', error='Expression too long', expression=expression)
        
        # Security: Only allow alphanumeric, operators, and safe function names
        allowed_chars = set('0123456789+-*/.()()sin cos tan log sqrt exp pi e asin acos atan log10 log2 ln factorial degrees radians tau inf math ., ')
        if not all(c in allowed_chars for c in expression.lower()):
            logger.warning(f'Invalid characters in expression: {expression}')
            return render_template('index.html', error='Invalid characters in expression', expression=expression)
        
        # Evaluate expression safely
        result = eval(expression, SAFE_MATH_DICT)
        
        # Format result
        if isinstance(result, float):
            # Round to 10 decimal places to avoid floating point precision issues
            result = round(result, 10)
        
        result_str = str(result)
        logger.info(f'Expression evaluated: {expression} = {result_str}')
        
        return render_template('index.html', result=result_str, expression=expression)
    
    except ZeroDivisionError:
        logger.warning(f'Division by zero attempted: {expression}')
        return render_template('index.html', error='Error: Division by zero', expression=expression)
    except ValueError as e:
        logger.warning(f'ValueError in expression {expression}: {str(e)}')
        return render_template('index.html', error=f'Error: Invalid value - {str(e)}', expression=expression)
    except Exception as e:
        logger.error(f'Exception in expression {expression}: {type(e).__name__} - {str(e)}')
        return render_template('index.html', error=f'Error: {str(e)}', expression=expression)

@app.errorhandler(404)
def not_found(error):
    logger.warning(f'404 Error: {request.path}')
    return render_template('index.html', error='Page not found'), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f'500 Error: {str(error)}')
    return render_template('index.html', error='Server error'), 500

if __name__ == '__main__':
    # Set debug to False in production
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    logger.info(f'Starting Flask Calculator (Debug: {debug_mode})')
    app.run(debug=debug_mode, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
