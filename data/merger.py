import os

input_server_data_path = 'ifpps_formatted.dat'
input_server_settings_path = 'gnuplot_header.txt'
input_client_path = 'java.log'
output_path = 'merged.dat'

# 1:unixtime
init_unix_time = None

with open(input_server_data_path) as fp_server_data_in, \
        open(input_server_settings_path) as fp_server_settings_in, \
        open(input_client_path) as fp_client_in, \
        open(output_path, "w") as fp_out:

    # ===========
    # FORMATTING INPUT
    # ===========

    client_lines = fp_client_in.read().splitlines()
    server_data_lines = fp_server_data_in.read().splitlines()
    server_settings_lines = fp_server_settings_in.read().splitlines()

    client_init_time = server_data_lines[0].split()[0]
    server_init_time = client_lines[0].split()[0]

    # syncing starting point
    client_idx = 0
    server_idx = 0
    curr_client_time = int(client_lines[client_idx].split()[0])
    curr_server_time = int(server_data_lines[server_idx].split()[0])
    while curr_client_time != curr_server_time:
        if curr_client_time < curr_server_time:
            client_idx = client_idx + 1
            curr_client_time = int(client_lines[client_idx].split()[1])
        elif curr_client_time > curr_server_time:
            server_idx = server_idx + 1
            curr_server_time = int(server_data_lines[server_idx].split()[0])
    init_unix_time = curr_client_time

    fp_out.write('set xlabel "Queries"\n')
    # fp_out.write('set ylabel "???"\n')
    fp_out.write('plot "merged.dat" using 1:2 title "Response time" with lines\n')

    for i in range(len(server_settings_lines)):
        fp_out.write(server_settings_lines[i] + '\n')

    # ===========
    # MERGING
    # ===========

    for client_line_idx in range((len(client_lines) - 1) - client_idx):
        current_client_line = client_lines[client_idx + client_line_idx]
        current_server_line = server_data_lines[server_idx]

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
            # server measure cannot be ahead of client
            if server_data_lines[server_idx + 1] > current_client_line_time:
                break
            server_idx = server_idx + 1

        merged_line = str(client_line_idx) + ' ' + current_client_line + ' ' + current_server_line + '\n'
        fp_out.write(merged_line)
