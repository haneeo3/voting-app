from flask import Flask, render_template, request, jsonify
import json
import boto3

app = Flask(__name__, template_folder='../templates')

# Connect to LocalStack S3
s3 = boto3.client(
    's3',
    endpoint_url='http://localhost:4566',
    aws_access_key_id='test',
    aws_secret_access_key='test',
    region_name='us-east-1'
)

BUCKET = 'voting-app'
VOTES_FILE = 'votes.json'

def get_votes():
    try:
        obj = s3.get_object(Bucket=BUCKET, Key=VOTES_FILE)
        return json.loads(obj['Body'].read())
    except:
        return {"Python": 0, "JavaScript": 0, "Terraform": 0, "Docker": 0}

def save_votes(votes):
    s3.put_object(Bucket=BUCKET, Key=VOTES_FILE, Body=json.dumps(votes))

@app.route('/')
def index():
    votes = get_votes()
    return render_template('index.html', votes=votes)

@app.route('/vote', methods=['POST'])
def vote():
    choice = request.json.get('choice')
    votes = get_votes()
    if choice in votes:
        votes[choice] += 1
        save_votes(votes)
        return jsonify({"success": True, "votes": votes})
    return jsonify({"success": False})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
