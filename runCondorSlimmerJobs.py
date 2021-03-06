import os,shutil,datetime,time
import getpass
from ROOT import *
execfile("/uscms_data/d3/jmanagan/EOSSafeUtils.py")

start_time = time.time()

shift = sys.argv[1]

#IO directories must be full paths

relbase = '/uscms_data/d3/jmanagan/CMSSW_9_4_6_patch1/'
inputDir='/eos/uscms/store/user/lpcljm/2018/LJMet94X_1lep_013019/'+shift+'/'
outputDir='/eos/uscms/store/user/lpcljm/2018/LJMet94X_1lepTT_confusionplots_031219/'+shift+'/'
condorDir='/uscms_data/d3/jmanagan/LJMet94X_1lepTT_confusionplots_031219/'+shift+'/'

runDir=os.getcwd()
# Can change the file directory if needed
#if '' not in shift: runDirPost = ''
#else: runDirPost = shift+'Files'
runDirPost = ''
print 'Files from',runDirPost

gROOT.ProcessLine('.x compileStep1.C')

cTime=datetime.datetime.now()
date='%i_%i_%i_%i_%i_%i'%(cTime.year,cTime.month,cTime.day,cTime.hour,cTime.minute,cTime.second)

inDir=inputDir[10:]
outDir=outputDir[10:]

print 'Starting submission'
count=0

signalList = [
    'TprimeTprime_M-1000_TuneCP5_13TeV-madgraph-pythia8',
    'TprimeTprime_M-1100_TuneCP5_13TeV-madgraph-pythia8',
    'TprimeTprime_M-1200_TuneCP5_13TeV-madgraph-pythia8',
    'TprimeTprime_M-1300_TuneCP5_13TeV-madgraph-pythia8',
    'TprimeTprime_M-1400_TuneCP5_13TeV-madgraph-pythia8',
    'TprimeTprime_M-1500_TuneCP5_13TeV-madgraph-pythia8',
    'TprimeTprime_M-1600_TuneCP5_13TeV-madgraph-pythia8',
    'TprimeTprime_M-1700_TuneCP5_13TeV-madgraph-pythia8',
    'TprimeTprime_M-1800_TuneCP5_13TeV-madgraph-pythia8'
    ]

signalOutList = ['BWBW','TZBW','THBW','TZTH','TZTZ','THTH']

for sample in signalList:
    rootfiles = EOSlist_root_files(inputDir+sample)
    relPath = sample        
    for outlabel in signalOutList:
        os.system('eos root://cmseos.fnal.gov/ mkdir -p '+outDir+sample+'_'+outlabel)
        os.system('mkdir -p '+condorDir+sample+'_'+outlabel)

        tmpcount = 0
        for i in range(0,len(rootfiles),20):            
            rawname = relPath
            count+=1
            tmpcount += 1

            idlist = (rootfiles[i].split('.')[0]).split('_')[-1]+' '
            for j in range(i+1,i+20):
                if j >= len(rootfiles): continue
                idlist += (rootfiles[j].split('.')[0]).split('_')[-1]+' '
            idlist = idlist.strip()
            print idlist

            dict={'RUNDIR':runDir, 'POST':runDirPost, 'RELPATH':relPath, 'LABEL':outlabel, 'CONDORDIR':condorDir, 'INPUTDIR':inDir, 'FILENAME':rawname, 'CMSSWBASE':relbase, 'OUTPUTDIR':outDir, 'LIST':idlist, 'ID':tmpcount}
            jdfName=condorDir+'/%(RELPATH)s_%(LABEL)s/%(FILENAME)s_%(LABEL)s_%(ID)s.job'%dict
            print jdfName
            jdf=open(jdfName,'w')
            jdf.write(
                """use_x509userproxy = true
universe = vanilla
Executable = %(RUNDIR)s/makeStep1.sh
Should_Transfer_Files = YES
WhenToTransferOutput = ON_EXIT
Transfer_Input_Files = %(RUNDIR)s/makeStep1.C, %(RUNDIR)s/%(POST)s/step1.cc, %(RUNDIR)s/%(POST)s/step1.h, %(RUNDIR)s/%(POST)s/step1_cc.d, %(RUNDIR)s/%(POST)s/step1_cc.so
Output = %(FILENAME)s_%(LABEL)s_%(ID)s.out
Error = %(FILENAME)s_%(LABEL)s_%(ID)s.err
Log = %(FILENAME)s_%(LABEL)s_%(ID)s.log
Notification = Never
Arguments = "%(FILENAME)s %(FILENAME)s_%(LABEL)s %(INPUTDIR)s/%(RELPATH)s %(OUTPUTDIR)s/%(RELPATH)s_%(LABEL)s '%(LIST)s'"

Queue 1"""%dict)
            jdf.close()
            os.chdir('%s/%s_%s'%(condorDir,relPath,outlabel))
            os.system('condor_submit %(FILENAME)s_%(LABEL)s_%(ID)s.job'%dict)
            os.system('sleep 0.5')                                
            os.chdir('%s'%(runDir))
            print count, "jobs submitted!!!"


