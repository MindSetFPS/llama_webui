from flask import Flask, request, render_template
import threading
from flask_socketio import SocketIO, emit, send
from example import generator
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

def generate_text(
    prompt: str,
    temperature: float = 0.8,
    top_p: float = 0.95,
    max_seq_len: int = 10
):
    results = generator.generate(
        prompt, max_gen_len=max_seq_len, temperature=temperature, top_p=top_p
    )

    for result in results:
        print("\n==================================\n")
        print(result)
        print("\n==================================\n")
        emit('response', result)

print('listening')
@app.route('/', methods=['get'])
def get_handler():
    return render_template('index.html')

@socketio.on('connect')
def test_connect():
    print('Client connected')

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

@socketio.on('message')
def handle_message(message):
    print('Received message: ' + message)
    generate_text(prompt=[message])
    emit('response', 'Server received message: ' + message)

@app.route('/', methods=['POST'])
def post_handler():
    # Get the request data
    data = request.json
    
    # Process the data as needed
    # processed_data = process_data(data)
    
    # Return a response
    return {'result': 'welcome'}

def process_data(data):
    # Do something with the data, e.g. return its length
    return len(data)

if __name__ == '__main__':
    app.run()
