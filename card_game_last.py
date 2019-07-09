from tkinter import *
from tkinter import messagebox
import numpy as np  #random function
import time

print("201002022 최봉순")
print("2016.12.08 Card_game 0.2")

class Rectan:       #카드가 랜덤으로 배열되는 창과 쌓기할 창의 클래스
    def __init__(self,x1,y1,x2,y2,Wind):
        gWin.create_rectangle(x1,y1,x2,y2)
        self.label1 = Label(text=Wind, bg="YELLOW")
        self.label1.place(x=x2-50,y=y1, height = 15,width = 50)
        #여기에 이미지 추가

def showxy(event):  #마우스 포인터의 위치를 알려주는 메소드
    x = event.x
    y = event.y
    str1 = "mouse at x=%d  y=%d" % (x, y)
    gWin.master.title("Card Game ("+str1+")")

class Card():       #카드 클래스, 13개의 인스턴스 생성하기 위함.
    def __init__(self,value,canvas,path):
        self.last_x= int(np.random.random(1)*1000 % 460 + 40)#카드 생성위치 랜덤하게
        self.last_y= int(np.random.random(1)*1000 % 360 + 60)
        self.canvas = canvas    #카드가 생성될 캔버스
        self.value = value      #카드 테그값 주기 위함
        self.cImg = PhotoImage(file=path)   #카드 이미지. 매개변수로 위치값 받음.
        self.cimage = canvas.create_image(self.last_x,self.last_y,
                                          image = self.cImg,
                                          tags = "{}".format(self.value))

def onMouseLeftDown(event):     #마우스 좌클릭시 발생하는 이벤트
    global last_x, last_y
    x, y = event.x, event.y   
    last_x, last_y = x, y
    gWin.lift(CURRENT)
    #클릭하는 카드를 맨위로 올리는것. 랜덤 생성되어 카드를 가리기때문에
    #잘보일수 있도록 코딩함.
    if 600<event.x<750 and 10<event.y<490:  #카드쌓기 창에서 클릭시
        if len(Stackarray) != 0:            #스택구조에서 팝 됨
            Stackarray.pop()
    
def onMouseMove(event):     #마우스 드래그시 발생하는 이벤트
    global last_x, last_y
    dx = event.x - last_x   #x축 이동거리
    dy = event.y - last_y   #y축 이동거리
    gWin.move(CURRENT, dx, dy)  # 마우스를 드래그하면 클릭된 카드가 이동거리만큼 이동하게됨
    last_x, last_y = event.x, event.y   #이동된 위치를 원점으로 재설정

def stackCheck(event):  # 카드쌓기 순서가 맞는지 체크. 테그 순서를 따라 쌓기진행.
    global Tstop,Stackarray
    Checkarray = [check for check in range(13)] #테그 순서에 맞는지 확인하기위한 리스트.
    if int(event.widget.find_withtag(CURRENT)[0]-3)==Checkarray[len(Stackarray)]:
    #테그값에서 -3을 하는 이유는 테그가 생성될때 제일 먼저 카드창이 생성되면서 1번이고 2번이 쌓기 창이되어
    #이를 체크리스트에 맞추기위해서 -3을 하였음
        Stackarray.append(event.widget.find_withtag(CURRENT)) #if문 통해 순서가 맞다면 추가.
        Val = int(event.widget.find_withtag(CURRENT)[0]-3)
        gWin.coords(CURRENT, 650,Val*20+100)    #카드를 놓게 되면 자기 순서에 맞는 위치로 이동.
        if len(Stackarray)==13:     #스택의 크기가 13이 되면 모든 카드를 쌓았으므로 타이머 종료해줌.
            Tstop = True        #타이머 정지신호 
            
    else:
        gWin.coords(CURRENT,300,200)    #카드 순서가 맞지 않을경우 카드창으로 이동

def onMouseRelease(event):  #클릭 해제시 이벤트
    global last_x, last_y
    if 10<event.x<550 and 10<event.y<490:   
        if event.widget.find_withtag(CURRENT): pass #카드창에서 카드클릭해제시 카드
    elif 600<event.x<750 and 10<event.y<490 :
        if event.widget.find_withtag(CURRENT):  #쌓기창에서 카드클릭해제시 스택체크 메소드로 이동.
            stackCheck(event)                   #append 시킬지 카드창으로 이동할지 체크
    else:
        gWin.coords(CURRENT, 300, 200)          # 카드창과 쌓기창 외부에서 카드클릭해제시 카드창으로 카드 이동

