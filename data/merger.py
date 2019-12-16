import os
import sys
script_path = os.path.dirname(__file__)
sys.path.append(os.path.join(script_path, 'utils'))
from utils import plot_type

logs_folder_path = os.path.join(script_path, 'logs')
plots_folder_path = os.path.join(script_path, 'plots')

def merge(plot_type, query):

    init_unix_time = None
    data_file = plot_type + ".dat"
    plot_file = plot_type + "_merged.dat"
    client_input_path = os.path.join(logs_folder_path, query, "java.log")
    server_input_path = os.path.join(plots_folder_path, query, "data", data_file)
    output_path = os.path.join(plots_folder_path, query, plot_file)

    with open(client_input_path) as fp_client_in, \
        open(server_input_path) as fp_server_in, \
        open(output_path, "w") as fp_out:

        # files lines into arrays
        client_lines = fp_client_in.read().splitlines()
        server_lines = fp_server_in.read().splitlines()

        # syncing starting point
        client_idx = 0
        server_idx = 0
        curr_client_time = int(client_lines[client_idx].split()[0])
        curr_server_time = int(server_lines[server_idx].split()[0])
        while curr_client_time != curr_server_time:
            if curr_client_time < curr_server_time:
                client_idx = client_idx + 1
                curr_client_time = int(client_lines[client_idx].split()[1])
            elif curr_client_time > curr_server_time:
                server_idx = server_idx + 1
                curr_server_time = int(server_lines[server_idx].split()[0])
        init_unix_time = curr_client_time

        # ===========
        # MERGING
        # ===========

        for client_line_idx in range((len(client_lines) - 1) - client_idx):
            current_client_line = client_lines[client_idx + client_line_idx]
            current_server_line = server_lines[server_idx]

            # removing initial timestamps
            current_client_line_list = current_client_line.split()
            current_server_line_list = current_server_line.split()
            current_client_line_time = current_client_line_list[1]
            current_server_line_time = current_server_line_list[0]
            del current_client_line_list[0:1]
            del current_server_line_list[0]

            current_client_line = ' '.join(current_client_line_list)
            current_server_line = ' '.join(current_server_line_list)

            # matching server time to client time
            while current_client_line_time > current_server_line_time:
                # server measurement cannot be ahead of client
                if (server_idx + 1) >= len(server_lines) or server_lines[server_idx + 1] > current_client_line_time:
                    break
                server_idx = server_idx + 1

            merged_line = str(client_line_idx) + ' ' + current_client_line + ' ' + current_server_line + '\n'
            fp_out.write(merged_line)
    return
