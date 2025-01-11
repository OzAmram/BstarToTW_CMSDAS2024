cd $CMSSW_BASE/../
tar --exclude-caches-all --exclude-vcs --exclude-caches-all --exclude-vcs -cvzf BstarTW.tgz CMSSW_12_3_5 --exclude=tmp --exclude=".scram" --exclude=".SCRAM" --exclude=CMSSW_12_3_5/src/timber-env --exclude=CMSSW_12_3_5/src/BstarToTW_CMSDAS2025/rootfiles/*.root --exclude=CMSSW_12_3_5/src/BstarToTW_CMSDAS2025/plots --exclude=CMSSW_12_3_5/src/BstarToTW_CMSDAS2023/logs
xrdcp -f BstarTW.tgz root://cmseos.fnal.gov//store/user/cmsdas/2025/long_exercises/BstarTW/BstarTW.tgz
cd $CMSSW_BASE/src/BstarToTW_CMSDAS2025/
