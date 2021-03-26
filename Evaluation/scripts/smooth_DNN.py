import ROOT
import argparse
import os
import math
from array import array

def findMin(vec):
  min = 999.
  for i in vec:
    if i<min: min=i
  return min  

def findMax(vec):
  max = -999.
  for i in vec:
    if i>max: max=i
  return max    

def nonZeroMin(h):
   min = 999.
   for bin in range(1,h.GetNbinsX()+1):
      if h.GetBinContent(bin)>0. and h.GetBinContent(bin)<min: min = h.GetBinContent(bin)
   return min
    
def isPositive(h):
   isPos = True
   for bin in range(1,h.GetNbinsX()+1):
     if h.GetBinContent(bin)<=0.: 
       isPos = False 
       break
   return isPos

def reduceTree(inTree, cut):
  small = inTree.CopyTree(str(cut))
  return small

def makeRatio(h_num,h_denom):
  h_ratio = h_num.Clone()
  h_ratio.Divide(h_denom) 
  return h_ratio

def MakeTree(inputTree, h_ratio, scale, ouputFile):
 print("inputTree: ",inputTree)
 print("h_ratio: ",h_ratio)
 print("scale: ",scale)
 print("ouputFile: ",ouputFile)
 # inputTree.Print()
 print("="*51)
 outFile = ROOT.TFile(ouputFile, "RECREATE")
 outTree = inputTree.CloneTree(0)
 outTree.SetBranchStatus('*',1)
 bdt_weight = array('f', [0.])
 # inputTree.SetBranchStatus('bdt_weight',0)
 _DNN_weight = outTree.Branch('bdt_weight', bdt_weight, 'bdt_weight/F')     
 nentries = inputTree.GetEntries()
 print("nentries: %f"%nentries)
 for i in range(0, nentries):
    inputTree.GetEntry(i)
    if h_ratio.GetBinContent(h_ratio.FindBin(inputTree.DNN_evaluation))!=0.: 
        bdt_weight[0] = scale*float(h_ratio.GetBinContent(h_ratio.FindBin(inputTree.DNN_evaluation)))
    else: bdt_weight[0] = scale 
    outTree.Fill() 
 outFile.cd()
 print("DEBUG:#62")
 outTree.Write()
 outFile.Close()

