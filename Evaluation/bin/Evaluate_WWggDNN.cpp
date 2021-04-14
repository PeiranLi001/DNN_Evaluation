#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ParameterSetReader/interface/ParameterSetReader.h"
#include "PhysicsTools/Utilities/macros/setTDRStyle.C"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "PhysicsTools/TensorFlow/interface/TensorFlow.h"

#include "TFile.h"
#include "TTree.h"
#include "TROOT.h"
#include "TChain.h"
#include "TGraphErrors.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TCanvas.h"
#include "TVector2.h"
#include "TMath.h"
#include "TLegend.h"
#include "TEfficiency.h"
#include "TProfile.h"
#include "TStyle.h"
#include "TTreeReader.h"
#include <algorithm> 
#include <iostream>
#include <utility>

using namespace std;

void SplitString(const std::string& str, vector<string>& cont, char delim = ' ')
{
    std::stringstream ss(str);
    std::string token;
    while (std::getline(ss, token, delim)) {
        cont.push_back(token);
    }
    std::cout <<"test1"<<std::endl;
}

vector<string> ListTrees(TDirectory* dir)
{
    std::cout <<"inside_listtree"<<std::endl;
    vector<string> names;
    TIter next(dir->GetListOfKeys());
    std::cout <<"inside_listtree111"<<std::endl;
    TObject* object = 0;
    while ((object = next())){
           names.push_back(string(object->GetName()));
           std::cout << "ListTrees: " << dir->GetName() << " - " << object->GetName() << std::endl; 
	   
    }
    return names;
}

vector<string> ListTrees(TFile* file)
{
    vector<string> names;
    TIter next(file->GetListOfKeys());
    TObject* object = 0;
    while ((object = next())){
           names.push_back(string(object->GetName()));
           //std::cout << "ListTrees: " << object->GetName() << std::endl; 
    }
    std::cout <<"test3"<<std::endl;
    return names;
}

void SetTree(TTree* tree, vector<float>* branchVals, vector<TBranch*>* branchRefs, vector<string>* inputBranches)
{

   size_t nBranches = tree->GetListOfBranches()->GetEntries();
   branchVals->resize(inputBranches->size());
   branchRefs->resize(inputBranches->size()); 
   std::cout <<"test4"<<std::endl;
   for(unsigned int iVar = 0; iVar < inputBranches->size(); ++iVar)
   {
       for(size_t i = 0; i < nBranches; ++i)
       {
           TBranch *br =dynamic_cast<TBranch*>(tree->GetListOfBranches()->At(i));
           if(string(br->GetName()) == inputBranches->at(iVar)){ 
              if(i==5) continue;
              //std::cout << "Branch: " << i << " - " << br->GetName() << std::endl;  
              tree->SetBranchAddress(br->GetName(), &branchVals->at(iVar), &branchRefs->at(iVar)); 
           }
       }
   }
   std::cout <<"test5"<<std::endl;

}

void SetValues(vector<float>* inputVals, vector<float>* branchVals)
{
   for(unsigned int iBranch =0; iBranch<branchVals->size(); iBranch++){
       if(isnan(branchVals->at(iBranch))) std::cout << "Bad iBranch NAN: " << iBranch << std::endl; 
       if(isinf(branchVals->at(iBranch))) std::cout << "Bad iBranch INF: " << iBranch << std::endl;  
   }  
   
   inputVals->push_back(branchVals->at(0));
   inputVals->push_back(branchVals->at(1));
   inputVals->push_back(branchVals->at(2));
   inputVals->push_back(branchVals->at(3));
   inputVals->push_back(branchVals->at(4)/branchVals->at(35));
   inputVals->push_back(branchVals->at(5));
   inputVals->push_back(branchVals->at(6));
   inputVals->push_back(branchVals->at(7));
   inputVals->push_back(branchVals->at(8));
   inputVals->push_back(branchVals->at(9));
   inputVals->push_back(branchVals->at(10));
   inputVals->push_back(branchVals->at(11));
   inputVals->push_back(branchVals->at(12));
   inputVals->push_back(branchVals->at(13));
   inputVals->push_back(branchVals->at(14));
   inputVals->push_back(branchVals->at(15));
   inputVals->push_back(branchVals->at(16));
   inputVals->push_back(branchVals->at(17));
   inputVals->push_back(branchVals->at(18));
   inputVals->push_back(branchVals->at(19));
   inputVals->push_back(branchVals->at(20));
   inputVals->push_back(branchVals->at(21));
   inputVals->push_back(branchVals->at(22));
   inputVals->push_back(branchVals->at(23));
   inputVals->push_back(branchVals->at(24));
   inputVals->push_back(branchVals->at(25));
   inputVals->push_back(branchVals->at(26));
   inputVals->push_back(branchVals->at(27));
   inputVals->push_back(branchVals->at(28));
   inputVals->push_back(branchVals->at(29));
   inputVals->push_back(branchVals->at(30));
   inputVals->push_back(branchVals->at(31));
   inputVals->push_back(branchVals->at(32));
   inputVals->push_back(branchVals->at(33));
   inputVals->push_back(branchVals->at(34));
}

