# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 14:35:13 2023

@author: griffin.kowash
"""

#import re
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

from gtools import gtools
    

class Processing:
    @staticmethod
    def load_probe(filepath):
        
        """
        file = open(filepath, 'r')
        lines = file.readlines()
        file.close()
        
        time = []
        data = []
        timestep = []
        new_timestep = True
        
        for line in lines:
            #line_split = re.split('  | ', line) #is there a better way to split on generic white space?
            line_split = line.split()
            #line_split = line_split[1:]  #remove leading gap
            #line_split[-1] = line_split[-1][:-1]  #remove trailing newline character on last entry
            #print(line_split)
            
            try:
                values = list(map(lambda x: float(x), line_split))
            except:
                print(line_split)
            
            if new_timestep:  #could instead just check len(timestep)
                time.append(values[0])
                new_timestep = False
                timestep = timestep + values[1:]
                
            else:
                timestep = timestep + values
            
            if len(values) != 9:
                #could probably also use np.reshape
                x = timestep[::3]
                y = timestep[1::3]
                z = timestep[2::3]
                data.append([x, y, z])
                
                timestep = []
                new_timestep = True
        """
        
        time, data = gtools.load_distributed_probe(filepath, last_index='probe', precision='single')
                
        return np.array(time), np.array(data)
    
    @staticmethod
    def load_probes(filepaths):
        #loads multiple probe files and combines into one dataset
        data_sets = []
        
        for filepath in filepaths:
            t, d = Processing.load_probe(filepath)
            data_sets.append(d)
            
        data = np.concatenate(data_sets, axis=2)
        
        return t, data
    
    @staticmethod
    def load_source(source_name_and_path):
        #loads source time series
        t, source = np.loadtxt(source_name_and_path).T
        return t, source

    @staticmethod
    def load_source_fft(source_filepath):
        #loads plane wave source and return frequencies and fft
        source_data = np.loadtxt(source_filepath)
        dt = np.mean(source_data[1:, 0] - source_data[:-1, 0])
        source_freq = np.fft.rfftfreq(source_data.shape[0]) / dt
        source_fft = np.fft.rfft(source_data[:, 1], norm='forward') * 2
        
        return source_freq, source_fft

    @staticmethod
    def calc_magnitude(data):
        #takes in efield data in the form of load_probe or calc_fft results, returns vector magnitude
        return np.sqrt(np.abs(data[:, 0, :])**2 + np.abs(data[:, 1, :])**2 + np.abs(data[:, 2, :])**2)
    
    @staticmethod
    def calc_fft(t, data):
        #takes in time and efield components of the form of load_probe results, returns ex/ey/ex FFTs at each probe location       
        dt = np.mean(t[1:] - t[:-1])
        freq = np.fft.rfftfreq(t.size) / dt
        
        data_fft = np.fft.rfft(data, axis=0, norm='forward') * 2
        
        return freq, data_fft
    
    @staticmethod
    def calc_statistics(data):
        #takes in data (time, probes) and returns min, max, and mean over time between all probes
        data_min = data.min(axis=1)
        data_mean = data.mean(axis=1)
        data_max = data.max(axis=1)
        return data_min, data_mean, data_max

    @staticmethod
    def calc_shielding(data_fft, source_fft):
        #takes in data from calc_fft and plane wave fft to calcalate shielding effectiveness
        #assumes same time step and sample size for source and probe
        shielding = 20 * np.log10(np.abs(source_fft / data_fft))
        #shielding = 20 * np.log10(np.abs(source_fft[:, np.newaxis] / data_fft))
        
        return shielding
    
    
class Workflows:
    @staticmethod
    def generate_shielding_statistics_from_results(probe_path, source_path, cutoff=None, pad=None):
        #takes in file paths, calculate shielding effectivess, and saves in probe_path directory
        if type(probe_path) == list or type(probe_path) == tuple:
            #stack results from multiple probes
            t, data = Processing.load_probes(probe_path)
            save_path = '\\'.join(probe_path[0].split('\\')[:-1] + ['se_stats.dat'])
            
        else:
            #process single probe file
            t, data = Processing.load_probe(probe_path)
            save_path = '\\'.join(probe_path.split('\\')[:-1] + ['se_stats.dat'])
            
        if cutoff != None:
            warnings.warn(f'User has requested cutoff time of {cutoff} seconds, which may affect results.')
            index = np.abs(t - cutoff).argmin()
            t = t[:index]
            data = data[:index, ...]
        
        if pad != None:
            warnings.warn(f'User has requested zero-padding out to {pad} seconds, which may affect results.')
            dt = t[1] - t[0]
            t_pad = np.arange(t[0], pad + dt, dt)
            pad_size = t_pad.size - t.size
            data_pad = np.pad(data, ((0, pad_size), (0, 0), (0, 0)))
            t = t_pad
            data = data_pad
                
        
        freq, e_fft = Processing.calc_fft(t, data)
        e_fft_mag = Processing.calc_magnitude(e_fft)
        
        #_, source_fft = Processing.load_source_fft(source_path)
        _, esource = Processing.load_source(source_path)
        esource = gtools.pad_array_to_length(esource, t.size, 0)
        _, source_fft = Processing.calc_fft(t, esource)
        
        #print('source mean, probe mean: ', np.abs(source_fft.mean()), e_fft_mag.mean())
          
        if True:
            e_fft_mag_stats = Processing.calc_statistics(e_fft_mag)
            se_max, se_mean, se_min = Processing.calc_shielding(e_fft_mag_stats, source_fft)
            #se_min = Processing.calc_shielding(e_fft_mag_max, source_fft)
            #se_mean = Processing.calc_shielding(e_fft_mag_mean, source_fft)
            #se_max = Processing.calc_shielding(e_fft_mag_min, source_fft)
            
        else:
            se = Processing.calc_shielding(e_fft_mag, source_fft)
            se_min, se_mean, se_max = Processing.calc_statistics(se)
        
        np.savetxt(save_path, np.transpose([freq, se_min, se_mean, se_max]))
        
        #print('Shielding statistics saved to ', save_path, '\n')
        
        return freq, se_min, se_mean, se_max
        
    
    @staticmethod
    def plot_shielding_statistics_from_file(se_path, title=None, ylim=None, xlim=None):
        #takes in filepath and generates plot of min, max, and mean shielding effectiveness
        freq, se_min, se_mean, se_max = np.loadtxt(se_path).T
    
        sns.set()
        plt.fill_between(freq, se_min, se_max, color=(0.5, 0.5, 0.5, 0.5))
        plt.plot(freq, se_mean, linestyle='--', color='C0')
        
        plt.xscale('log')
        
        if ylim == None:
            plt.ylim(15, 150)
        else:
            plt.ylim(ylim[0], ylim[1])
            
        if xlim == None:
            plt.xlim(1e7, 5e10)
        else:
            plt.xlim(xlim[0], xlim[1])
        
        if title != None:
            plt.suptitle(title)
            
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Shielding (dB)')
        
        plt.show()
        
        
    @staticmethod
    def plot_shielding_statistics_from_multiple_runs(se_paths, title=None, xlim=None, ylim=None, first=False):
        se_mins = []
        se_means = []
        se_maxs = []
        
        for se_path in se_paths:
            freq, se_min, se_mean, se_max = np.loadtxt(se_path).T
            se_mins.append(se_min)
            se_means.append(se_mean)
            se_maxs.append(se_max)
            
        se_mins = np.array(se_mins)
        se_means = np.array(se_means)
        se_maxs = np.array(se_maxs)
        
        se_min_all = np.min(se_mins, axis=0)
        se_mean_all = np.mean(se_means, axis=0)
        se_max_all = np.max(se_maxs, axis=0)
        
        # optionally trim first frequency from FFT results
        if first:
            start = 0
        else:
            start = 1
        
        plt.fill_between(freq[start:], se_min_all[start:], se_max_all[start:], color=(0.5, 0.5, 0.5, 0.5), label='Range')
        #plt.fill_between(freq, se_min_all, se_max_all, color=(.30, .45, .69, .5))    #(.87, .52, .32, .5))
        plt.plot(freq[start:], se_mean_all[start:], linestyle='--', color='C0', label='Mean')
        
        if xlim == None:
            plt.xlim(1e7, 5e10)
        else:
            plt.xlim(xlim[0], xlim[1])
            
        if ylim == None:
            plt.ylim(0, 150)
        else:
            plt.ylim(ylim[0], ylim[1])
            
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Shielding effectiveness (dB)')
        
        if title == None:
            plt.suptitle('Shielding effectiveness, all runs')
        else:
            plt.suptitle(title)
            
        plt.legend(loc='upper left')
        plt.xscale('log')
        plt.show()
    
    
    @staticmethod
    def plot_electric_field_time_domain(probe_paths, suffix=None):
        fig1, ax1 = plt.subplots(1)
        fig2, ax2 = plt.subplots(1)
                
        if type(probe_paths) in [list, tuple]:           
            t, data = Processing.load_probes(probe_paths)
        else:
            t, data = Processing.load_probe(probe_paths)
        
        # E-field magnitude
        emag = Processing.calc_magnitude(data)
        emag_min, emag_mean, emag_max = Processing.calc_statistics(emag)
        
        ax1.fill_between(t, emag_min, emag_max, color=(.5, .5, .5, .5), label='Range')
        ax1.plot(t, emag_mean, color='C0', label='Mean')
        ax1.legend()
        if suffix == None:
            fig1.suptitle('Electric field magnitude time series')
        else:
            fig1.suptitle(f'Electric field magnitude time series ({suffix})')
    
        # E-field components
        ex, ey, ez = data[:,0,:], data[:,1,:], data[:,2,:]
        _, ex_mean, _ = Processing.calc_statistics(ex)
        _, ey_mean, _ = Processing.calc_statistics(ey)
        _, ez_mean, _ = Processing.calc_statistics(ez)

        ax2.plot(t, ex_mean, label='Ex')
        ax2.plot(t, ey_mean, label='Ey')
        ax2.plot(t, ez_mean, label='Ez')
        
        ax2.legend()
        ax2.set_xlabel('Time (s)')
        ax2.set_ylabel('Electric field (V/m)')
        if suffix == None:
            fig2.suptitle('Electric field components time series')
        else:
            fig2.suptitle(f'Electric field components time series ({suffix})')

        # Display figures (comment out for IPython)
        #fig1.show()
        #fig2.show()
        
        
    @staticmethod
    def plot_with_range(x, ymin, ymean, ymax, xlabel, ylabel, title, xscale='linear', yscale='linear', xlim=None, ylim=None, suppress_range=False, subtitle=None):
        fig, ax = plt.subplots(1)
        if not suppress_range:
            ax.fill_between(x, ymin, ymax, color=(.5, .5, .5, .5), label='Range')
        ax.plot(x, ymean, label='Mean', linestyle='--')
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        if not suppress_range:
            ax.legend()
        if subtitle is not None:
            ax.set_title(subtitle)
        ax.set_xscale(xscale)
        ax.set_yscale(yscale)
        if xlim is not None:
            ax.set_xlim(xlim[0], xlim[1])
        if ylim is not None:
            ax.set_ylim(ylim[0], ylim[1])
        fig.suptitle(title)
        #fig.show()
        
        
    @staticmethod
    def plot_shielding_by_source(basepath, folders, only_positives=False, subtitle=None, f0=0, f1=1e16):
        # visualizes shielding by orientation of the plane wave source
        
        # for positive and negative orientations
        runs_to_matrix_12 = {
            1: (4, 0),
            2: (4, 1),
            3: (1, 2),
            4: (1, 1),
            5: (5, 1),
            6: (5, 0),
            7: (0, 2),
            8: (0, 1),
            9: (3, 2),
            10: (3, 0),
            11: (2, 0),
            12: (2, 2)
        }
        
        # just positive orientations
        runs_to_matrix_6 = {
            1: (2, 0),
            2: (2, 1),
            7: (0, 2),
            8: (0, 1),
            11: (1, 0),
            12: (1, 2)
        }
        
        # Calculate and plot shielding
        fig, ax = plt.subplots(1)
        vals = []
        max_val, min_val = -np.inf, np.inf
        
        se_paths = ['\\'.join([basepath, str(i), 'se_stats.dat']) for i in folders]

        for se_path in se_paths:   
            f, smin, smean, smax = np.loadtxt(se_path).T

            i0 = np.abs(f - f0).argmin()
            i1 = np.abs(f - f1).argmin() + 1
            vals.append(smean[i0:i1].mean())

            max_val = max(max_val, smax[0])
            min_val = min(min_val, smin[0])

        for i, val in enumerate(vals):
            modifier = (val - min(vals)) / (max(vals) - min(vals))
            r = (1 - modifier)  * 1
            g = 0.5 - 0.0*(0.5 - modifier)
            b = modifier * 0.9
            color = (r, g, b)
            #print(color)

            if only_positives:
                anchor = runs_to_matrix_6[folders[i]]
            else:
                anchor = runs_to_matrix_12[folders[i]]
                
            rect = plt.Rectangle(anchor, 1, 1, facecolor=color, edgecolor='white', linewidth=2)

            ax.add_patch(rect)
            ax.text(anchor[0] + 0.28, anchor[1] + 0.47, str(round(val)) + 'dB', color='white')

        if only_positives:
            ax.set_xlim(0, 3)
            ax.set_xticks(np.arange(0.5, 3.5, 1), ['+X', '+Y', '+Z'])
            
        else:
            ax.set_xlim(0, 6)
            ax.set_xticks(np.arange(0.5, 6.5, 1), ['+X', '-X', '+Y', '-Y', '+Z', '-Z'])
            
        ax.set_ylim(0, 3)
        ax.set_yticks(np.arange(0.5, 3.5, 1), ['+X', '+Y', '+Z'])

        ax.set_xlabel('Orientation (k)')
        ax.set_ylabel('Polarization (E)')

        fig.suptitle('Shielding effectiveness by source configuration')
        
        if subtitle != None:
            ax.set_title(subtitle)

        print('Low-frequency min: ', min_val)
        print('Low-frequency mean: ', np.mean(vals))
        print('Low-frequency max: ', max_val)

        
    @staticmethod
    def plot_cable_from_multiple_runs(Isc_paths, Voc_paths, suppress_range=False, subtitle=None):    
        # refactor later. Plots Voc and Isc data with statistics across multuple sims
        
        t = None
        f = None
        
        i_c1_all = []
        i_c2_all = []
        i_c3_all = []
        i_shield_all = []
        
        v_c1_all = []
        v_c2_all = []
        v_c3_all = []
        v_shield_all = []
        
        i_c1_fft_all = []
        i_c2_fft_all = []
        i_c3_fft_all = []
        i_shield_fft_all = []
        
        v_c1_fft_all = []
        v_c2_fft_all = []
        v_c3_fft_all = []
        v_shield_fft_all = []
        
        
        for path in Isc_paths:
            # Load time series data
            _, i_c1 = np.loadtxt('\\'.join([path, 'Current_(C1).dat'])).T
            _, i_c2 = np.loadtxt('\\'.join([path, 'Current_(TSP_C2).dat'])).T
            _, i_c3 = np.loadtxt('\\'.join([path, 'Current_(TSP_C3).dat'])).T
            _, i_shield = np.loadtxt('\\'.join([path, 'Current_(TSP_shield).dat'])).T
            
            # Generate FFTs
            i_c1_fft = np.abs(np.fft.rfft(i_c1, norm='forward') * 2)
            i_c2_fft = np.abs(np.fft.rfft(i_c2, norm='forward') * 2)
            i_c3_fft = np.abs(np.fft.rfft(i_c3, norm='forward') * 2)
            i_shield_fft = np.abs(np.fft.rfft(i_shield, norm='forward') * 2)
            
            # Append data from run to full collection
            i_c1_all.append(i_c1)
            i_c2_all.append(i_c2)
            i_c3_all.append(i_c3)
            i_shield_all.append(i_shield)
            
            i_c1_fft_all.append(i_c1_fft)
            i_c2_fft_all.append(i_c2_fft)
            i_c3_fft_all.append(i_c3_fft)
            i_shield_fft_all.append(i_shield_fft)
            
            if t is None:
                t = _
                dt = t[1] - t[0]
                f = np.fft.rfftfreq(t.size, d=dt)
                
                
        for path in Voc_paths:
            _, v_c1 = np.loadtxt('\\'.join([path, 'Voltage_(C1_J1).dat'])).T
            _, v_c2 = np.loadtxt('\\'.join([path, 'Voltage_(TSP_C2_J1).dat'])).T
            _, v_c3 = np.loadtxt('\\'.join([path, 'Voltage_(TSP_C3_J1).dat'])).T
            _, v_shield = np.loadtxt('\\'.join([path, 'Voltage_(TSP_shield_J1).dat'])).T
            
            v_c1_fft = np.abs(np.fft.rfft(v_c1, norm='forward') * 2)
            v_c2_fft = np.abs(np.fft.rfft(v_c2, norm='forward') * 2)
            v_c3_fft = np.abs(np.fft.rfft(v_c3, norm='forward') * 2)
            v_shield_fft = np.abs(np.fft.rfft(v_shield, norm='forward') * 2)
            
            v_c1_all.append(v_c1)
            v_c2_all.append(v_c2)
            v_c3_all.append(v_c3)
            v_shield_all.append(v_shield)
            
            v_c1_fft_all.append(v_c1_fft)
            v_c2_fft_all.append(v_c2_fft)
            v_c3_fft_all.append(v_c3_fft)
            v_shield_fft_all.append(v_shield_fft)
            
            
        # Reshape full datasets to form (time, runs) to use with Processing.calc_statistics
        i_c1_all = np.array(i_c1_all).T
        i_c2_all = np.array(i_c2_all).T
        i_c3_all = np.array(i_c3_all).T
        i_shield_all = np.array(i_shield_all).T
        
        v_c1_all = np.array(v_c1_all).T
        v_c2_all = np.array(v_c2_all).T
        v_c3_all = np.array(v_c3_all).T
        v_shield_all = np.array(v_shield_all).T
        
        i_c1_fft_all = np.array(i_c1_fft_all).T
        i_c2_fft_all = np.array(i_c2_fft_all).T
        i_c3_fft_all = np.array(i_c3_fft_all).T
        i_shield_fft_all = np.array(i_shield_fft_all).T
        
        v_c1_fft_all = np.array(v_c1_fft_all).T
        v_c2_fft_all = np.array(v_c2_fft_all).T
        v_c3_fft_all = np.array(v_c3_fft_all).T
        v_shield_fft_all = np.array(v_shield_fft_all).T
        
        # Calculate min, mean, and max
        i_c1_min, i_c1_mean, i_c1_max = Processing.calc_statistics(i_c1_all)
        i_c2_min, i_c2_mean, i_c2_max = Processing.calc_statistics(i_c2_all)
        i_c3_min, i_c3_mean, i_c3_max = Processing.calc_statistics(i_c3_all)
        i_shield_min, i_shield_mean, i_shield_max = Processing.calc_statistics(i_shield_all)
        
        v_c1_min, v_c1_mean, v_c1_max = Processing.calc_statistics(v_c1_all)
        v_c2_min, v_c2_mean, v_c2_max = Processing.calc_statistics(v_c2_all)
        v_c3_min, v_c3_mean, v_c3_max = Processing.calc_statistics(v_c3_all)
        v_shield_min, v_shield_mean, v_shield_max = Processing.calc_statistics(v_shield_all)
        
        i_c1_fft_min, i_c1_fft_mean, i_c1_fft_max = Processing.calc_statistics(i_c1_fft_all)
        i_c2_fft_min, i_c2_fft_mean, i_c2_fft_max = Processing.calc_statistics(i_c2_fft_all)
        i_c3_fft_min, i_c3_fft_mean, i_c3_fft_max = Processing.calc_statistics(i_c3_fft_all)
        i_shield_fft_min, i_shield_fft_mean, i_shield_fft_max = Processing.calc_statistics(i_shield_fft_all)
        
        v_c1_fft_min, v_c1_fft_mean, v_c1_fft_max = Processing.calc_statistics(v_c1_fft_all)
        v_c2_fft_min, v_c2_fft_mean, v_c2_fft_max = Processing.calc_statistics(v_c2_fft_all)
        v_c3_fft_min, v_c3_fft_mean, v_c3_fft_max = Processing.calc_statistics(v_c3_fft_all)
        v_shield_fft_min, v_shield_fft_mean, v_shield_fft_max = Processing.calc_statistics(v_shield_fft_all)
            
        # Generate plots
        #fig, ax = plt.subplots(1)
        #ax.fill_between(t, i_c1_min, i_c1_max, color=(.5, .5, .5, .5), label='Range')
        #ax.plot(t, i_c1_mean, label='Mean', linestyle='--')
        #ax.set_xlabel('Time (s)')
        #ax.set_ylabel('Current (A)')
        #ax.legend()
        #fig.suptitle('Bare conductor - current (time series)')
        #fig.show()
        
        range_isc = (-1e-6, 6e-6)
        range_voc = (-3e-4, 5e-5)
        
        range_isc_fft = (1e-10, 1e-6)
        range_voc_fft = (1e-10, 1e-4)
        
        Workflows.plot_with_range(t, i_c1_min, i_c1_mean, i_c1_max, xlabel='Time (s)', ylabel='Current (A)', title='Bare conductor - current (time series)', ylim=range_isc, suppress_range=suppress_range, subtitle=subtitle)
        Workflows.plot_with_range(t, i_c2_min, i_c2_mean, i_c2_max, xlabel='Time (s)', ylabel='Current (A)', title='Shielded conductor - current (time series)', ylim=range_isc, suppress_range=suppress_range, subtitle=subtitle)
        #Workflows.plot_with_range(t, i_c3_min, i_c3_mean, i_c3_max, xlabel='Time (s)', ylabel='Current (A)', title='Shielded conductor 2 - current (time series)', ylim=range_isc, suppress_range=suppress_range, subtitle=subtitle)
        #Workflows.plot_with_range(t, i_shield_min, i_shield_mean, i_shield_max, xlabel='Time (s)', ylabel='Current (A)', title='Shield - current (time series)', ylim=range_isc, suppress_range=suppress_range, subtitle=subtitle)

        Workflows.plot_with_range(f, i_c1_fft_min, i_c1_fft_mean, i_c1_fft_max, xlabel='Frequency (Hz)', ylabel='Current (A)', title='Bare conductor - current (FFT)', xscale='log', yscale='log', xlim=(1e6, 1e10), ylim=range_isc_fft, suppress_range=suppress_range, subtitle=subtitle)
        Workflows.plot_with_range(f, i_c2_fft_min, i_c2_fft_mean, i_c2_fft_max, xlabel='Frequency (Hz)', ylabel='Current (A)', title='Shielded conductor - current (FFT)', xscale='log', yscale='log', xlim=(1e6, 1e10), ylim=range_isc_fft, suppress_range=suppress_range, subtitle=subtitle)
        #Workflows.plot_with_range(f, i_c3_fft_min, i_c3_fft_mean, i_c3_fft_max, xlabel='Frequency (Hz)', ylabel='Current (A)', title='Shielded conductor 2 - current (FFT)', xscale='log', yscale='log', xlim=(1e6, 1e10), ylim=range_isc_fft, suppress_range=suppress_range, subtitle=subtitle)
        #Workflows.plot_with_range(f, i_shield_fft_min, i_shield_fft_mean, i_shield_fft_max, xlabel='Frequency (Hz)', ylabel='Current (A)', title='Shield - current (FFT)', xscale='log', yscale='log', xlim=(1e6, 1e10), ylim=range_isc_fft, suppress_range=suppress_range, subtitle=subtitle)

        Workflows.plot_with_range(t, v_c1_min, v_c1_mean, v_c1_max, xlabel='Time (s)', ylabel='Voltage (V)', title='Bare conductor - voltage (time series)', ylim=range_voc, suppress_range=suppress_range, subtitle=subtitle)
        Workflows.plot_with_range(t, v_c2_min, v_c2_mean, v_c2_max, xlabel='Time (s)', ylabel='Voltage (V)', title='Shielded conductor - voltage (time series)', ylim=range_voc, suppress_range=suppress_range, subtitle=subtitle)
        #Workflows.plot_with_range(t, v_c3_min, v_c3_mean, v_c3_max, xlabel='Time (s)', ylabel='Voltage (V)', title='Shielded conductor 2 - voltage (time series)', ylim=range_voc, suppress_range=suppress_range, subtitle=subtitle)
        #Workflows.plot_with_range(t, v_shield_min, v_shield_mean, v_shield_max, xlabel='Time (s)', ylabel='Voltage (V)', title='Shield - voltage (time series)', ylim=range_voc, suppress_range=suppress_range, subtitle=subtitle)

        Workflows.plot_with_range(f, v_c1_fft_min, v_c1_fft_mean, v_c1_fft_max, xlabel='Frequency (Hz)', ylabel='Voltage (V)', title='Bare conductor - voltage (FFT)', xscale='log', yscale='log', xlim=(1e6, 1e10), ylim=range_voc_fft, suppress_range=suppress_range, subtitle=subtitle)
        Workflows.plot_with_range(f, v_c2_fft_min, v_c2_fft_mean, v_c2_fft_max, xlabel='Frequency (Hz)', ylabel='Voltage (V)', title='Shielded conductor - voltage (FFT)', xscale='log', yscale='log', xlim=(1e6, 1e10), ylim=range_voc_fft, suppress_range=suppress_range, subtitle=subtitle)
        #Workflows.plot_with_range(f, v_c3_fft_min, v_c3_fft_mean, v_c3_fft_max, xlabel='Frequency (Hz)', ylabel='Voltage (V)', title='Shielded conductor 2 - voltage (FFT)', xscale='log', yscale='log', xlim=(1e6, 1e10), ylim=range_voc_fft, suppress_range=suppress_range, subtitle=subtitle)
        #Workflows.plot_with_range(f, v_shield_fft_min, v_shield_fft_mean, v_shield_fft_max, xlabel='Frequency (Hz)', ylabel='Voltage (V)', title='Shield - voltage (FFT)', xscale='log', yscale='log', xlim=(1e6, 1e10), ylim=range_voc_fft, suppress_range=suppress_range, subtitle=subtitle)