def smoothing(h_bdt,method="SmoothSuper"):
 print("[DEBUG#69:]: Inside smoothing function")
 print(h_bdt)
 
 bin_min = h_bdt.GetBinCenter(1)-h_bdt.GetBinWidth(1)/2.
 bin_max = h_bdt.GetBinCenter(h_bdt.GetNbinsX())+h_bdt.GetBinWidth(h_bdt.GetNbinsX())/2.
 h_DNN_smooth = ROOT.TH1F(h_bdt.GetName()+"_smooth",h_bdt.GetName()+"_smooth",h_bdt.GetNbinsX(),float(bin_min),float(bin_max))
 h_DNN_smooth_rnd = ROOT.TH1F(h_bdt.GetName()+"_smooth_rnd",h_bdt.GetName()+"_smooth_rnd",h_bdt.GetNbinsX(),float(bin_min),float(bin_max))
 h_DNN_smooth_up = ROOT.TH1F(h_bdt.GetName()+"_smooth_up",h_bdt.GetName()+"_smooth_up",h_bdt.GetNbinsX(),float(bin_min),float(bin_max))
 h_DNN_smooth_down = ROOT.TH1F(h_bdt.GetName()+"_smooth_down",h_bdt.GetName()+"_smooth_down",h_bdt.GetNbinsX(),float(bin_min),float(bin_max))
 h_diff = ROOT.TH1F(h_bdt.GetName()+"_smoothing_Diff",h_bdt.GetName()+"_smoothing_Diff",200,-20.,20.)

 g_bdt = ROOT.TGraph()
 g_DNN_smooth = ROOT.TGraph() 
 smoother = ROOT.TGraphSmooth()

 h_bdt.Print("all")

 for bin in range(0,h_bdt.GetNbinsX()): 
  g_bdt.SetPoint(bin,h_bdt.GetBinCenter(bin+1),h_bdt.GetBinContent(bin+1))
 if method=="SmoothLowess": g_DNN_smooth = smoother.SmoothLowess(g_bdt)
 elif method=="SmoothKern": g_DNN_smooth = smoother.SmoothKern(g_bdt)
 elif method=="SmoothSuper": g_DNN_smooth = smoother.SmoothSuper(g_bdt,"",0)
 else: 
    print( "WARNING: unknown smoothing method!")
    return -1

 rnd = ROOT.TRandom()
 x = array('d', [0])
 y = array('d', [0])
 for bin in range(0,h_DNN_smooth.GetNbinsX()): 
  g_DNN_smooth.GetPoint(bin+1,x,y)
  print("x = ",x)
  print("y = ",y)
  h_DNN_smooth.SetBinContent(bin+1,y[0])
  h_DNN_smooth_rnd.SetBinContent(bin+1,rnd.Poisson(float(y[0])))
  
 print("[DEBUG:#99] h_DNN_smooth.Integral() = ",h_DNN_smooth.Integral())
 h_DNN_smooth.Scale(h_bdt.Integral()/h_DNN_smooth.Integral())
 h_DNN_smooth_rnd.Scale(h_bdt.Integral()/h_DNN_smooth_rnd.Integral())

 for bin in range(0,h_DNN_smooth.GetNbinsX()): 
  y = h_DNN_smooth.GetBinContent(bin+1) 
  if y>=0.: 
     h_DNN_smooth_up.SetBinContent(bin+1,y+math.sqrt(y))
     if (y-math.sqrt(y))>0.: h_DNN_smooth_down.SetBinContent(bin+1,y-math.sqrt(y))
     else: h_DNN_smooth_down.SetBinContent(bin+1,0.)
  else:
     h_DNN_smooth_up.SetBinContent(bin+1,0.)
     h_DNN_smooth_down.SetBinContent(bin+1,0.)
  h_diff.Fill(y-h_bdt.GetBinContent(bin+1)) 

 return [h_DNN_smooth,h_DNN_smooth_up,h_DNN_smooth_down,h_DNN_smooth_rnd,h_diff] 

def compareHistos(hist_data_tmp,hist_bkg_tmp,name,rebin):

   ROOT.gStyle.SetOptStat(0000)
 
   hist_data = hist_data_tmp.Clone()
   hist_data.SetName(hist_data_tmp.GetName()+'_Rebin') 
   hist_data.Rebin(rebin)

   hist_bkg = hist_bkg_tmp.Clone()
   hist_bkg.SetName(hist_bkg_tmp.GetName()+'_Rebin') 
   hist_bkg.Rebin(rebin)
  
   hist_data.SetLineColor(ROOT.kBlack)
   hist_data.SetMarkerColor(ROOT.kBlack)
   hist_data.SetMarkerStyle(20)
   hist_bkg.SetLineColor(ROOT.kBlack)

   #hist_bkg.Scale(hist_data.Integral()/hist_bkg.Integral())

   min = nonZeroMin(hist_bkg)
   if min>nonZeroMin(hist_data): min = nonZeroMin(hist_data)
   max = hist_bkg.GetMaximum()
   if max<hist_data.GetMaximum(): max = hist_data.GetMaximum()
   #hist_bkg.GetYaxis().SetRangeUser(min*0.5,max*2.)
   # hist_bkg.GetYaxis().SetRangeUser(3.,200.)

   c = ROOT.TCanvas()
   #if isPositive(hist_bkg) and isPositive(hist_data): c.SetLogy()
   c.SetLogy()
   hist_bkg.Draw("HIST") 
   hist_data.Draw("P,same")
   c.SaveAs(name+".png","png") 
   c.SaveAs(name+".pdf","pdf") 

   ROOT.gStyle.SetOptStat(1111)

