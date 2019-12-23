import re
import os
import calendar
import datetime
dict((v, k) for k, v in enumerate(calendar.month_abbr))

script_dir = os.path.dirname(__file__)

def format(log_folder, plot_folder):

    in_file = os.path.join(script_dir, "..", log_folder, "perf.log")
    out_file = os.path.join(script_dir, "..", plot_folder, "perf.dat")

    with open(in_file) as fp_in, \
            open(out_file, "w") as fp_out:

        lines = fp_in.read().splitlines()

        init_timestamp = lines[0]
        init_timestamp = init_timestamp.replace('# started on ', '')
        init_timestamp = init_timestamp.split()
        # year, month, day, hour, minute, second
        year = int(init_timestamp[4])
        month = list(calendar.month_abbr).index(init_timestamp[1])
        day = int(init_timestamp[2])
        time = init_timestamp[3].split(':')
        init_timestamp = datetime.datetime(year, month, day, int(time[0]), int(time[1]), int(time[2])).timestamp()
        init_timestamp = str(init_timestamp).split('.')
        init_timestamp = int(init_timestamp[0])

        idx = 3  # skipping headers
        timestamp = None
        tokens_out = []
        while idx < len(lines):
            # lines are printed by group of 3
            is_start = idx % 3 == 0
            # line is not a comment/empty
            if len(lines[idx]) > 0 and lines[idx].find('#') != 0:
                line_tokens = lines[idx].split()
                if is_start:
                    timestamp = line_tokens[0]
                    timestamp = timestamp.split('.')[0]
                    timestamp = init_timestamp + int(timestamp)
                del line_tokens[0]
                del line_tokens[1:]
                token_out = line_tokens[0].replace(',', '')
                tokens_out.append(token_out)

            idx = idx + 1
            line_out = ''
            if (idx % 3 == 0):  # next line is the start of a new group
                line_out = str(timestamp) + ' ' + ' '.join(tokens_out)
                tokens_out = []
                fp_out.write(line_out + '\n')
    return
