# Installing SKIRT

This repo downloads and compiles the radiative transfer code SKIRT, following the instructions provided on the SKIRT [website](https://skirt.ugent.be/root/_home.html). 
Jupyter notebooks for reducing FIRE snapshot data for SKIRT, creating template SKIRT parameter files, and simple IO for SKIRT output FITS files are provided in the **/ntbk** directory and are discussed below.


To download and compile SKIRT run the below command from the main directory.
```console
make compile
```
This will take a while. At the end it will ask you about downloading SKIRT resources, say yes to `SKIRT9_Resources_Core` and `SKIRT9_Resources_ExtraBands` (this includes extra band pass filters you may want) for now. These are usually all you need and the extra resources can take up >100 GB of space. If you end up trying to use a resource you do not have installed SKIRT will throw a "no resource" error. To download resources after installing SKIRT, run the shell script in the `/git` directory.
```console
./git/downloadResources.sh 
```


If there is an issue with the install, before rerunning the compile command run the purge command to clear up any lingering files.
```console
make purge
```

To confirm the installation is successful run
```console
./release/SKIRT/main/skirt
```
This should output
```console
(mini) cchoban@login1:~/SKIRT/git> ./release/SKIRT/main/skirt
17/05/2024 15:48:07.264   Welcome to SKIRT v9.0 (git 3c9e4d7 built on 17/05/2024 at 15:20:47)
17/05/2024 15:48:07.264   Running on login1 for cchoban
17/05/2024 15:48:07.405   Interactively constructing a simulation...
17/05/2024 15:48:07.405 ? Enter the name of the ski file to be created:
```
Then use [CTRL] + C to exit the program.


To make the SKIRT program callable every time you login to the supercomputer SKIRT edit your `.bash_rc` file in your your $HOME directory by adding the following lines.
```console
# Setup SKIRT
module load cmake # Make sure this is the how you load the cmake module on your preferred supercomputer
export PATH="$HOME/SKIRT/release/SKIRT/main:${PATH}"
```
If you downloaded SKIRT to a different directory you will need to edit the above path to the directory you specified.
To check if this works logout and back into the supercomputer and run the skirt command again. If the skirt command cannot be found then something went wrong.

## Creating SKIRT parameter files from scratch

If you want to set up your own parameters for SKIRT run skirt without any arguments 
```console
skirt
```
This will step you through creating a .ski file with user specified properties. Tutorials can be found [here](https://skirt.ugent.be/version9/_tutorials.html). Fair warning, this Q&A process can be long.

A few template SKIRT builds for FIRE snapshots are provided in the **/ntbk** folder. 

You can edit .ski files directly if you know what you are doing. If you have minor changes to make this is faster than using the Q&A process. Tutorials can be found [here](https://skirt.ugent.be/version9/_tutorial_custom_dust.html).

# Reducing FIRE Snapshot Data

To prepare the data from FIRE snaps to be used by SKIRT, use the `data_reduction.ipynb` Jupyter notebook in the **/ntbk** \ directory. Note this script uses functions from my [crc_scripts](https://github.com/calebchoban/crc_scripts/) repository, so you will need to install that first.

# Creating SKIRT Parameter Files

To create SKIRT parameter files from a template, use the `set_input_params.ipynb` Jupyter notebook in the **/ntbk**  directory. 

# Running SKIRT on a Supercomputer

To run SKIRT you will first want to have stars.dat, dust.dat, and the .ski file you want to use in the same folder (named run.ski in the below example). You now have two options to run SKIRT on Big Red 200 (note job scripts will need to be edited for use on other supercomputers) shown below. Note, SKIRT can use a lot of RAM. The RAM usage scales with the number of instruments and their resolution so the more of them you have and the finer the resolution the more RAM you will need. The template examples have 6 instruments with numerous broad bands which use a lot of memory so make sure you have ~220GB of memory allocated in the example job scripts below.

1) Use the submission script job.sh. Copy the jobs submission script into the same folder as the other files, replace EMAIL in job.sh with your email, and then run
```console
qsub job.sh
```
This will make a new output folder and all the SKIRT output will be saved there. Note that SKIRT can use a large amount of RAM depending on how many instruments and probes are used. The template examples have 6 instruments with many broadbands so it will use a lot of memory.

2) You can run SKIRT in an interactive session. This is useful when you want to debug things and don't want to wait for each job to get through the SLURM queue. To submit an interactive job that has the same resources as the job.sh script run and a 1 hr time limit
```console
salloc -p general -A r00380 --nodes=1 --ntasks-per-node=4 --cpus-per-task=8 --mem=220G -t 1:00:00
```
Once this is running, you can run the same lines of codes as in job.sh.

Note that for the default setup provided this should take ~15 minutes to run for a Milky Way-mass galaxy.

# Creating Broadband Images From SKIRT Outputs

Use the `mock_image.ipynb` Juypter notebook to create mock broadband and 3-color images from the outputs.


# SKIRT Python Analysis Tools

If you want to install the premade analysis scripts provided by SKIRT, called PTS, run
```console
qsub pts
```
Then add these two lines to your .bashrc
```console
export PYTHONPATH=$HOME/SKIRT/PTS
alias pts="python -m pts.do"
```
Again, if you cloned SKIRT to a different directory you will need to edit the above path to the directory you specified.
To test that PTS is installed run
```console
pts try me
```
The output should be similar to
```console
23/05/2024 12:48:48.690   Starting admin/try_do...
23/05/2024 12:48:48.690   Command line arguments are:
23/05/2024 12:48:48.690     Fixed string:    me
23/05/2024 12:48:48.690     Optional string: PTS is great
23/05/2024 12:48:48.690     Float number:    3.14
23/05/2024 12:48:48.690     Integer number:  7
23/05/2024 12:48:48.690   Finished admin/try_do.
```
Note that some PTS functionality uses Python packages you may not have installed. PTS will let you know if you need to install a package.


# General Tips

Here is a list of general tips we have encountered

* Test/Debugging: When creating mock images to compare to surveys or observations, tests/debugging are best done with high instrument resolution. Once you want to compare with your observational survey, set the instrument resolution to the resolution of the survey to avoid having to down-sample the outputs later on.
* Convergence: The higher the resolution of your instrument, the larger the photon packet required for convergence and the higher the resolution needed for the octotree grid. To check convergence of photometric images follow the [SKIRT guidelines](https://skirt.ugent.be/root/_user_statistics.html). Convergence will also vary with wavelength.
* Octotree vs Voronoi: During photometric image testing, we have found using the postprocessed octotree is best for high spatial resolution images. If your problem does not require high spatial resolution the Voronoi tesselation medium grid may be better since it both greatly shortens the run times and converges well.
* Medium Spatial Extent: Note that when defining the extent of the spatial domain in SKIRT, only gas/dust medium data inside the domain will be included BUT all star data will be included. For example, if you give the entire snapshot star and dust/gas data, but define the SKIRT domain to a small 1 kpc box, only gas/dust data in the box will be used for the radiative transfer BUT all of the star particle data will be used for primary emission! Best practice is to only extract star and dust/gas particle data from the domain you want to run SKIRT for.