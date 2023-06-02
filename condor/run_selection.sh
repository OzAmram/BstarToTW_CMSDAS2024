#!/bin/bash
echo "Run script starting"
echo "All arguments passed:"
echo $*
echo "Arg 1:"
echo $1
echo "Arg 2:"
echo $2
echo "Arg 3:"
echo $3

ls
source /cvmfs/cms.cern.ch/cmsset_default.sh

export X509_USER_PROXY=$1
echo $(voms-proxy-info -all)
echo $(voms-proxy-info -all -file $1)

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

echo python exercises/selection.py -s $2 -y $3
python exercises/selection.py -s $2 -y $3

cp -f rootfiles/*.root /eos/home-a/ammitra/
