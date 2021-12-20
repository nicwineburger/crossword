#!/usr/bin/env python

# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Lambda intended to be containerized.
"""

import os
import subprocess
import sys
import json

# Filename for stats CSV file on local fileystem
LOCAL_CSV_FILENAME = "/tmp/data.csv"

# date example: "2021-11-01"
def update_csv(auth_key, earliest_date):
    print("running rust!")
    subprocess.run(["crossword", "--start-date", earliest_date, "-t", auth_key, LOCAL_CSV_FILENAME], check=True)
    print("done running rust!")

def reset_csv():
    print('resetting csv')
    try:
        os.remove(LOCAL_CSV_FILENAME)
    except OSError:
        pass
    open(LOCAL_CSV_FILENAME, "a").close()

def update_database(auth_key, earliest_date):
    reset_csv()
    update_csv(auth_key, earliest_date)
    with open(LOCAL_CSV_FILENAME, 'r') as csv:
        return { "content": csv.read() }

def message(message_in):
    return { "message": message_in }

def lambda_handler(event, context):
    try:
        print('Hello from AWS Lambda using Python' + sys.version + '!')

        body = event.get('body', None)
        if not body:
            return message("no body available")
        body_json = json.loads(body)
        auth_key = body_json.get('auth_key', None)
        earliest_date = body_json.get('earliest_date', None)
        if not auth_key or not earliest_date:
            return message("auth key or date not provided")

        return update_database(auth_key, earliest_date)
    except Exception as e:
        print("encountered error: " + str(e))
        return message("sorry, something went wrong")
