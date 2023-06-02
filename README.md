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

To submit Condor jobs on LXPLUS, first create a valid proxy:
```
voms-proxy-init --rfc --voms cms -valid 192:00
```
The x509 proxy will be created and automatically outputted to the default location `/tmp/x509up_u$(id -u)`

Next, copy your proxy to your AFS home directory:
```
cp /tmp/x509up_u$(id -u) ~/
```

You'll now have to modify the JDL (job description language) template provided for you. Open the file `condor/jdl_template` and replace the following two lines with your proxy filename and proxy path. The filename is of the form `x509up_uXXXXXX`, where you can find your user id from the file name, or from `echo $(id -u)`. The proxy path is wherever your AFS home is. Replace the `/a/` with the first letter of your username, and replace the username in the template with your own:
```
Proxy_filename = x509up_u133882
Proxy_path = /afs/cern.ch/user/a/ammitra/$(Proxy_filename)
```

Finally, before submitting the Condor job, you just need to change the directory that the output ROOT file from the job will be sent to. Change the last line in the `condor/run_*.sh` scripts to your username to send the job results to your CERN EOS space:
```
cp -f rootfiles/*.root /eos/home-a/ammitra/
```
should become:
```
cp -f rootfiles/*.root /eos/home-u/username/
```
where `u` is the first letter of your username and `username` is your LXPLUS username. 

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
condor_tail -name bigbird28@cern.ch <job ID>
```

To remove a job:
```
condor_rm -name bigbird28@cern.ch <job ID>
```
