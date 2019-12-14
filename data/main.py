import os
import sys
sys.path.append('formatters')
import pidstat_formatter
import perf_formatter

logs_folder_path = "logs"
plots_folder_path = "plots"

logs_files = os.listdir(logs_folder_path)
plots_files = os.listdir(plots_folder_path)

# building "to format" list
todo_list = ["select_1000"]
for index, item in enumerate(logs_files):
    if item not in plots_files:
        todo_list.append(item)

# ======================
#   FORMATTERS
# ======================

for idx, query in enumerate(todo_list):
    log_folder = os.path.join(logs_folder_path, query)
    plot_folder = os.path.join(plots_folder_path, query)
    plot_data_folder = os.path.join(plots_folder_path, query, "data")

    os.mkdir(plot_folder)
    os.mkdir(plot_data_folder)
    # perf_formatter.format(log_folder, plot_folder)
    # pidstat_formatter.format(log_folder, plot_folder)

# ======================
#   MERGERS / PLOTTERS
# ======================
