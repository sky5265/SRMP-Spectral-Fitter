import numpy as np
import random
import matplotlib.pyplot as plt

directory = 'All Shifts Outputs/'
output_dir = "sic_Redshift_outputs_plotted_separately/"
mkdir(output_dir)

W = 15
H = 10

colors = [sKy_colors['light blue'], sKy_colors['red'], sKy_colors['purple'], sKy_colors['very dark blue']]
legend_labels = [r'Si II', r'O I', r'Ca H&K']
ing = 0

plt, _, _ = get_pretty_plot()
idx = 0
# iterate over files in
# that directory
for filename in os.scandir(directory):
    if filename.is_dir():
        long_name = filename.path+"/"
        
        dirlist = os.listdir(long_name)
        for filename1 in dirlist:
            extension = filename1[-4:]
            if extension == '.txt':
            
                line_name = filename1[0:-4]
                file_loc =str(long_name)+str(filename1)
                shifts_found = read_file(file_loc)["dict"]
                times = [i for i in shifts_found[0]]
                shift_s = np.asarray([abs(float(i)) for i in shifts_found[1]]) / 1.0E5 #bring from cm/s to km/s
                unc_s = np.asarray([float(i) for i in shifts_found[2]]) / 1.0E5 #bring from cm/s to km/s

                times_to_plot = []

                for i in range(len(times)):
                    time = times[i]
                    if '_' in time:
                        time = time[:time.index('_')]
                    times_to_plot.append(float(time))
                    
                times_to_plot = np.asarray(times_to_plot)



                print("ing is "+str(ing))
                plt.scatter(x=times_to_plot, y=np.asarray(shift_s)/-1.0E3, label=legend_labels[ing], color = colors[ing], s = 130)
                plt.errorbar(x=times_to_plot, y=np.asarray(shift_s)/-1.0E3, yerr = unc_s/1.0E3, fmt = "o", color = colors[ing])
                ing+=1
                plt.xlabel(r'Time (Days)', fontsize=3*W)
                plt.xticks(fontsize=30)
                plt.ylabel(r'$V$ ($10^3$ $km$ $s^{-1}$)', fontsize=3*W)
                plt.yticks(fontsize=30)
plt.legend(fontsize = 2*W, ncol = 2, framealpha=1, fancybox=False, edgecolor='black', loc = 4)
plt.ylim([-20, 2])
plt.savefig(output_dir+"center_shifts.pdf", bbox_inches = 'tight')
plt.close()
