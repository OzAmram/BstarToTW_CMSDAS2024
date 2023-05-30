# BstarToTW_CMSDAS2023

## Getting started (in bash shell)

### Setup CMSSW environment:
```
ssh -Y USERNAME@lxplus.cern.ch
export SCRAM_ARCH=slc7_amd64_gcc820 
cd ~/public/
mkdir CMSDAS2023 && cd CMSDAS2023
cmsrel CMSSW_11_1_4
cd CMSSW_11_1_4/src
cmsenv
```

### In the `CMSSW_11_1_4/src/` directory, clone this exercise repo:
```
git clone https://github.com/ammitra/BstarToTW_CMSDAS2023.git
```
OR fork the code onto your personal project space and set the upstream:
```
git clone https://github.com/<GitHubUsername>/BstarToTW_CMSDAS2023.git
cd BstarToTW_CMSDAS2023
git remote add upstream https://github.com/ammitra/BstarToTW_CMSDAS2023.git
git remote -v
```

### In the `CMSSW_11_1_4/src/` directory, create a python virtual environment and install TIMBER within it:
```
cd ~/public/CMSDAS2023/CMSSW_11_1_4/src/
git clone https://github.com/ammitra/TIMBER.git
python -m virtualenv timber-env
source timber-env/bin/activate
cd TIMBER
source setup.sh
cd ..
```

You can test that the TIMBER installation is working by running the following in your shell:
```
python -c 'import TIMBER.Analyzer'
```
If all went well, the command should be executed with no output.

### At this point you should have a directory structure that looks like this: 
```
└── ~/public/CMSDAS2023/CMSSW_11_1_4/src/
    ├── TIMBER/
    ├── timber-env/
    └── BstarToTW_CMSDAS2023/
```

## Starting up once environment is set:

Once you have an environment:
```
cd CMSSW_11_1_4/src/
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

## If you need to update BstarToTW_CMSDAS2023
```
cd BstarToTW_CMSDAS2023
git fetch --all
git pull origin master
cd ../
```

## Submitting Condor jobs

Create the appropriate output directory in your EOS space:
```
eosmkdir /store/user/$USER/CMSDAS2023/
eosmkdir /store/user/$USER/CMSDAS2023/rootfiles/
```

**WARNING:** In order for the scripts to work, you must change the `$USER` value in the `condor/run_*.sh` script to your LPC username used in the above step. 


You can now run either your selection, N-1 script, or the script for generating 2D template histograms for 2DAlphabet:

*Selection:*
```
python $CMSSW_BASE/src/BstarToTW_CMSDAS2023/CondorHelper.py -r condor/run_selection.sh -a condor/2016_args.txt -i "bstar.cc bstar_config.json helpers.py"
```

*N - 1:*
```
python $CMSSW_BASE/src/BstarToTW_CMSDAS2023/CondorHelper.py -r condor/run_Nminus1.sh -a condor/2016_args.txt -i "bstar.cc bstar_config.json helpers.py"
```

*2D template histos:*
```
python $CMSSW_BASE/src/BstarToTW_CMSDAS2023/CondorHelper.py -r condor/run_bstar.sh -a condor/2016_args_2DTemplates.txt -i "bstar.cc bstar_config.json helpers.py"
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
eosls /store/user/$USER/CMSDAS2023/rootfiles/
```

To copy file from EOS to local (`-f` overwrites):
```
xrdcp [-f] root://cmseos.fnal.gov//store/user/$USER/CMSDAS2023/rootfiles/FileYouWant.root ./
```

To copy files from local to EOS:
```
xrdcp [-f] FileToSend.root root://cmseos.fnal.gov//store/user/$USER/CMSDAS2023/rootfiles/
```
