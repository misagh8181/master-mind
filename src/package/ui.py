from tkinter import *
from .bl import processForGuess
from tkinter import font
from tkinter import messagebox
from email import header
from operator import le
from turtle import color, right
from cProfile import label
from cgitb import text
from random import randint
import mysql.connector
from .bl import checkTime

def help():
  help=Tk()
  help.title("Help")
  help.resizable(width=False,height=False)
  help.geometry("600x500")
  help.configure(bg="white")
  label1=Label(master=help,text="The letter (T) means that the value \nand the place of the digit is right.\nThe letter (L) ,means that the value is \nright but the place is wrong.\nThe digit itself means both the place \nand the value were wrong.",font=("arial",18,"bold"),fg="green",bg="pink",width=34,height=14)
  label1.place(x=10,y=10)
  help.mainloop()
  
def history():
  history=Tk()
  history.title("History")
  history.resizable(width=False,height=False)
  history.geometry("600x500")
  history.configure(bg="white")
  mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="mastermind"
  )
  mycursor = mydb.cursor()
  query="Select * from history"
  mycursor.execute(query)
  data=mycursor.fetchall()
  userHistory = Listbox(master=history)
  userHistory.pack(side = LEFT, fill = BOTH,expand=True)
  scrollbar1=Scrollbar(master=history)
  scrollbar1.pack(side = RIGHT, fill = BOTH)
  for element in data:
    userHistory.insert(0,"user name : "+element[1]+"  **  check time : "+element[2]+"  **  state : "+element[3]+"  **  level : "+element[4])
  userHistory.config(yscrollcommand = scrollbar1.set)
  scrollbar1.config(command=userHistory.yview)
  history.mainloop()
  
def exit_time(form,username,checkTime,temp,state):
  mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="mastermind"
  )
  mycursor = mydb.cursor()
  sql = "INSERT INTO history (username,checktime,state,level) VALUES (%s, %s, %s, %s)"
  val = (username,str(len(checkTime)),state,str(temp))
  mycursor.execute(sql,val)
  mydb.commit()
  form.destroy()
  
def register(NameVar_name,NameVar_family,NameVar_id,NameVar_username1,NameVar_password1,NameVar_confirmpassword):
    if(NameVar_name.get()!="" and NameVar_family.get()!="" and NameVar_username1.get()!="" and NameVar_id.get()!="" and NameVar_password1.get()!="" and NameVar_confirmpassword.get()!=""):
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="mastermind"
        )
        mycursor = mydb.cursor()
        if(NameVar_password1.get()==NameVar_confirmpassword.get()):
            writting=True
            try:
              query="Select * from master"
              mycursor.execute(query)
              data=mycursor.fetchall()
              for element in data:
                if(NameVar_username1.get()==element[3]):
                    messagebox.showinfo("Exist","This user has been created :( !!!")
                    writting=False
            except:
              pass
            if(writting==True):
                sql = "INSERT INTO master (name,familyname,username,idnumber,password) VALUES (%s, %s, %s, %s, %s)"
                val = (NameVar_name.get(),NameVar_family.get(),NameVar_username1.get(),NameVar_id.get(),NameVar_password1.get())
                mycursor.execute(sql, val)
                mydb.commit()
                NameVar_name.set("") 
                NameVar_family.set("")
                NameVar_username1.set("") 
                NameVar_id.set("") 
                NameVar_password1.set("")
                NameVar_confirmpassword.set("")
        else:
            messagebox.showerror("Error","The Password and Confirm Password arent the same !!!")
    else:
        messagebox.showerror("Error","Not all entries are given !!!")
        
def login(NameVar_username2,NameVar_password2,root):
    if(NameVar_username2.get()!="" and NameVar_password2.get()!=""):
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="mastermind"
        )
        mycursor = mydb.cursor()
        Exist=False
        try:
            query="Select * from master"
            mycursor.execute(query)
            data=mycursor.fetchall()
            for element in data:
                if(NameVar_username2.get()==element[3]):
                    if(NameVar_password2.get()==element[5]):
                        root.destroy()
                        master_gui(element[3])
                        Exist=True
        except:
          pass
        if(Exist==False):
            messagebox.showinfo("Doesnt Exist","This user doesnt exist :( !!!")       
    else:
        messagebox.showerror("Error","Not all entries are given!!!")

