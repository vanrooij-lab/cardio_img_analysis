

NR_FRAMES=1500


list_traces_corrcontr = pickle.load( open( "/Users/m.wehrens/Data/__other_analyses/contractility/Thomas/files_Thomas/saved_data_py/2024-04-30_list_traces_corrcontr.p", "rb" ) )


##############################################



if not os.path.exists(my_out_dir+"analysis/"):
    os.mkdir(my_out_dir+"analysis/")

import matplotlib.pyplot as plt

# Important parameters required for the analysis
PEAKMINTIME   = .5 # estimate of minimum distance between peaks, in seconds
SMOOTHINGTIME = .2 # width of smoothing window, in seconds 
PEAKMINHEIGHT = .8 # minimum height of peak, expressed as quantile

# Call the function which plots traces and analyzes important features    
first_peaks, second_peaks, first_peak_height, list_traces_1min, list_minvals, list_maxvals = \
        cuslibc.find_features_and_plot(sample_info_dicts, list_traces_corrcontr, my_out_dir, 
                            PEAKMINTIME=PEAKMINTIME, SMOOTHINGTIME=SMOOTHINGTIME, PEAKMINHEIGHT=PEAKMINHEIGHT) 
                            # , samples_to_do=range(3)) # for testing purposes


##############################################


XMAX = 3.5


SEARCHTERMS = ['diff4']
mycolors    = ['b']


# Now run the function which determines (extra) features of interest and groups them by search terms.
peak_durations, peak_durations_byterm, interpeak_times, interpeak_times_byterm, \
                first_peak_height_byterm, selected_samples_list_byterm = \
    cuslibc.create_plots_extract_final_features(sample_info, sample_info_dicts, \
                            list_traces_1min, first_peaks, second_peaks, first_peak_height, list_minvals, list_maxvals, \
                            SEARCHTERMS, mycolors, XMAX, my_out_dir)



##############################################


sample_nr = 6 # this is a problematic example
sample_nr = 1 # this one is nice

sample_name= sample_info['sample_name'][sample_nr] # 'contractility_measurements_DIFF4_MYBPC3_20240419_Cor-50%-1'
current_dt= sample_info['dt'][sample_nr]

current_trace          = list_traces_corrcontr[sample_name]
current_trace_1min     = list_traces_1min[sample_name]
current_t              = np.arange(0,NR_FRAMES)*current_dt
corr                   = list_traces_corrcontr[sample_name]

plt.plot(current_t, current_trace_1min)
plt.xlabel('Time')
plt.ylabel('Correlation')
plt.title('Correlation vs Time')
plt.show()


##############################################
# now find the baseline

# determine the baseline window
WINDOW_WIDTH= int( interpeak_times[sample_name]*2/current_dt ) // 2 * 2 + 1

baseline = [np.min(current_trace_1min[i:i+WINDOW_WIDTH]) for i in range(len(current_trace_1min)-WINDOW_WIDTH+1)]
len(baseline)

padding_width = (WINDOW_WIDTH) // 2
padded_baseline = np.pad(baseline, (padding_width, padding_width), mode='constant', constant_values=[baseline[1], baseline[-1]])

current_trace_1min_baselinecorr = current_trace_1min - padded_baseline

# Smooth the padded baseline using a 2nd order polynomial local approximation
smoothed_baseline = np.polyval(np.polyfit(current_t, padded_baseline, 4), current_t)
current_trace_1min_baselinecorr_smoothed = current_trace_1min - smoothed_baseline

# Plot original, adding the baseline (polynomial)
plt.plot(current_t, current_trace_1min)
plt.plot(current_t, smoothed_baseline)
plt.xlabel('Time')
plt.ylabel('Correlation')
plt.title('Correlation vs Time (Polynomial Baseline)')
plt.show()

# Plot minus the baseline (polynomial)
plt.plot(current_t, current_trace_1min_baselinecorr)
plt.xlabel('Time')
plt.ylabel('Correlation')
plt.title('Correlation vs Time (Minus Polynomial Baseline)')
plt.show()


##############################################
# Now find the values that intersect with a line at 5%

PEAK_BASE_FRACTION = .05

