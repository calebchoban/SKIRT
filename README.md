# SKIRT Test Run

This example downloads, compiles, and runs the radiative transfer code SKIRT, following the instructions provided on the SKIRT [website](https://skirt.ugent.be/root/_home.html).

First, download and compile SKIRT with
```console
make compile
```
This will take a while. At the end it will ask you about downloading SKIRT resources, say yes to only SKIRT9\_Resources\_Core for now. It's usually all you ever need.

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

If there is an issue with the install clean up the directory first before retrying using
```console
make purge
```

Now you want to edit your .bash\_rc file so that everytime you login to the supercomputer SKIRT will be ready to use. Add the following lines to your .bash\_rc in your $HOME directory
```console
# Setup SKIRT
module load cmake
export PATH="$HOME/SKIRT/release/SKIRT/main:${PATH}"
```
If you cloned SKIRT to a different directory you will need to edit the above path to the directory you specified.
To check if this works logout and back into the supercomputer and run the skirt command again. If the skirt command cannot be found then something went wrong.

Second, if you want to set up your own parameters for SKIRT build SKIRT using 
```console
make build
```
This will step you through creating a .ski file with user specified dust properties. Tutorials can be found [here](https://skirt.ugent.be/version9/_tutorials.html). Fair warning, this Q&A process can be long.

Some preset SKIRT builds for FIRE snapshots are already provided in the sample folder. Sample\_MW.ski is for MW like dust species, and Sample\_SMC.ski is for SMC like dust species.

You can also edit .ski files directly if you know what you are doing and want to create custom dust mixes! Tutorials can be found [here](https://skirt.ugent.be/version9/_tutorial_custom_dust.html).

Now you need to prepare the data from FIRE snaps to be used by SKIRT. Edit the parameters in run.py to get data from the snapshot you want and what data you want to include. Then process your snapshot using
```console
make compile_data
```

Before submitting the SKIRT job to the queue edit job.pbs to make sure you are using the correct number of processes and threads. It's recommended that you use 4-8 threads per process. Also add your email if you want email updates.

Last, submit your SKIRT job using
```console
make submit
```

After SKIRT is finished running, all outputs can be found in the output directory.

Note that for the default setup provided this takes <1 hour for m12i at z=0.



