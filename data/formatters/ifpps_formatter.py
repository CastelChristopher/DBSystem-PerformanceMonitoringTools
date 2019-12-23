import re
import os
import calendar
import datetime
dict((v, k) for k, v in enumerate(calendar.month_abbr))

script_dir = os.path.dirname(__file__)

def format(log_folder, plot_folder):

    in_file = os.path.join(script_dir, "..", log_folder, "ifpps.log")
    out_file = os.path.join(script_dir, "..", plot_folder, "ifpps.dat")

    with open(in_file) as fp_in, \
            open(out_file, "w") as fp_out:
        lines = fp_in.read().splitlines()
        idx = 5  # skipping headers
        while idx < len(lines):
            fp_out.write(lines[idx] + '\n')
            idx = idx + 1
    return
