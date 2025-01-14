import ROOT, collections,sys,os
from collections import OrderedDict
from TIMBER.Analyzer import analyzer, HistGroup, VarGroup, CutGroup
from TIMBER.Tools.Common import CompileCpp, OpenJSON
from TIMBER.Tools.Plot import *
import helpers
ROOT.gROOT.SetBatch(True)

###########################################
# Establish some global variables for use #
###########################################
plotdir = 'plots/'
redirector = 'root://cmsxrootd.fnal.gov/'
rootfile_path = '/store/user/cmsdas/2021/long_exercises/BstarTW/rootfiles'
config = 'bstar_config.json'
if not os.path.exists(plotdir):
    os.makedirs(plotdir)

#################################################
# Create structs for MET flags and trigger info #
#################################################
# MET flags - https://twiki.cern.ch/twiki/bin/view/CMS/MissingETOptionalFiltersRun2
flags = ["Flag_goodVertices",
        "Flag_globalSuperTightHalo2016Filter",
        "Flag_HBHENoiseFilter",
        "Flag_HBHENoiseIsoFilter",
        "Flag_EcalDeadCellTriggerPrimitiveFilter",
        "Flag_BadPFMuonFilter"
        #"Flag_ecalBadCalibReducedMINIAODFilter"  # Still work in progress flag, may not be used
        ]
triggers = {
        '16': ["HLT_PFHT800","HLT_PFHT900","HLT_PFJet450"],
        '17': ["HLT_PFHT1050","HLT_PFJet500","HLT_AK8PFJet380_TrimMass30","HLT_AK8PFJet400_TrimMass30"],
        '18': ["HLT_PFHT1050","HLT_PFJet500","HLT_AK8PFJet380_TrimMass30","HLT_AK8PFJet400_TrimMass30"]
}

########################################
# Variables we want to create and plot #
########################################
# Dictionary will have form {'RDataFrame column name' : 'LaTeX title'}
varnames = {
    'deltaY' : '|#Delta y|',
    'tau21'  : '#tau_{2} / #tau_{1}',
    'tau32'  : '#tau_{3} / #tau_{2}',
    'mW'     : 'm_{W} [GeV]',
    'mtop'   : 'm_{top} [GeV]',
}

