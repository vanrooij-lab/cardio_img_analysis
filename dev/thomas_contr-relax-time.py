

list_traces_corrcontr = pickle.load( open( "/Users/m.wehrens/Data/__other_analyses/contractility/Thomas/files_Thomas/saved_data_py/2024-04-30_list_traces_corrcontr.p", "rb" ) )


XMAX = 3.5

def determine_features_per_searchterm():

SEARCHTERMS = ['before_no-treatment$',     'after_no-treatment$', 
               'before_spiny-FB$',       'after_spiny-FB$', 'before_mus-FB$', 'after_mus-FB$', 
               'before_spiny-FB-medium$', 'after_spiny-FB-medium$', 'before_mus-FB-medium$',      'after_mus-FB-medium$']
mycolors    = ['b','r',
               'b','r','b','r',
               'b','r','b','r']


# Now run the function which determines (extra) features of interest and groups them by search terms.
peak_durations, peak_durations_byterm, interpeak_times, interpeak_times_byterm, \
                first_peak_height_byterm, selected_samples_list_byterm = \
    cuslibc.create_plots_extract_final_features(sample_info, sample_info_dicts, \
                            list_traces_1min, first_peaks, second_peaks, first_peak_height, list_minvals, list_maxvals, \
                            SEARCHTERMS, mycolors, XMAX, my_out_dir)