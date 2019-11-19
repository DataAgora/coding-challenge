from github import Github, GithubException
import uuid
import os
import base64
from flask import Flask, request, render_template
import boto3

GITHUB_USERNAME = os.environ["GITHUB_USERNAME"]
GITHUB_PASSWORD = os.environ["GITHUB_PASSWORD"]
g = Github(GITHUB_USERNAME, GITHUB_PASSWORD)

user = g.get_user()
repo_name = "coding-challenge"
repo = user.get_repo(repo_name)
try:
    repo.add_to_collaborators("neeleshdodda44", "admin")
except GithubException as e:
    print("YAY")
    print(e)