%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%		README -- CASE_dataset/data/non-interpolated
%
% This short guide to the non-interpolated data, covers the following topics:
% (1) Preamble.
% (2) Structure of this subfolder.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

-------------------------------------------------------------------------------
(1) Preamble:
-------------------------------------------------------------------------------
The raw data acquired from each participant during the experiment is stored in
two different tab delimited text files. Where, one contains the physiological,
and the other, the annotation data. This was required because the the sampling
rates for the DAQ and annotation setups are different, i.e., 1000 Hz and 20 Hz,
respectively. Due to hardware restrictions, the sampling rate for annotation
joystick could not be set higher than 20 Hz.

The non-interpolated data is similar to interpolated data in the sense that 
both these data are a result of pre-processing with the difference being that
interpolated data includes an extra step where the data is interpolated to make
sampling frequency consistent across all samples and subjects. As such, we 
recommend that users work with interpolated data. The non-interpolated data 
has been included in the dataset, so that users who don't wish to use our 
interpolation approach can instead work with this data.


-------------------------------------------------------------------------------
(2) Structure of this subfolder:
-------------------------------------------------------------------------------
This subfolder to the dataset contains the following two folders that
respectively contain the physiological and annotation data for all 30
participants:

(a) CASE_dataset/data/non-interpolated/physiological
(b) CASE_dataset/data/non-interpolated/annotations

Each of above mentioned subfolders contain a README file explaining the data
present there.