signalList = [
    'BprimeBprime_M-900_TuneCUETP8M1_13TeV-madgraph-pythia8',
    'BprimeBprime_M-1000_TuneCUETP8M1_13TeV-madgraph-pythia8',
    'BprimeBprime_M-1100_TuneCUETP8M1_13TeV-madgraph-pythia8',
    'BprimeBprime_M-1200_TuneCUETP8M1_13TeV-madgraph-pythia8',
    'BprimeBprime_M-1300_TuneCUETP8M1_13TeV-madgraph-pythia8',
    'BprimeBprime_M-1400_TuneCUETP8M1_13TeV-madgraph-pythia8',
    'BprimeBprime_M-1500_TuneCUETP8M1_13TeV-madgraph-pythia8',
    'BprimeBprime_M-1600_TuneCUETP8M1_13TeV-madgraph-pythia8',
    #'BprimeBprime_M-1700_TuneCUETP8M1_13TeV-madgraph-pythia8',
    'BprimeBprime_M-1800_TuneCUETP8M1_13TeV-madgraph-pythia8',
    ]

signalOutList = ['TWTW','BZTW','BHTW','BZBH','BZBZ','BHBH']

for sample in signalList:
    rootfiles = EOSlist_root_files(inputDir+sample)
    relPath = sample        
    for outlabel in signalOutList:
        os.system('eos root://cmseos.fnal.gov/ mkdir -p '+outDir+sample+'_'+outlabel)
        os.system('mkdir -p '+condorDir+sample+'_'+outlabel)

        tmpcount = 0
        for i in range(0,len(rootfiles),20):            
            rawname = relPath
            count+=1
            tmpcount += 1

            idlist = (rootfiles[i].split('.')[0]).split('_')[-1]+' '
            for j in range(i+1,i+20):
                if j >= len(rootfiles): continue
                idlist += (rootfiles[j].split('.')[0]).split('_')[-1]+' '
            idlist = idlist.strip()
            print idlist

            dict={'RUNDIR':runDir, 'POST':runDirPost, 'RELPATH':relPath, 'LABEL':outlabel, 'CONDORDIR':condorDir, 'INPUTDIR':inDir, 'FILENAME':rawname, 'CMSSWBASE':relbase, 'OUTPUTDIR':outDir, 'LIST':idlist, 'ID':tmpcount}
            jdfName=condorDir+'/%(RELPATH)s_%(LABEL)s/%(FILENAME)s_%(LABEL)s_%(ID)s.job'%dict
            print jdfName
            jdf=open(jdfName,'w')
            jdf.write(
                """use_x509userproxy = true
universe = vanilla
Executable = %(RUNDIR)s/makeStep1.sh
Should_Transfer_Files = YES
WhenToTransferOutput = ON_EXIT
Transfer_Input_Files = %(RUNDIR)s/makeStep1.C, %(RUNDIR)s/%(POST)s/step1.cc, %(RUNDIR)s/%(POST)s/step1.h, %(RUNDIR)s/%(POST)s/step1_cc.d, %(RUNDIR)s/%(POST)s/step1_cc.so
Output = %(FILENAME)s_%(LABEL)s_%(ID)s.out
Error = %(FILENAME)s_%(LABEL)s_%(ID)s.err
Log = %(FILENAME)s_%(LABEL)s_%(ID)s.log
Notification = Never
Arguments = "%(FILENAME)s %(FILENAME)s_%(LABEL)s %(INPUTDIR)s/%(RELPATH)s %(OUTPUTDIR)s/%(RELPATH)s_%(LABEL)s '%(LIST)s'"

Queue 1"""%dict)
            jdf.close()
            os.chdir('%s/%s_%s'%(condorDir,relPath,outlabel))
            os.system('condor_submit %(FILENAME)s_%(LABEL)s_%(ID)s.job'%dict)
            os.system('sleep 0.5')                                
            os.chdir('%s'%(runDir))
            print count, "jobs submitted!!!"

