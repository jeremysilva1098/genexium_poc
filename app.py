from flask import Flask, render_template, request, jsonify, Response
from research_agent import ResearchAgent
import os
from functools import wraps

app = Flask(__name__)

# Password for the app (you can change this or set via environment variable)
APP_PASSWORD = os.environ.get('APP_PASSWORD')

# Available genes based on the docs directory
AVAILABLE_GENES = ['actn3', 'ppargc1a', 'adrb2', 'nos3']

def check_auth(username, password):
    """Check if a username/password combination is valid."""
    return username == 'admin' and password == APP_PASSWORD

def authenticate():
    """Sends a 401 response that enables basic auth."""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route('/')
@requires_auth
def index():
    return render_template('index.html', genes=AVAILABLE_GENES)

@app.route('/generate_plan', methods=['POST'])
@requires_auth
def generate_plan():
    try:
        data = request.get_json()
        gene_string = data.get('gene')
        goal = data.get('goal')
        
        if not gene_string or not goal:
            return jsonify({'error': 'Both gene and goal are required'}), 400
        
        if gene_string not in AVAILABLE_GENES:
            return jsonify({'error': 'Invalid gene selected'}), 400
        
        # Initialize the research agent
        research_agent = ResearchAgent(doc_load_strat='server')

        # Generate the training plan
        training_plan, research_report = research_agent.build_training_plan(goal=goal, gene_string=gene_string)
        
        return jsonify({
            'success': True,
            'training_plan': training_plan,
            'gene': gene_string,
            'goal': goal,
            'research_report': research_report
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate_daily_workout', methods=['POST'])
@requires_auth
def generate_daily_workout():
    try:
        data = request.get_json()
        training_plan = data.get('training_plan')
        week_number = data.get('week_number')
        day_of_week = data.get('day_of_week')
        hrv = data.get('hrv')
        resting_heart_rate = data.get('resting_heart_rate')
        hours_of_sleep = data.get('hours_of_sleep')

        if not training_plan or not week_number or not day_of_week:
            return jsonify({'error': 'Training plan, week number, and day of week are required'}), 400
        
        # Initialize the research agent
        research_agent = ResearchAgent(doc_load_strat='server')

        # Generate the daily workout with health metrics
        daily_workout = research_agent.generate_daily_workout(
            training_plan=training_plan, 
            week_number=week_number, 
            day_of_week=day_of_week,
            hrv=hrv,
            resting_heart_rate=resting_heart_rate,
            hours_of_sleep=hours_of_sleep
        )

        return jsonify({
            'success': True,
            'daily_workout': daily_workout
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=False, host='0.0.0.0', port=port) 