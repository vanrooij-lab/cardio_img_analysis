


current_t[idx_l], current_trace_1min_baselinecorr_smoothed[idx_l], peak_line[idx_l]

plt.close('all')

import matplotlib.pyplot as plt


current_trace             = list_traces_1min[sample_name]        
NR_FRAMES                 = len(current_trace)       
current_firstpeak         = first_peaks[sample_name]
current_second_peak       = second_peaks[sample_name]    
current_firstpeak_time    = current_firstpeak*sample_info_dicts['dt'][sample_name]
current_secondpeak_time    = current_second_peak*sample_info_dicts['dt'][sample_name]
current_t                 = np.arange(0,NR_FRAMES)*sample_info_dicts['dt'][sample_name]

# Now with baseline in the corrected trace
plt.close('all')
plt.plot(current_t, current_trace_1min_baselinecorr_smoothed)
plt.axvline(x=current_firstpeak_time, linestyle='dotted', color='red')
plt.axvline(x=current_t[current_firstpeak], linestyle='dotted', color='green')

plt.axvline(x=current_t[peak2_regionstart_f], linestyle='dotted', color='red')
plt.axvline(x=current_t[peak2_regionend_f], linestyle='dotted', color='red')
plt.axvline(x=current_t[peak2_regionend_f], linestyle='dotted', color='red')
plt.axvline(x=xl, linestyle='dotted', color='grey')
plt.axvline(x=xr, linestyle='dotted', color='grey')
plt.axvline(x=current_t[current_second_peak], linestyle='dotted', color='grey')
plt.scatter(xl, yl1, color='blue')
plt.scatter(xr, yr2, color='blue')
plt.scatter(current_t[current_second_peak], current_trace_1min_baselinecorr_smoothed[current_second_peak], color='blue')
plt.xlabel('Time')
plt.ylabel('Correlation')
plt.title('Correlation vs Time (Polynomial Baseline)')
plt.show()