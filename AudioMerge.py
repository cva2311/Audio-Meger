# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 10:40:39 2019

@author: Siva
"""

''' Python Code to read the list of audio files and merge using SOX utility in Linux '''

import sys,os
import glob
#import time
#from datetime import datetime

MrgAudLog = open("MergeAudio.log","w")
ReadAudLog = open("ReadAudio.log","w")
DeleteAudLog = open("DeleteAudio.log","w")


def setaudiopath():
    Testpath = os.getcwd()
    Audiopatharray = []
    Audiopatharray.append(Testpath)
    Silencewav = Testpath+"/"+"silence"+"/"+"silence.wav"
    Audiopatharray.append(Silencewav)
    Outputwav = Testpath+"/"+"MergdAudio"+"/"+"MergdAudio_"
    Audiopatharray.append(Outputwav)
    ShellFilePath = "./"+"AudioMerge.sh"
    Audiopatharray.append(ShellFilePath)
    return Audiopatharray
   

def MergeAudio(uttwavpath,GetPath):
    #Testpath = GetPath[0]
    Silencewav = GetPath[1]
    Outputwav = GetPath[2]
    ShellFilePath = GetPath[3]

    MrgeCnt = 0
    prevwav = Silencewav    

   
    for currentfile in glob.glob("*.wav"):
        ReadAudLog.write(str(currentfile)+"_"+str(MrgeCnt))
        ReadAudLog.write("\n")
        MrgeCnt = MrgeCnt + 1
        ##Call Sox
        Scmd = ShellFilePath+" "+prevwav+" "+Silencewav+" "+uttwavpath+str(currentfile)+" "+Outputwav+str(MrgeCnt)+".wav"
        MrgAudLog.write(Scmd) 
        MrgAudLog.write("\n") 
        os.system(Scmd)
         #To Debug
        prevwav = Outputwav+str(MrgeCnt)+".wav"
        if(MrgeCnt>1):
            CurMrgeCnt = MrgeCnt - 1
            TempAudio = Outputwav+str(CurMrgeCnt)+".wav"
            os.remove(TempAudio)   
            DeleteAudLog.write(str(TempAudio))
            DeleteAudLog.write("\n")
    return MrgeCnt

def main(args):
    GetPath = setaudiopath() 
    if len(args)!=1:
        sys.stderr.write('Usage : AudioMerge.py <<Audio file path to be merged is required')
        sys.exit(1)
    
    uttwavpath = sys.argv[1]
    
    os.chdir(uttwavpath)
    
    WavFileCount = sum(1 for filename in glob.glob("*.wav"))  
    print ("Number of Wav file in the chosen directory is ",WavFileCount)
    
    MrgedAudioCnt = MergeAudio(uttwavpath,GetPath)
    
    print ("Total Number of Audio Merged",MrgedAudioCnt)
    
    if(MrgedAudioCnt == WavFileCount):
        print ("Audio Merging is Successful !!!!")
    else:
        print ("Audio Merging Failed !!!")
        FaultAudioLog = open("FaultAudioMerge.log","w")
        FaultAudioLog.write("Audio Merging Failed !!!" )
        FaultAudioLog.close()

    MrgAudLog.close()
    ReadAudLog.close()
    DeleteAudLog.close()
    

if __name__=='__main__':
    main(sys.argv[1:])
    

    
        
    
    
