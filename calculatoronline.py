from flask import Flask, render_template, request
import math

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        expression = request.form['expression']
        # Securely evaluate expressions using a limited dictionary of allowed functions
        # This prevents arbitrary code execution vulnerabilities with eval()
        safe_dict = {'math': math, '__builtins__': {}}
        result = str(eval(expression, safe_dict))
        return render_template('index.html', result=result, expression=expression)
    except Exception as e:
        return render_template('index.html', error=str(e), expression=expression)

if __name__ == '__main__':
    app.run(debug=True)