def master_gui(username):
  form = Tk()
  
  #region CONFIG
  form.title("Master Mind")
  form.geometry("700x500")
  form.resizable(width=False,height=False)
  form.config(bg="white")
  #endregion
  
  #region HEADER
  menubar = Menu(form)
  file = Menu(menubar, tearoff = 0)
  menubar.add_cascade(label ='File', menu = file)
  file.add_command(label ='help', command =lambda:help())
  file.add_command(label ='history', command =lambda:history())
  file.add_separator()
  file.add_command(label ='Exit', command = form.destroy)
  form.config(menu = menubar)
  
  header_frame = Frame(master=form, height=70,bg="#19242e",highlightthickness=1,highlightbackground="#d9d9d9")
  header_frame.pack(side=TOP,fill=X)
  header_frame.propagate(0)
  Label(master=header_frame, text=username,fg="white",font=("arial",12,"bold"),bg="#19242e",anchor=W).pack(side=LEFT,fill=X,padx=15,pady=(0,0))
  #endregion
  
  #region BODY
  body_frame = Frame(master=form,height=50,bg="white")
  body_frame.pack(fill=BOTH,expand=True)
  body_frame.propagate(0)
  #endregion
  
  #region FOOTER
  footer_frame = Frame(master=form,height=70,bg="#19242e",highlightthickness=1,highlightbackground="#d9d9d9")
  footer_frame.pack(side=BOTTOM,fill=X)
  footer_frame.propagate(0)
  button_exit = Button(master=footer_frame, text="Exit", bg="red", fg="white", width=50, height=2, command=form.destroy)
  button_exit.pack(pady=15)
  #endregion
  
  #region BUTTON_BODY1
  body_frame1 = Frame(master=body_frame,height=50,bg="grey")
  body_frame1.pack(side=TOP,fill=BOTH,expand=True)
  body_frame1.propagate(0)
  
  button4=Button(
  master = body_frame1, 
  pady=20, padx=60,
  font=("arial",10,"bold"), 
  text="4", 
  bg="pink", 
  fg="black",
  command=lambda:game_form(form,4,username)
  )
  button4.pack(side=LEFT,padx=45)
  
  button5=Button(
  master = body_frame1, 
  pady=20, padx=60,
  font=("arial",10,"bold"), 
  text="5", 
  bg="pink", 
  fg="black",
  command=lambda:game_form(form,5,username)
  )
  button5.pack(side=LEFT,padx=45)
  
  button6=Button(
  master = body_frame1, 
  pady=20, padx=60,
  font=("arial",10,"bold"), 
  text="6", 
  bg="pink", 
  fg="black",
  command=lambda:game_form(form,6,username)
  )
  button6.pack(side=LEFT,padx=45)
  #endregion
  
  #region BUTTON_BODY2
  body_frame2 = Frame(master=body_frame,height=50,bg="grey")
  body_frame2.pack(side=TOP,fill=BOTH,expand=True)
  body_frame2.propagate(0)
  
  button7=Button(
  master = body_frame2, 
  pady=20, padx=60,
  font=("arial",10,"bold"), 
  text="7", 
  bg="pink", 
  fg="black",
  command=lambda:game_form(form,7,username)
  )
  button7.pack(side=LEFT,padx=45)
  
  button8=Button(
  master = body_frame2, 
  pady=20, padx=60,
  font=("arial",10,"bold"), 
  text="8", 
  bg="pink", 
  fg="black",
  command=lambda:game_form(form,8,username)
  )
  button8.pack(side=LEFT,padx=45)
  
  button9=Button(
  master = body_frame2, 
  pady=20, padx=60,
  font=("arial",10,"bold"), 
  text="9", 
  bg="pink", 
  fg="black",
  command=lambda:game_form(form,9,username)
  )
  button9.pack(side=LEFT,padx=45)
  #endregion
  
  form.mainloop()
  
