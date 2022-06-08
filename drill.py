import pgzrun
from selfmaths import *

WIDTH,HEIGHT=1250,800 #窗口长1250px，宽800px

HillsAndOres={'rhill':'rock','ihill':'iron','dhill':'diamond'} #山名与矿物名的对应关系
Land=Actor('land') #地面
Land.bottomleft=(0,HEIGHT) #地面位置，左下在窗口左下
Home=Actor('home') #收货点
Home.bottomleft=Land.topleft #收货点位置，左下角在地面左上
Help=Actor('help')
Help.topright=(WIDTH,0)

Ores={'rock':'0','iron':'0','diamond':'0','money':'0'} #矿物数量表

KeyAndTexts={} #按键与工人名字、序号对照表
KeyAndTexts[keys.K_1]=('worker',1)
KeyAndTexts[keys.K_2]=('van',2)
KeyAndTexts[keys.K_3]=('super van',3)
KeyAndTexts[keys.K_4]=('DRILLER',4)
KeyAndTexts[keys.K_5]=('SUPER DRILLER',5)

NumsAndNames={} #序号与工人参数对照表
NumsAndNames[1]=(1,1,'worker')
NumsAndNames[2]=(2,2,'van')
NumsAndNames[3]=(2,4,'sup_van')
NumsAndNames[4]=(3,4,'driller')
NumsAndNames[5]=(5,5,'sup_driller')

NumsAndPrices={} #序号与工人价格对照表
NumsAndPrices[1]='20'
NumsAndPrices[2]='40'
NumsAndPrices[3]='55'
NumsAndPrices[4]='75'
NumsAndPrices[5]='100'

Extra={} #购买时额外物品对照表，还未实装
Extra[3]=('iron','1')
Extra[4]=('iron','3')
Extra[5]=('diamond','3')

OresAndPrices={} #矿物与价格对照表
OresAndPrices['rock']=1
OresAndPrices['iron']=2
OresAndPrices['diamond']=3

MenuNo=0 #菜单序号


class Hill: #山的类
    def __init__(self,Img,x,Count): #山的参数 Img-山图片 x-x坐标 Count-山的耐久
        self.Actor=Actor(Img) #山
        self.Actor.x=x #山的x坐标
        self.Actor.bottom=Land.top #山的y坐标，底部在地面上
        self.Count=str(Count) #耐久转换为字符串格式，方便绘制
        self.Death=0 #山是否被挖空
    def draw(self): #绘制山的相关部分
        self.Actor.draw() #绘制山
        screen.draw.text(self.Count,(self.Actor.x,self.Actor.y-20)) #绘制耐久度
    def up(self): #山的更新部分
        if int(self.Count)<=0: #如果耐久小于等于0
            self.Death=1 #视为山没了

         
class Worker: #工人的类
    def __init__(self,Speed=1,Count=1,Img='worker'): #工人的参数 其实没有
        self.Speed=Speed
        self.Count=Count
        self.Actor=Actor(Img,(Home.right,0)) #工人
        self.FD=0 #工人是否往左右走
        self.Ore=Actor('rock') #工人所背矿物
        self.Ore.bottom=Land.top-self.Actor.height-10 #矿物底部位置在工人上方10px
        
    def draw(self): #绘制工人的相关部分
        if self.Actor.bottom<Land.top: #如果工人悬空
            screen.blit('umbrella',(self.Actor.x-35,self.Actor.top-80)) #绘制降落伞
        self.Actor.draw() #绘制工人
        if Hills and self.FD==-1: #如果工人不往右即挖到矿物，同时还没通关
            self.Ore.draw() #绘制矿物图标

            
    def up(self): #工人的更新部分
        if self.Actor.bottom<Land.top: #如果工人悬空
            self.Actor.y+=0.1 #工人下降0.1px
        if Hills: #如果还没通关
            if self.FD==1: #如果工人往右
                    h=Hills[0]
                    if self.Actor.colliderect(h.Actor): #如果与某个山碰撞
                        h.Count=StrP(h.Count,-self.Count) #山的耐久减1
                        self.FD=-1 #工人往左
                        self.Actor.image+='_l' #工人往左的图像
                        self.Ore.image=HillsAndOres[h.Actor.image] #利用写好的矿物-山关系更改图像
                        
            elif self.FD==-1: #如果工人往左
                self.Ore.x=self.Actor.x #矿物的x坐标设为工人的
                if self.Actor.colliderect(Home): #如果碰到收货点
                    Ores[self.Ore.image]=StrP(Ores[self.Ore.image],self.Count)
                    self.FD=1 #工人往右
                    self.Actor.image=self.Actor.image[:-2] #工人往右的图像

            elif not self.FD: #如果工人不移动
                if self.Actor.bottom<Land.top: #如果悬空
                    self.Actor.y+=5 #工人下降5px
                else: #如果没有
                    self.FD=1 #开始往右
                    self.Actor.bottom=Land.top #避免落到地下方
                    
        self.Actor.x+=self.FD*self.Speed #工人依据左右方向移动