def drawHistos(hist,hist_smooth,hist_smooth_up,hist_smooth_down,name):

   ROOT.gStyle.SetOptStat(0000)

   mins = [float(nonZeroMin(hist)),float(nonZeroMin(hist_smooth)),float(nonZeroMin(hist_smooth_up)),float(nonZeroMin(hist_smooth_down))]
   maxs = [float(hist.GetMaximum()),float(hist_smooth.GetMaximum()),float(hist_smooth_up.GetMaximum()),float(hist_smooth_down.GetMaximum())]
   
   minimum = findMin(mins)
   maximum = findMax(maxs)
   hist.SetLineColor(ROOT.kBlack)
   hist_smooth.SetLineColor(ROOT.kRed)
   hist_smooth_up.SetLineColor(ROOT.kGreen)
   hist_smooth_down.SetLineColor(ROOT.kBlue)
   hist.GetYaxis().SetRangeUser(minimum*0.5,2.*maximum)
   hist.GetXaxis().SetTitle('DNN_evaluation')
   
   title = name
   hist.SetTitle(title.replace('h_',''))

   leg = ROOT.TLegend(0.70,0.7,0.85,0.88)
   leg.SetFillColor(ROOT.kWhite)
   leg.SetFillStyle(1000)
   leg.SetLineWidth(0)
   leg.SetLineColor(ROOT.kWhite)
   leg.SetTextFont(42)
   leg.SetTextSize(0.035)
   leg.AddEntry(hist_smooth_up,"Smoothing + #sigma","L")
   leg.AddEntry(hist_smooth,"Smoothing ","L")
   leg.AddEntry(hist_smooth_down,"Smoothing - #sigma","L")
   
   c = ROOT.TCanvas()
   #if isPositive(hist) and isPositive(hist_smooth) and isPositive(hist_smooth_up) and isPositive(hist_smooth_down): c.SetLogy()
   c.SetLogy()
   hist.Draw("HIST") 
   hist_smooth.Draw("HIST,same")
   hist_smooth_up.Draw("HIST,same")
   hist_smooth_down.Draw("HIST,same")
   leg.Draw("same")
   c.SaveAs(name+".png","png") 
   c.SaveAs(name+".pdf","pdf") 

   ROOT.gStyle.SetOptStat(1111)

def drawHisto(hist,name):

   ROOT.gStyle.SetOptStat(1111)

   hist.SetLineColor(ROOT.kBlack)
   
   c = ROOT.TCanvas()
   hist.Draw("HIST") 
   c.SaveAs(name+".png","png") 
   c.SaveAs(name+".pdf","pdf") 

