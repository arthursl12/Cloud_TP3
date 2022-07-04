"""
handler(input: dict, context: object) -> dict[str, Any]

"""

def handler(input, context):
    def mean(lst):
        total = 0
        for x in lst:
            total += x
        return total / len(lst)
    
    output = {}
    if ("n_cpus" not in context.env):
        # First run, must populate 'env' dictionary

        # Find all cpu_percent-X, i.e. find how many CPUs are there
        keys = input.keys()
        result = [i for i in keys if i.startswith("cpu_percent")]
        n_cpus = len(result)
        context.env["n_cpus"] = n_cpus
    
        # Store current averages in 'env' for later
        for i in range(n_cpus):
            n = i+1
            context.env[f"60-cpu_percent-{n}"] = [input[f"cpu_percent-{n}"]]
            context.env[f"1h-cpu_percent-{n}"] = [input[f"cpu_percent-{n}"]]
    else:
        # Just add the current readings
        n_cpus = context.env["n_cpus"]
        for i in range(n_cpus):
            n = i+1
            # Append the new reading
            context.env[f"60-cpu_percent-{n}"].append(input[f"cpu_percent-{n}"])
            context.env[f"1h-cpu_percent-{n}"].append(input[f"cpu_percent-{n}"])
            
            # Remove the first one, i.e., 
            # taking only the necessary for current rolling average
            context.env[f"60-cpu_percent-{n}"][-60//5:]
            context.env[f"1h-cpu_percent-{n}"][-3600//5:]
            
    # Compute moving average
    for i in range(n_cpus):
        n = i+1
        output[f"avg-util-cpu{n}-60sec"] = mean(context.env[f"60-cpu_percent-{n}"])
        output[f"avg-util-cpu{n}-1h"] = mean(context.env[f"1h-cpu_percent-{n}"])
    return output


if __name__ == "__main__":
    handler(mydict ,context_dict)