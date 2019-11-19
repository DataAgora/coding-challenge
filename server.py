from github import Github, GithubException
import uuid
import os
import base64
from flask import Flask, request, render_template
import boto3


GITHUB_USERNAME = os.environ["GITHUB_USERNAME"]
GITHUB_PASSWORD = os.environ["GITHUB_PASSWORD"]
g = Github(GITHUB_USERNAME, GITHUB_PASSWORD)

dynamodb = boto3.resource('dynamodb', region_name='us-west-1')
table = dynamodb.Table('CandidateAuth')

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template("index.html")

@app.route('/challenge', methods = ["POST", "GET"])
def challenge():
    keys = ["name", "uuid", "github_username"]
    if any([key not in request.form for key in keys]):
        return render_template("index.html")

    candidate_name = request.form["name"]
    github_username = request.form["github_username"]
    user_id = request.form["uuid"]

    try:
        _validate_user_id(user_id)
    except Exception as e:
        error_message = str(e)
        return render_template("error.html", error=error_message)

    user = g.get_user()
    
    repo_name = str(uuid.uuid4()) + "-" + candidate_name
    repo = user.create_repo(repo_name, private=True)
    repo_contents_path = "repo_contents"
    files = os.listdir(repo_contents_path)
    for file in files:
        full_path = os.path.join(repo_contents_path, file)
        with open(full_path, 'r') as f:
            content = f.read()
            repo.create_file(file, 'Adding file: ' + file, content)

    try:
        repo.add_to_collaborators(github_username, "push")
    except GithubException as e:
        repo.delete()
        error_message = "Authorization failed due to invalid Github username!"
        return render_template("error.html", error=error_message)

    

    # repo.add_to_collaborators(github_username, "push")

    return 

def _validate_user_id(user_id):
    response = table.get_item(
        Key={
            "uuid": user_id,
        }
    )

    if "Item" not in response:
        raise Exception("Authorization failed due to invalid UUID! UUID not recognized.")

    item = response["Item"]
    if item["status"]:
        raise Exception("Authorization failed due to invalid UUID! UUID already used.")

def _invalidate_user_id(user_id):
    table.update_item(
        Key={
            'uuid': user_id,
        },
        UpdateExpression='SET status = :val1',
        ExpressionAttributeValues={
            ':val1': True
        }
    )

if __name__ == '__main__':
    app.run()
