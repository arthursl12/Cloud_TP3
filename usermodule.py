def handler(input, context):
    def mean(lst):
        total = 0
        for x in lst:
            total += x
        return total / len(lst)

    output = {}
    #print(input)
    if ("n_cpus" not in context.env):
        # First run, must populate 'env' dictionary

        # Find all cpu_percent-X, i.e. find how many CPUs are there
        keys = input.keys()
        result = [i for i in keys if i.startswith("cpu_percent")]
        n_cpus = len(result)
        context.env["n_cpus"] = n_cpus

        # Store current averages in 'env' for later
        for i in range(n_cpus):
            context.env[f"60-cpu_percent-{i}"] = [input[f"cpu_percent-{i}"]]
            context.env[f"1h-cpu_percent-{i}"] = [input[f"cpu_percent-{i}"]]
            
        # Other metric: virtual memory used in the last 60s
        context.env[f"60-virtual_memory-percent"] = [input[f"virtual_memory-percent"]]
    else:
        # Just add the current readings
        n_cpus = context.env["n_cpus"]
        for i in range(n_cpus):
            # Append the new reading
            context.env[f"60-cpu_percent-{i}"].append(input[f"cpu_percent-{i}"])
            context.env[f"1h-cpu_percent-{i}"].append(input[f"cpu_percent-{i}"])

            # Remove the first one, i.e.,
            # taking only the necessary for current rolling average
            context.env[f"60-cpu_percent-{i}"][-60//5:]
            context.env[f"1h-cpu_percent-{i}"][-3600//5:]
        
        # Add readings for memory used
        context.env[f"60-virtual_memory-percent"].append(input[f"virtual_memory-percent"])
        context.env[f"60-virtual_memory-percent"][-60//5:]

    # Compute moving average
    for i in range(n_cpus):
        output[f"avg-util-cpu{i}-60sec"] = mean(context.env[f"60-cpu_percent-{i}"])
        output[f"avg-util-cpu{i}-1h"] = mean(context.env[f"1h-cpu_percent-{i}"])
    output[f"avg-util-memory-60sec"] = mean(context.env[f"60-virtual_memory-percent"])
        
    return output