########################################################
import sqlite3
from tkinter import messagebox
from tkinter import *
import tkinter.messagebox as box
import sys
import hashlib
import random
from datetime import datetime

today = datetime.today()
xxx=datetime.strftime(today,'%Y-%m-%d')
xx=str(xxx)
############################################################
def encrypthash(x):

    result = hashlib.md5(x.encode()) 

    return(result.hexdigest())
r=""
###########################################################
#Declares root as the tkinter main window
root=Tk()
root.title("Beta Password Manager")
root.geometry("900x500")
root.configure(bg="SteelBlue2")
###########################################################
#Creates the toplevel window
top = Toplevel() 
top.title("Login Page")
top.geometry("500x400")
L1=Label(top,text="Username")
L2=Label(top,text="Password")
entry1 = Entry(top) #Username entry has been made default to Admin
entry2 = Entry(top) #Password entry user defined
button1 = Button(top, text="Login", command=lambda:verify()) #Login button
button2 = Button(top,text="Create New Account",command=lambda:newuser())
############################################################
#Creating the Database
conn = sqlite3.connect("Manager.db")
#cursor.execute("PRAGMA key='mypassword'")
cursor = conn.cursor()
cursor.execute("PRAGMA key='mypassword'")
#Creating the Table
#Name of table being manager
cursor.execute(""" CREATE TABLE IF NOT EXISTS login1 (
                       username_l text NOT NULL UNIQUE,
                       password_l text
                        )
""")
cursor.execute("""CREATE TABLE IF NOT EXISTS logintime(
                    time_login text,
                    username_l text,
                    FOREIGN KEY(username_l) REFERENCES login1(username_l))""")
# Commit changes
conn.commit()
# Close the connection
conn.close()
############################################################
def newuser():

    top4=Toplevel()
    top4.title("Signup")
    top4.geometry("500x400")
    L11=Label(top4,text="Username")
    L22=Label(top4,text="Password")
    entry11=Entry(top4)
    entry22=Entry(top4)
    button=Button(top4,text="Submit",command=lambda:newusersubmit())
    def newusersubmit():
        conn = sqlite3.connect("Manager.db")
        cursor = conn.cursor()
        try:
            if(entry11.get()!="" and entry22.get()!=""):
                
                cursor.execute("INSERT INTO login1 VALUES (:username_l,:password_l)",
                               {
                                   'username_l':entry11.get(),
                                   'password_l':encrypthash(entry22.get())
                                })
                cursor.execute("insert into logintime values(:time_login,:username_l)",
                               {
                               'time_login':xx,
                               'username_l':entry11.get()})
                conn.commit()
                conn.close()
                messagebox.showinfo("Alert", "Successfull")
                top4.destroy()
            else:
                messagebox.showinfo("Alert", "Please Enter the details")
        except:
            
            messagebox.showinfo("Alert", "Username Already taken")
    entry11.pack()
    L11.pack()
    #L22.pack()
    entry22.pack()
    L22.pack()
    button.pack()
        
