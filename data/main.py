import os
import sys
from enum import Enum
script_path = os.path.dirname(__file__)
sys.path.append(os.path.join(script_path, 'formatters'))
sys.path.append(os.path.join(script_path, 'utils'))
from utils import plot_type
from formatters import ifpps_formatter
from formatters import perf_formatter
from formatters import pidstat_formatter
import merger
import plotter

logs_folder_path = os.path.join(script_path, 'logs')
plots_folder_path = os.path.join(script_path, 'plots')

logs_folders = os.listdir(logs_folder_path)
plots_folders = os.listdir(plots_folder_path)

# builds "to format" list
todo_list = []
for index, item in enumerate(logs_folders):
    if item not in plots_folders:
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

    # formatters
    perf_formatter.format(log_folder, plot_folder)
    pidstat_formatter.format(log_folder, plot_folder)
    ifpps_formatter.format(log_folder, plot_folder)

# ======================
#   MERGERS / PLOTTERS
# ======================

gnuplot_headers = [
    'set xlabel "Queries"'
]

# PIDSTAT
# -----------------------------------------------------------------------------------------------------------
# 1 | minflt/s      minor faults (did NOT load a memory page from disk)
# 2 | majflt/s      major faults (DID load a memory page from disk)
# 3 | VSZ           KB of virtual memory used
# 4 | RSS           (KB) Resident Set Size (non-swapped physical memory used by the task)
# 5 | %MEM          % of RAM used
# 6 | kB_rd/s       KB read from disk
# 7 | kB_wr/s       KB wrote to disk
# 8 | kB_ccwr/s     KB whose writing to disk has been cancelled by the task
#   |                   (This may occur when the task truncates some dirty pagecache.
#   |                   In this case, some IO which another task has been accounted for will not be happening)
# 9 | iodelay       Block I/O delay in clock ticks.
#   |                   (Includes the delays spent waiting for sync block I/O completion
#   |                   and for swapin block I/O completion)

pidstat_col_labels = [
    (1, 'minflt/s'),
    (2, 'majflt/s'),
    (3, 'VSZ'),
    (4, 'RSS'),
    (5, '%MEM'),
    (6, 'kB_rd/s'),
    (7, 'kB_wr/s'),
    (8, 'kB_ccwr/s'),
    (9, 'iodelay')
]

FILTER_PIDSTAT_ALL = [1, 2, 3, 4, 5, 6, 7, 8, 9]

# PERF
# -----------------------------------------------------------------------------------------------------------
# 1 | cache-references
# 2 | cache-misses
# 3 | page-faults

perf_col_labels = [
    (1 , 'cache-references'),
    (2 , 'cache-misses'),
    (3 , 'page-faults')
]

FILTER_PERF_ALL = [1, 2, 3]

# IFPPS
# -----------------------------------------------------------------------------------------------------------

# 1:unixtime                  21:mem-total                    41:cpu1-sys-per-t               61:cpu3-usr-per-t
# 2:rx-bytes-per-t            22:swap-free                    42:cpu1-idle-per-t              62:cpu3-nice-per-t
# 3:rx-pkts-per-t             23:swap-used                    43:cpu1-iow-per-t               63:cpu3-sys-per-t
# 4:rx-drops-per-t            24:swap-total                   44:cpu1-net-irqs-per-t          64:cpu3-idle-per-t
# 5:rx-errors-per-t           25:procs-total                  45:cpu1-net-irqs                65:cpu3-iow-per-t
# 6:rx-bytes                  26:procs-in-run                 46:cpu1-net-rx-soft-irqs-per-t  66:cpu3-net-irqs-per-t
# 7:rx-pkts                   27:procs-in-iow                 47:cpu1-net-rx-soft-irqs        67:cpu3-net-irqs
# 8:rx-drops                  28:cpu0-usr-per-t               48:cpu1-net-tx-soft-irqs-per-t  68:cpu3-net-rx-soft-irqs-per-t
# 9:rx-errors                 29:cpu0-nice-per-t              49:cpu1-net-tx-soft-irqs        69:cpu3-net-rx-soft-irqs
# 10:tx-bytes-per-t           30:cpu0-sys-per-t               50:cpu2-usr-per-t               70:cpu3-net-tx-soft-irqs-per-t
# 11:tx-pkts-per-t            31:cpu0-idle-per-t              51:cpu2-nice-per-t              71:cpu3-net-tx-soft-irqs
# 12:tx-drops-per-t           32:cpu0-iow-per-t               52:cpu2-sys-per-t
# 13:tx-errors-per-t          33:cpu0-net-irqs-per-t          53:cpu2-idle-per-t
# 14:tx-bytes                 34:cpu0-net-irqs                54:cpu2-iow-per-t
# 15:tx-pkts                  35:cpu0-net-rx-soft-irqs-per-t  55:cpu2-net-irqs-per-t
# 16:tx-drops                 36:cpu0-net-rx-soft-irqs        56:cpu2-net-irqs
# 17:tx-errors                37:cpu0-net-tx-soft-irqs-per-t  57:cpu2-net-rx-soft-irqs-per-t
# 18:context-switches-per-t   38:cpu0-net-tx-soft-irqs        58:cpu2-net-rx-soft-irqs
# 19:mem-free                 39:cpu1-usr-per-t               59:cpu2-net-tx-soft-irqs-per-t
# 20:mem-used                 40:cpu1-nice-per-t              60:cpu2-net-tx-soft-irqs

