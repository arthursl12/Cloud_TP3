import os
import json
import redis
import time
from datetime import datetime

import usermodule

# Get variables set by deployment and setup redis connection
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT"))
REDIS_INPUT_KEY = os.getenv("REDIS_INPUT_KEY")
REDIS_OUTPUT_KEY = os.getenv("REDIS_OUTPUT_KEY")
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)

# Define interval between calls, in seconds
STEP = 5

class Context:
    """
    Context object used by handler function
    
    Attributes:
    host: Hostname of the server running Redis.
    port: Port where the Redis server is listening.
    input_key: Input key used to read monitoring data from Redis.
    output_key: Output key used to store metrics on Redis.
    function_getmtime: Timestamp of the last update to your module's Python 
                       file.
    last_execution: Timestamp of last execution of your serverless function and 
                    result storage on Redis.
    env: A JSON-encodable dictionary that persists between calls to the your 
         serverless function. This variable can be used to persist small amounts
         of user data (context environment) between executions
    """
    
    def __init__(self):
        self.host = REDIS_HOST
        self.port = REDIS_PORT
        self.input_key = REDIS_INPUT_KEY
        self.output_ket = REDIS_OUTPUT_KEY
        self.last_execution = ""
        self.env = {}
        
        # Getting last modified time
        tmstmp = os.path.getmtime("usermodule.py")
        self.function_getmtime = datetime.fromtimestamp(tmstmp)
    
    def update_execution(self):
        self.last_execution = datetime.now()

def main():
    ctx = Context()
    last_data = None
    data = None
    while(1):
        # Read data from redis 
        r_dict = r.get(REDIS_INPUT_KEY)
        r_dict = json.loads(r_dict)
        
        last_data = data
        data = r_dict
        
        # Call handler to update the differences, if any
        if (last_data != data):
            output = usermodule.handler(data, ctx)
            r.set(REDIS_OUTPUT_KEY, json.dumps(output))
            ctx.update_execution()
        time.sleep(STEP)

# Write back on redis
if __name__ == "__main__":
    main()