if __name__ == '__main__': 

 ROOT.gROOT.SetBatch(ROOT.kTRUE)

 parser =  argparse.ArgumentParser(description='smooth DNN')
 parser.add_argument('-d', '--inDir', dest='inDir', required=True, type=str)
 parser.add_argument('-n', '--nBins', dest='nBins', required=False, type=int)
 parser.add_argument('-m', '--min', dest='min', required=False, type=float)
 parser.add_argument('-M', '--max', dest='max', required=False, type=float)
 parser.add_argument('-r', '--massMin', dest='massMin', required=False, type=float)
 parser.add_argument('-R', '--massMax', dest='massMax', required=False, type=float)
 
 args = parser.parse_args()
 inDir = args.inDir
 #inDir = '/eos/user/b/bmarzocc/HHWWgg/January_2021_Production/HHWWyyDNN_binary_noHgg_noNegWeights_BalanceYields_allBkgs_LOSignals_noPtOverM/'

 nBins = 100
 #print( args.nBins,args.min,args.max)
 if args.nBins: nBins = args.nBins
 min = 0.1
 if args.min: min = args.min
 max = 1.
 if args.max: max = args.max
 massMin = 115.
 if args.massMin: massMin = args.massMin
 massMax = 135.
 if args.massMax: massMax = args.massMax

 print( "inDir:",inDir)
 print( "nBins:",nBins)
 print( "Min:",min)
 print( "Max:",max)
 print( "massMin:",massMin)
 print( "massMax:",massMax)
 
 histo_scale = ROOT.TH1F("histo_scale","",100000,-1.1,1.)
 Cut_noMass = '( DNN_evaluation>'+str(min)+' )'
 Cut_SR = '( CMS_hgg_mass>100. && CMS_hgg_mass<180. && (CMS_hgg_mass > '+str(massMin)+' && CMS_hgg_mass < '+str(massMax)+') && DNN_evaluation>'+str(min)+' )'
 Cut_SB = '( CMS_hgg_mass>100. && CMS_hgg_mass<180. && !(CMS_hgg_mass > 115 && CMS_hgg_mass < 135) && DNN_evaluation>'+str(min)+' )'

 h_DNN_signal_SB_2017 = ROOT.TH1F("h_DNN_signal_SB_2017","h_DNN_signal_SB_2017",int(nBins),float(min),float(max))
 h_DNN_signal_SR_2017 = ROOT.TH1F("h_DNN_signal_SR_2017","h_DNN_signal_SR_2017",int(nBins),float(min),float(max)) 
 h_DNN_data_SB_2017 = ROOT.TH1F("h_DNN_data_SB_2017","h_DNN_data_SB_2017",int(nBins),float(min),float(max))  
 h_DNN_bkg_SR_2017 = ROOT.TH1F("h_DNN_bkg_SR_2017","h_DNN_bkg_SR_2017",int(nBins),float(min),float(max)) 
 
 diffBins = 30
 h_DNN_data_SB_2017_diffBins = ROOT.TH1F("h_DNN_data_SB_2017_diffBins","h_DNN_data_SB_2017_diffBins",diffBins,float(min),float(max))  
 h_DNN_bkg_SB_2017_diffBins = ROOT.TH1F("h_DNN_bkg_SB_2017_diffBins","h_DNN_bkg_SB_2017_diffBins",diffBins,float(min),float(max)) 

 h_DNN_ggHtoGG_SR_2017 = ROOT.TH1F("h_DNN_ggHtoGG_SR_2017","h_DNN_ggHtoGG_SR_2017",int(nBins),float(min),float(max))
 h_DNN_VBFHtoGG_SR_2017 = ROOT.TH1F("h_DNN_VBFHtoGG_SR_2017","h_DNN_VBFHtoGG_SR_2017",int(nBins),float(min),float(max))  
 h_DNN_VHtoGG_SR_2017 = ROOT.TH1F("h_DNN_VHtoGG_SR_2017","h_DNN_VHtoGG_SR_2017",int(nBins),float(min),float(max)) 
 h_DNN_ttHtoGG_SR_2017 = ROOT.TH1F("h_DNN_ttHtoGG_SR_2017","h_DNN_ttHtoGG_SR_2017",int(nBins),float(min),float(max))  
 
 ### 2017 ###
 lumi_2017 = 41.5

 histo_scale.Reset() 
 sig_tree_2017 = ROOT.TChain()
 sig_tree_2017.AddFile(inDir+'/GluGluToHHTo2G4Q_node_cHHH1_2018.root/output_tree')
 sig_tree_2017.Draw("Leading_Photon_MVA<-1.?-1.1:Leading_Photon_MVA>>histo_scale","weight*0.441*0.00097*31.049*"+Cut_SR)
 sig_scale_2017 = float(histo_scale.Integral())
 sig_tree_2017.Draw("DNN_evaluation>>h_DNN_signal_SB_2017",str(lumi_2017)+"*weight*0.441*0.00097*31.049*"+Cut_SB)  
 sig_tree_2017.Draw("DNN_evaluation>>h_DNN_signal_SR_2017",str(lumi_2017)+"*weight*0.441*0.00097*31.049*"+Cut_SR) 

 ### HtoGG Bkgs ###
 ggHtoGG_tree_2017 = ROOT.TChain()
 ggHtoGG_tree_2017.AddFile(inDir+'/GluGluHToGG_M125_TuneCP5_13TeV.root/output_tree')
 ggHtoGG_tree_2017.Draw("DNN_evaluation>>h_DNN_ggHtoGG_SR_2017",str(lumi_2017)+"*weight*"+Cut_SR)  
 VBFHtoGG_tree_2017 = ROOT.TChain()
 VBFHtoGG_tree_2017.AddFile(inDir+'/VBFHToGG_M125_13TeV.root/output_tree')
 VBFHtoGG_tree_2017.Draw("DNN_evaluation>>h_DNN_VBFHtoGG_SR_2017",str(lumi_2017)+"*weight*"+Cut_SR)
 VHtoGG_tree_2017 = ROOT.TChain()
 VHtoGG_tree_2017.AddFile(inDir+'/VHToGG_M125_13TeV.root/output_tree')
 VHtoGG_tree_2017.Draw("DNN_evaluation>>h_DNN_VHtoGG_SR_2017",str(lumi_2017)+"*weight*"+Cut_SR) 
 ttHJetToGG_tree_2017 = ROOT.TChain()
 ttHJetToGG_tree_2017.AddFile(inDir+'/ttHJetToGG_M125_13TeV.root/output_tree')
 ttHJetToGG_tree_2017.Draw("DNN_evaluation>>h_DNN_ttHtoGG_SR_2017",str(lumi_2017)+"*weight*"+Cut_SR)   
 
 histo_scale.Reset() 
 data_tree_2017 = ROOT.TChain()
 data_tree_2017.AddFile(inDir+'/allData.root/output_tree') 
 data_tree_2017.AddFile(inDir+'/allData.root/output_tree') 
 data_tree_2017.AddFile(inDir+'/allData.root/output_tree') 
 data_tree_2017 = reduceTree(data_tree_2017,Cut_noMass)
 data_tree_2017.Draw("Leading_Photon_MVA<-1.?-1.1:Leading_Photon_MVA>>histo_scale",Cut_SB)
 data_scale_2017 = float(histo_scale.Integral())
 data_tree_2017.Draw("DNN_evaluation>>h_DNN_data_SB_2017",Cut_SB)
 data_tree_2017.Draw("DNN_evaluation>>h_DNN_data_SB_2017_diffBins",Cut_SB)
 
 #Bkgs MC samples
 treeNames = [
  "GluGluHToGG_M125_TuneCP5_13TeV.root/output_tree",
  "ttHJetToGG_M125_13TeV.root/output_tree",
  "VHToGG_M125_13TeV.root/output_tree",
  "DiPhotonJetsBox_MGG-80toInf_13TeV.root/output_tree",
  "GluGluToHHTo2G4Q_node_cHHH1_2018.root/output_tree",
  "VBFHToGG_M125_13TeV.root/output_tree",
 ]

 histo_scale.Reset() 
 bkg_tree_2017 = ROOT.TChain()
 for tree in treeNames: 
   bkg_tree_2017.AddFile(inDir+'/'+tree)
 bkg_tree_2017 = reduceTree(bkg_tree_2017,Cut_noMass)
 bkg_tree_2017.Draw("Leading_Photon_MVA<-1.?-1.1:Leading_Photon_MVA>>histo_scale","weight*"+Cut_SB)
 bkg_scale_2017 = float(histo_scale.Integral())
 print("bkg_scale_2017: %f"%bkg_scale_2017)
 bkg_tree_2017.Draw("DNN_evaluation>>h_DNN_bkg_SR_2017",str(data_scale_2017/bkg_scale_2017)+"*weight*"+Cut_SR)
 bkg_tree_2017.Draw("DNN_evaluation>>h_DNN_bkg_SB_2017_diffBins",str(data_scale_2017/bkg_scale_2017)+"*weight*"+Cut_SB)

 print( "2017 Data/bkg SB scale:",data_scale_2017/bkg_scale_2017)

 h_DNN_signal_SB = h_DNN_signal_SB_2017.Clone()
 h_DNN_signal_SB.SetName('h_DNN_signal_SB')
 h_DNN_signal_SB.SetTitle('h_DNN_signal_SB')

 h_DNN_signal_SR = h_DNN_signal_SR_2017.Clone()
 h_DNN_signal_SR.SetName('h_DNN_signal_SR')
 h_DNN_signal_SR.SetTitle('h_DNN_signal_SR')
 
 h_DNN_bkg_SR = h_DNN_bkg_SR_2017.Clone()
 h_DNN_bkg_SR.SetName('h_DNN_bkg_SR')
 h_DNN_bkg_SR.SetTitle('h_DNN_bkg_SR')

 h_DNN_data_SB = h_DNN_data_SB_2017.Clone()
 h_DNN_data_SB.SetName('h_DNN_data_SB')
 h_DNN_data_SB.SetTitle('h_DNN_data_SB')
 
 h_DNN_data_SB_diffBins = h_DNN_data_SB_2017_diffBins.Clone()
 h_DNN_data_SB_diffBins.SetName('h_DNN_data_SB_diffBins')
 h_DNN_data_SB_diffBins.SetTitle('h_DNN_data_SB_diffBins')

 h_DNN_bkg_SB_diffBins = h_DNN_bkg_SB_2017_diffBins.Clone()
 h_DNN_bkg_SB_diffBins.SetName('h_DNN_bkg_SB_diffBins')
 h_DNN_bkg_SB_diffBins.SetTitle('h_DNN_bkg_SB_diffBins')

 h_DNN_ratio_SB = makeRatio(h_DNN_data_SB_diffBins,h_DNN_bkg_SB_diffBins)

 compareHistos(h_DNN_data_SB_diffBins,h_DNN_bkg_SB_diffBins,"h_DNN_SB",1)

 h_DNN_bkg_SB_weighted_2017 = ROOT.TH1F("h_DNN_bkg_SB_weighted_2017","h_DNN_bkg_SB_weighted_2017",int(nBins),float(min),float(max))
 h_DNN_bkg_SB_weighted_2017_diffBins = ROOT.TH1F("h_DNN_bkg_SB_weighted_2017_diffBins","h_DNN_bkg_SB_weighted_2017_diffBins",diffBins,float(min),float(max))

 h_DNN_bkg_SR_weighted_2017 = ROOT.TH1F("h_DNN_bkg_SR_weighted_2017","h_DNN_bkg_SR_weighted_2017",int(nBins),float(min),float(max))
 
 print( "Fill 2017 bkg reweighting...")
 bkg_tree_2017_bdtWeight = ROOT.TChain()
 MakeTree(bkg_tree_2017, h_DNN_ratio_SB, data_scale_2017/bkg_scale_2017, 'file.root')
 print("DEBUG:#352")
 bkg_tree_2017_bdtWeight.AddFile('file.root/'+str(treeNames[0].split('/')[1]))
 print("DEBUG:#354")
 bkg_tree_2017_bdtWeight.Draw("DNN_evaluation>>h_DNN_bkg_SB_weighted_2017","weight*"+Cut_SB)
 print("DEBUG:#356")
 bkg_tree_2017_bdtWeight.Draw("DNN_evaluation>>h_DNN_bkg_SB_weighted_2017_diffBins","weight*"+Cut_SB)
 bkg_tree_2017_bdtWeight.Draw("DNN_evaluation>>h_DNN_bkg_SR_weighted_2017","weight*"+Cut_SR)
 
 h_DNN_bkg_SB_weighted = h_DNN_bkg_SB_weighted_2017.Clone()
 h_DNN_bkg_SB_weighted.SetName('h_DNN_bkg_SB_weighted')
 h_DNN_bkg_SB_weighted.SetTitle('h_DNN_bkg_SB_weighted')

 h_DNN_bkg_SB_weighted_diffBins = h_DNN_bkg_SB_weighted_2017_diffBins.Clone()
 h_DNN_bkg_SB_weighted_diffBins.SetName('h_DNN_bkg_SB_weighted_diffBins')
 h_DNN_bkg_SB_weighted_diffBins.SetTitle('h_DNN_bkg_SB_weighted_diffBins')

 h_DNN_bkg_SR_weighted = h_DNN_bkg_SR_weighted_2017.Clone()
 h_DNN_bkg_SR_weighted.SetName('h_DNN_bkg_SR_weighted')
 h_DNN_bkg_SR_weighted.SetTitle('h_DNN_bkg_SR_weighted')

 compareHistos(h_DNN_data_SB_diffBins,h_DNN_bkg_SB_weighted_diffBins,"h_DNN_SB_weighted",1)

 print( "Smooth distributions...")
 algos = ['SmoothSuper']

 for algo in algos:
   print("[DEBUG:#385] algo: ",algo)
   outFile = ROOT.TFile(inDir+'/DNN_Histos_smoothing_'+algo+'_bins'+str(nBins)+'_massMin'+str(massMin)+'_massMax'+str(massMax)+'.root',"RECREATE")
   outFile.cd()
   print("[DEBUG:#388] algo: ",algo)
   hist_smooth = smoothing(h_DNN_bkg_SR_weighted,algo)
   if hist_smooth!=-1: 
     drawHistos(h_DNN_bkg_SR_weighted,hist_smooth[0],hist_smooth[1],hist_smooth[2],h_DNN_bkg_SR_weighted.GetName()+"_smoothing_"+algo+"_nBins_"+str(nBins))
     drawHisto(hist_smooth[4],h_DNN_bkg_SR_weighted.GetName()+"_smoothing_"+algo+"_Diff_nBins_"+str(nBins)) 
     h_DNN_bkg_SR_weighted.Write()
     hist_smooth[0].Write() 
     hist_smooth[1].Write() 
     hist_smooth[2].Write() 
   hist_smooth = smoothing(h_DNN_bkg_SR,algo)
   if hist_smooth!=-1: 
     drawHistos(h_DNN_bkg_SR,hist_smooth[0],hist_smooth[1],hist_smooth[2],h_DNN_bkg_SR.GetName()+"_smoothing_"+algo+"_nBins_"+str(nBins))
     drawHisto(hist_smooth[4],h_DNN_bkg_SR.GetName()+"_smoothing_"+algo+"_Diff_nBins_"+str(nBins)) 
     h_DNN_bkg_SR.Write()
     hist_smooth[0].Write() 
     hist_smooth[1].Write() 
     hist_smooth[2].Write() 
   hist_smooth = smoothing(h_DNN_bkg_SB_weighted,algo)
   if hist_smooth!=-1: 
     drawHistos(h_DNN_bkg_SB_weighted,hist_smooth[0],hist_smooth[1],hist_smooth[2],h_DNN_bkg_SB_weighted.GetName()+"_smoothing_"+algo+"_nBins_"+str(nBins))
     drawHisto(hist_smooth[4],h_DNN_bkg_SB_weighted.GetName()+"_smoothing_"+algo+"_Diff_nBins_"+str(nBins)) 
     h_DNN_bkg_SB_weighted.Write()
     hist_smooth[0].Write() 
     hist_smooth[1].Write() 
     hist_smooth[2].Write()  
   hist_smooth = smoothing(h_DNN_data_SB,algo)
   if hist_smooth!=-1: 
     drawHistos(h_DNN_data_SB,hist_smooth[0],hist_smooth[1],hist_smooth[2],h_DNN_data_SB.GetName()+"_smoothing_"+algo+"_nBins_"+str(nBins))
     drawHisto(hist_smooth[4],h_DNN_data_SB.GetName()+"_smoothing_"+algo+"_Diff_nBins_"+str(nBins)) 
     h_DNN_data_SB.Write()
     hist_smooth[0].Write() 
     hist_smooth[1].Write() 
     hist_smooth[2].Write() 
   h_DNN_signal_SR.Write()
   h_DNN_signal_SB.Write()
   h_DNN_data_SB_diffBins.Write()
   h_DNN_bkg_SB_diffBins.Write()
   h_DNN_bkg_SB_weighted_diffBins.Write()
   h_DNN_ggHtoGG_SR_2017.Write('h_DNN_ggHtoGG_SR')
   h_DNN_VBFHtoGG_SR_2017.Write('h_DNN_VBFHtoGG_SR')
   h_DNN_VHtoGG_SR_2017.Write('h_DNN_VHtoGG_SR')
   h_DNN_ttHtoGG_SR_2017.Write('h_DNN_ttHtoGG_SR')
   outFile.Close()

