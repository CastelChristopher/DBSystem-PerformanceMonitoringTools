import re
import os
import calendar
import datetime
dict((v, k) for k, v in enumerate(calendar.month_abbr))

script_dir = os.path.dirname(__file__)

def format(log_folder, plot_folder):
    in_file = os.path.join(script_dir, "..", log_folder, "java.log")
    out_file = os.path.join(script_dir, "..", plot_folder, "data", "java.dat")

    with open(in_file) as fp_in, open(out_file, "w") as fp_out:
        lines = fp_in.read().splitlines()
        response_times = [float(i.split()[2]) for i in lines]
        min_time = str(min(response_times))
        max_time = str(max(response_times))
        for line in lines:
            fp_out.write(line + ' ' + min_time  + ' ' + max_time + '\n')
    return
