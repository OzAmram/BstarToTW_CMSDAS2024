#!/bin/bash
echo "Run script starting"
ls
source /cvmfs/cms.cern.ch/cmsset_default.sh
xrdcp root://cmseos.fnal.gov//store/user/cmsdas/2025/long_exercises/BstarTW/BstarTW.tgz ./
scramv1 project CMSSW CMSSW_12_3_5
tar -xzvf BstarTW.tgz
rm BstarTW.tgz
rm *.root
echo "Current working directory path: ---------------------------------------"
pwd
echo "Current working directory contents: -----------------------------------"
ls
echo "-----------------------------------------------------------------------"

mkdir tardir; cp tarball.tgz tardir/; cd tardir/
echo "Current working directory path: ---------------------------------------"
pwd
echo "-----------------------------------------------------------------------"
tar -xzf tarball.tgz; rm tarball.tgz
cp -r * ../CMSSW_12_3_5/src/BstarToTW_CMSDAS2025/; cd ../CMSSW_12_3_5/src/
echo 'IN RELEASE'
echo "Current working directory path: ---------------------------------------"
pwd
echo "Current working directory contents: -----------------------------------"
ls
echo "-----------------------------------------------------------------------"
eval `scramv1 runtime -sh`
rm -rf timber-env
python -m virtualenv timber-env
source timber-env/bin/activate
cd TIMBER
source setup.sh
cd ../BstarToTW_CMSDAS2025
rm rootfiles/*.root

echo python exercises/selection.py $*
python exercises/selection.py $*

xrdcp -f rootfiles/*.root root://cmseos.fnal.gov//store/user/$USER/CMSDAS2025/rootfiles/
