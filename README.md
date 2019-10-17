# kmodel_selector

kmodel selector for M5StickV
sample movie is here; https://youtu.be/APMaJ7DCfN8

This script is a object detector it can select a kmodel from some models.
This script doesn't work alone, needs below:
  * .kmodels : It may create by V-Training site
      http://v-training.m5stack.com/
      M5Stack Docs > M5StickV > QuickStart > V-Training

  * .wmv audio files, using to speak .kmodel labels and object classes.

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


[label.csv]
//,,,,,,, // 1st line : no use(for comment)
c1_petbottle,,,,,,, // 2nd line : filename of .wav file for label name 
ad00df55d7e25a1b_mbnet10_quant,,,,,,, // 3rd line : filename of .kmodel
kurot,akat,shirot,,,,, // 4th line : filenames of .wav file for classes in .kmodel


