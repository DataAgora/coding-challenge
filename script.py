import os
import boto3

os.system('pytest test.py > output.txt')

with open('output.txt', 'r') as f:
    output = f.readlines()[5].split()[1]
    print(output)
    num_passed = len([result for result in output if result == '.'])
    print("Num passed: ", num_passed)
    print("Num failed: ", len(output) - num_passed)
    
    