def login_form():
  #region confige
  root = Tk()
  root.title("Information")
  root.resizable(width=False,height=False)
  root.geometry("600x500")
  root.configure(bg="white")
  #endregion confige
  
  #region header
  header=Frame(master=root,bg="blue")
  header.pack(side=TOP,fill=X)
  Label(master=header,text="Information",font=("arial",40,"bold"),bg="blue",fg="black").pack(side=TOP,fill=X)
  #endregion header
  
  #region right
  right_frame=Frame(master=root,bg="brown")
  right_frame.pack(side=RIGHT,fill=BOTH,expand=True)
  right_frame.propagate(False)
  
  Label(master=right_frame,bg="grey" ,fg="white", text="LOGIN",font=("arial",15,"bold")).pack(side=TOP,fill=X)
  
  buttonFrame_right=Frame(master=right_frame,bg="maroon",height=40)
  buttonFrame_right.pack(side=BOTTOM,fill=X)
  
  
  
  body_username2=Frame(master=right_frame,bg="brown",height=40)
  body_username2.pack(side=TOP,fill=X)
  body_username2.propagate(False)
  labelUserName2=Label(master=body_username2,text="UserName :",fg="black",bg="brown",font=("arial",10,"bold"))
  labelUserName2.pack(side=TOP,anchor="w")
  NameVar_username2=StringVar()
  userNameEntry2=Entry(master=body_username2,textvariable=NameVar_username2,font=("arial",10,"normal"),width=35)
  userNameEntry2.pack(side=BOTTOM)
  
  body_password2=Frame(master=right_frame,bg="brown",height=40)
  body_password2.pack(side=TOP,fill=X)
  body_password2.propagate(False)
  labelPassWord2=Label(master=body_password2,text="PassWord :",fg="black",bg="brown",font=("arial",10,"bold"))
  labelPassWord2.pack(side=TOP,anchor="w")
  NameVar_password2=StringVar()
  passWordEntry2=Entry(master=body_password2,textvariable=NameVar_password2,font=("arial",10,"normal"),width=35)
  passWordEntry2.pack(side=BOTTOM)
  
  button1_right = Button(master=buttonFrame_right, text="Exit", bg="red", fg="white", width=7, height=2, command=root.destroy)
  button1_right.pack(side=LEFT)
  
  button2_right = Button(master=buttonFrame_right, text="login", bg="green", fg="white", width=7, height=2, command=lambda :login(NameVar_username2,NameVar_password2,root))
  button2_right.pack(side=RIGHT)
  #endregion right
  
  #region center
  center_frame=Frame(master=root,bg="black",width=2)
  center_frame.pack(side=RIGHT,fill=Y)
  center_frame.propagate(False)
  #endregion center
  
  #region left
  left_frame=Frame(master=root,bg="brown")
  left_frame.pack(side=LEFT,fill=BOTH,expand=True)
  left_frame.propagate(False)
  
  Label(master=left_frame,bg="grey" ,fg="white", text="REGISTER",font=("arial",15,"bold")).pack(side=TOP,fill=X)
  
  buttonFrame_left=Frame(master=left_frame,bg="maroon",height=40)
  buttonFrame_left.pack(side=BOTTOM,fill=X)
  
  body_name=Frame(master=left_frame,bg="brown",height=40)
  body_name.pack(side=TOP,fill=X)
  body_name.propagate(False)
  labelName=Label(master=body_name,text="Name :",fg="black",bg="brown",font=("arial",10,"bold"))
  labelName.pack(side=TOP,anchor="w")
  NameVar_name=StringVar()
  nameEntry=Entry(master=body_name,textvariable=NameVar_name,font=("arial",10,"normal"),width=35)
  nameEntry.pack(side=BOTTOM)
  
  body_familyname=Frame(master=left_frame,bg="brown",height=40)
  body_familyname.pack(side=TOP,fill=X)
  body_familyname.propagate(False)
  labeFamilyName=Label(master=body_familyname,text="Family Name :",fg="black",bg="brown",font=("arial",10,"bold"))
  labeFamilyName.pack(side=TOP,anchor="w")
  NameVar_family=StringVar()
  familyNameEntry=Entry(master=body_familyname,textvariable=NameVar_family,font=("arial",10,"normal"),width=35)
  familyNameEntry.pack(side=BOTTOM)
  
  body_username1=Frame(master=left_frame,bg="brown",height=40)
  body_username1.pack(side=TOP,fill=X)
  body_username1.propagate(False)
  labelUserName=Label(master=body_username1,text="UserName :",fg="black",bg="brown",font=("arial",10,"bold"))
  labelUserName.pack(side=TOP,anchor="w")
  NameVar_username1=StringVar()
  userNameEntry1=Entry(master=body_username1,textvariable=NameVar_username1,font=("arial",10,"normal"),width=35)
  userNameEntry1.pack(side=BOTTOM)
  
  body_id=Frame(master=left_frame,bg="brown",height=40)
  body_id.pack(side=TOP,fill=X)
  body_id.propagate(False)
  labelId=Label(master=body_id,text="Id :",fg="black",bg="brown",font=("arial",10,"bold"))
  labelId.pack(side=TOP,anchor="w")
  NameVar_id=StringVar()
  idEntry=Entry(master=body_id,textvariable=NameVar_id,font=("arial",10,"normal"),width=35)
  idEntry.pack(side=BOTTOM)
  
  body_password1=Frame(master=left_frame,bg="brown",height=40)
  body_password1.pack(side=TOP,fill=X)
  body_password1.propagate(False)
  labelPassWord1=Label(master=body_password1,text="PassWord :",fg="black",bg="brown",font=("arial",10,"bold"))
  labelPassWord1.pack(side=TOP,anchor="w")
  NameVar_password1=StringVar()
  passWordEntry1=Entry(master=body_password1,textvariable=NameVar_password1,font=("arial",10,"normal"),width=35)
  passWordEntry1.pack(side=BOTTOM)
  
  body_confirmpassword=Frame(master=left_frame,bg="brown",height=40)
  body_confirmpassword.pack(side=TOP,fill=X)
  body_confirmpassword.propagate(False)
  labelConfirmPassWord=Label(master=body_confirmpassword,text="Confirm PassWord :",fg="black",bg="brown",font=("arial",10,"bold"))
  labelConfirmPassWord.pack(side=TOP,anchor="w")
  NameVar_confirmpassword=StringVar()
  passWordEntry=Entry(master=body_confirmpassword,textvariable=NameVar_confirmpassword,font=("arial",10,"normal"),width=35)
  passWordEntry.pack(side=BOTTOM)
  
  button1_left = Button(master=buttonFrame_left, text="Exit", bg="red", fg="white", width=7, height=2, command=root.destroy)
  button1_left.pack(side=LEFT)
  
  button2_left = Button(master=buttonFrame_left, text="register", bg="green", fg="white", width=7, height=2, command=lambda :register(NameVar_name,NameVar_family,NameVar_id,NameVar_username1,NameVar_password1,NameVar_confirmpassword))
  button2_left.pack(side=RIGHT)
  #endregion left
  
  root.mainloop()
  
