
###############################################################################
###############################################################################
# Below some more stuff that was used previously, but not for my latest
# analysis.


###############################################################################
# Create aligned plots, on top of each other

NR_FRAMES = 500

fig = plt.figure(figsize=(7/2.54,7/2.54), dpi=600) 

ax=fig.add_subplot(1, 1, 1)
samples_scrambled1hz = [sample for sample in my_samples if '-nt' in sample]
for sample_name in samples_scrambled1hz:
    
    current_firstpeak      = first_peaks[sample_name]
    current_firstpeak_time = current_firstpeak*sample_dt[sample_name]
    current_t              = np.arange(0,NR_FRAMES)*sample_dt[sample_name]
    current_t_adj          = current_t-current_firstpeak_time
    current_trace          = list_traces_1min[sample_name]
    current_trace_norm     = (current_trace-list_minvals[sample_name])/(list_maxvals[sample_name]-list_minvals[sample_name])
    
    plt.plot(current_t_adj, current_trace_norm,'b-', linewidth=.5)
       
samples_siDes1hz = [sample for sample in my_samples if '10uM-EPI' in sample]
for sample_name in samples_siDes1hz:
    
    current_firstpeak      = first_peaks[sample_name]
    current_firstpeak_time = current_firstpeak*sample_dt[sample_name]
    current_t              = np.arange(0,NR_FRAMES)*sample_dt[sample_name]
    current_t_adj          = current_t-current_firstpeak_time
    current_trace          = list_traces_1min[sample_name]
    current_trace_norm     = (current_trace-list_minvals[sample_name])/(list_maxvals[sample_name]-list_minvals[sample_name])
    
    plt.plot(current_t_adj, current_trace_norm,'r-' , linewidth=.5)

plt.ylim((-.2,1.2))
plt.xlim((-1,1)) 
ax.set_xticks(np.arange(-1,1+.1,.5))
ax.set_xticks(np.arange(-1,1+.1,.1), minor=True)
ax.grid(axis = 'x', which='minor', linewidth=.5)
ax.grid(axis = 'x', which='major', linewidth=.5)
plt.xlabel('Time (s)')
plt.ylabel('1-corr (normalized)')
    
plt.show()

###############################################################################
# Create aligned plots, now normalize plots

NR_FRAMES = 500

samples_scrambled1hz = [sample for sample in my_samples if '-nt' in sample]

fig = plt.figure(figsize=(20/2.54,20/2.54), dpi=600) 
ax=fig.add_subplot(2, 1, 1)

for sample_name in samples_scrambled1hz:
    
    current_firstpeak      = first_peaks[sample_name]
    current_firstpeak_time = current_firstpeak*sample_dt[sample_name]
    current_t              = np.arange(0,NR_FRAMES)*sample_dt[sample_name]
    current_t_adj          = current_t-current_firstpeak_time
    current_trace          = list_traces_1min[sample_name]
    
    plt.plot(current_t_adj, current_trace)
    plt.plot(current_t_adj[current_firstpeak], current_trace[current_firstpeak],'ko')
    
plt.show()



NR_FRAMES = 500

samples_scrambled1hz = [sample for sample in my_samples if '10uM-EPI' in sample]

fig = plt.figure(figsize=(20/2.54,20/2.54), dpi=600) 
ax=fig.add_subplot(2, 1, 1)

for sample_name in samples_scrambled1hz:
    
    current_firstpeak      = first_peaks[sample_name]
    current_firstpeak_time = current_firstpeak*sample_dt[sample_name]
    current_t              = np.arange(0,NR_FRAMES)*sample_dt[sample_name]
    current_t_adj          = current_t-current_firstpeak_time
    current_trace          = list_traces_1min[sample_name]
    
    plt.plot(current_t_adj, current_trace)
    plt.plot(current_t_adj[current_firstpeak], current_trace[current_firstpeak],'ko')
    
plt.show()

