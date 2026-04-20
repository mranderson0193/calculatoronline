# Simple Calculator

A clean, minimalist web-based calculator with a classic layout and responsive design.

## Features

- **Basic Arithmetic**: Addition (+), Subtraction (−), Multiplication (×), Division (÷)
- **Classic Layout**: Familiar 4×4 button grid with function buttons on top
- **Keyboard Support**: 
  - Number keys (0-9) for input
  - Operators: `+`, `-`, `*`, `/`
  - `Enter` to calculate
  - `Backspace` to delete last digit
  - `Escape` to clear display
- **Error Handling**: Validates expressions and shows clear error messages
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Dark Theme**: Modern dark interface with green display for easy reading

## Project Structure

```
project_Restructure/
├── calculatoronline.py          # Flask backend application
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Container configuration
├── templates/
│   └── index.html              # HTML/CSS/JavaScript frontend
├── .github/
│   └── workflows/
│       └── deploy_to_azure_container_app.yml  # CI/CD pipeline
├── README.md                    # This file
├── FINAL_STEPS_AND_NOTES.md    # Setup and maintenance notes
└── AZURE_DEPLOYMENT_CONFIG.md   # Azure deployment instructions
```

## Installation & Running Locally

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Development Server
```bash
python calculatoronline.py
```

The app will be available at `http://127.0.0.1:5000`

## API Endpoints

### GET `/`
Returns the calculator UI (index.html)

### POST `/calculate`
Evaluates a mathematical expression

**Request:**
```json
{
  "expression": "5+3"
}
```

**Response (Success):**
```json
{
  "result": 8
}
```

**Response (Error):**
```json
{
  "error": "Division by zero"
}
```

## Security

- Only basic arithmetic operators allowed: `+ − × ÷ ( ) . 0-9`
- Expression limited to 200 characters
- Safe evaluation using restricted `eval()` with empty builtins
- Input validation for incomplete or malformed expressions

## Docker Deployment

### Build Image
```bash
docker build -t flask-calculator .
```

### Run Container
```bash
docker run -p 5000:5000 flask-calculator
```

## Deployment to Azure Container Apps

See [AZURE_DEPLOYMENT_CONFIG.md](AZURE_DEPLOYMENT_CONFIG.md) for detailed deployment instructions.

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `0-9` | Enter digit |
| `+` `-` `*` `/` | Enter operator |
| `.` | Enter decimal point |
| `Enter` | Calculate result |
| `Backspace` | Delete last character |
| `Escape` | Clear display (AC) |

## Button Layout

```
AC   DEL  ÷   ×
 7    8   9   −
 4    5   6   +
 1    2   3   =
 0       .
```

- **AC**: Clear all
- **DEL**: Delete last digit
- **÷**: Divide
- **×**: Multiply
- **−**: Subtract
- **+**: Add
- **=**: Calculate result
- **.**: Decimal point

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers

## Development

### Backend (Python/Flask)
- Location: `calculatoronline.py`
- Port: 5000 (development), 80 (production with gunicorn)
- Logging: `calculator.log` and console

### Frontend (HTML/CSS/JavaScript)
- Location: `templates/index.html`
- No external dependencies (vanilla JavaScript)
- Responsive CSS Grid layout

## Troubleshooting

### "Invalid expression" error
- Check for incomplete operations (e.g., `5+`)
- Ensure only allowed characters are used
- Verify expression length is under 200 characters

### "Division by zero"
- Cannot divide by zero; use a non-zero divisor

### Port already in use
- Change `PORT` environment variable: `$env:PORT=8000; python calculatoronline.py`

## License

This project is provided as-is for educational and personal use.
