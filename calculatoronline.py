from flask import Flask, render_template, request, jsonify
import logging
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

# Security: Allow only basic math operations
SAFE_MATH_DICT = {
    '__builtins__': {},
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
        
        # Validate expression
        if not expression or expression == '0':
            return jsonify({'error': 'Please enter a valid expression'})
        
        # Check for incomplete expressions
        if expression[-1] in '+-*/.\\' or expression[0] in '+-*/.\\' :
            return jsonify({'error': 'Invalid expression'})
        
        # Validate length
        if len(expression) > 200:
            return jsonify({'error': 'Expression too long'})
        
        # Allow only: digits, operators, parentheses, decimal point
        allowed_chars = set('0123456789+-*/(). ')
        if not all(c in allowed_chars for c in expression):
            return jsonify({'error': 'Invalid characters in expression'})
        
        # Evaluate expression safely
        result = eval(expression, SAFE_MATH_DICT)
        
        # Format result
        if isinstance(result, float):
            result = round(result, 10)
        
        logger.info(f'Calculated: {expression} = {result}')
        return jsonify({'result': result})
    
    except ZeroDivisionError:
        logger.warning(f'Division by zero: {expression}')
        return jsonify({'error': 'Division by zero'})
    except Exception as e:
        logger.error(f'Error: {type(e).__name__} - {str(e)}')
        return jsonify({'error': 'Invalid expression'})
@app.errorhandler(500)
def internal_error(error):
    logger.error(f'500 Error: {str(error)}')
    return jsonify({'error': 'Server error'}), 500

if __name__ == '__main__':
    # Set debug to False in production
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    logger.info(f'Starting Flask Calculator (Debug: {debug_mode})')
    app.run(debug=debug_mode, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
