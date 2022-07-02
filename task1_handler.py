"""
handler(input: dict, context: object) -> dict[str, Any]

"""

mydict = {
    "cpu_percent-1": 10,
    "cpu_percent-2": 15,
    "cpu_percent-3": 18,
    "n_pids": 4
}

context_dict = {
    "env": {
        "60-cpu_percent-1": 10,
        "1-cpu_percent-1": 10,
        "60-cpu_percent-2": 10,
        "1-cpu_percent-2": 10,
        "60-cpu_percent-1": 10,
        "1-cpu_percent-1": 10,
        "60-n-pids": 15
    }
}

def handler(input, context):
    output = {}
    if (not context["env"].has_key("n_cpus")):
        # First run, must populate 'env' dictionary
        
        # Find all cpu_percent-X, i.e. find how many CPUs are there
        keys = input.keys()
        result = [i for i in keys if i.startswith("cpu_percent")]
        context["env"]["n_cpus"] = result.size()
        
        # Store current averages in 'env' for later
        context["env"]["60-cpu_percent-1"] = input["cpu_percent-1"]
        
        # TODO: moving average
        output["avg-util-cpu1-60sec"] = input["cpu_percent-1"]
    else:
        output["avg-util-cpu1-60sec"] = input["cpu_percent-1"]
    return output
    
    
    # Read data from input
    

    # Update moving averages


    # Build response dictionary
    pass


if __name__ == "__main__":
    handler(mydict ,context_dict)