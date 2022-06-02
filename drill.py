import pgzrun
from selfmaths import *

WIDTH,HEIGHT=1250,800 #窗口长1250px，宽800px

HillsAndOres={'rhill':'rock','ihill':'iron','dhill':'diamond'} #山名与矿物名的对应关系
Land=Actor('land') #地面
Land.bottomleft=(0,HEIGHT) #地面位置，左下在窗口左下
Home=Actor('home') #收货点
Home.bottomleft=Land.topleft #收货点位置，左下角在地面左上

Ores={'rock':'0','iron':'0','diamond':'0','money':'100'} #矿物数量表

KeyAndTexts={}
KeyAndTexts[keys.K_1]=('worker',1)
KeyAndTexts[keys.K_2]=('van',2)
KeyAndTexts[keys.K_3]=('super van',3)
KeyAndTexts[keys.K_4]=('DRILLER',4)
KeyAndTexts[keys.K_5]=('SUPER DRILLER',5)

NumsAndNames={}
NumsAndNames[1]=(1,1,'worker')
NumsAndNames[2]=(2,2,'van')
NumsAndNames[3]=(2,4,'sup_van')
NumsAndNames[4]=(3,4,'driller')
NumsAndNames[5]=(5,5,'sup_driller')

NumsAndPrices={}
NumsAndPrices[1]=20
NumsAndPrices[2]=40
NumsAndPrices[3]=55
NumsAndPrices[4]=75
NumsAndPrices[5]=100

Extra={}
Extra[3]=('iron',1)
Extra[4]=('iron',3)
Extra[5]=('diamond',3)

OresAndPrices={}
OresAndPrices['rock']=1
OresAndPrices['iron']=2
OresAndPrices['diamond']=3

MenuNo=0


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
        self.Ore.bottom=Land.top-self.Actor.height-10
        
    def draw(self): #绘制工人的相关部分
        self.Actor.draw() #绘制工人
        if self.FD==-1: #如果工人不往右即挖到矿物
            self.Ore.draw() #绘制矿物图标

            
    def up(self): #工人的更新部分
        if self.Actor.bottom<Land.top: #如果工人悬空
            self.Actor.y+=0.1 #工人下降0.1px
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


class LifeText:
    def __init__(self,Msg,Pos,Size=20,LifeTime=-1):
        self.Msg=Msg
        self.Pos=Pos
        self.LifeTime=LifeTime
        self.Size=Size
        self.Death=0

    def draw(self):
            screen.draw.text(self.Msg,self.Pos,color='black',fontsize=self.Size)
            
    def up(self):
        self.LifeTime-=1
        if not self.LifeTime:
            self.Death=1


class Menu:
    def __init__(self,Pos,Img):
        self.Pos=Pos
        self.Icon=Actor(Img)
        self.Icon.topleft=Pos

    def draw(self):
        self.Icon.draw()
        screen.draw.text(Ores[self.Icon.image],self.Icon.topright,fontsize=65,color='black')
               
        
Hills=[Hill('rhill',500,1500),Hill('ihill',800,3000),Hill('dhill',1150,5500)] #山的系列
Workers=[Worker()] #工人的系列
Texts=[] #文本系列
Menus=[]
Menus.append(Menu((0,HEIGHT//2-50),'rock'))
Menus.append(Menu((0,HEIGHT//2),'iron'))
Menus.append(Menu((0,HEIGHT//2+50),'diamond'))
Menus.append(Menu((0,HEIGHT//4),'money'))


def update(): #更新部分，这一段执行60次/s
    for i in Hills: #逐一翻找山
        i.up() #山的更新代码
        if i.Death: #如果山没了
            Hills.remove(i) #删掉山
    for i in Texts:
        i.up()
        if i.Death:
            Texts.remove(i)
    for i in Workers: #逐一翻找工人
        i.up() #工人更新代码

def draw(): #绘制部分
    screen.fill((255,255,255)) #用白色填满背景
    for i in Hills+Workers+Texts+Menus: #逐一翻找山和工人
        i.draw() #它们的绘制代码
    Home.draw() #绘制收货点
    Land.draw() #绘制地面
    

def on_key_down(key):
    global Texts,MenuNo,KeyAndTexts,NumsAndNames
    for i,j in KeyAndTexts.items():
        if key==i:
            if MenuNo==j[1]:
                Texts=[]
                MenuNo=0
                break
            Texts=[]
            Msg='Buy {}?\nEnter for yes\nPress again for no'.format(j[0])
            Texts.append(LifeText(Msg,(WIDTH*0.3,HEIGHT//2),75))
            MenuNo=j[1]
            break
    if key==keys.RETURN and MenuNo:
        Texts=[]
        if NumsAndPrices[MenuNo]>=int(Ores['money']):
            Texts.append(LifeText('No enough money!',(WIDTH*0.3,HEIGHT//2),75,60))
        else:
            n=NumsAndNames[MenuNo]
            s=n[0]
            c=n[1]
            i=n[2]
            Workers.append(Worker(s,c,i))
            Texts.append(LifeText('Success!',(WIDTH*0.3,HEIGHT//2),75,60))
            Ores['money']=StrP(Ores['money'],-NumsAndPrices[MenuNo])
            MenuNo=0

def on_mouse_down(pos,button):
    global Home,Ores,OresAndPrices
    if button==mouse.LEFT and Home.collidepoint(pos):
        t=0
        for i,j in Ores.items():
            if i!='money':
                t+=int(j)*OresAndPrices[i]
                Ores[i]='0'
        Ores['money']=StrP(Ores['money'],t)
        Texts.append(LifeText('Sell!',(Home.x,Home.top-15),20,60))

pgzrun.go()
