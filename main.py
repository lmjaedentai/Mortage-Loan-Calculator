import tkinter as tk
from tkinter import*
from tkinter.ttk import*
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image
from pathlib import Path
import webbrowser

firstclick = True 
totalperiod = 0
allprinciple = []*1201
allinterest = []*1201
allbalance = []*1201

def gopath(path: str) -> Path:   #determine correct path for every file
	return  Path("./assets") / Path(path)

def next():
    global show,proceed
    proceed = 0
    show = False

    def check(data):
        global proceed
        try:
            data = float(data)
            if data <1:
                messagebox.showerror('No negative input !','Please input a positive value')
                return
        except ValueError:
            messagebox.showerror('Incorrect Input','Please input a correct value!\nAll input should be in decimals only')
        else:
            proceed = proceed + 1         
        if proceed > 3:
            calculate()

    check(inputqty2.get())
    check(inputqty3.get())
    check(inputqty4.get())
    check(inputqty1.get())
	 
def calculate():
	root.geometry ("790x380") #adjust window size bcom larger
	root.maxsize (790,380)

	global firstclick,totalperiod,allbalance,allinterest,allprinciple,totalinterest,totalprinciple,monthpay
	period = 0
	totalprinciple = 0
	totalinterest = 0
	principle = 0.00 
	interest = 0.00 

	loan = float(inputqty1.get())   #get all input data from gui
	downpayment = float(inputqty2.get())
	rate = float(inputqty3.get())
	time = int(inputqty4.get())

	if firstclick == False: #clear previous data before proceeding
		x = len(table.get_children())
		for i in range(x):
			table.delete(i+1)

	loan = loan*((100 - downpayment)/100)  #count the money user want to borrow from bank
	balance = loan                         #determine how many money havent return
	time = time*12                         #calcualte the total month 
	rate = rate/100/12                     #calcualte the rate per month
	monthpay = loan*(rate/(1-((1+rate)**-time)))  #calcualte monthly repayment

	for period in range(1,time+1): 
		interest = balance*rate
		principle = monthpay - interest
		balance = balance - principle

		if balance < 0:
			balance = 0
		 #show result
		if period % 2 == 0:
			table.insert(values=(period,format(principle,"0.2f"),format(interest,"0.2f"),format(balance,"0.2f")), tags=('even'),parent='', index='end', iid=period, text="")
		else:
			table.insert(values=(period,format(principle,"0.2f"),format(interest,"0.2f"),format(balance,"0.2f")), tags=('odd'),parent='', index='end', iid=period, text="")

		allprinciple.append(float(format(principle,"0.2f")))
		allbalance.append(float(format(balance,"0.2f")))
		allinterest.append(float(format(interest,"0.2f")))
		totalprinciple +=principle
		totalinterest += interest
	#show total and monthly repayment
	table.insert(values=('Total',format(totalprinciple,"0.2f"),format(totalinterest,"0.2f"),' '), tags=('end'),parent='', index='end', iid=period+1, text="")
	totalUI = Label(root, text = ('RM',format(monthpay,'0.2f')) , font = (fontstyle, 12), background="white",foreground='black')
	totalUI.place(x=423,y=345)
	firstclick = False
	totalperiod = period

def files(): #export xlsx
	global totalperiod,allprinciple,allinterest,allbalance,totalinterest,totalprinciple,monthpay
	import csv
	import os
	header = ["Period", "Principle", "Interest", "Balance"]
	thepath = filedialog.askdirectory(title='  choose the place you want') #ask where to save

	if os.path.exists(os.path.join(thepath,'mortage loan.csv')):  #error handling
		try:
			os.remove(os.path.join(thepath,'mortage loan.csv')) #delete the file if the file is exist
		except:
			if PermissionError():
				messagebox.showerror('File in use','The action cant be completed because the previous version csv is open in another app\n\nClose the file and try again later.')
			else:
				messagebox.showerror('Sorry','An unexpected error has occurred and we fail to export CSV\nYou may contact Jaeden for futher help')
		print('deleted')

	with open(os.path.join(thepath,'mortage loan.csv'), 'w', encoding='UTF8', newline='') as f:
		writer = csv.writer(f) #create csv 
		writer.writerow(header)
		for a in range(totalperiod):
			writer.writerow([a,allprinciple[a],allinterest[a],allbalance[a]])

		writer.writerow(['Total ',format(totalinterest,"0.2f"),format(totalprinciple,"0.2f")])
		writer.writerow(' ')
		writer.writerow(['Monthly Repayment: ','','',format(monthpay,'0.2f')])
		writer.writerow(['Auto generated by Mortage Loan Calculator','','','',''])

def end():
	global firstclick
	if firstclick == True:
		root.destroy()
	else:
		confirm = messagebox.askyesnocancel("Quit app", "Before you quit the app\nDo you want to generate an analysis?")
		if confirm == True:  #user click yes
			files()
			root.destroy()
		elif confirm == False:  #user click no
			root.destroy()  #just close the window

