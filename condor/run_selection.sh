#!/bin/bash
echo "Run script starting"
ls
source /cvmfs/cms.cern.ch/cmsset_default.sh
cp /eos/user/c/cmsdas/2023/long-ex-b2g/BstarTW.tgz ./
scramv1 project CMSSW CMSSW_11_1_4
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
cp -r * ../CMSSW_11_1_4/src/BstarToTW_CMSDAS2023/; cd ../CMSSW_11_1_4/src/
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
cd ../BstarToTW_CMSDAS2023
rm rootfiles/*.root

echo python exercises/selection.py $*
python exercises/selection.py $*

cp -f rootfiles/*.root /eos/home-a/ammitra/