def onNewGame():        #메뉴에서 새게임 선택시 
    global gtimer, Tstop
    if len(Stackarray) != 0:        #스택에 쌓인 카드 모두 팝시키기.
        for i in range(len(Stackarray)):
            Stackarray.pop()
    for i in range(3,16):           #카드창에 랜덤위치로 카드 배치
        x= int(np.random.random(1)*1000 % 460 + 40)
        y= int(np.random.random(1)*1000 % 360 + 60)
        gWin.coords(i, x, y)
    Tstop = False                   #타이머 정지 해제
    gtimer=gTimer(root,0)           #타이머 생성
    gtimer.update_clock()           #타이머 시작

def onRecord():     #기록
    fileopen1 = open('c:/tmp/record.txt','r')   #기록 파일 불러오기
    total = fileopen1.readlines()       #전체 라인 불러오기
    root2=Tk()
    root2.title("성적표")  
    recWin=Canvas(root2,width=250,height=400)   
    recWin.pack()
    reclabeltitle = Label(recWin,text='기록')
    reclabeltitle.pack(side='top')
    reclabel = Label(recWin,text=total) #기록 적혀진 레이블 불러오기
    reclabel.pack(side="top")
    fileopen1.close()   #파일 닫기

def onClear():  #기록 초기화
    result = messagebox.askyesno("Card game","기록을 초기화 하시겠습니까?")
    if result == True:
        fileopen = open('c:/tmp/record.txt','w')    #w모드로 기존 파일 삭제
        fileopen.write("")  #공백 기록
        fileopen.close()

def makeMenu(canvas):       #메뉴 생성
    menuBar = Menu(canvas)
    canvas.config(menu = menuBar)
    filemenu = Menu(menuBar, tearoff = 0)
    filemenu.add_command(label='새 게임',command=onNewGame)
    filemenu.add_command(label='기록',command=onRecord)
    filemenu.add_command(label='기록 초기화',command=onClear)
    filemenu.add_command(label='종료',command=canvas.destroy)
    menuBar.add_cascade(label='파일',menu = filemenu)
    
class gTimer():         #타이머 클래스
    global Tstop
    Tstop = False
    def __init__(self,root,now):    #초기화
        self.root = root
        self.label1 = Label(text="타이머: ", bg="YELLOW")
        self.label1.place(x=10,y=0, height = 12,width = 44)
        self.label = Label(text="",bg="YELLOW")
        self.label.place(x=50,y=0, height = 12,width = 25)
        self.now=now
 
    def update_clock(self):
        self.label.configure(text=self.now) #레이블 변경
        self.now +=1
        After = self.root.after(1000, self.update_clock)    #1000ms 이후 update_clock 호출 //1초마다 1씩 증가
        if Tstop:   #타이머 정지신호 발생시 반복 정지.
            self.root.after_cancel(After)
            strt=str(self.label["text"])
            recordT(strt)
            retrymsg(strt)   
            
def retrymsg(str1):
    result = messagebox.askretrycancel("Retry",str1 +"초입니다.\n다시 도전하시겠습니까?\n")
    if result == True:
        onNewGame()
    else:
        result2 = messagebox.askyesno("Card game","종료 하시겠습니까?")
        if result2 == True:
            root.destroy()

def recordT(str1):
    gt = time.localtime()
    day = '{}년 {}월 {}일 {}시 {}분 {}초'.format(gt.tm_year,gt.tm_mon,gt.tm_mday,
                                           gt.tm_hour,gt.tm_min,gt.tm_sec )
    recTime = open('c:/tmp/record.txt','a')
    recTime.write('\n'+day+' // '+str1+' ')
    recTime.close()
    
def binding(canvas):        # 이벤트 설정
    canvas.bind("<Motion>", showxy)
    canvas.bind("<Button-1>", onMouseLeftDown)
    canvas.bind("<B1-Motion>", onMouseMove)
    canvas.bind("<ButtonRelease-1>",onMouseRelease)
    
global Stackarray, gWin, Tstop
Stackarray =[]
root = Tk()     #윈도우 생성.
gWin = Canvas(root, bg="green",width =800, height = 500)   #800x500 gWin 객체 생성
gWin.pack(expand=YES, fill = BOTH)  #레이아웃. 부모윈도우에 위치 시킴.
gtimer=gTimer(root,0)   
gtimer.update_clock()   
binding(canvas = gWin)
makeMenu(root)
cardpart = Rectan(10,10,550,490,'카드창')    #카드창 객체 생성
base = Rectan(600,10,750,490,'쌓기창')       #쌓기창 객체 생성
card = [card for card in range(13)] #13개 카드 객체 생성
for i in range(13):
    card[i] = Card(i,gWin,'c:/tmp/{}.png'.format(i))
root.mainloop()
