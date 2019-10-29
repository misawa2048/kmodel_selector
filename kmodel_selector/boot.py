# Untitled - By: misaw - 日 10 13 2019

import sensor, image, time, lcd
from pye_mp import pye
from machine import I2C
import audio
from fpioa_manager import *
from time import sleep

SEL_DISP_NUM = 7
SETTINGS_DIR_NAME = "-- settings --"
#====================
from Maix import GPIO
class ButtonClass():
    _btns = [None,None]
    _btnOn = [False,False]
    _btnOnPrev = [False,False]
    _btnTrg = [False,False]
    _btnRel = [False,False]

    def __init__(self):
        fm.register(board_info.BUTTON_A, fm.fpioa.GPIO1)
        fm.register(board_info.BUTTON_B, fm.fpioa.GPIO2)
        self._btns[0]=GPIO(GPIO.GPIO1, GPIO.IN, GPIO.PULL_UP) #PULL_UP is required here!
        self._btns[1]=GPIO(GPIO.GPIO2, GPIO.IN, GPIO.PULL_UP) #PULL_UP is required here!
        #self.reset()

    def reset(self):
        self._btnOn = self._btnOnPrev = [False,False]
        self._btnTrg = self._btnRel = [False,False]

    def update(self):
        for id in range(2):
            self._btnOnPrev[id] = self._btnOn[id]
            self._btnOn[id] = (self._btns[id].value()==0)
            self._btnTrg[id] = (self._btnOn[id]==True) and (self._btnOnPrev[id]==False)
            self._btnRel[id] = (self._btnOn[id]==False) and (self._btnOnPrev[id]==True)

    def getTrg(self, _btnId):
        return self._btnTrg[0 if _btnId==board_info.BUTTON_A else 1]

    def getRel(self, _btnId):
        return self._btnRel[0 if _btnId==board_info.BUTTON_A else 1]

    def getOn(self, _btnId):
        return self._btnOn[0 if _btnId==board_info.BUTTON_A else 1]

#====================
from Maix import GPIO
from Maix import I2S
class WavClass():
    _isPlaying = False
    _player = None
    _wavInfo = None
    _wavDev = None

    def __init__(self):
        self._isPlaying=False
        self._wavDev = I2S(I2S.DEVICE_0)
        fm.register(board_info.SPK_SD, fm.fpioa.GPIO0)
        spk_sd=GPIO(GPIO.GPIO0, GPIO.OUT)
        spk_sd.value(1) #Enable the SPK output
        fm.register(board_info.SPK_DIN,fm.fpioa.I2S0_OUT_D1)
        fm.register(board_info.SPK_BCLK,fm.fpioa.I2S0_SCLK)
        fm.register(board_info.SPK_LRCLK,fm.fpioa.I2S0_WS)

    def update(self):
        if(self._isPlaying):
            ret = self._player.play()
            if (ret == None) or (ret==0):
                self.stop()
        return self._isPlaying

    def play(self,_filename, _isOverrite=True):
        if(_isOverrite==True)and(self._isPlaying==True):
            self.stop()

        if(self._isPlaying==False):
            try:
                self._isPlaying=True
                self._player = audio.Audio(path = _filename)
                self._wavInfo = self._player.play_process(self._wavDev)
                self._wavDev.channel_config(self._wavDev.CHANNEL_1, I2S.TRANSMITTER,resolution = I2S.RESOLUTION_16_BIT, align_mode = I2S.STANDARD_MODE)
                self._wavDev.set_sample_rate(self._wavInfo[1])
                self._player.volume(100)
                ret = self._player.play()
            except:
                self._isPlaying=False
                pass

    def stop(self):
        if(self._isPlaying==True):
            self._isPlaying=False
        try:
            self._player.volume(0)
            self._player.finish()
        except:
            pass

    def wait(self):
        while(self._isPlaying):
            ret = self._player.play()
            if (ret == None) or (ret==0):
                self.stop()

#====================
class CatInfoList():
    def __init__(self):
        self.dirName = ''
        self.modelName = ''
        self.wavName = ''
        self.classList = []

