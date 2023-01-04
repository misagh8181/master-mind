from tkinter import *
from sys import exit
from random import randint
import mysql.connector

checkTime=list()
def processForGuess(digits,data1,data2,randomNumber,master1,master2,state,form,check,exit,username):
    checkTime.append("")
    label2=Label(master=master1,text="Counter :"+str(len(checkTime)),font=("arial",14,"bold"),fg="black",bg="blue",width=10,height=3)
    label2.place(x=10,y=20)
    rand=randomNumber
    list1=list()    
    while(rand>0):
        list1.append(rand%10)
        rand//=10
    list1.reverse()
    notCheck=list()
    finalList=digits*[None]
    copy_list=digits*[None]
    for i in range(digits):
        copy_list[i]=list1[i]
    for i in range(0,len(list1)):
        if(int(data1[i].get()) == copy_list[i]): 
            copy_list[i]=-1
            finalList[i]="T"
        else:
            if(int(data1[i].get()) in list1):
                x=int(data1[i].get())
                counter=0
                for j in range(0,len(list1)):
                    if(x==copy_list[j]):
                        if(int(data1[j].get())!=copy_list[j]):
                            copy_list[j]=-1
                            finalList[i]="L"
    for i in range(digits):
        if(finalList[i]==None):
            finalList[i]=data1[i].get()
    label_list=list()
    str1=""
    truth=0
    for i in range(digits):
        if(finalList[i]!="T"):
            truth=1
    if(truth==0):
        state="Win"
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="mastermind"
        )
        mycursor = mydb.cursor()
        sql = "INSERT INTO history (username,checktime,state,level) VALUES (%s, %s, %s, %s)"
        val = (username,str(len(checkTime)),state,str(digits))
        mycursor.execute(sql,val)
        mydb.commit()
        label1=Label(master=master1,text="You Win :)",font=("arial",20,"bold"),fg="green",bg="pink",width=40,height=6)
        label1.place(x=28,y=140)
        check.destroy()
        exit.destroy()
        button_ok = Button(master=master2, text="OK", bg="gray", fg="white", width=200, height=2, command=form.destroy)
        button_ok.pack(pady=15,side=RIGHT,padx=10)
        
    else:        
        for i in range(digits):
            str1+=finalList[i]
        label1=Label(master=master1,text=str1,font=("arial",20,"bold"),fg="green",bg="pink",width=15,height=3)
        label1.place(x=200,y=220)
        
        
 