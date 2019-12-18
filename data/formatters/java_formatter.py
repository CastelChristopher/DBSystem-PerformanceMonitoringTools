import re
import os
import calendar
import datetime
dict((v, k) for k, v in enumerate(calendar.month_abbr))

script_dir = os.path.dirname(__file__)


def format(log_folder, plot_folder):
    in_file = os.path.join(script_dir, "..", log_folder, "java.log")
    out_file = os.path.join(script_dir, "..", "plots", "java.dat")

    with open(in_file) as fp_in, open(out_file, "a+") as fp_out:
        lines = fp_in.read().splitlines()

        idx = 10
        response_times = []
        while idx < len(lines) - 1:
            response_times.append(float(lines[idx].split()[2]))
            idx = idx + 1

        min_time = str(min(response_times))
        max_time = str(max(response_times))
        sum_time = sum(response_times)
        avg_time = str(sum_time / len(response_times))
        # for line in lines:
        #     fp_out.write(line + ' ' + min_time  + ' ' + max_time + '\n')
        fp_out.write(log_folder + ' -> ' + avg_time + ' ' + min_time + ' ' + max_time + '\n')
    return