#GUI
root = Tk()
root.title ("House Loan Calculator   |   2021 by Jaeden")
root.geometry ("390x380")
root.maxsize (390,390)
root.configure (bg='white')
root.protocol("WM_DELETE_WINDOW", end)
p1 = PhotoImage(file = gopath('icon.png'))
root.iconphoto(False, p1)
#dec
canvas = Canvas(root,bg='#FFFFFF',height = 600,width = 600,bd = 0,highlightthickness = 0,relief = "ridge")
canvas.place(x = 0, y = 0)
pic1 = PhotoImage(file= gopath('dec1.png'))
dec1 = canvas.create_image(300,200.0,image= pic1)
#label
fontstyle = 'Arial Rounded MT Bold'
aboutUI = Label(root, text = ('2021 by Jaeden') , font = (fontstyle, 7), background="white",foreground='lightgrey')
aboutUI.place(x=100, y=363)
h1 = Label(root, text = ('House Loan Calculator') , font = (fontstyle, 20), background="white",foreground='#6C63FF')
h1.place(x= 10 , y= 10)
ln1 = Label(root, text = ('______________') , font = ('Arial', 15), background="white",foreground='#E5E5FF')
ln1.place(x= 10 , y= 100)
ln2 = Label(root, text = ('______________') , font = ('Arial', 15), background="white",foreground='#E5E5FF')
ln2.place(x= 10 , y= 180)
ln3 = Label(root, text = ('______________') , font = ('Arial', 15), background="white",foreground='#E5E5FF')
ln3.place(x= 10 , y= 260)
ln4 = Label(root, text = ('______________') , font = ('Arial', 15), background="white",foreground='#E5E5FF')
ln4.place(x= 10 , y= 340)
a1=Label(root, text = ('Loan amount (RM)') , font = (fontstyle, 15), background="white",foreground='black')
a1.place(x= 10 , y= 60)
a2=Label(root, text = ('Down payment %') , font = (fontstyle, 15), background="white",foreground='black')
a2.place(x= 10 , y= 140)
a3=Label(root, text = ('Interest rate %') , font = (fontstyle, 15), background="white",foreground='black')
a3.place(x= 10 , y= 220)
a4=Label(root, text = ('Time period (year)') , font = (fontstyle, 15), background="white",foreground='black')
a4.place(x= 10 , y= 300)
#inputbox
inputqty1 = StringVar()
i1 = tk.Entry(root, textvariable = inputqty1,bg='white',bd=0 ,font = (fontstyle, 12),fg='#514D57')
i1.place (x=10, y= 90, width=145, height= 30)
inputqty2 = StringVar()
i2 = tk.Entry(root, textvariable = inputqty2,bg='white',bd=0,font = (fontstyle, 12),fg='#514D57')
i2.place (x=10, y= 170, width=150, height= 30)
inputqty3 = StringVar()
i3 = tk.Entry(root, textvariable = inputqty3,bg='white',bd=0,font = (fontstyle, 12),fg='#514D57')
i3.place (x=10, y= 250, width=150, height= 30)
inputqty4 = StringVar()
i4 = tk.Entry(root, textvariable = inputqty4,bg='white',bd=0,font = (fontstyle, 12),fg='#514D57')
i4.place (x=10, y= 330, width=150, height= 30)
ln5 = Label(root, text = ('______________') , font = ('Arial', 15), background="white",foreground='#E5E5FF')
ln5.place(x=423,y=350)
inputqty1.set('1')
inputqty2.set('1')
inputqty3.set('1')
inputqty4.set('1')
#next button
style = Style()
style.configure("btn.TLabel",background="white",anchor="center")
btnimg = tk.PhotoImage(file=gopath('next.png'))
button = Button(root, style="btn.TLabel",image=btnimg,command=next)
button.place (x=200, y=290)
button.configure (state = NORMAL,cursor="hand2")
#help button
helpimg = tk.PhotoImage(file=gopath('help.png'))
helpUI = Button(root, style="btn.TLabel",image=helpimg)
helpUI.place (x=345, y=15)
helpUI.configure (state = NORMAL,cursor="hand2")
helpUI.bind("<Button-1>", lambda e:webbrowser.open_new_tab('https://github.com/lmjaedentai/Mortage-Loan-Calculator#readme'))
#table
style.configure("Treeview", background="#D3D3D3",foreground="black",rowheight=25,fieldbackground="#D3D3D3")
style.map('Treeview', background=[('selected', '#6C63FF')])
frame = Frame(root)
frame.place(x=423,y=15)
table = ttk.Treeview(frame, selectmode="extended")
table.pack(side=LEFT)
scrollbar = Scrollbar(frame, orient=VERTICAL)
scrollbar.pack(side=RIGHT, fill=Y)
table.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=table.yview)
table.tag_configure('odd', background="white")
table.tag_configure('even', background="#D9D9FF")
table.tag_configure('end', background="gold")
table['columns'] = ("Period", "Principle", "Interest", "Balance")
table.column("#0", width=0, stretch=NO)
table.column("Period", anchor=CENTER, width=50)
table.column("Principle", anchor=CENTER, width=100)
table.column("Interest", anchor=CENTER, width=80) 
table.column("Balance", anchor=CENTER, width=120)
table.heading("#0", text="", anchor=CENTER)
table.heading("Period", text="Period", anchor=CENTER)
table.heading("Principle", text="Principle", anchor=CENTER)
table.heading("Interest", text="Interest", anchor=CENTER)
table.heading("Balance", text="Balance", anchor=CENTER)
#monthly repayment lbl
h2 = Label(root, text = ('$ Monthly Repayment :') , font = (fontstyle, 15), background="white",foreground='#FFB100')
h2.place(x=423,y=310)
#download button
downloadimg = tk.PhotoImage(file=gopath('download.png'))
downloadbtn = Button(root, style="btn.TLabel",image=downloadimg,command=files)
downloadbtn.place (x=707, y=305)
downloadbtn.configure (state = NORMAL,cursor="hand2")
downloadUI = Label(root, text = ('export as csv') , font = (fontstyle, 9), background="white",foreground='black')
downloadUI.place (x=690, y=360)
root.mainloop()