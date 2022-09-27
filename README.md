# SKIRT Test Run

This example downloads, compiles, and runs SKIRT.

First, download and compile SKIRT (this can take a while)
```console
make compile
```

If there is an issue with the install clean up the directory first before retrying using
```console
make purge
```

Second, if you want to set up your own parameters for SKIRT build SKIRT using (make sure to not do this on the login node and is a long Q&A process)
```console
make build
```
This will step you through creating a .ski file with user specified dust properties. Tutorials can be found [here](https://skirt.ugent.be/version9/_tutorials.html).

Some preset SKIRT builds for FIRE snapshots are already provided in the sample folder. Sample_MW.ski is for MW like dust species, and Sample_SMC.ski is for SMC like dust species.

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

Note that for the default TSCC setup provided this takes <1 hour for m12i at z=0.