############################################################
def verify():
    global ul
    flag=0
    conn = sqlite3.connect("Manager.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM login1")
    data=cursor.fetchall()
    ul="fjjfgj"
    for i in range(len(data)):
        if entry1.get()==data[i][0] and encrypthash(entry2.get())==data[i][1]:
            ul=data[i][0]
            pl=data[i][1]
            temp=ul
            cursor.execute("select time from manager1 where username_l=?",(temp,))
            dtime=cursor.fetchall()
            cursor.execute("select time_login from logintime where username_l=?",(temp,))
            d0time=cursor.fetchall()
            p0_time=[]
            for j in d0time:
                p0_time+=j
            d02=datetime.strptime(p0_time[0],'%Y-%m-%d')
            cursor.execute("""UPDATE logintime SET
                           time_login= :time_login,
                           username_l= :username_l
                           WHERE username_l=:username_l""",
                           {
                               'time_login':xx,
                               'username_l':temp
                               })

            p_time=[]
            for i in dtime:
                p_time+=i
            print(p_time)
            for j in range(len(p_time)):
                t=p_time[j]
                d1=datetime.strptime(xx,'%Y-%m-%d')
                d2=datetime.strptime(t,'%Y-%m-%d')
                if((d1-d2).days)>90:
                    print("hh")
                    cursor.execute("select id from manager1 where time=? and username_l=?",(t,temp,))
                    w=cursor.fetchall()
                    r=[]
                    for i in w:
                        r+=i
                    if(len(r)>0):
                        messagebox.showinfo("Alert","Need Update in these ids  "+str(r)+"  These have not been updated for more than 90 days" )
                        break
            

            messagebox.showinfo("Alert","Login Successfull / Last Login on "+str(d02))
            conn.commit()
            conn.close()
            flag=1

            def tp2(): #Nested window toplevel2
                top1=Toplevel()
                top1.title("Password")
                top1.geometry("500x400")
                button3=Button(top1,text="Continue",command=lambda:cont())
                button2=Button(top1,text="Change Password",command=lambda:changepass())
                #Functioning of Continue Button
                def cont():

                    root.deiconify() #Unhides the root window
                    top.destroy() #Removes the toplevel window
                    top1.destroy()
                #Function of ChangePassword Button
                def changepass():
                    temp0=ul
                    top2=Toplevel()
                    top2.title("Update Password")
                    top2.geometry("500x450")
                    L3=Label(top2,text="New Password")
                    entry3=Entry(top2)
                    button4=Button(top2,text="Save",command=lambda:save())
                    L3.pack()
                    entry3.pack()
                    button4.pack()
                    

                    def save():
                        conn=sqlite3.connect('Manager.db')
                        cursor=conn.cursor()
                        f=encrypthash(entry3.get())
                        cursor.execute("UPDATE login1 SET password_l=? WHERE username_l=?",(f,temp0))

                        conn.commit()
                        conn.close()
                        top2.destroy()
                        
                button3.pack()
                button2.pack()
        
            tp2()
    else:
        if(flag==0):
                
            l3=Label(top,text="Wrong Password")
            l3.pack()

###################################################################

L1.pack()
entry1.pack() #This pack the elements, this includes the items for the main window
L2.pack()
entry2.pack()
button1.pack()
button2.pack()#This hides the main window, it's still present it just can't be seen or interacted with
root.withdraw() 
frame = Frame(root, bg="black", bd=15)
frame.place(relx=1, rely=0.00, relwidth=0.80, relheight=1.00, anchor = "n")

####################################################################
#Creating the Database
conn = sqlite3.connect("Manager.db")
cursor = conn.cursor()

#Creating the Table
#Name of table being manager
cursor.execute(""" CREATE TABLE IF NOT EXISTS manager1 (
                       username text,
                        url text,
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        email_id text,
                        password text,
                        username_l text,
                        time text,
                        hulu integer,
                        FOREIGN KEY(username_l) REFERENCES login1(username_l)
                        )
""")
cursor.execute("""CREATE TRIGGER if not exists  tri
                    AFTER UPDATE ON manager1
                    BEGIN
                    UPDATE manager1
                    SET time = DATE()
                    WHERE hulu=ID;
                    
                    end;""")

                    

# Commit changes
conn.commit()
# Close the connection
conn.close()

#####################################################################
#Submit Button Functioning
def submit():
    #Database connection
    temp=ul
    conn = sqlite3.connect("Manager.db")
    cursor = conn.cursor()
    

    #Insert Into Table using sql command INSERT
    if username.get()!="" and url.get()!="" and email_id.get()!="" and password.get()!="":
        cursor.execute("INSERT INTO manager1(username,url,email_id,password,username_l,time) VALUES (:username, :url, :email_id, :password,:username_l,:time)",
            {
                'username': username.get(),
                'url': url.get(),
                'email_id': email_id.get(),
                'password': password.get()[::-1],
                'username_l':temp,
                'time':xx
                
                
            }

        
        )
        r=password.get()
        conn.commit()
        conn.close()
        # Message box
        messagebox.showinfo("Info", "Record Added in the Database!")

        # After data entry clearing text boxes
        username.delete(0, END)
        url.delete(0, END)
        email_id.delete(0, END)
        password.delete(0, END)

    else:
        messagebox.showinfo("Alert", "Please fill all the details!")
        conn.close()
        