peak_line_height = first_peak_height[sample_name]*PEAK_BASE_FRACTION
peak_line = np.array([peak_line_height for i in range(len(current_trace_1min))])

# Plot original, adding the baseline (polynomial)
plt.plot(current_t, current_trace_1min)
plt.plot(current_t, peak_line)
plt.xlabel('Time')
plt.ylabel('Correlation')
plt.title('Correlation vs Time (Polynomial Baseline)')
plt.show()

# Now with baseline in the corrected trace
plt.plot(current_t, current_trace_1min_baselinecorr_smoothed)
plt.plot(current_t, peak_line)
plt.xlabel('Time')
plt.ylabel('Correlation')
plt.title('Correlation vs Time (Polynomial Baseline)')
plt.show()


##############################################
# Now find the matching intersection points

# Find the intersection points

# !!!!
# See line 464 of custom_functions_contractitility
# There, I use the normalized cross-correlation to find the intersection points at 0.5 (given that the peak is at 1
# I think it's wisest to merge this into the create_plots_extract_final_features function, as the loop is already there


# !!!!
# CODE BELOW WAS COPIED FROM THE FUNCTION create_plots_extract_final_features, SO I SHOULD EDIT THIS 
# TO LOOK FOR THE 5% VALUE IN THE CORRECTED TRACE FROM ABOVE, AND ALSO ADD THAT CORRECTION TO THAT FUNCTION
# This is a bit redundant
current_trace             = list_traces_1min[sample_name]        
NR_FRAMES                 = len(current_trace)       
current_firstpeak         = first_peaks[sample_name]
current_second_peak       = second_peaks[sample_name]    
current_firstpeak_time    = current_firstpeak*sample_info_dicts['dt'][sample_name]
current_secondpeak_time    = current_second_peak*sample_info_dicts['dt'][sample_name]
#current_t                 = np.arange(0,NR_FRAMES)*sample_info_dicts['dt'][sample_name]
#current_t_adj             = current_t-current_firstpeak_time
#current_trace_norm        = (current_trace-list_minvals[sample_name])/(list_maxvals[sample_name]-list_minvals[sample_name])

# Find the peak_duration_50
interpeak_frames = current_second_peak - current_firstpeak
peak2_regionstart_f  = current_second_peak - round(interpeak_frames/2*1.5)
peak2_regionend_f    = current_second_peak + round(interpeak_frames/2*1.5)

t_50a = location_closest_value(current_trace_norm[peak2_regionstart_f:current_second_peak], PEAK_BASE_FRACTION)+peak2_regionstart_f
t_50b = location_closest_value(current_trace_norm[current_second_peak:peak2_regionend_f], PEAK_BASE_FRACTION)+current_second_peak    
peak_duration_50 = t_50b-t_50a  

# Determine intersects
# xint, yint1, yint2 = find_intersections(current_t, current_trace_1min_baselinecorr_smoothed, peak_line) # For all
idx_l = range(peak2_regionstart_f,current_second_peak); idx_r = range(current_second_peak,peak2_regionend_f)
xl_, y1l_, y2l_ = find_intersections(current_t[idx_l], current_trace_1min_baselinecorr_smoothed[idx_l], peak_line[idx_l]) # For points left of peak, closest one
xr_, y1r_, y2r_ = find_intersections(current_t[idx_r], current_trace_1min_baselinecorr_smoothed[idx_r], peak_line[idx_r]) # For points right of peak, closest one
xl=xl_[-1]; yl1=y1l_[-1]; yl2=y2l_[-1]
xr=xr_[0]; yr1=y1r_[0]; yr2=y2r_[0]

# Now with baseline in the corrected trace
plt.plot(current_t, current_trace_1min_baselinecorr_smoothed)
plt.plot(current_t, peak_line)
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

# Now give the times of interest
duration_contraction = current_t[current_second_peak] - xl
duration_relaxation  = xr - current_t[current_second_peak]
duration_contraction_fraction = duration_contraction / (duration_contraction+duration_relaxation)
duration_relaxation_fraction  = duration_relaxation / (duration_contraction+duration_relaxation)