dirList = [
    'WW_TuneCP5_13TeV-pythia8',
    'WZ_TuneCP5_13TeV-pythia8',
    'ZZ_TuneCP5_13TeV-pythia8',
    'ttH_M125_TuneCP5_13TeV-powheg-pythia8',
    'ttWJets_TuneCP5_13TeV_madgraphMLM_pythia8',
    'ttZJets_TuneCP5_13TeV_madgraphMLM_pythia8',
    'QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8',
    'QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8',
    'QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8',
    'QCD_HT200to300_TuneCP5_13TeV-madgraph-pythia8',
    'QCD_HT300to500_TuneCP5_13TeV-madgraph-pythia8',
    'QCD_HT500to700_TuneCP5_13TeV-madgraph-pythia8',
    'QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8',
    'DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8',
    'ST_s-channel_antitop_leptonDecays_13TeV-PSweights_powheg-pythia',
    'ST_s-channel_top_leptonDecays_13TeV-PSweights_powheg-pythia',
    'ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8',
    'ST_t-channel_top_4f_InclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8',
    'ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8',
    'ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8',
    'WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8',
    'WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8',
    'WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8',
    'WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8',
    'WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8',
    'WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8',
    'TT_Mtt-1000toInf_TuneCP5_PSweights_13TeV-powheg-pythia8',
    'TT_Mtt-700to1000_TuneCP5_13TeV-powheg-pythia8',
]
if shift == 'nominal':
    dirList.append('SingleElectron_Mar2018')
    dirList.append('SingleMuon_Mar2018')

for sample in dirList:
    os.system('eos root://cmseos.fnal.gov/ mkdir -p '+outDir+sample)
    os.system('mkdir -p '+condorDir+sample)
    relPath = sample

    rootfiles = EOSlist_root_files(inputDir+sample)
    tmpcount = 0
    for i in range(0,len(rootfiles),20):            
        rawname = relPath
        count+=1
        tmpcount += 1

        idlist = (rootfiles[i].split('.')[0]).split('_')[-1]+' '
        for j in range(i+1,i+20):
            if j >= len(rootfiles): continue
            idlist += (rootfiles[j].split('.')[0]).split('_')[-1]+' '
        idlist = idlist.strip()
        print idlist

        dict={'RUNDIR':runDir, 'POST':runDirPost, 'RELPATH':relPath, 'LABEL':outlabel, 'CONDORDIR':condorDir, 'INPUTDIR':inDir, 'FILENAME':rawname, 'CMSSWBASE':relbase, 'OUTPUTDIR':outDir, 'LIST':idlist, 'ID':tmpcount}
        jdfName=condorDir+'/%(RELPATH)s/%(FILENAME)s_%(ID)s.job'%dict
        print jdfName
        jdf=open(jdfName,'w')
        jdf.write(
            """use_x509userproxy = true
universe = vanilla
Executable = %(RUNDIR)s/makeStep1.sh
Should_Transfer_Files = YES
WhenToTransferOutput = ON_EXIT
Transfer_Input_Files = %(RUNDIR)s/makeStep1.C, %(RUNDIR)s/%(POST)s/step1.cc, %(RUNDIR)s/%(POST)s/step1.h, %(RUNDIR)s/%(POST)s/step1_cc.d, %(RUNDIR)s/%(POST)s/step1_cc.so
Output = %(FILENAME)s_%(ID)s.out
Error = %(FILENAME)s_%(ID)s.err
Log = %(FILENAME)s_%(ID)s.log
Notification = Never
Arguments = "%(FILENAME)s %(FILENAME)s %(INPUTDIR)s/%(RELPATH)s %(OUTPUTDIR)s/%(RELPATH)s '%(LIST)s'"

Queue 1"""%dict)
        jdf.close()
        os.chdir('%s/%s'%(condorDir,relPath))
        os.system('condor_submit %(FILENAME)s_%(ID)s.job'%dict)
        os.system('sleep 0.5')                                
        os.chdir('%s'%(runDir))
        print count, "jobs submitted!!!"