###############################################################################

# Now also find the peaks

mytrace_cut = np.array(mytrace)
mytrace_cut[mytrace_cut<(max(mytrace)*.9)]=0 
peaks_in_mytrace, _ = signal.find_peaks(mytrace_cut)
peak_times = sample_dt[my_samples[S_IDX]]*peaks_in_mytrace

###############################################################################

###############################################################################
# Now show the trace, showing peaks
# Also calculate inter-peak times

f=np.array(range(0,1000))
t=f*sample_dt[my_samples[S_IDX]]

mytrace_arr=np.array(mytrace)
plt.plot(t,mytrace)
plt.plot(t[peaks_in_mytrace],mytrace_arr[peaks_in_mytrace],'ro')
plt.xlabel('Time (s)')
plt.ylabel('Correlation with image 0')
plt.title("Trace v0")
plt.show()



###############################################################################
# Can we make a nice movie out of this?

# Set up some parameters
t=np.array(range(0,1000)) # TO DO: more convenient to do this at start

#######################
# Make plot 1
plt.plot(t,mytrace)
#plt.plot(t[10],mytrace[10],'ok') highlight a point
plt.xlabel('frame')
plt.ylabel('Correlation with image 0')
plt.title("Trace v0")
plt.show()

fig, (ax1, ax2) = plt.subplots(1,2)


#######################
# Plot with both trace and image

fig = plt.figure() # figsize=(10, 7)

fig.add_subplot(1, 2, 1)

plt.plot(t,mytrace)
plt.plot(t[10],mytrace[10],'ok')
plt.xlabel('frame')
plt.ylabel('Correlation with image 0')
plt.title("Trace v0")

fig.add_subplot(1, 2, 2)
plt.imshow(img[roi_c1:roi_c2,roi_r1:roi_r2])
plt.show()

fig.savefig(my_output_dir+'my_plot.tif')


#######################
# Plot with both trace and image


t_seconds=t*frame_interval

for img_idx in range(0,1000):
    
    # Load image
    imgageXXXX_path = my_image_dir+my_image_base+str(img_idx).zfill(4)+'.tif'
    img_XXXX = mpimg.imread(imgageXXXX_path)
    
    # Create the figure
    my_dpi=300 # (arbitrary, actually)
    fig = plt.figure(figsize=(1600/my_dpi, 800/my_dpi), dpi=my_dpi) # figsize=(10, 7)
    
    fig.add_subplot(1, 2, 1)
    
    plt.plot(t_seconds,mytrace)
    plt.plot(t_seconds[img_idx],mytrace[img_idx],'ok')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Correlation with image 0')
    plt.title("Trace v0")
    
    fig.add_subplot(1, 2, 2)
    plt.imshow(img_XXXX[roi_c1:roi_c2,roi_r1:roi_r2])
    plt.title('Image @ '+str(np.round(t_seconds[img_idx],2))+' seconds')
    
    fig.savefig(my_output_dir+'my_plot_'+str(img_idx)+'.tif')

    if (img_idx%25==0):
        print(str(img_idx/1000*100)+'% done..')
        plt.show()

    plt.close(fig)

###############################################################################


#####


# test code
img_0010 = mpimg.imread(my_image_dir+my_image_base+str(10).zfill(4)+'.tif')
stats.pearsonr(img_0000[roi_c1:roi_c2,roi_r1:roi_r2].flatten(), img_0010[roi_c1:roi_c2,roi_r1:roi_r2].flatten())

###############################################################################

#read image
img_raw = cv2.imread(my_image_path)

#select ROI function
roi = cv2.selectROI(img_raw)

#print rectangle points of selected roi
print(roi)

#Crop selected roi from raw image
roi_cropped = img_raw[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]

#show cropped image
cv2.imshow("ROI", roi_cropped)

cv2.imwrite("crop.jpeg",roi_cropped)

#hold window
cv2.waitKey(0)