ifpps_col_labels = [
    (1, 'unixtime'),
    (2, 'rx-bytes-per-t'),
    (3, 'rx-pkts-per-t'),
    (4, 'rx-drops-per-t'),
    (5, 'rx-errors-per-t'),
    (6, 'rx-bytes'),
    (7, 'rx-pkts'),
    (8, 'rx-drops'),
    (9, 'rx-errors'),
    (10, 'tx-bytes-per-t'),
    (11, 'tx-pkts-per-t'),
    (12, 'tx-drops-per-t'),
    (13, 'tx-errors-per-t'),
    (14, 'tx-bytes'),
    (15, 'tx-pkts'),
    (16, 'tx-drops'),
    (17, 'tx-errors'),
    (18, 'context-switches-per-t'),
    (19, 'mem-free'),
    (20, 'mem-used'),
    (21, 'mem-total'),
    (22, 'swap-free'),
    (23, 'swap-used'),
    (24, 'swap-total'),
    (25, 'procs-total'),
    (26, 'procs-in-run'),
    (27, 'procs-in-iow'),
    (28, 'cpu0-usr-per-t'),
    (29, 'cpu0-nice-per-t'),
    (30, 'cpu0-sys-per-t'),
    (31, 'cpu0-idle-per-t'),
    (32, 'cpu0-iow-per-t'),
    (33, 'cpu0-net-irqs-per-t'),
    (34, 'cpu0-net-irqs'),
    (35, 'cpu0-net-rx-soft-irqs-per-t'),
    (36, 'cpu0-net-rx-soft-irqs'),
    (37, 'cpu0-net-tx-soft-irqs-per-t'),
    (38, 'cpu0-net-tx-soft-irqs'),
    (39, 'cpu1-usr-per-t'),
    (40, 'cpu1-nice-per-t'),
    (41, 'cpu1-sys-per-t'),
    (42, 'cpu1-idle-per-t'),
    (43, 'cpu1-iow-per-t'),
    (44, 'cpu1-net-irqs-per-t'),
    (45, 'cpu1-net-irqs'),
    (46, 'cpu1-net-rx-soft-irqs-per-t'),
    (47, 'cpu1-net-rx-soft-irqs'),
    (48, 'cpu1-net-tx-soft-irqs-per-t'),
    (49, 'cpu1-net-tx-soft-irqs'),
    (50, 'cpu2-usr-per-t'),
    (51, 'cpu2-nice-per-t'),
    (52, 'cpu2-sys-per-t'),
    (53, 'cpu2-idle-per-t'),
    (54, 'cpu2-iow-per-t'),
    (55, 'cpu2-net-irqs-per-t'),
    (56, 'cpu2-net-irqs'),
    (57, 'cpu2-net-rx-soft-irqs-per-t'),
    (58, 'cpu2-net-rx-soft-irqs'),
    (59, 'cpu2-net-tx-soft-irqs-per-t'),
    (60, 'cpu2-net-tx-soft-irqs'),
    (61, 'cpu3-usr-per-t'),
    (62, 'cpu3-nice-per-t'),
    (63, 'cpu3-sys-per-t'),
    (64, 'cpu3-idle-per-t'),
    (65, 'cpu3-iow-per-t'),
    (66, 'cpu3-net-irqs-per-t'),
    (67, 'cpu3-net-irqs'),
    (68, 'cpu3-net-rx-soft-irqs-per-t'),
    (69, 'cpu3-net-rx-soft-irqs'),
    (70, 'cpu3-net-tx-soft-irqs-per-t'),
    (71, 'cpu3-net-tx-soft-irqs'),
]


FILTER_IFPPS_RAM = [20]

def fill_col_labels(col_labels, filter):
    filters_out = []
    for col in filter:
        filters_out.append(col_labels[col - 1])
    return filters_out


for idx, query in enumerate(plots_folders):

    # PERF
    # --------------------

    custom_headers = gnuplot_headers.copy()
    merger.merge("perf", query)

    filters = fill_col_labels(perf_col_labels, FILTER_PERF_ALL)
    custom_headers.append('set title "perf_all"')
    custom_headers.append('set ylabel "measurement"')
    custom_headers.append('plot "perf_merged.dat" with errorbars')
    custom_headers.append('set xrange [0:100]')
    custom_headers.append('set yrange [0:500]')

    plotter.plot("perf", query, custom_headers, [])

    # IFPPS
    # --------------------
    
    # PIDSTAT
    # --------------------
