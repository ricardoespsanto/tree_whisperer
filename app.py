from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import logging
import json
from datetime import datetime
from typing import Dict, List

from config import Config
from ai_sql_generator import AISQLGenerator
from database_connection import DatabaseConnection
from rate_limiter import RateLimiter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('tree_whisperer.log'),
        logging.StreamHandler()
    ]
)

app = Flask(__name__)
app.config['SECRET_KEY'] = Config.SECRET_KEY
CORS(app)

# Initialize components
ai_generator = AISQLGenerator()
rate_limiter = RateLimiter()

# Store conversation history (in production, use Redis or database)
conversation_history = {}

@app.route('/')
def index():
    """Serve the main chat interface"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages and generate responses"""
    try:
        data = request.get_json()
        question = data.get('question', '').strip()
        user_id = data.get('user_id', 'anonymous')
        session_id = data.get('session_id', 'default')

        if not question:
            return jsonify({
                'success': False,
                'error': 'No question provided',
                'response': None
            }), 400

        # Check rate limiting
        is_allowed, rate_message = rate_limiter.check_rate_limit(user_id)
        if not is_allowed:
            return jsonify({
                'success': False,
                'error': rate_message,
                'response': None
            }), 429

        # Get conversation history for context
        history_key = f"{user_id}_{session_id}"
        conversation = conversation_history.get(history_key, [])

        # Generate SQL query
        sql_result = ai_generator.generate_sql(question, conversation)

        if not sql_result['success']:
            # Add to conversation history
            conversation.append({'role': 'user', 'content': question})
            conversation.append({'role': 'assistant', 'content': sql_result['error']})
            conversation_history[history_key] = conversation[-10:]  # Keep last 10 messages

            return jsonify({
                'success': False,
                'error': sql_result['error'],
                'response': sql_result['error'],
                'sql': None,
                'explanation': sql_result.get('explanation')
            })

        # Execute SQL query
        try:
            with DatabaseConnection() as db:
                query_results = db.execute_query(sql_result['sql'])

                # Format response
                response = ai_generator.format_response(question, query_results, sql_result['explanation'])

                # Add to conversation history
                conversation.append({'role': 'user', 'content': question})
                conversation.append({'role': 'assistant', 'content': response})
                conversation_history[history_key] = conversation[-10:]  # Keep last 10 messages

                return jsonify({
                    'success': True,
                    'response': response,
                    'sql': sql_result['sql'],
                    'explanation': sql_result['explanation'],
                    'data': query_results,
                    'error': None
                })

        except Exception as db_error:
            logging.error(f"Database error: {str(db_error)}")
            return jsonify({
                'success': False,
                'error': f'Database error: {str(db_error)}',
                'response': 'I encountered an error while querying the database. Please try again.',
                'sql': sql_result['sql'],
                'explanation': sql_result['explanation']
            }), 500

    except Exception as e:
        logging.error(f"Unexpected error in chat endpoint: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'An unexpected error occurred',
            'response': 'I encountered an unexpected error. Please try again.',
            'sql': None,
            'explanation': None
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        # Test database connection
        with DatabaseConnection() as db:
            db.test_connection()

        # Get usage stats
        usage_stats = rate_limiter.get_usage_stats()

        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'database': 'connected',
            'usage_stats': usage_stats
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'timestamp': datetime.now().isoformat(),
            'error': str(e)
        }), 500

@app.route('/api/usage', methods=['GET'])
def get_usage():
    """Get current usage statistics"""
    try:
        stats = rate_limiter.get_usage_stats()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/schema', methods=['GET'])
def get_schema():
    """Get database schema information"""
    try:
        with DatabaseConnection() as db:
            schema_info = db.get_table_info()
        return jsonify(schema_info)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Test database connection on startup
    try:
        with DatabaseConnection() as db:
            if db.test_connection():
                logging.info("Database connection test successful")
            else:
                logging.error("Database connection test failed")
    except Exception as e:
        logging.error(f"Failed to connect to database: {e}")

    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )
