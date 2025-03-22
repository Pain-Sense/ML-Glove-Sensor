%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%			README -- CASE_dataset/data/raw
%
% This short guide to the raw data, covers the following topics:
% (1) Preamble.
% (2) Structure of this subfolder.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

-------------------------------------------------------------------------------
(1) Preamble:
-------------------------------------------------------------------------------
The raw data acquired from each participant during the experiment is stored in
two different tab delimited text files. Where, one contains the physiological
(e.g., sub1_DAQ.txt), and the other, the annotation data (e.g.,
sub1_joystick.txt). This was required because the the sampling rates for the DAQ
and annotation setups are different, i.e., 1000 Hz and 20 Hz, respectively.
Due to hardware restrictions, the sampling rate for annotation joystick could
not be set higher than 20 Hz.

The raw data and the pre-processing scripts has been provided such that users
can replicate the processing steps undertaken by us to generate the 
non-interpolated and interpolated data. 

-------------------------------------------------------------------------------
(2) Structure of this subfolder:
-------------------------------------------------------------------------------
This subfolder to the dataset contains the following two folders that
respectively contain the physiological and annotation data for all 30
participants:

(a) CASE_dataset/data/raw/physiological
(b) CASE_dataset/data/raw/annotations

Each of above mentioned subfolders contain a README file explaining the data
present there.