#====================
import uos
class FilerClass():
    m_infoList = [] #[[dirStr,modelStr,wavStr,[class1,2,,,]],,]

    def __init__(self):
        self.m_infoList = []

    def getAllInfo(self,_basePath):
        self.m_infoList = [] #[[dirStr,modelStr,wavStr,[class1,2,,,]],,]
        files = uos.listdir(_basePath)
        for filename in files:
            if len(filename) < 20 and len(filename) > 2:
                catFolderPath = _basePath+'/'+filename
                if (self.getIsFile(catFolderPath)==False):
                    fd = open(catFolderPath+'/label.csv','r', encoding='utf-8')
                    self.m_infoList.append(self.getCategoryInfo(catFolderPath))
                    fd.close()
        #append [settings] line in m_infoList
        tmpCatInfoList = CatInfoList()
        tmpCatInfoList.dirName = SETTINGS_DIR_NAME
        tmpCatInfoList.wavName = "_settings"
        tmpCatInfoList.modelName = "mSettings"
        tmpCatInfoList.classList = []
        self.m_infoList.append(tmpCatInfoList)

        return self.m_infoList

    def isSelectSettings(self): # is [settings] line?
        global g_cFiler
        global g_selCnt
        tmpInfoList = g_cFiler.getInfoList()
        return True if tmpInfoList[g_selCnt].dirName == SETTINGS_DIR_NAME else False

    def getIsFile(self,_path):
        ret = True
        try:
            tmpfile = open(_path,'rb')
        except:
            ret = False
        else:
            tmpfile.close()
        return ret

    def getCategoryInfo(self,_labelPath):
        tmpCatInfoList = CatInfoList()
        tmpCatInfoList.dirName = _labelPath.rsplit('/',1)[-1]

        fd = open(_labelPath+'/label.csv','r', encoding='utf-8')
        line = line2Utf8(fd.readline())
        line = line2Utf8(fd.readline())
        strList = line.split(',')
        tmpCatInfoList.wavName = strList[0]
        line = line2Utf8(fd.readline())
        strList = line.split(',')
        tmpCatInfoList.modelName = strList[0]
        line = line2Utf8(fd.readline())
        strList = line.split(',')
        fd.close()

        tmpCatInfoList.classList = []
        for name in strList:
            tmpCatInfoList.classList.append(name)
        return tmpCatInfoList

    def getInfoList(self):
        return self.m_infoList

    def getDirOrFileNameFromFullPath(self,_filePath):
        return _filePath.rsplit('/', 1)

g_isLoop = False
g_i2c = None
g_clock = None
g_task = None
g_powArr = []

g_cButton = ButtonClass()
g_cWav = WavClass()
g_cFiler = FilerClass()

#--------------------
def line2Utf8(_data):
    _data = _data.replace(chr(0xfeff),'') # bom
    _data = _data.replace('\r','')
    _data = _data.replace('\n','')
    return _data

#--------------------
def setBacklight(_level):
    global g_i2c
    level = min(max(_level,0),8)
    g_i2c.writeto_mem(0x34, 0x91,int((_level+7) << 4))

#--------------------
def setup():
    global g_isLoop
    global g_i2c
    global g_clock
    g_i2c = I2C(I2C.I2C0, freq=400000, scl=28, sda=29)
    lcd.init()
    lcd.rotation(2)
    lcd.clear()
    #lcd.font(lcd.FONT_DejaVu24)
    g_clock = time.clock()

    g_isLoop = True;

    setBacklight(1)

#--------------------
def updateSelect():
    global g_clock
    global g_cButton
    global g_cWab
    global g_cFiler

    g_clock.tick()

    g_cButton.update()
    #print(g_clock.fps())

    if(fileTestUpdate()):
        tmpInfoList = g_cFiler.getInfoList()
        classStr = ''
        classList = tmpInfoList[g_selCnt].classList
        for cl in classList:
            classStr += cl+','
        lcd.draw_string(0,0, classStr, lcd.WHITE, lcd.BLACK)
        fullPath = 'models/' + tmpInfoList[g_selCnt].dirName+'/'+tmpInfoList[g_selCnt].wavName
        spcStr='                          '
        sttCnt = min(max(0,len(tmpInfoList)-SEL_DISP_NUM),g_selCnt)
        for i in range(min(SEL_DISP_NUM,len(tmpInfoList))):
            selCol = lcd.RED if (sttCnt+i)==g_selCnt else lcd.BLUE
            dispStr=str(sttCnt+1+i)+':'+tmpInfoList[sttCnt+i].dirName+spcStr
            lcd.draw_string(0,20+i*16,dispStr, lcd.WHITE, selCol)
        if(tmpInfoList[g_selCnt].dirName == SETTINGS_DIR_NAME):
            fullPath = 'snd/sys_voicesettings'
        g_cWav.stop()
        g_cWav.play('/sd/'+fullPath+'.wav')
        #g_cWav.wait()
    g_cWav.update()
    return True

