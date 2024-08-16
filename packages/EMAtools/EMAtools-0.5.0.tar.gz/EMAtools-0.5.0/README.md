# <span style="color:black">EMA</span><span style="color:red">tools</span>

# Description

An assortment of computational tools to make life easier for users of EMC Plus and Charge Plus. Focuses on automation of tasks that require:
- Analysis of simulation results
- Bulk editing of simulation files
- Complex preprocessing operations


# Table of Contents

- **[Installation](#installation)**
- **[Examples](#examples)**
- **[Usage](#usage)**
	- **[Results module](#results-module)**
		- **[Loading point probe results](#loading-point-probe-results)**
		- **[Loading box/distributed probe results](#loading-boxdistributed-probe-results)**
		- **[Loading Charge results](#loading-charge-results)**
	- **[Signal module](#signal-module)**
		- **[FFT](#fft)**
		- **[Trimming](#trimming)**
		- **[Padding](#padding)**
		- **[Resampling](#resampling)**
		- **[Statistics](#statistics)**
	- **[EMC module](#emc_module)**
		- **[Shielding from frequency data](#shielding-from-frequency-data)**
		- **[Shielding from timeseries](#shielding-from-timeseries)**
		- **[Shielding from file](#shielding-from-file)**
	- **[File class](#file-class)**
		- **[Instantiating a File object](#instantiating-a-file-object)**
		- **[Accessing contents](#accessing-contents)**
		- **[Viewing contents](#viewing-contents)**
		- **[Searching](#searching)**
		- **[Inserting](#inserting)**
		- **[Removing](#removing)**
		- **[Replacing](#replacing)**
		- **[Saving](#saving)**
	- **[Emin class](#emin-class)**
		- **[Instantiating an Emin object](#instantiating-an-emin-object)**
		- **[Modifying isotropic materials](#modify-isotropic-material)**
		- **[Restricting surface currents](#restrict-surface-current)**
	- **[Inp class](#inp-class)**
		- **[Instantiating an Inp object](#instantiating-an-inp-object)**
		- **[Probing voltage/current](#probing-voltagecurrent)**
	- **[CoupledSim class](#coupledsim-class)**
		- **[Instantiating a CoupledSim object](#instantiating-a-coupledsim-object)**
		- **[Probing current at midpoints](#probing-currents-at-midpoints)**
		- **[Probing voltage at terminations](#probing-voltage-at-terminations)**


# Installation

EMAtools can be installed using the Pip package manager:

```
pip install ematools
```

Check for updates periodically to access new features and improvements:

```
pip install --upgrade ematools
```

Import EMAtools in a Python script or shell:

```
import ema
```


# Examples

This document focuses on technical descriptions of the capabilities of EMAtools. For walkthroughs of practical use cases, please see the following entries in the [Examples](https://github.com/GriffinKowash/EMAtools/tree/main/examples) section of the repository:
- [Shielding effectiveness of an irregular box](https://github.com/GriffinKowash/EMAtools/tree/main/examples#shielding-effectiveness-of-an-irregular-box)
- [Bulk modification of plane wave sources](https://github.com/GriffinKowash/EMAtools/tree/main/examples#bulk-modification-of-plane-wave-sources)



# Usage

When in doubt, refer to inline documention for the feature in question at https://github.com/GriffinKowash/EMAtools/tree/main/src/ema. Please notify Griffin at griffin.kowash@ema3d.com if any conflicts between documentation and true behavior are observed.

## Results module

### Loading point probe results

Any probe results that are formatted with a single timestep per line can be loaded using the `load_probe` function:

```
results = ema.load_probe('path/to/file.dat')
```

If the number of columns in the file is known, the data can be conveniently unpacked into separate variables. For example, since an electric field point probe produces three measurements for X/Y/Z components, it can be unpacked as follows:

```
t, ex, ey, ez = ema.load_probe('efield_probe.dat')
```

Note that for time series results, the first index of the ```results``` array will always provide the time steps.

To reduce memory consumption, data is stored used single-precision (int-32) by default. For double-precision results, provide the `precision` keyword argument:

```
t, ex, ey, ez = ema.load_probe('probe_x64.dat', precision='double')
```


### Loading box/distributed probe results

Box and distributed probe results have a different format and require the `load_box_probe` function or its alias `load_distributed_probe`:

```
t, data = ema.load_box_probe('path/to/box_probe.dat')
```

The `t` array is a 1D NumPy array of the measurement timesteps, while `data` is a 3D array containing the measurement data. By default, `data` has dimensions of [sample, component, time]. The "sample" index refers to the individual sample points defined over the probed region, while "component" corresponds to the X, Y, and Z components of the field measurement. For example, to obtain the Y component at the fifth sample point for every timestep:
  
```
ey_5 = data[4, 1, :]
```


The physical location of each sample point can be determined by reference to the Emin file, where they are listed in the same order along with their mesh indices.
  
  Note that probe results generated by older versions of EMA3D may fail to load due to a difference in file format. The oldest version currently known to be supported is 2023R2.
  
  Precision can be specified in the same way as for the `load_probe` function.
 
 
### Loading Charge results

Any Charge Plus output file ending in `_results.dat` can be loaded using the `load_charge_results` function. For example:

```
t, data = load_charge_results('path/to/picCHARGE_results.dat')
```
 
The function returns a tuple of the time steps and field data, with the field data arranged in the shape [field, node, time].



## Signal module
  
### FFT

A fast Fourier transform (FFT) can be applied to real-valued time series data `t, x` as follows:

```
f, xfft = ema.rfft(t, x)
```

where `f` is the frequency array and `xfft` is the complex-valued result of the FFT operation. Note that `xfft` is normalized such that a sine wave of amplitude *A* will produce a peak of amplitude *A* at the corresponding frequency upon transformation.

  The input array `x` can have arbitrary dimensions, allowing multiple FFTs to be computed simultaneously. For example, the following lines calculate the FFT for all sample points in a box probe:
  
```
t, x = ema.load_box_probe(“box_probe.dat”)
f, xfft = ema.rfft(t, x)
```

`ema.rfft` computes the FFT along the last axis by default; an alternative axis can be specified using the `axis` argument. For example, if axis 0 of `x` corresponds to time while axis 1 contains the X/Y/Z components, the FFT can be computed as:

```
f, xfft = ema.rfft(t, x, axis=0)
```

If the first and last values of a time series measurement are not equal, the discontinuity will introduce erroneous spectral content to the FFT. Window functions are often used to address this problem. For example, the following line applies a Hann window prior to taking the transform:

```
f, xfft = ema.rfft(t, x, window='Hann')
```

The full list of window functions currently supported is shown below. Note that for the Kaiser window, the β parameter is set internally to 14.

- Hann
- Hamming
- Bartlett
- Blackman
- Kaiser


### Trimming

Time series data (timesteps and measurements) can be trimmed to a desired time window. For example, to truncate a dataset to an end time of 5ns:

```
t_trim, x_trim = ema.trim_to_time(t, x, 5e-9)
```

To slice the dataset between 1ns and 5ns:

```
t_trim, x_trim = ema.trim_to_time(t, x, 1e-9, 5e-9)
```

The array `x` may have arbitrary dimensions as long as the last axis corresponds to time.


### Padding

Time series data can be padded to match a desired end time using the `pad_to_time` function. The time steps will automatically be extended under the assumption that they are linearly spaced.

  To pad with zeroes out to 1e-6s:

```
t_pad, x_pad = ema.pad_to_time(t, x, 1e-6)
```

To pad with ones instead of zeroes:

```
t_pad, x_pad = ema.pad_to_time(t, x, 1e-6, val=1)
```

Instead of specifying an end time, a single array can be padded to a particular number of entries using the `pad` function. For example, to pad the array `x` to match the first dimension of another array `y`:

```
x_pad = ema.pad(x, y.shape[0])
```

The array `x` may have arbitrary dimensions as long as the last axis corresponds to time.


### Resampling

Time series data can be resampled to a new set of timesteps using linear interpolation, which is particularly useful when performing frequency domain operations between datasets with different time steps. For example, if a field probe measurement `t, x` has a time step of 1e-11s, but another probe has a time step of 2.67e-11s, it can be resampled to match:

```
t_res, x_res = ema.resample(t, x, 2.67e-11)
```

Instead of resampling to a uniform step size, the user can provide a custom array of monotonically increasing time steps. For example, if `t0` is an array containing the desired time sequence:

```
t_res, x_res = ema.resample(t, x, t0)
```
  
This tool can also be applied to simulations with magnetostatic scaling, where the original time steps are non-uniform. Care should be taken to ensure that the limitations to the frequency content of the original data are understood.

  The array `x` may have arbitrary dimensions as long as the last axis corresponds to time.
  
  
### Statistics

The `statistics` function, also accessible via the alias `stats`, returns the minimum, mean, and maximum of an array. The `axis` argument can be used to specify the desired axis along which to apply the operation. For example, to obtain the statistics along axis 1 of an array `x`:

```
xmin, xmean, xmax = ema.stats(x, axis=1)
```

If an axis is not specified, statistics will be calculated for the array as a whole.


## EMC module

The EMC module contains functionality related to electromagnetic compatibility analysis.


### Shielding from frequency data

The `shielding` function calculates shielding effectiveness from measurement and reference data in the frequency domain. For example, given frequency-domain data `xf` and a reference array `xf_ref`, the shielding effectiveness in decibels can be calculated as:

```
se = ema.shielding(xf, xf_ref)
```

The array `xf` may have arbitrary dimensions, allowing shielding to be calculated for multiple sets of measurements at once. By default, the last axis is expected to correspond to frequency; alternative data structures can be accomodated using the `axis` keyword argument.
  

### Shielding from timeseries

The `shielding_from_timeseries` function accepts time series data and calculates the shielding effectiveness, obviating the need for the user to transform the data to the frequency domain.
  
The measurement array may have arbitrary dimensions, allowing multiple sets of measurements to be processed simultaneously. As an example, the following lines calculate the shielding effectiveness for each sample point in an electric field box probe:
  
```
t, x = ema.load_box_probe("box_probe.dat")
t_ref, x_ref = ema.load_probe("reference_probe.dat")

f, se = ema.shielding_from_timeseries(t, x, x_ref)
```

The measurement array is expected to have time along the last axis and X/Y/Z components along the second-to-last axis. If the user wishes to provide a measurement array without vector components, the best option currently available is to use `np.newaxis` to insert an empty second-to-last axis:

```
x = x[..., np.newaxis, :]
f, se = ema.shielding_from_timeseries(t, x, x_ref)
```

The reference array is not required to have vector components, allowing alternatives to probes such as source waveforms to be used as the reference.

  Note that the measurement and reference arrays must correspond to the same sequence of time steps in order to produce meaningful results. The tools from the `signal` module can be used to fix discrepancies in this respect. For example, if the reference waveform `x_ref` cuts off at 1e-8s while the measurement `x` extends to 1e-6s, padding the reference array to the longer endtime should produce a valid result:

```
t_ref_pad, x_ref_pad = ema.pad_to_time(t_ref, x_ref, 1e-6)
f, se = ema.shielding_from_timeseries(t, x, x_ref_pad)
```

If the arrays still have minor discrepancies due to machine precision issues, or if the time step intervals are different, the padded array can be resampled to exactly match the timesteps of the measured data:

```
t_ref_resamp, x_ref_resamp = ema.resample(t_ref_pad, x_ref_pad, t)
```


### Shielding from file

If shielding is to be computed using results from two electric field point probes, the `shielding_from_file` function can be used to automate the entire calculation. Provided paths `path` and `ref_path` to the respective probe result files, the shielding effectiveness can be computed as follows:

```
path = "path/to/probe.dat"
ref_path = "path/to/reference.dat"

f, se = ema.shielding_from_file(path, ref_path)
```

Note that this function does not currently support box and distributed probes.



## File class

The `Emin`, `Inp`, and `Cin` classes help streamline the pre-processing workflow in two ways:
- By enabling the bulk modification of arbitrarily many simulation files
- By providing functionality that is impractical or impossible to achieve manually

All three classes inherit their base functionality from the `File` class, which contains general methods to facilitate the editing of simulation files. These are the core tools used to implement more complex operations specific to each file type.

### Instantiating a File object
A File object is instantiated by providing a file path to the constructor:

```
from ema import File
file = File('path/to/file.ext')
```

In practice, one will typically use one of the simulation-specific child classes:

```
from ema import Emin, Inp, Cin

emin = Emin('path/to/file.emin')
inp = Inp('path/to/file.inp')
cin = Cin ('path/to/file.cin')
```

### Accessing contents
A list of all lines in the file is stored in the `lines` attribute. To access lines 10 through 20, which correspond to indices 9 thorugh 19:

```
section = file.lines[9:20]
```

As shown above, slice notation requires the final index to be incremented by one in order to return the desired endpoint. For more intuitive and readable code, the endpoint-inclusive `File.get` method can be used instead. For the example above:

```
section_10_20 = file.get(9, 19)
```

To obtain just one line, a single index can be provided as an argument. For example, to access line 17:

```
line_17 = file.get(16)
```

For convenience, the wrapper method `File.getlines` accepts line numbers (one-indexed) instead of list indices (zero-indexed). The previous two examples can be rewritten as follows:

```
section_10_20 = file.getlines(10, 20)
line_17 = file.getlines(17)
```

### Viewing contents

The `File.printlines` method prints a line or range of lines to the console with readable formatting, which is useful when testing a script's functionality. For example, using an Emin file for demonstration, executing `file.printlines(10, 15)` will print the following to the console:

```
10 	| * -----------------------------------------------------------------------------
11 	| * ---------------------------------- GENERAL ----------------------------------
12 	| * -----------------------------------------------------------------------------
13 	| 
14 	| !MPIBLOCKS
15 	| 6    3    4   
```

Alternatively, a list of line numbers can be provided. For example, `file.printlines([1, 14, 25])` will print the following:

```
1 	| * File Name: test.emin
14 	| !MPIBLOCKS
25 	| !EMRESULTS
```

The `File.print` method performs the same function but accepts indices (0-indexed) instead of line numbers (1-indexed). For the examples above, `file.print(9, 14)` and `file.print([0, 13, 24])` would produce identical results.

The `File.head` method is a wrapper for `File.printlines` that displays the first `n` lines, where `n` is an integer provided as an argument. For example, running `file.head(5)` will display the following:

```
1 	| * File Name: test.emin
2 	| * Created  : Tue, 05 Sep 08:39:11 GMT-06:00  
3 	| * DO NOT MODIFY >>>       
4 	| * <Cached>test_.sav</Cached>
5 	| * <CachedId>28120648-340b-4e3a-8138-63381f05d812</CachedId>
```

By default, the result is printed with line numbers and indentation for readability. To suppress this behavior, set the optional argument `numbered` to `False` in any of the print methods described above. For example, executing `file.head(5, numbered=False)` outputs the following:

```
* File Name: test.emin
* Created  : Tue, 05 Sep 08:39:11 GMT-06:00  
* DO NOT MODIFY >>>       
* <Cached>test_.sav</Cached>
* <CachedId>28120648-340b-4e3a-8138-63381f05d812</CachedId>
```


### Searching

#### Find all

Any change to a simulation file typically begins with locating a particular string of text. The base function for this task is `File.find_all`, which returns a list of all indices at which the provided search string is present in the file. For example, to search for every instance of `!NEW PROBE FILE NAME`:

```
probe_indices = file.find_all('!NEW PROBE FILE NAME')
```

Printing the result using `file.print(probe_indices)` reveals that several probes have been identified in the file:

```
121 	| !NEW PROBE FILE NAME
131 	| !NEW PROBE FILE NAME
141 	| !NEW PROBE FILE NAME
151 	| !NEW PROBE FILE NAME
161 	| !NEW PROBE FILE NAME
171 	| !NEW PROBE FILE NAME
```

Several optional keyword arguments can be set to refine the search parameters. 

- `start` specifies an index at which to begin searching, with all previous lines being omitted from the search. (Default 0)

- `exact` is a boolean that determines whether a line must exactly match or simply contain the search string. (Default False)

- `separator` is an optional string that modifies the behavior of `exact` mode; [see explanation below](#separator-keyword).
  
- `case` is a boolean that determines whether the comparison against the search string should be case-sensitive. (Default True)
  
- `n_max` is an integer that interrupts the search operation after `n_max` number of instances have been found, which can reduce search time when working with large files. (Default None)

As an example, the following command will locate case-insensitive exact matches to the string "* geometry: line", beginning at index 150 and exiting after five matches have been found:
  
  ```
  indices = file.find_all('* geometry: line', start=150, exact=True, case=False, n_max=5)
  ```
  
#### Find
  
 `File.find` is a wrapper method for `File.find_all` that finds a single match to the search string rather than returning a list of all matches. To find the first instance of "!NEW PROBE FILE NAME":

```
file.find('!NEW PROBE FILE NAME')
```

The positional argument `n` can be used to locate the nth instance of the search string. For example, to find the index of the fifth probe defined in the file:

```
file.find('!NEW PROBE FILE NAME', 5)
```

The same keyword arguments used by `File.find_all` can also be provided to `File.find`, apart from `n_max`, which is automatically set to `n`.

#### Find next

  Finally, the `File.find_next` method provides a convenient syntax for finding the next occurrence of a text string after a specified index. For example, after finding the starting index of a current source definition, a user may wish to locate the next blank line in the file:
  
```
source_index = file.find('SOURCE NAME: Current Source')
next_blank = file.find_next(source_index, '')
```

#### Separator keyword

The `separator` argument is only used with `exact=True` and allows a non-endline separator to be specified when searching for an exact match. During the search process, each line is split into separate strings at instances of the separator, and the search text is compared against each resulting string rather than against the line as a whole.

 Setting the separator to an empty string will split each line by whitespace. Instead of a string, multiple separators can be specified in a list or tuple; for example, providing `separator=['(', ')']` will split each line by open and closed parentheses. Any standard regular expression may also be used. This option is supported for all of the search methods described above.

 For a practical use case, consider that segment names in MHARNESS files have topology information encoded using underscores; for example, "SEG5___S0___C0" indicates a conductor nested in a shield along segment SEG5. If the user wishes to find occurrences of SEG5 that do *not* contain topology information, executing `file.find('SEG5')` will yield false positives, since "SEG5" is a partial match for "SEG5___S0___C0". On the other hand, `file.find('SEG5', exact=True)` will likely yield no results, since an "exact" search only identifies exact matches to entire lines, and additional information will typically be present in the same line.

 The desired result can be achieved by executing `file.find('SEG5', exact=True, separator='')`, with an empty string as the separator. This will only flag occurrences of "SEG5" that are surrounded by whitespace, which excludes instances with topology information, and it will not overlook lines where additional, whitespace-delimited information is present.



### Inserting

The `File.insert` method allows the user to insert one or more lines at a given index. For example, utilizing `File.find` from the previous section, a comment can be inserted at the index of the line "!SUMMARY":

```
index = file.find('!SUMMARY', exact=True)
file.insert(index, 'Comment inserted before "!SUMMARY"')
```

Note that this operation displaces the line previously located at the target index, which results in the new text being positioned immediately before it in the file. To insert the text after the target index instead, the `File.insert_after` method can be used:

```
index = file.find('!SUMMARY', exact=True)
file.insert_after(index, 'Comment inserted after "!SUMMARY")
```

Calling `file.print(index-1, index+1)` illustrates the difference between the two insertion methods:

```
22 	| * Comment inserted before "!SUMMARY"
23 	| !SUMMARY
24 	| * Comment inserted after "!SUMMARY"
```

If the `text` argument is a list of strings, multiple lines will be inserted. For example, executing

```
text = ['!MAGNETOSTATIC',
	'2.0000000000E-010   	1.0000000000E+000',
	'6.5000000000E-006   	2.0000000000E+001',
	'2.5000000000E-004   	1.0000000000E+003']
		
file.insert(file.find('!TIME STEPS') + 3, text)
```

will insert a list of magnetostatic scaling intervals after the timestep definition:

```
34 	| !TIME STEPS
35 	| 1.0000000000E-010   	5000000 
36 	| 
37 	| !MAGNETOSTATIC
38 	| 2.0000000000E-010   	1.0000000000E+000
39 	| 6.5000000000E-006   	2.0000000000E+001
40 	| 2.5000000000E-004   	1.0000000000E+003
```


### Removing

The `File.remove` method removes the line located at a specified index. To remove the line at index 15:

```
file.remove(15)
```

The method can also accept an endpoint-inclusive interval of indices to remove. For example, to remove all lines between indices 15 and 20:

```
file.remove(15, 20)
```


### Replacing

The `File.replace` method combines the functionality of `File.remove` and `File.insert` to help the user replace one or more lines in the file with new text. To replace the line at index 15 with a comment:

```
file.replace(15, '* Replaced index 15 with one comment')
```

The user can instead provide an endpoint-inclusive range of indices to replace:

```
file.replace((15, 20), '* Replaced indices 15 to 20 with one comment')
```

Multiple lines of new text can be added by providing a list of strings:

```
file.replace(15, ['* Replaced index 15', '* with two comments'])
```


### Saving

The operations described above only affect the `file.lines` buffer. To save all changes to the original file, call the `File.save` method with no arguments:

```
file.save()
```

To save the file to a new location instead of overwriting the original, provide the new file path as an argument:

```
file.save('path/to/new/file.ext')
```


## Emin class

The `Emin` class inherits all functionality of the `File` class described above and implements several methods specific to EMC Plus.


### Instantiating an Emin object

As with the `File` parent class, an `Emin` object is instantiated from a file path:

```
from ema import Emin
emin = Emin('path/to/file.emin')
```


### Modifying isotropic materials

The `Emin.modify_isotropic_material` method allows the user to modify the physical properties of all instances of an isotropic material. For example, the conductivity of a material named "CFRP" can be set to 300 S/m as follows:

```
emin.modify_isotropic_material('CRFP', sig=300)
```

The following keyword arguments can optionally be provided:
- `sig` — electric conductivity
- `sigm` — magnetic conductivity
- `eps` — absolute permittivity
- `mu` — absolute permeability
- `eps_rel` — relative permittivity
- `mu_rel` — relative permeability

Note that if both `eps_rel` and `eps` or `mu_rel` and `mu` are provided, the relative value will be used and the absolute value discarded.


### Restricting surface currents

As of EMA3D 2024R1, surface current definitions are always generated with current elements in both of the tangent directions. The `Emin.restrict_surface_current` method restricts the surface current to a single coordinate direction. One application of this tool is shielding effectiveness submodels, where it may be desirable to use a surface current to generate a plane wave polarized along a coordinate axis.

  The method is called with a string specifying the desired direction (x, y, or z) of the current. For example, to restrict the current to the y direction:
  
```
Emin.restrict_surface_current("y")
```

Prior to the method call, the source definition contains both x- and y-oriented current elements:

```
86 	| !CURRENT DENSITY SOURCE
87 	| !!ELECT
88 	| !!!1PNT
89 	| SourceCurrent.dat
90 	| 2    2    991  1.0000000000E+000    0.0000000000E+000    0.0000000000E+000   
91 	| 2    2    991  0.0000000000E+000    1.0000000000E+000    0.0000000000E+000   
92 	| 3    2    991  1.0000000000E+000    0.0000000000E+000    0.0000000000E+000   
93 	| 3    2    991  0.0000000000E+000    1.0000000000E+000    0.0000000000E+000  
..... 
```

Afterward, only the y-oriented elements remain:

```
86 	| !CURRENT DENSITY SOURCE
87 	| !!ELECT
88 	| !!!1PNT
89 	| SourceCurrent.dat
90 	| 2    2    991  0.0000000000E+000    1.0000000000E+000    0.0000000000E+000   
91 	| 3    2    991  0.0000000000E+000    1.0000000000E+000    0.0000000000E+000   
92 	| 3    3    991  0.0000000000E+000    1.0000000000E+000    0.0000000000E+000   
93 	| 2    3    991  0.0000000000E+000    1.0000000000E+000    0.0000000000E+000  
..... 
```

If no current elements are aligned in the requested direction, the probe definition will remain unchanged and a warning will be raised.


## Inp class

The Inp class inherits all functionality of the File class described above and implements several methods specific to MHARNESS.


### Instantiating an Inp object

As with the `File` parent class, an `Inp` object is instantiated from a file path:

```
from ema import Inp
inp = Inp('path/to/file.inp')
```


### Probing voltage/current

The `Inp.probe_voltage` and `Inp.probe_current` methods allow the user to add voltage and current pin probes to a harness.

  The three required arguments are:
- `segment` — name of the MHARNESS segment to probe
- `conductor` — name of the conductor within the segment
- `index` — mesh index at which to place probe

The following keyword arguments are optional:
- `name` — name of probe, used for output filename
- `start` — measurement start time; zero by default
- `end` — measurement end time; matches domain by default
- `timestep` — measurement timestep; matches domain by default

For example, the following command places a voltage probe on conductor C1 in segment SEG at mesh index 12 with default time settings:

```
inp.probe_voltage("SEG", "C1", 12)
```

To create a current probe at the same location with alternative name and time settings:

```
inp.probe_current("SEG", "C1", 12, name='current_probe', start=1e-9, end=1e-7, timestep=1e-12)
```

`Inp.print` can be used to view the result of the previous two operations:

```
116 	| * -----------------------------------------------------------------------------
117 	| * ------------------------ Section 14: OUTPUT / PROBES ------------------------
118 	| * -----------------------------------------------------------------------------
119 	| 
120 	| !PROBE
121 	| !!CABLE CURRENT
122 	| current_probe.dat  
123 	| 1.0000000000E-09    1.0000000000E-07    1.0000000000E-12   
124 	| SEG      C1      12  
125 	| 
126 	| !PROBE
127 	| !!CABLE VOLTAGE
128 	| voltage_SEG_C1_12.dat  
129 	| 0.0000000000E+00    9.9999812000E-07    8.3600000000E-12   
130 	| SEG      C1      12  
```

Note that `Inp.probe_voltage` and `Inp.probe_current` do not verify whether the segment and conductor names provided by the user actually exist in the harness.


## CoupledSim class

The CoupledSim class provides functionality specific to coupled EMA3D/MHARNESS simulations.

### Instantiating a CoupledSim object

To instantiate a `CoupledSim` object, first import the `Emin`, `Inp`, and `CoupledSim` classes:

```
from ema import Emin, Inp, CoupledSim
```

Next, load the simulation input files as `Emin` and `Inp` objects, as described in the previous sections:

```
emin = Emin('path/to/file.emin')
inp = Inp('path/to/file.inp')
```

Finally, pass the `Emin` and `Inp` objects as arguments to the `CoupledSim` constructor:
```
coupled = CoupledSim(emin, inp)
```


### Probing currents at midpoints

Manually placing current probes on a harness can be extremely time intensive when working with large models. The `probe_midpoint_currents` method automates this procedure by detecting points of interest in the harness and adding probe definitions to the input file.

 Probes are placed at the midpoint of each unbranching chain of MHARNESS segments comprising a given conductor. This ensures that all unique currents in the conductor are captured without requiring a probe to be placed on every segment.

 The image below shows the probe placement generated for an example conductor. Since the conductor is not routed into `SEG1` (top right), segments `SEG` and `SEG2` are treated as a single, continuous current path. The `probe_midpoint_currents` method therefore places a single probe at their combined midpoint rather than placing one on `SEG` and another on `SEG2`.

 <p align="center"><img src="resources/readme_midpoint_probes.png" /></p>
 <p align="center">Figure 1: Placement of current probes by CoupledSim.probe_midpoint_currents</p>
 <br>

 After creating a `CoupledSim` object as described above, simply call the `probe_midpoint_currents` method:

```
coupled.probe_midpoint_currents()
```

By default, this method places current probes on every conductor in the harness. To probe a single conductor, pass the conductor name as a positional argument:

```
coupled.probe_midpoint_currents('Conductor_1')
```

To probe several conductors, provide a list of names:

```
coupled.probe_midpoint_currents(['Conductor_1', 'Conductor_2'])
```

If additional information from the algorithm is desired for debugging purposes, set the `verbose` keyword argument to `True`:

```
coupled.probe_midpoint_currents('Conductor_1', verbose=True)
```


### Probing voltage at terminations

The `CoupledSim` class also supports automatic probing of conductor terminations. After creating a `CoupledSim` object as described above, call the  `probe_termination_voltages` method:

```
coupled.probe_termination_voltages()
```

As with `CoupledSim.probe_midpoint_currents`, a conductor or list of conductors can optionally be provided:

```
coupled.probe_termination_voltages('Conductor_1')
coupled.probe_termination_voltages(['Conductor_3, 'Conductor_4'])
```

By default, this method places probes on all conductor terminations; however, for open-circuit voltage analysis, it is generally only necessary to probe high-resistance terminations. To exclude terminations below a minimum resistance, specify a cutoff using the `threshold` keyword argument:

```
coupled.probe_termination_voltages(threshold=1e6)
```

Note that any conductor endpoints without defined terminations will be ignored by this method.