int main(int argc, char** argv)
{
   std::cout <<"test7"<<std::endl;
   const edm::ParameterSet &process         = edm::readPSetsFrom( argv[1] )->getParameter<edm::ParameterSet>( "process" );
   const edm::ParameterSet &filesOpt        = process.getParameter<edm::ParameterSet>( "ioFilesOpt" );
    std::cout <<"test8"<< std::endl;
   // config inputs
   vector<string> inputFiles_    = filesOpt.getParameter<vector<string>>( "inputFiles" );
   string inputDir_              = filesOpt.getParameter<string>( "inputDir" );
   string outputDir_             = filesOpt.getParameter<string>( "outputDir" );

   string inputModel_            = filesOpt.getParameter<string>( "inputModel" );
   std::cout <<"test9"<< std::endl;
   vector<string> inputParams_   = filesOpt.getParameter<vector<string>>( "inputParams" );
   vector<string> inputBranches_ = filesOpt.getParameter<vector<string>>( "inputBranches" );
   vector<string> inputVars_     = filesOpt.getParameter<vector<string>>( "inputVars" );
   std::cout <<"test10"<< std::endl;
   // create a DNN session
   std::cout << "inputModel: " << inputModel_.c_str() << std::endl;
   std::cout <<"test11"<< std::endl;
   tensorflow::Session* session = tensorflow::createSession(tensorflow::loadGraphDef(inputModel_.c_str()));
   std::cout <<"test12"<< std::endl;
   float evalDNN = -999.;
   //TDirectory* dir;
   for(unsigned int iFile=0; iFile<inputFiles_.size(); iFile++)
   {
       TFile* inFile = TFile::Open(inputFiles_.at(iFile).c_str());
       vector<string> categories_;
       std::cout <<"test13"<< std::endl;
       if(inputDir_!=""){
	  std::cout <<"test133"<< std::endl;
	  inFile->cd("tagsDumper/trees");
	  //dir =(TDirectory*)inFile->Get(inputDir_.c_str());
	  
	  std::cout <<"test134"<< std::endl;
	  std::cout <<iFile<< std::endl;
	  std::cout <<inputFiles_.at(iFile).c_str()<< std::endl;
	  std::cout <<inputDir_.c_str()<< std::endl;
	  //std::cout << "ListTrees: " << dir->GetName() << " - " << object->GetName() << std::endl;
	  //std::cout <<sizeof(dir)<< std::endl;
	  //std::cout <<dir<< std::endl;
          categories_ = ListTrees(gDirectory);
	  //categories_ = ListTrees(dir);
	  std::cout <<"test999"<< std::endl;
       }
       else{
          categories_ = ListTrees(inFile);  
       }
       std::cout <<"test14"<< std::endl;
       vector<string> split_str;
       SplitString(inputFiles_.at(iFile), split_str, '/');
       
       TFile* outFile = new TFile((outputDir_+split_str.at(split_str.size()-1)).c_str(),"recreate");
       outFile->cd();

       //if(inputDir_!="") inputDir_ = inputDir_ + '/';
       
       for(unsigned int iCat=0; iCat<categories_.size(); iCat++)
       { 
	 std::cout <<categories_.at(iCat).c_str()<< std::endl;
           if(!inFile->Get((inputDir_+categories_.at(iCat)).c_str())){
              std::cout << "WARNING ----> NOT FOUND: " << (inputDir_+categories_.at(iCat)).c_str() << std::endl;         
              continue;
           }
	   //std::cout <<"test17"<< std::endl;
           TTree* inTree = (TTree*)inFile->Get((inputDir_+categories_.at(iCat)).c_str());
	   
           inTree->SetBranchStatus("evalDNN",0);
	   
           TTree* copyTree = (TTree*)inTree->CopyTree("");
	   
           copyTree->SetName(categories_.at(iCat).c_str());
	   
           copyTree->SetTitle(categories_.at(iCat).c_str());
	   
           vector<float> inputValues; 
           vector<float> branchVals; 
           vector<TBranch*> branchRefs;
           SetTree(copyTree, &branchVals, &branchRefs, &inputBranches_);
	   
           TBranch* evalDNNBranch = copyTree->Branch("evalDNN",&evalDNN,"evalDNN/F");
	   
           // Loop over all entries of the Tree
           for(int entry = 0; entry < copyTree->GetEntries(); entry++)
           {  
               //if(entry>0) continue;
               if(entry%10==0) std::cout << "--- Reading " << categories_.at(iCat).c_str() << " = " << entry << std::endl;
               copyTree->GetEntry(entry);
	       
               //if( entry < 10000 ) continue;
               inputValues.clear();
               SetValues(&inputValues, &branchVals);
	       
               // fill input variables
               unsigned int shape = inputValues.size();
               tensorflow::Tensor inputVals(tensorflow::DT_FLOAT, {1,shape});
               for(unsigned int i = 0; i < shape; i++){
                   //if(std::isinf(inputValues[i])) std::cout << "inf: " << i << std::endl; 
                   if(inputValues[i]<-25. || std::isinf(inputValues[i]) || std::isnan(inputValues[i])) inputVals.matrix<float>()(0,i) =  -9.;
                   else inputVals.matrix<float>()(0,i) =  float(inputValues.at(i));
               } 
               
               // evaluate DNN
               std::vector<tensorflow::Tensor> outputs;
               tensorflow::run(session, { {inputParams_[0].c_str(), inputVals} } , { inputParams_[1].c_str() }, &outputs); 
               evalDNN = outputs[0].matrix<float>()(0, 0);   
               evalDNNBranch->Fill(); 

           }
       }
       outFile->Write();
       outFile->Close(); 
       std::cout <<"test24"<< std::endl;
       //categories_.clear();
   }
   // cleanup
   tensorflow::closeSession(session);
   std::cout <<"test25"<< std::endl;


}

