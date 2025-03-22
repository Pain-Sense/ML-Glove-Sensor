%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%             README -- CASE_dataset/data/raw/physiological
%
% This short guide to the raw physiological data, covers the following topics:
% (1) General Information.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

-------------------------------------------------------------------------------
(1) General Information:
-------------------------------------------------------------------------------
This folder contains the raw physiological data for all 30 subjects.
Each file (e.g., sub1_DAQ.txt) contains the following 9 variables (1 variable
per column), where the 1st variable (i.e. daqtime) was measured in seconds
and the rest of variables are in volts:

(1) daqtime: is the time provided by LabVIEW while logging. It is the global
    time and is also used for annotation files to allow synchronization of
    data across the two files. It is named daqtime to keep the variable name
    different from jstime (used in annotation data).

(2) ecg: data from the Electrocardiogram sensor. 

(3) bvp: data from the Blood Volume Pulse sensor.

(4) gsr: data from the Galvanic Skin Response sensor. 

(5) rsp: data from the Respiration sensor.

(6) skt: data from the Skin Temperature sensor.

(7) emg_zygo: data from the Surface Electromyography (sEMG) sensor placed on the  Zygomaticus major muscles.

(8) emg_coru: data from the Surface Electromyography (sEMG) sensor placed on the Corrugator supercilli muscles.

(9) emg_trap: data from the Surface Electromyography (sEMG) sensor placed on the
Trapezius muscles.


