# BstarToTW_CMSDAS2025

## Getting started 

## Setup TIMBER environment
Follow the instructions in the [TIMBER Repo](https://github.com/JHU-Tools/TIMBER)
This will create a `CMSSW_12_3_5` release and install TIMBER in it

For convenience these instructions are copied here as well

### TIMBER Install
[Full Documentation](https://lcorcodilos.github.io/TIMBER/)

TIMBER (Tree Interface for Making Binned Events with RDataFrame) is an easy-to-use and fast python analysis framework used to quickly process CMS data sets.
Default arguments assume the use of the NanoAOD format but any ROOT TTree can be processed.

These instructions use python3 and CMSSW. The instructions below have been tested on el8 (lxplus and lpc). To make it work on lxplus9 (el9), the CMSSW version should be changed to CMSSW_13_2_10.

```
cmsrel CMSSW_12_3_5
cd CMSSW_12_3_5/src
cmsenv
python3 -m virtualenv timber-env
git clone git@github.com:JHU-Tools/TIMBER.git
cd TIMBER/
mkdir bin
cd bin
git clone git@github.com:fmtlib/fmt.git
cd ../..
```

Boost library path (the boost version as well!) may change depending on the CMSSW version so this may need to be modified by hand. This version works for both CMSSW versions used for lxplus8 and lxplus9. If one does not wish to use CMSSW, boost libraries will have to be installed (and added to the MakeFile).

Copy the whole multi-line string to the environment activation script

```
cat <<EOT >> timber-env/bin/activate

export BOOSTPATH=/cvmfs/cms.cern.ch/el8_amd64_gcc10/external/boost/1.78.0-0d68c45b1e2660f9d21f29f6d0dbe0a0/lib
if grep -q '\${BOOSTPATH}' <<< '\${LD_LIBRARY_PATH}'
then
  echo 'BOOSTPATH already on LD_LIBRARY_PATH'
else
  export LD_LIBRARY_PATH=\${LD_LIBRARY_PATH}:\${BOOSTPATH}
  echo 'BOOSTPATH added to PATH'
fi
EOT
```

This will activate the python3 environment, set a proper LD_LIBRARY_PATH for boost libraries and build the TIMBER binaries

```
source timber-env/bin/activate
cd TIMBER
source setup.sh
```

You can test that the TIMBER installation is working by running the following in your shell:
```
python -c 'import TIMBER.Analyzer'
```
If all went well, the command should be executed with no output.


## In the `CMSSW_12_3_4/src/` directory, clone this exercise repo:
```
git clone -b lpc-2025 git@github.com:OzAmram/BstarToTW_CMSDAS2024.git BstarToTW_CMSDAS2025 
```


## Starting up once environment is set:

Once you have an environment:
```
cd CMSSW_12_3_4/src/
cmsenv
source timber-env/bin/activate
```
You will need to perform this step *every* time you log on to the LPC cluster.

## If you need to update TIMBER
```
cd TIMBER/
git fetch --all
git checkout master
python setup.py develop
cd ../
```

## If you need to update BstarToTW_CMSDAS2025
```
cd BstarToTW_CMSDAS2025
git fetch --all
git pull origin master
cd ../
```

## Submitting Condor jobs

Create the appropriate output directory in your EOS space:
```
eosmkdir /store/user/$USER/CMSDAS2025/
eosmkdir /store/user/$USER/CMSDAS2025/rootfiles/
```

**WARNING:** In order for the scripts to work, you must change the `$USER` value in the `condor/run_*.sh` script to your LPC username used in the above step. 


You can now run either your selection, N-1 script, or the script for generating 2D template histograms for 2DAlphabet:

*Selection:*
```
python $CMSSW_BASE/src/BstarToTW_CMSDAS2025/CondorHelper.py -r condor/run_selection.sh -a condor/2016_args.txt -i "bstar.cc bstar_config.json helpers.py"
```

*N - 1:*
```
python $CMSSW_BASE/src/BstarToTW_CMSDAS2025/CondorHelper.py -r condor/run_Nminus1.sh -a condor/2016_args.txt -i "bstar.cc bstar_config.json helpers.py"
```

*2D template histos:*
```
python $CMSSW_BASE/src/BstarToTW_CMSDAS2025/CondorHelper.py -r condor/run_bstar.sh -a condor/2016_args_2DTemplates.txt -i "bstar.cc bstar_config.json helpers.py"
```


The argument files for the various years for *selection* and *N - 1* are:
```
condor/2016_args.txt
condor/2017_args.txt
condor/2018_args.txt
```
The argument files for the various years for *2D template histos* are:
```
condor/2016_args_2DTemplates.txt
condor/2017_args_2DTemplates.txt
condor/2018_args_2DTemplates.txt
```

To check the status of your submitted jobs:
```
condor_q $USER
```

To check the progress of your submitted jobs:
```
condor_tail -name lpcschedd<schedd#>.fnal.gov <job ID>
```

To remove a job:
```
condor_rm -name lpcschedd<schedd#>.fnal.gov <job ID>
```

To list contents of directory on EOS:
```
eosls /store/user/$USER/CMSDAS2025/rootfiles/
```

To copy file from EOS to local (`-f` overwrites):
```
xrdcp [-f] root://cmseos.fnal.gov//store/user/$USER/CMSDAS2025/rootfiles/FileYouWant.root ./
```

To copy files from local to EOS:
```
xrdcp [-f] FileToSend.root root://cmseos.fnal.gov//store/user/$USER/CMSDAS2023/rootfiles/
```