class LifeText: #文本的类
    def __init__(self,Msg,Pos,Size=20,LifeTime=-1): #文本参数
        self.Msg=Msg #文本
        self.Pos=Pos #位置
        self.LifeTime=LifeTime #持续时间，-1表示永久存在
        self.Size=Size #大小
        self.Death=0 #时间是否结束

    def draw(self): #绘制文本部分
            screen.draw.text(self.Msg,self.Pos,color='black',fontsize=self.Size) #依据文本、位置、大小绘制黑色文本
            
    def up(self): #文本更新部分
        self.LifeTime-=1 #持续时间-1
        if not self.LifeTime: #如果时间到了
            self.Death=1 #表示时间结束


class Menu: #菜单类，即矿物和钱的显示
    def __init__(self,Pos,Img): #菜单参数
        self.Pos=Pos #位置
        self.Icon=Actor(Img) #图标
        self.Icon.topleft=Pos #设置位置到左上角

    def draw(self): #绘制部分
        self.Icon.draw() #绘制图标
        screen.draw.text(Ores[self.Icon.image],self.Icon.topright,fontsize=65,color='black') #绘制文本，文字为矿物表中对应的文本，颜色为黑，左上位置在图标右上角，大小65
               
#       
Hills=[Hill('rhill',500,1500),Hill('ihill',800,3000),Hill('dhill',1150,5000)] #山的系列
Workers=[Worker()] #工人的系列
Texts=[] #文本系列
Menus=[] #四个菜单
Menus.append(Menu((0,HEIGHT//2-50),'rock'))
Menus.append(Menu((0,HEIGHT//2),'iron'))
Menus.append(Menu((0,HEIGHT//2+50),'diamond'))
Menus.append(Menu((0,HEIGHT//4),'money'))


def update(): #更新部分，这一段执行60次/s
    for i in Hills: #逐一翻找山
        i.up() #山的更新代码
        if i.Death: #如果山没了
            Hills.remove(i) #删掉山
    for i in Texts: #文本更新，和上面山的工作原理相同
        i.up()
        if i.Death:
            Texts.remove(i)
    for i in Workers: #逐一翻找工人
        i.up() #工人更新代码

    if not Hills: #如果通关
        for i in Workers: #逐一翻找工人
            i.Actor.y-=5 #令其上浮5px
            if i.Actor.top<=0: #如果到顶
                Workers.remove(i) #将其删除

def draw(): #绘制部分
    screen.fill((255,255,255)) #用白色填满背景

    if not Hills+Workers: #如果山和工人都没有了
        screen.draw.text('You Win!',(WIDTH//4,HEIGHT//4),fontsize=100,color='yellow') #绘制胜利文本，金色，大小100

    for i in Hills+Workers+Texts+Menus: #逐一翻找山和工人
        i.draw() #它们的绘制代码
    Home.draw() #绘制收货点
    Land.draw() #绘制地面
    Help.draw() #绘制帮助按钮
    

def on_key_down(key): #当有按键按下时执行此段
    global Texts,MenuNo,KeyAndTexts,NumsAndNames,NumsAndPrices #把这些变量声明为全局变量，否则不能用
    if Hills: #如果没通关
        for i,j in KeyAndTexts.items(): #逐一翻找键与名字对应表
            if key==i: #如果按下的键刚好是翻找的
                if MenuNo==j[1]: #如果菜单标号正好是这个
                    Texts=[] #代表关闭，先清空文本
                    MenuNo=0 #菜单标号设为0
                    break #不再翻找
                else:
                    Texts=[] #如果菜单标号不是，先清空文本
                    MenuNo=j[1] #文本标号根据对应表更换
                    Msg='Buy {}({}N)?\nEnter for yes\nPress again for no'.format(j[0],NumsAndPrices[MenuNo]) #即将显示的文本，大括号会被转换为对应表中的名字
                    e=Extra.get(MenuNo) #从额外表中安全获取值
                    if e: #如果获取到
                        Msg='Buy {}?\n({}N and {}*{})\nEnter for yes\nPress again for no'.format(j[0],NumsAndPrices[MenuNo],e[0],e[1]) #更改文本以显示额外物品
                    Texts.append(LifeText(Msg,(WIDTH*0.3,HEIGHT//2),75)) #在宽度约1/3，高1/2个屏幕处绘制大小75的文本
                    break #不再翻找
        if key==keys.RETURN and MenuNo: #如果按下回车并且标号不是0
            Texts=[] #先清空文本
            e=Extra.get(MenuNo) #安全获取额外值
            if e: #如果获取到
                if int(e[1])>int(Ores[e[0]]): #如果当前矿不够
                    e=1 #表示不能
                else: #否则
                    e=0 #表示能
            if int(NumsAndPrices[MenuNo])>int(Ores['money']) or e: #如果价格比钱高
                Texts.append(LifeText('No enough money or ores!',(WIDTH*0.3,HEIGHT//2),75,60)) #不能购买
            else: #如果价格比钱低或者相等
                n=NumsAndNames[MenuNo] #获取对应工人参数并逐一存储
                s=n[0]
                c=n[1]
                i=n[2]
                Workers.append(Worker(s,c,i)) #用参数创建工人
                Texts.append(LifeText('Success!',(WIDTH*0.3,HEIGHT//2),75,60)) #成功购买
                Ores['money']=StrP(Ores['money'],-int(NumsAndPrices[MenuNo])) #扣除钱
                MenuNo=0 #菜单标号设为0

def on_mouse_down(pos,button): #当鼠标按下时执行此段
    global Home,Ores,OresAndPrices,MenuNo,Texts #声明全局变量
    if button==mouse.LEFT and Home.collidepoint(pos): #如果左键按下并且鼠标碰到收货点
        t=0 #存储所卖矿物价格
        for i,j in Ores.items(): #逐一翻找钱
            if i!='money': #如果翻到的不是钱本身
                t+=int(j)*OresAndPrices[i] #利用对应表计算钱
                Ores[i]='0' #把矿物设为0
        Ores['money']=StrP(Ores['money'],t) #金钱增加
        Texts.append(LifeText('Sell!',(Home.x,Home.top-15),20,60)) #成功售卖

    if button==mouse.LEFT and Help.collidepoint(pos): #如果按下左键并且碰到帮助按钮
        if MenuNo==6: #如果菜单标号为6表示退出帮助
            Texts=[] #清空文本
            MenuNo=0 #菜单标号设为0
        else: #如果不是
            MenuNo=6 #菜单标号设为6
            Texts=[] #清空文本
            Msg='''
Help Menu
Drill-An afk game
Buy workers by keyboard 1-5
Sell ores by click home
(Rock-1N Iron-2N Diamond-3N)
Finish all hills off to win
Have fun!
''' #帮助文本
            Texts.append(LifeText(Msg,(150,150),50)) #将其显示到屏幕上

pgzrun.go()
