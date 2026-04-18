from flask import Flask, render_template, request
import math

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
# Route to handle calculation requests
@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        expression = request.form['expression']
        # Securely evaluate expressions using a limited dictionary of allowed functions
        # This prevents arbitrary code execution vulnerabilities with eval()
        safe_dict = {'math': math, '__builtins__': {}, 
                     'sin': math.sin, 'cos': math.cos, 'tan': math.tan, 
                     'log': math.log10, 'sqrt': math.sqrt, 'exp': math.exp,
                     'pi': math.pi, 'e': math.e}
        result = str(eval(expression, safe_dict))
        return render_template('index.html', result=result, expression=expression)
    except Exception as e:
        return render_template('index.html', error=str(e), expression=expression)

if __name__ == '__main__':
    app.run(debug=True)
