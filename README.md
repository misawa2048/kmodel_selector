# kmodel_selector for M5StickV

![image of demo](https://i.ytimg.com/vi/APMaJ7DCfN8/hqdefault.jpg?sqp=-oaymwEZCNACELwBSFXyq4qpAwsIARUAAIhCGAFwAQ==&rs=AOn4CLA-hBSxCVmJyfx8ZAq17gno0UseHA)  

kmodel selector using M5StickV for blind person  
sample movie is here; https://youtu.be/APMaJ7DCfN8  

*What is M5StickV?  
M5StickV is an Edge AI Camera using K210 RiskV chip.  
https://m5stack.com/collections/all/products/stickv  
  
*What is kmodel_selector?  
This script is an object detector it can customize by user  
(blind person may need help to setup, sorry).  
and may support any language because user may provide his own voice data. 

This script doesn't work alone, needs below:  
  * .kmodels : It may create by V-Training site  
      http://v-training.m5stack.com/  
      M5Stack Docs > M5StickV > QuickStart > V-Training  
  
  * .wmv audio files, using to speak .kmodel labels and object classes.  

```
<directry tree>  
/sd/ : top level of sd card in M5Stick V  
 |-boot.py   : this script  
 |-resdme.txt: this text  
 |-/snd/     : .wav file for system sound  
     |-sys_decide.wav  : .wav file for system sound(decide sound)  
 |-/models/  : parent folder of kmodel folders  
     |-/{model 1}/  : 1st folder of kmodel {nameable}  
         |-label.csv  : utf-8 .csv file [see below]  
         |-{kmodel1.kmodel}  : .kmodel generated by V-Training {nameable}   
         |-{kmodel1.wav}     : monoral audio file to speak model name {nameable}  
         |-{class1.wav}      : audio file of 1st class in .kmodel {nameable}  
         |-{class2.wav}      : audio file of 2nd class in .kmodel {nameable}  
         |-{class3.wav}      : audio file of 3rd class in .kmodel {nameable}  
                 :  
         |-{classx.wav}      : audio file of final class in .kmodel {nameable}  
     |-/{model 2}/  : 2nd folder of kmodel {nameable}  
         |-label.csv  : utf-8 .csv file  
         |-{kmodel2.kmodel}  : .kmodel generated by V-Training {nameable}   
                 :  
```  
  
```
[label.csv]  
//,,,,,,, // 1st line : no use(for comment)  
c1_petbottle,,,,,,, // 2nd line : filename of .wav file for label name   
ad00df55d7e25a1b_mbnet10_quant,,,,,,, // 3rd line : filename of .kmodel  
kurot,akat,shirot,,,,, // 4th line : filenames of .wav file for classes in .kmodel  
```  
  
![system image](https://github.com/misawa2048/kmodel_selector/blob/master/system_image.png)  

# An easier way to make wav files

1.Record voice data including all of classes [here](https://cloud.google.com/text-to-speech/).
2.Trim each wav data using [WavePad音声編集ソフト](https://www.nch.com.au/wavepad/jp/index.html?kw=wav%20%E7%B7%A8%E9%9B%86&gclid=EAIaIQobChMIu6mCjbfA5QIV0QhcCh2Y9g2EEAEYASAAEgJlHPD_BwE) for free.