dirList = [
    'TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8',
    'TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8',
    'TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8'
    ]
TTOutList = ['Mtt0to700','Mtt700to1000','Mtt1000toInf']

for sample in dirList:
    rootfiles = EOSlist_root_files(inputDir+sample)
    relPath = sample        
    for outlabel in TTOutList:
        os.system('eos root://cmseos.fnal.gov/ mkdir -p '+outDir+sample+'_'+outlabel)
        os.system('mkdir -p '+condorDir+sample+'_'+outlabel)

        tmpcount = 0
        for i in range(0,len(rootfiles),20):            
            rawname = relPath
            count+=1
            tmpcount += 1

            idlist = (rootfiles[i].split('.')[0]).split('_')[-1]+' '
            for j in range(i+1,i+20):
                if j >= len(rootfiles): continue
                idlist += (rootfiles[j].split('.')[0]).split('_')[-1]+' '
            idlist = idlist.strip()
            print idlist

            dict={'RUNDIR':runDir, 'POST':runDirPost, 'RELPATH':relPath, 'LABEL':outlabel, 'CONDORDIR':condorDir, 'INPUTDIR':inDir, 'FILENAME':rawname, 'CMSSWBASE':relbase, 'OUTPUTDIR':outDir, 'LIST':idlist, 'ID':tmpcount}
            jdfName=condorDir+'/%(RELPATH)s_%(LABEL)s/%(FILENAME)s_%(LABEL)s_%(ID)s.job'%dict
            print jdfName
            jdf=open(jdfName,'w')
            jdf.write(
                """use_x509userproxy = true
universe = vanilla
Executable = %(RUNDIR)s/makeStep1.sh
Should_Transfer_Files = YES
WhenToTransferOutput = ON_EXIT
Transfer_Input_Files = %(RUNDIR)s/makeStep1.C, %(RUNDIR)s/%(POST)s/step1.cc, %(RUNDIR)s/%(POST)s/step1.h, %(RUNDIR)s/%(POST)s/step1_cc.d, %(RUNDIR)s/%(POST)s/step1_cc.so
Output = %(FILENAME)s_%(LABEL)s_%(ID)s.out
Error = %(FILENAME)s_%(LABEL)s_%(ID)s.err
Log = %(FILENAME)s_%(LABEL)s_%(ID)s.log
Notification = Never
Arguments = "%(FILENAME)s %(FILENAME)s_%(LABEL)s %(INPUTDIR)s/%(RELPATH)s %(OUTPUTDIR)s/%(RELPATH)s_%(LABEL)s '%(LIST)s'"

Queue 1"""%dict)
            jdf.close()
            os.chdir('%s/%s_%s'%(condorDir,relPath,outlabel))
            os.system('condor_submit %(FILENAME)s_%(LABEL)s_%(ID)s.job'%dict)
            os.system('sleep 0.5')                                
            os.chdir('%s'%(runDir))
            print count, "jobs submitted!!!"


print("--- %s minutes ---" % (round(time.time() - start_time, 2)/60))



