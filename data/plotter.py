import os
import sys
script_path = os.path.dirname(__file__)
sys.path.append(os.path.join(script_path, 'utils'))

logs_folder_path = os.path.join(script_path, 'logs')
plots_folder_path = os.path.join(script_path, 'plots')

def plot(plot_type, query, gnuplot_headers, columns_filter):
    # data_file = plot_type + ".dat"
    plot_file = plot_type + ".plot"
    # client_input_path = os.path.join(logs_folder_path, query, "java.log")
    # server_input_path = os.path.join(plots_folder_path, query, "data", data_file)
    output_path = os.path.join(plots_folder_path, query, plot_file)

    with open(output_path, "w") as fp_out:

        # Gnuplot headers
        for header in gnuplot_headers:
            fp_out.write(header + '\n')

        for col_filter in columns_filter:
            cols = '1:' + str(5 + col_filter[0]) + ' '
            fp_out.write('replot "' + plot_type + '_merged.dat" using ' + cols + 'title "' + col_filter[1] + '" with lines\n')
            # if col_filter[0] <= 1:
                # fp_out.write('plot "' + plot_type + '.plot" using ' + cols + 'title "' + col_filter[1] + '" with lines\n')
            # else:
            #     fp_out.write('replot "' + plot_type + '.plot" using ' + cols + 'title "' + col_filter[1] + '" with lines\n')
