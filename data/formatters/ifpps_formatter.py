input_path = 'ifpps.dat'
out_data_path = 'ifpps_formatted.dat'
out_settings_path = 'gnuplot_header.txt'

# 1:unixtime 
init_unix_time = None

with open(input_path) as fp_in, \
    open(out_data_path, "w") as fp_data_out, \
    open(out_settings_path, "w") as fp_settings_out:
    
        # fp_settings_out.write('replot "ifpps_formatted.dat" using 1:3 title "rx-pkts-per-t" with lines\r\n')
        # fp_settings_out.write('replot "ifpps_formatted.dat" using 1:11 title "tx-pkts-per-t" with lines\r\n')

        # fp_settings_out.write('replot "ifpps_formatted.dat" using 1:5 title "rx-errors-per-t" with lines\r\n')
        # fp_settings_out.write('replot "ifpps_formatted.dat" using 1:13 title "tx-errors-per-t" with lines\r\n')

        # fp_settings_out.write('replot "ifpps_formatted.dat" using 1:9 title "rx-errors" with lines\r\n')
        # fp_settings_out.write('replot "ifpps_formatted.dat" using 1:17 title "tx-errors" with lines\r\n')

        # fp_data_out.write('replot "ifpps_formatted.dat" using 1:4 title "rx-drops-per-t" with lines\r\n')
        # fp_data_out.write('replot "ifpps_formatted.dat" using 1:12 title "tx-drops-per-t" with lines\r\n')

        # fp_settings_out.write('replot "ifpps_formatted.dat" using 1:7 title "rx-pkts" with lines\r\n')
        # fp_settings_out.write('replot "ifpps_formatted.dat" using 1:15 title "tx-pkts" with lines\r\n')

        fp_data_out.write('replot "ifpps_formatted.dat" using 1:8 title "rx-drops" with lines\r\n')
        fp_data_out.write('replot "ifpps_formatted.dat" using 1:16 title "tx-drops" with lines\r\n')

        # fp_settings_out.write('replot "ifpps_formatted.dat" using 1:6 title "rx-bytes" with lines\r\n')
        # fp_settings_out.write('replot "ifpps_formatted.dat" using 1:14 title "tx-bytes" with lines\r\n')

        fp_data_out.write('replot "ifpps_formatted.dat" using 1:10 title "tx-bytes-per-t" with lines\r\n')

        # skipping header
        for x in range(0, 5):
            fp_in.readline()

        line = fp_in.readline()
        init_unix_time = line.split()[0]

        while line:
        
            fp_data_out.write(line)

            # line = line.split()
            
            # line[0] = str(int(line[0]) - int(init_unix_time))
            # line_str = ' '.join(line)
            # fp_data_out.write(line_str + '\r\n')

            line = fp_in.readline()
'''
