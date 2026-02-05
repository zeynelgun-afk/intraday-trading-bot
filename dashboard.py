from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
import logging
import threading
import time

# Flask & SocketIO Setup
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Global State (Main bot updates this)
bot_state = {
    "status": "Starting...",
    "balance": 0.0,
    "positions": [],
    "last_update": "",
    "market_active": False
}

def update_dashboard_state(new_state):
    """Called by main bot to push updates to UI"""
    global bot_state
    bot_state.update(new_state)
    socketio.emit('state_update', bot_state)

class DashboardLogHandler(logging.Handler):
    """Custom Log Handler to stream logs to WebSocket"""
    def emit(self, record):
        log_entry = self.format(record)
        socketio.emit('new_log', {'message': log_entry, 'level': record.levelname})

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/api/status')
def get_status():
    return jsonify(bot_state)

def run_dashboard():
    """Starts the Flask server"""
    socketio.run(app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)