#####################################################################
#Query Button Functioning
def query():
    temp=ul
    #set button text
    query_btn.configure(text="Hide", command=hide)
    conn = sqlite3.connect("Manager.db")
    cursor = conn.cursor()
    #Query the database
    cursor.execute("SELECT *,oid FROM manager1 WHERE username_l=?",(temp,))
    #fetchall predined function
    records = cursor.fetchall() 
    p_records = ""
    for record in records:
        p_records += "ID:- "+str(record[2])+"\n"+ "Username:- " +str(record[0])+"\n"+"Url:- " + str(record[1])+"\n"+ "Email-Id:-  " + str(record[3])+"\n"+ "Password:- " + str(record[4])[::-1]+ "\n\n\n"

    
    query_label['text'] = p_records
    conn.commit()
    conn.close()
######################################################################
#Delete Button Functoining
def delete():
    temp0=ul
    conn = sqlite3.connect("Manager.db")
    cursor = conn.cursor()
    cursor.execute("SELECT *,oid FROM manager1 WHERE username_l=?",(temp0,))
    rec=cursor.fetchall()
    temp=[]
    flag=0
    for r in rec:
        temp.append(r[2])
    t = delete_id.get()
    for i in range(len(temp)):
        if(t==str(temp[i])):
            cursor.execute("DELETE FROM manager1 where oid = " + delete_id.get())
            delete_id.delete(0, END)
            messagebox.showinfo("Record is Deleted")
            flag=1
            

        
    if(flag==0):
        
        messagebox.showinfo("Alert","Enter a Valid Id")
    else:
        print("")
        
        



    conn.commit()
    conn.close()
#######################################################################
#Function to Update
def update():
    temp0=ul
    conn = sqlite3.connect("Manager.db")
    cursor = conn.cursor()
    cursor.execute("SELECT oid FROM manager1 WHERE username_l=?",(temp0,))
    rec=cursor.fetchall()
    temp=[]
    flag=0
    for r in rec:
        temp.append(r[0])
    t = update_id.get()
    for i in range(len(temp)):
        if(t==str(temp[i])):
            flag=1
            global edit
            edit = Tk()
            edit.title("Update Record")
            edit.geometry("500x400")
            edit.minsize(450, 300)
            edit.maxsize(450, 300)

            #Global variables
            global username_edit, url_edit, email_id_edit, password_edit
            # Creating Text Boxes
            
            username_edit = Entry(edit, width=40)
            username_edit.grid(row=0, column=1, padx=30)
            url_edit = Entry(edit, width=40)
            url_edit.grid(row=1, column=1, padx=30)
            email_id_edit = Entry(edit, width=40)
            email_id_edit.grid(row=2, column=1, padx=30)
            password_edit = Entry(edit, width=40)
            password_edit.grid(row=3, column=1, padx=30)

            # Create Text Box Labels
            
            username_label_edit = Label(edit, text="Username")
            username_label_edit.grid(row=0, column=0)
            url_label_edit = Label(edit, text="URL:")
            url_label_edit.grid(row=1, column=0)
            email_id_label_edit = Label(edit, text="Email-Id:")
            email_id_label_edit.grid(row=2, column=0)
            password_label_edit = Label(edit, text="Password:")
            password_label_edit.grid(row=3, column=0)

            # Create Save Button
            submit_btn_edit = Button(edit, text="Save Record", command=change)
            submit_btn_edit.grid(row=4, column=0, columnspan=2, pady=5, padx=15, ipadx=135)

            conn = sqlite3.connect("Manager.db")
            cursor = conn.cursor()

            cursor.execute("""UPDATE MANAGER1
                           SET
                           hulu=:hulu""",
                    
                           {
                               'hulu':update_id.get()
                               }
                           )
            conn.commit()

            conn.close()

            
            conn = sqlite3.connect("Manager.db")
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM manager1 where oid = " + update_id.get())
            records = cursor.fetchall()

            for record in records:
                username_edit.insert(0, record[0])
                url_edit.insert(0, record[1])
                email_id_edit.insert(0, record[3])
                password_edit.insert(0, record[4][::-1])
            

            conn.commit()

            conn.close()

    if(flag==0):
        
        messagebox.showinfo("Alert","Enter a Valid Id")
    else:
        print("")
