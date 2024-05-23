# SKIRT Test Run

This example downloads, compiles, and runs the radiative transfer code SKIRT, following the instructions provided on the SKIRT [website](https://skirt.ugent.be/root/_home.html).

First, download and compile SKIRT with
```console
make compile
```
This will take a while. At the end it will ask you about downloading SKIRT resources, say yes to only SKIRT9\_Resources\_Core for now. It's usually all you ever need.

If there is an issue with the install, before rerunning the above command run the purge command before retrying again
```console
make purge
```

To confirm the installation is successful run
```console
skirt
```
This should output
```console
(mini) cchoban@login1:~/SKIRT/git> skirt
17/05/2024 15:48:07.264   Welcome to SKIRT v9.0 (git 3c9e4d7 built on 17/05/2024 at 15:20:47)
17/05/2024 15:48:07.264   Running on login1 for cchoban
17/05/2024 15:48:07.405   Interactively constructing a simulation...
17/05/2024 15:48:07.405 ? Enter the name of the ski file to be created:
```
Then use [CTRL] + C to exit the program.



Now you want to edit your .bash\_rc file so that everytime you login to the supercomputer SKIRT will be ready to use. Add the following lines to your .bash\_rc in your $HOME directory
```console
# Setup SKIRT
module load cmake
export PATH="$HOME/SKIRT/release/SKIRT/main:${PATH}"
```
If you cloned SKIRT to a different directory you will need to edit the above path to the directory you specified.
To check if this works logout and back into the supercomputer and run the skirt command again. If the skirt command cannot be found then something went wrong.

Second, if you want to set up your own parameters for SKIRT run skirt without any arguments 
```console
skirt
```
This will step you through creating a .ski file with user specified dust properties. Tutorials can be found [here](https://skirt.ugent.be/version9/_tutorials.html). Fair warning, this Q&A process can be long.

A preset SKIRT build for FIRE snapshots is provided in the sample folder, labelled basic\_MW.ski. This .ski is set such that the star and gas data are provided as star.dat and gas.dat, it uses a Milky-Way dust population from Weingartner & Draine (2001), and has 3 camera instruments (at 0, 45, and 90 degrees) which produce spectral data cubes.

You can also edit .ski files directly if you know what you are doing. If you have minor changes to make this is faster than using the Q&A process. Tutorials can be found [here](https://skirt.ugent.be/version9/_tutorial_custom_dust.html).

To prepare the data from FIRE snaps to be used by SKIRT, use the data_reduction Jupyter notebook in the ntbk/ directory. Note this script uses functions from my [crc_scripts](https://github.com/calebchoban/crc_scripts/) repository, so you will need to install that first.

To run SKIRT you will first want to have star.dat, gas.dat, and the .ski file you want to use in the same folder (names out.ski in the below example). You now have two options to run SKIRT on Big Red 200. 1) Use the submission script job.sh. Copy this into the same folder as the other files, replace EMAIL in job.sh with your email, and then run
```console
qsub job.sh
```
This will make a new output folder and all the SKIRT output will be saved there. 2) You can run SKIRT in an interactive session. This is useful when you want to debug things and don't want to wait for each job to get through the SLURM queue. To submit an interactive job that has the same resources as the job.sh script run and a 1 hr time limit
```console
salloc -p general -A r00380 --nodes=1 --ntasks-per-node=4 --cpus-per-task=8 --mem=50G -t 1:00:00
```
Once this is running, you can run the same lines of codes as in job.sh.

Note that for the default setup provided this should take ~15 minutes to run for a Milky Way-like galaxy.


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
Note that some PTS fuctionality uses Python packages you may not have installed. PTS will let you know if you need to install a package.
