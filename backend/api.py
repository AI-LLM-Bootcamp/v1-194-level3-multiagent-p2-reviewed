from flask import Flask, jsonify, request, abort
from uuid import uuid4
from threading import Thread

app = Flask(__name__)

def kickoff_crew(input_id, technologies: list[str], businessareas: list[str]):
    print(f"Running crew for {input_id} with technologies {technologies} and businessareas {businessareas}")
    
    # TODO: SETUP THE CREW HERE

    # TODO: RUN THE CREW HERE
    
    # TODO: LET APP KNOW WE ARE DONE

@app.route('/api/multiagent', methods=['POST'])
def run_crew():
    data = request.json
    if not data or 'technologies' not in data or 'businessareas' not in data:
        abort(400, description="Invalid request with missing data.")
 
    input_id = str(uuid4())
    technologies = data['technologies']
    businessareas = data['businessareas']
    
    thread = Thread(target=kickoff_crew, args=(input_id, technologies, businessareas))
    thread.start()
    
    # return jsonify({"status": "success"}), 200
    return jsonify({"input_id": input_id}), 200


@app.route('/api/multiagent/<input_id>', methods=['GET'])
def get_status(input_id):
    return jsonify({
        "status": f"Getting status for {input_id}"
        }), 200

if __name__ == '__main__':
    app.run(debug=True, port=3001)