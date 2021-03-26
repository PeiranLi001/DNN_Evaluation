# DNN_Evaluation

1) Install:
   ```bash
   scram project CMSSW_10_5_X # or CMSSW_10_6_X or inside any Flashgg CMSSW release
   cd CMSSW_10_5_X/src/
   cmsenv
   git clone https://github.com/bmarzocc/DNN_Evaluation
   scram b -j 5
   ```

2) Run: set parameters in python/Evaluate_WWggDNN.py
   ```bash
   cd DNN_Evaluation/Evaluation
   cmsenv
   Evaluate_WWggDNN python/Evaluate_WWggDNN.py
   ```

3) Run categorization

   ```bash
   cd DNN_Evaluation/Evaluation/scripts/
   cmsenv
   python smooth_DNN.py -d /eos/user/b/bmarzocc/HHWWgg/January_2021_Production/HHWWyyDNN_binary_withHgg_noNegWeights_BalanceYields_allBkgs_LOSignals_noPtOverM/ --min 0.1 --max 1.-n 30 -r 115 -R 135
   python smooth_DNN_Condor.py -d /eos/user/b/bmarzocc/HHWWgg/January_2021_Production/HHWWyyDNN_binary_withHgg_noNegWeights_BalanceYields_allBkgs_LOSignals_noPtOverM/ --min 0.1 --max 1. -r 115 -R 135 -n 1 #Condor
   python optimizeCategories.py -d /eos/user/b/bmarzocc/HHWWgg/January_2021_Production/HHWWyyDNN_binary_withHgg_noNegWeights_BalanceYields_allBkgs_LOSignals_noPtOverM/ -n 30 -c 2 --massMin 115 --massMax 135 -s 1 -w 1
   python optimizeCategories_Condor.py -d /eos/user/b/bmarzocc/HHWWgg/January_2021_Production/HHWWyyDNN_binary_withHgg_noNegWeights_BalanceYields_allBkgs_LOSignals_noPtOverM/ --massMin 115 --massMax 135 -n 1 #Condor
   python Significance_plots.py -d /eos/user/b/bmarzocc/HHWWgg/January_2021_Production/HHWWyyDNN_binary_withHgg_noNegWeights_BalanceYields_allBkgs_LOSignals_noPtOverM/ -s 1 -w 1 #make summary plots
   ```