############################################################################
#Create function to save update records
def change():
    conn = sqlite3.connect("Manager.db")
    cursor = conn.cursor()


    if username_edit.get()!="" and url_edit.get()!="" and email_id_edit.get()!="" and password_edit.get()!="":
        cursor.execute("""UPDATE manager1 SET 
                username = :username,
                url = :url,
                email_id = :email_id,
                password = :password
                
                WHERE oid = :oid""",
                       {
                           'username': username_edit.get(),
                           'url': url_edit.get(),
                           'email_id': email_id_edit.get(),
                           'password': password_edit.get()[::-1],
                           'oid': update_id.get()
                       }
        )
        
        conn.commit()
        conn.close()
        messagebox.showinfo("Alert", "Record Updated in Database!")

        # After data entry clear the text box and destroy the secondary window
        update_id.delete(0, END)
        edit.destroy()

    else:
        messagebox.showinfo("Alert", "Please fill all details!")
        conn.close()

##############################################################
#Create Function to Hide Records
def hide():
    query_label['text'] = ""
    query_btn.configure(text="Show Records", command=query)
##############################################################
#Create Function to Generate Random Password
def genrpassword():
    gnrpass.delete(0, END)
    digits = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 !@#$%^&*()"
    password = ""
    for i in range(0, 10):
        password = password + random.choice(digits)
    gnrpass.insert(0,password)

##############################################################
#Create Text Boxes
username = Entry(root, width=50)
username.grid(row=0, column=1, padx=30)
url = Entry(root, width=50)
url.grid(row=2, column=1, padx=30)
email_id = Entry(root, width=50)
email_id.grid(row=4, column=1, padx=30)
password = Entry(root, width=50,show="*")
password.grid(row=6, column=1, padx=30)
delete_id = Entry(root, width=10)
delete_id.grid(row=10, column=1, padx=30)
update_id = Entry(root, width=10)
update_id.grid(row=12, column=1, padx=20)
gnrpass=Entry(root,width=30)
gnrpass.grid(row=13,column=1,padx=20)

###############################################################
#Create Text Box Labels
username_label = Label(root, text = "Username:",bd="5",borderwidth="1",relief="solid")
username_label.grid(row=0, column=0)
url_label = Label(root, text = "URL:",bd="5",borderwidth="1",relief="solid")
url_label.grid(row=2, column=0)
email_id_label = Label(root, text = "Email Id:",bd="5",borderwidth="1",relief="solid")
email_id_label.grid(row=4, column=0)
password_label = Label(root, text = "Password:",bd="5",borderwidth="1",relief="solid")
password_label.grid(row=6, column=0)
###############################################################
#Submit Button
submit_btn = Button(root, text = "Add Record",relief=RAISED,activebackground='yellow', command = submit)
submit_btn.grid(row = 8, column=0, pady=5, padx=15, ipadx=35)
###############################################################
#Query Button
query_btn = Button(root, text = "Show Records",fg="blue",relief=RAISED,command = query)
query_btn.grid(row=8, column=1, pady=5, padx=5, ipadx=35)
###############################################################
#Delete Button
delete_btn = Button(root, text = "Delete Record",relief=RAISED,activebackground='red',command = delete)
delete_btn.grid(row=10, column=0, ipadx=30)
###############################################################
#Update Button
update_btn = Button(root, text = "Update Record",relief=RAISED,activebackground='green', command = update)
update_btn.grid(row=12, column=0, ipadx=30)
###############################################################
#Genrate Password Button
gnr_btn=Button(root,text="Generate Password",relief=RAISED,activebackground='green',command = genrpassword)
gnr_btn.grid(row=13,column=0,ipadx=30)
###############################################################
#Create a Label to show responses
global query_label
query_label = Label(frame, anchor="nw", justify="left")
query_label.place(relwidth=1, relheight=1)

def main():
    root.mainloop()

if __name__ == '__main__':
    main()