def  game_form(form,digits,username):
  form.destroy()
  randomNumber=randint(10**(digits-1),10**(digits))
  form1=Tk()
  
    
  #region CONFIG
  form1.title("Master Mind")
  form1.geometry("700x500")
  form1.resizable(width=False,height=False)
  form1.config(bg="white")
  #endregion
  
  #region HEADER
  header_frame = Frame(master=form1, height=70,bg="#19242e",highlightthickness=1,highlightbackground="#d9d9d9")
  header_frame.pack(side=TOP,fill=X)
  header_frame.propagate(0)
  Label(master=header_frame, text="Guess the number :)",fg="white",font=("arial",12,"bold"),bg="#19242e",anchor=W).pack(side=LEFT,fill=X,padx=15,pady=(0,0))
  #endregion
  
  #region BODY
  body_frame = Frame(master=form1,height=50,bg="white")
  body_frame.pack(fill=BOTH,expand=True,padx=20)
  body_frame.propagate(0)
  data1=list()#stringVriables
  data2=list()#enterys
  counter=0
  temp=digits
  firstTime=0
  while(digits>0):
    data1.append(StringVar())
    data2.append(Entry(master=body_frame,textvariable=data1[counter],font=("arial",40,"bold"),width=0))
    if(firstTime==0):
        data2[counter].pack(side=LEFT,padx=(880/temp,10))
        firstTime=1
    else:
        data2[counter].pack(side=LEFT,padx=10)
    counter+=1
    digits-=1
  def character_limit_1(entry_text):
    if len(entry_text.get()) > 0:
        entry_text.set(entry_text.get()[-1])
  def character_limit_2(entry_text):
    if len(entry_text.get()) > 0:
        entry_text.set(entry_text.get()[-1])
  def character_limit_3(entry_text):
    if len(entry_text.get()) > 0:
        entry_text.set(entry_text.get()[-1])
  def character_limit_4(entry_text):
    if len(entry_text.get()) > 0:
        entry_text.set(entry_text.get()[-1]) 
  def character_limit_5(entry_text):
    if len(entry_text.get()) > 0:
        entry_text.set(entry_text.get()[-1])
  def character_limit_6(entry_text):
    if len(entry_text.get()) > 0:
        entry_text.set(entry_text.get()[-1]) 
  def character_limit_7(entry_text):
    if len(entry_text.get()) > 0:
        entry_text.set(entry_text.get()[-1]) 
  def character_limit_8(entry_text):
    if len(entry_text.get()) > 0:
        entry_text.set(entry_text.get()[-1])
  def character_limit_9(entry_text):
    if len(entry_text.get()) > 0:
        entry_text.set(entry_text.get()[-1])   
  if(temp==4):    
    data1[0].trace("w", lambda *args: character_limit_1(data1[0]))  
    data1[1].trace("w", lambda *args: character_limit_2(data1[1])) 
    data1[2].trace("w", lambda *args: character_limit_3(data1[2]))   
    data1[3].trace("w", lambda *args: character_limit_4(data1[3]))   
  if(temp==5):    
    data1[0].trace("w", lambda *args: character_limit_1(data1[0]))  
    data1[1].trace("w", lambda *args: character_limit_2(data1[1])) 
    data1[2].trace("w", lambda *args: character_limit_3(data1[2]))   
    data1[3].trace("w", lambda *args: character_limit_4(data1[3]))
    data1[4].trace("w", lambda *args: character_limit_5(data1[4]))
  if(temp==6):    
    data1[0].trace("w", lambda *args: character_limit_1(data1[0]))  
    data1[1].trace("w", lambda *args: character_limit_2(data1[1])) 
    data1[2].trace("w", lambda *args: character_limit_3(data1[2]))   
    data1[3].trace("w", lambda *args: character_limit_4(data1[3]))
    data1[4].trace("w", lambda *args: character_limit_5(data1[4]))
    data1[5].trace("w", lambda *args: character_limit_6(data1[5]))
  if(temp==7):    
    data1[0].trace("w", lambda *args: character_limit_1(data1[0]))  
    data1[1].trace("w", lambda *args: character_limit_2(data1[1])) 
    data1[2].trace("w", lambda *args: character_limit_3(data1[2]))   
    data1[3].trace("w", lambda *args: character_limit_4(data1[3]))
    data1[4].trace("w", lambda *args: character_limit_5(data1[4]))
    data1[5].trace("w", lambda *args: character_limit_6(data1[5]))
    data1[6].trace("w", lambda *args: character_limit_7(data1[6]))
  if(temp==8):    
    data1[0].trace("w", lambda *args: character_limit_1(data1[0]))  
    data1[1].trace("w", lambda *args: character_limit_2(data1[1])) 
    data1[2].trace("w", lambda *args: character_limit_3(data1[2]))   
    data1[3].trace("w", lambda *args: character_limit_4(data1[3]))
    data1[4].trace("w", lambda *args: character_limit_5(data1[4]))
    data1[5].trace("w", lambda *args: character_limit_6(data1[5]))
    data1[6].trace("w", lambda *args: character_limit_7(data1[6]))
    data1[7].trace("w", lambda *args: character_limit_8(data1[7]))
  if(temp==9):    
    data1[0].trace("w", lambda *args: character_limit_1(data1[0]))  
    data1[1].trace("w", lambda *args: character_limit_2(data1[1])) 
    data1[2].trace("w", lambda *args: character_limit_3(data1[2]))   
    data1[3].trace("w", lambda *args: character_limit_4(data1[3]))
    data1[4].trace("w", lambda *args: character_limit_5(data1[4]))
    data1[5].trace("w", lambda *args: character_limit_6(data1[5]))
    data1[6].trace("w", lambda *args: character_limit_7(data1[6]))
    data1[7].trace("w", lambda *args: character_limit_8(data1[7]))
    data1[8].trace("w", lambda *args: character_limit_9(data1[8]))
  #endregion
  
  #region FOOTER
  footer_frame = Frame(master=form1,height=70,bg="#19242e",highlightthickness=1,highlightbackground="#d9d9d9")
  footer_frame.pack(side=BOTTOM,fill=X)
  footer_frame.propagate(0) 
  button_exit = Button(master=footer_frame, text="Exit", bg="red", fg="white", width=20, height=2, command=lambda:exit_time(form1,username,checkTime,temp,"Run"))
  button_exit.pack(pady=15,side=RIGHT,padx=10)
  button_check = Button(master=footer_frame, text="check", bg="green", fg="white", width=20, height=2, command=lambda:processForGuess(temp,data1,data2,randomNumber,body_frame,footer_frame,"Run",form1,button_check,button_exit,username))
  button_check.pack(pady=15,side=LEFT,padx=10)
  #endregion

  form1.mainloop()