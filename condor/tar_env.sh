cd $CMSSW_BASE/../
tar --exclude-caches-all --exclude-vcs --exclude-caches-all --exclude-vcs -cvzf BstarTW.tgz CMSSW_11_1_4 --exclude=tmp --exclude=".scram" --exclude=".SCRAM" --exclude=CMSSW_11_1_4/src/timber-env --exclude=CMSSW_11_1_4/src/BstarToTW_CMSDAS2024/rootfiles/*.root --exclude=CMSSW_11_1_4/src/BstarToTW_CMSDAS2024/plots --exclude=CMSSW_11_1_4/src/BstarToTW_CMSDAS2023/logs
xrdcp -f BstarTW.tgz root://cmseos.fnal.gov//store/user/cmsdas/2024/long_exercises/BstarTW/BstarTW.tgz
cd $CMSSW_BASE/src/BstarToTW_CMSDAS2024/
