from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        expression = request.form['expression']
        result = eval(expression)
        return render_template('index.html', result=result, expression=expression)
    except Exception as e:
        return render_template('index.html', error=str(e), expression=expression)

if __name__ == '__main__':
    app.run(debug=True)