#--------------------
import KPU as kpu
def resetKpu():
    global g_selCnt
    global g_cFiler
    global g_task
    global g_powArr

    tmpInfoList = g_cFiler.getInfoList()
    fullPath = tmpInfoList[g_selCnt].dirName+'/'+tmpInfoList[g_selCnt].modelName
    lcd.draw_string(0,20, fullPath, lcd.GREEN, lcd.BLACK)
    fullPath = '/sd/models/'+fullPath+'.kmodel'
    g_powArr = []
    for ii in range(len(fullPath)):
           g_powArr.append(0.0)

    if(g_task==None):
        try:
            g_task = kpu.load(fullPath)
        except:
            lcd.draw_string(0,0, "Error0: Cannot find kmodel", lcd.WHITE, lcd.RED)

    sensor.reset()
    sensor.set_pixformat(sensor.RGB565)
    sensor.set_framesize(sensor.QVGA)
    sensor.set_windowing((224, 224))
    #sensor.skip_frames(time = 20000)
    sensor.run(1)

#--------------------
import KPU as kpu
def updateKpu():
    global g_cFiler
    global g_selCnt
    global g_cWav
    global g_task
    global g_powArr

    if(g_task==None):
        info = g_cFiler.getInfoList()[g_selCnt]
        fullPath = info.dirName+'/'+info.modelName+'.kmodel'
        try:
            g_task = kpu.load('/sd/model/'+fullPath)
            #g_task = kpu.load("/sd/model/9d00d555d7925a1b_mbnet10_quant.kmodel")
        except:
            lcd.draw_string(0,20, "Error1: Cannot find kmodel", lcd.WHITE, lcd.RED)
            g_cWav.play('/sd/snd/sys_ng.wav')
            g_cWav.wait()

    img = sensor.snapshot()
    fmap = kpu.forward(g_task, img,False)
    plist=fmap[:]
    pmax=max(plist)
    max_index=plist.index(pmax)

    colArr = [(255,0,0),(0,255,0),(0,0,255),(5,5,5),(0,255,255),(255,255,0),(128,128,128),(50,200,50)]
    for id in range(0, len(plist)):
        if(plist[id]>0.9):
            g_powArr[id] = min((g_powArr[id]+plist[id]-0.9)*5.0,100.0)
        else:
            g_powArr[id] -= 10.0
            g_powArr[id] = max(g_powArr[id],0.0)
        img.draw_rectangle((10,50+10*id,int(g_powArr[id]*1),8),colArr[id&7],10,True)

        if (g_powArr[id]>=100.0):
            g_powArr[id] = 0.0
            info = g_cFiler.getInfoList()[g_selCnt]
            labels = info.classList
            wavPath = info.dirName+'/'+labels[id]+'.wav'
            lcd.draw_string(0, 20, wavPath)
            g_cWav.play('/sd/models/'+wavPath)
            g_cWav.wait()
    a = lcd.display(img)
    g_cButton.update()

#--------------------
def destroy():
    lcd.deinit()

#--------------------
def fileInit(_basePath):
    global g_cFiler
    tmpInfoListArr = g_cFiler.getAllInfo(_basePath)

#--------------------
def fileTestUpdate():
    global g_selCnt
    global g_cFiler
    ret = False
    if(g_selCnt<0 or (g_cButton.getTrg(board_info.BUTTON_B))):
        ret = True
        tmpInfoList = g_cFiler.getInfoList()
        g_selCnt+=1
        if(g_selCnt >= len(tmpInfoList)):
            g_selCnt = 0
    return ret

#--------------------
g_dbgCnt=0
g_selCnt=-1
g_rno=0
fileInit('/sd/models')
setup()
time.sleep(1)
while(g_isLoop):
    if(g_rno==0):
        g_isLoop = updateSelect()
        col = lcd.BLUE if g_cButton.getOn(board_info.BUTTON_B) else lcd.RED
        lcd.draw_string(lcd.width()-len(str(g_dbgCnt))*8,0, str(g_dbgCnt), col, lcd.BLACK) #'loop:'+
        g_dbgCnt+=1
        if g_cButton.getOn(board_info.BUTTON_B):
            g_dbgCnt=0
        if g_cButton.getOn(board_info.BUTTON_A):
            if(g_cFiler.isSelectSettings()==False):
                g_cButton.reset()
                g_rno=1
                resetKpu()
                time.sleep(0.1)
                g_cWav.play('/sd/snd/sys_ok.wav')
                g_cWav.wait()
    else:
        updateKpu()
        if g_cButton.getOn(board_info.BUTTON_A):
            g_dbgCnt=0
            #g_cButton.reset()
            #a=kpu.deinit(g_task)
            #g_rno=0
    sleep(0.01)
destroy()