#########################################
# Define function for actual processing #
#########################################
def nminus1(setname, year):
    '''Performs the N minus 1 selection and plotting by
        (1) Making some basic kinematic selections
        (2) Creating a few TIMBER VarGroups to store variables we're interested in studying
        (3) Creating a CutGroup to store the cuts whose effects on the above variables we're interested in seeing
        (4) Perform the N-1 cut-making and plotting
    Args:
        setname (str): name of input dataset
        year    (str): 16, 17, 18
    '''
    # Open the JSON config file and grab information we will need
    config = OpenJSON('bstar_config.json')
    cuts = config['CUTS'][year]

    # Initialize TIMBER analyzer
    file_path = '{redirector}{rootfile_path}/{setname}_bstar{year}.root'.format(
        redirector=redirector, rootfile_path=rootfile_path, setname=setname, year=year
    )
    a = analyzer(file_path)

    # Determine normalization weight
    if not a.isData:
        norm = helpers.getNormFactor(setname,year,config)
    else:
        norm = 1

    # Book actions on the RDataFrame
    a.Cut('filters',a.GetFlagString(flags))
    a.Cut('trigger',a.GetTriggerString(triggers[year]))
    a.Define('jetIdx',    'hemispherize(FatJet_phi, FatJet_jetId)') # need to calculate if we have two jets (with Id) that are back-to-back
    a.Cut('nFatJets_cut', 'nFatJet > max(jetIdx[0], jetIdx[1])')    # If we don't do this, we may try to access variables of jets that don't exist! (leads to seg fault)
    a.Cut('hemis',        '(jetIdx[0] != -1)&&(jetIdx[1] != -1)')   # cut on that calculation
    a.SubCollection('Dijet', 'FatJet', 'jetIdx', useTake=True)
    a.Cut('pt_cut',  'Dijet_pt[0] > 400 && Dijet_pt[1] > 400')
    a.Cut('eta_cut', 'abs(Dijet_eta[0]) < 2.4 && abs(Dijet_eta[1]) < 2.4')
    a.Define('norm',str(norm))

    #################################
    # Build some variables for jets #
    #################################
    # We need to decide if any of the jets are likely to be a W or a top
    # TODO : Write an expression that selects the index of the jet we will use as the top candidate (0 or 1)

    # Starting point is to take the leading jet (highest pt) as the W candidate, how can we do better?
    w_index_str = "0"

    # Create a TIMBER VarGroup to store information about the jets
    jets = VarGroup('jets')
    jets.Add('w_index',    w_index_str)
    jets.Add('top_index',   '1 - w_index')
    # Calculate some new comlumns that we'd like to cut on (that were costly to do before the other filtering)
    jets.Add("lead_vect",   "hardware::TLvector(Dijet_pt[0], Dijet_eta[0], Dijet_phi[0], Dijet_msoftdrop[0])")
    jets.Add("sublead_vect","hardware::TLvector(Dijet_pt[1], Dijet_eta[1], Dijet_phi[1], Dijet_msoftdrop[1])")
    jets.Add("deltaY",      "abs(lead_vect.Rapidity() - sublead_vect.Rapidity())")
    jets.Add("mtw",         "hardware::InvariantMass({lead_vect + sublead_vect})")

    ######################################
    # Build some variables for the N - 1 #
    ######################################
    plotting_vars = VarGroup('plotting_vars') # These are the variables we'll track to see how the cuts influence them

    #TODO : Add variables for the mass and tau32 of the top candidate, the mass and tau21 of the W candidate 
    #plotting_vars.Add("mtop",  ...)

    N_cuts = CutGroup('Ncuts') # N cuts to make on the VarGroup above
    N_cuts.Add("deltaY_cut",      "deltaY < 1.6")
    N_cuts.Add("mtop_cut",        "(mtop > 105.) && (mtop < 220.)")
    N_cuts.Add("mW_cut",          "(mW > 65.) && (mW < 105.)")
    N_cuts.Add("tau32_cut",       "(tau32 > 0.0) && (tau32 < %s)"%(cuts['tau32']))
    N_cuts.Add("tau21_cut",       "(tau21 > 0.0)&&(tau21 < %s)"%(cuts['tau21']))

    nodeToPlot = a.Apply([jets,plotting_vars])
    nminus1Nodes = a.Nminus1(N_cuts, node=nodeToPlot) # constructs N nodes with a different N-1 selection for each
    nminus1Hists = HistGroup('nminus1Hists')

    # Add hists to group and write out
    outFile = ROOT.TFile.Open('rootfiles/{}_{}_Nminus1.root'.format(setname,year),'RECREATE')
    outFile.cd()
    binning = {
        'mtop': [25,50,300],
        'mW': [25,30,270],
        'tau32': [20,0,1],
        'tau21': [20,0,1],
        'deltaY': [20,0,2.0]
    }
    print('Plotting:')
    for nkey in nminus1Nodes.keys():
        if nkey == 'full': continue
        print('\t{}'.format(nkey))
        var = nkey.replace('_cut','').replace('minus_','')
        hist_tuple = (var,var,binning[var][0],binning[var][1],binning[var][2])
        hist = nminus1Nodes[nkey].DataFrame.Histo1D(hist_tuple,var,'norm')
        hist.GetValue()
        nminus1Hists.Add(var,hist)

    # Now, perform TH1.Write() on all TH1s in our HistGroup
    nminus1Hists.Do('Write')

    # Save the NodeTree so we can see how it works under the hood
    a.PrintNodeTree(plotdir+'/{}_{}_nminus1_tree.dot'.format(setname,year), verbose=True)

    # Finally, safely close the analyzer and the rootfile
    outFile.Close()
    a.Close()


if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-s', type=str, dest='setname',
                        action='store', required=True,
                        help='Setname to process. E.g. ttbar, signalLH2000, singletop_tW, QCDHT700, etc...')
    parser.add_argument('-y', type=str, dest='year',
                        action='store', required=True,
                        help='Year of set (16, 17, 18).')
    args = parser.parse_args()

    # Compile some of the C++ macros we'll need for our selection
    CompileCpp("TIMBER/Framework/include/common.h")
    CompileCpp('bstar.cc')      # Contains hemispherize() function for identifying back-to-back jets

    # Run our N - 1 script
    nminus1(args.setname, args.year)
