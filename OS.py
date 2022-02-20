import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
from pycoingecko import CoinGeckoAPI
from datetime import datetime
import csv
import time

from ui_function import *

cg = CoinGeckoAPI()
data = cg.get_price(ids=['bitcoin', 'ethereum', 'dogecoin'], vs_currencies=[
                     'usd', 'thb'], include_24hr_change='true')
now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def show_frame(frame):
    frame.tkraise()

def create_csv():
    print('Creating CSV...')
    with open('E:/OS/test.csv', 'w', newline='') as csvfile:
        fieldnames = ['Time',
                      'bitcoin[usb]', '[bitcoin]usd_24h_change', 'bitcoin[thb]', '[bitcoin]thb_24h_change',
                      'ethereum[usb]', '[ethereum]usd_24h_change', 'ethereum[thb]', '[ethereum]thb_24h_change',
                      'dogecoin[usb]', '[dogecoin]usd_24h_change', 'dogecoin[thb]', '[dogecoin]thb_24h_change', ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()


def save_data():
    print('Saving data...')
    data = cg.get_price(ids=['bitcoin', 'ethereum', 'dogecoin'], vs_currencies=['usd', 'thb'], include_24hr_change='true')
    localtime = time.localtime()
    with open('E:/OS/test.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([time.strftime("%d/%m/%Y %H:%M:%S", localtime),
        data['bitcoin']['usd'], data['bitcoin']['usd_24h_change'], data['bitcoin']['thb'], data['bitcoin']['thb_24h_change'],
        data['ethereum']['usd'], data['ethereum']['usd_24h_change'], data['ethereum']['thb'], data['ethereum']['thb_24h_change'],
        data['dogecoin']['usd'], data['dogecoin']['usd_24h_change'], data['dogecoin']['thb'], data['dogecoin']['thb_24h_change']
        ])
    print(time.strftime('%I:%M:%S', localtime),'Save to file price.csv complete')

def show_data():
    frame5_table.delete(*frame5_table.get_children())
    with open('E:/OS/test.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            frame5_table.insert('',0,values=(row['Time'],row['bitcoin[usb]'],row['bitcoin[thb]'],
            row['ethereum[usb]'],row['ethereum[thb]'],
            row['dogecoin[usb]'],row['dogecoin[thb]']))

def currency_changed():
    btc_btn.configure(
        text='Bitcoin : %.2f %s %.2f'%(data['bitcoin'][selected_coin.get()], selected_coin.get().upper(), data['bitcoin'][f'{selected_coin.get()}_24h_change']),
        bg='#FF6B6B' if data['bitcoin'][f'{selected_coin.get()}_24h_change'] <= 0 else '#6BFF6B'
    )
    eth_btn.configure(
        text='Ethereum : %.2f %s %.2f'%(data['ethereum'][selected_coin.get()], selected_coin.get().upper(), data['ethereum'][f'{selected_coin.get()}_24h_change']),
        bg='#FF6B6B' if data['ethereum'][f'{selected_coin.get()}_24h_change'] <= 0 else '#6BFF6B'
    )
    doge_btn.configure(
        text='Dogecoin : %.4f %s %.2f'%(data['dogecoin'][selected_coin.get()], selected_coin.get().upper(), data['dogecoin'][f'{selected_coin.get()}_24h_change']),
        bg='#FF6B6B' if data['dogecoin'][f'{selected_coin.get()}_24h_change'] <= 0 else '#6BFF6B'
    )

window = tk.Tk()
window.state('zoomed')

window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)

frame1 = tk.Frame(window)
frame2 = tk.Frame(window)
frame3 = tk.Frame(window)
frame4 = tk.Frame(window)
frame5 = tk.Frame(window)

for frame in (frame1, frame2, frame3, frame4,frame5):
    frame.grid(row=0,column=0,sticky='nsew')

#=========== Menu Bar
menu_bar = tk.Menu(window)
window.config(menu=menu_bar)
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='Close', command=window.destroy) 
file_menu.add_separator()
    
#==================Frame 1 code
frame1_title =  tk.Label(frame1, text='Cryptocurrency Monitor', font='times 55')
frame1_title.place(x=700, y=100)

img_1 = tk.PhotoImage(file="All_coin.png")
ttk.Label(frame1, image=img_1).place(x=100, y=100)

#==================function change colour button
btc_btn = tk.Button(
    frame1, 
    text='Bitcoin : %.2f USD  %.2f'%(data['bitcoin']['usd'], data['bitcoin']['usd_24h_change']),
    font='times 32',
    width=30,
    bg='#FF6B6B' if data['bitcoin']['usd_24h_change'] < 0 else '#6BFF6B',
    command=lambda:show_frame(frame2))
btc_btn.place(x=700, y=300)

eth_btn = tk.Button(
    frame1, 
    text='Ethereum : %.2f USD  %.2f'%(data['ethereum']['usd'], data['ethereum']['usd_24h_change']),
    font='times 32',
    width=30,
    bg='#FF6B6B' if data['ethereum']['usd_24h_change'] < 0 else '#6BFF6B',
    command=lambda:show_frame(frame3))
eth_btn.place(x=700, y=400)

doge_btn = tk.Button(
    frame1, 
    text='Dogecoin : %.4f USD  %.2f'%(data['dogecoin']['usd'], data['dogecoin']['usd_24h_change']),
    font='times 32',
    width=30,
    bg= '#FF6B6B' if data['dogecoin']['usd_24h_change'] < 0 else '#6BFF6B',
    command=lambda:show_frame(frame4))
doge_btn.place(x=700, y=500)

frame1_title=  tk.Label(frame1, text='Select Currency', font='times 24')
frame1_title.place(x=700, y=225)

frame1_text_updateTime = tk.Label(frame1, text=f'Last Update: {now}', font='times 24')
frame1_text_updateTime.place(x=700, y=600)

# create a combobox
selected_coin = tk.StringVar()
coin = ttk.Combobox(
    frame1, 
    font='times 24',
    width=30,
    textvariable=selected_coin)

coin['values'] = (
    'usd',
    'thb',
)

# prevent typing a value
coin['state'] = 'readonly'

coin.current(0)

# place the widget
coin.place(x=925, y=225)


def coin_changed(event):
    currency_changed()

coin.bind('<<ComboboxSelected>>', coin_changed)

def update_coin():
    global data
    global now
    data = cg.get_price(ids=['bitcoin', 'ethereum', 'dogecoin'], vs_currencies=[
                     'usd', 'thb'], include_24hr_change='true')
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    currency_changed()
    frame1_text_updateTime.configure(text=f'Last Update: {now}')
    window.after(30000,update_coin)

#==================Frame 2 code
frame2_title=  tk.Label(frame2, text='Bitcoin', font='times 35') 
frame2_title.place(x=700, y=100)

img_2 = tk.PhotoImage(file="bitcoin.png")
ttk.Label(frame2, image=img_2).place(x=20, y=20)

# Grpah Code
btc_fg1 = Figure(figsize=(5,5), dpi=100)
btc_fg1_plot=btc_fg1.add_subplot(111)
btc_usd = get_btc()
btc_fg1_plot.title.set_text('Bitcoin - USD')
btc_fg1_plot.plot(btc_usd['Close'], label='USD')
btc_fg1_plot.legend(loc='upper left')
canvas1 = FigureCanvasTkAgg(btc_fg1, frame2)
canvas1.draw()
canvas1.get_tk_widget().place(x=600, y=200,width=800,height=250)

btc_fg2 = Figure(figsize=(5,5), dpi=100)
btc_fg2_plot=btc_fg2.add_subplot(111)
btc_thb= get_btc()
btc_fg2_plot.title.set_text('Bitcoin - THB')
btc_fg2_plot.plot(btc_thb['Close']*32.5, label='THB', color='green')
btc_fg2_plot.legend(loc='upper left')
canvas2 = FigureCanvasTkAgg(btc_fg2, frame2)
canvas2.draw()
canvas2.get_tk_widget().place(x=600, y=450,width=800,height=250)

save_btn = tk.Button(frame1, text='Save', font='times 24', command=lambda:save_data())
save_btn.place(x=700, y=650)
show_table_btn = tk.Button(frame1, text='Show Table', font='times 24',command=lambda:[show_frame(frame5),show_data()])
show_table_btn.place(x=800, y=650)

frame2_btn_back = tk.Button(frame2, text='Home',command=lambda:show_frame(frame1),bg='#BFC9CA')
frame2_btn_back.pack(fill='x',ipady=15,side='bottom')


#==================Frame 3 code
frame3_title=  tk.Label(frame3, text='Ethereum',font='times 35')
frame3_title.place(x=700, y=100)

img_3 = tk.PhotoImage(file="ethereum.png")
ttk.Label(frame3, image=img_3).place(x=100, y=250)

eth_fg1 = Figure(figsize=(5,5), dpi=100)
eth_fg1_plot=eth_fg1.add_subplot(111)
eth_usd = get_eth()
eth_fg1_plot.title.set_text('Ethreuem - USD')
eth_fg1_plot.plot(eth_usd['Close'], label='USD')
eth_fg1_plot.legend(loc='upper left')
canvas_eth1 = FigureCanvasTkAgg(eth_fg1, frame3)
canvas_eth1.draw()
canvas_eth1.get_tk_widget().place(x=600, y=200,width=800,height=250)

eth_fg2 = Figure(figsize=(5,5), dpi=100)
eth_fg2_plot=eth_fg2.add_subplot(111)
eth_thb= get_eth()
eth_fg2_plot.title.set_text('Ethreuem - THB')
eth_fg2_plot.plot(eth_thb['Close']*32.5, label='THB', color='green')
eth_fg2_plot.legend(loc='upper left')
canvas_eth2 = FigureCanvasTkAgg(eth_fg2, frame3)
canvas_eth2.draw()
canvas_eth2.get_tk_widget().place(x=600, y=450,width=800,height=250)



frame3_btn_back = tk.Button(frame3, text='Home',command=lambda:show_frame(frame1),bg='#BFC9CA')
frame3_btn_back.pack(fill='x',ipady=15,side='bottom')

#==================Frame 4 code
frame4_title=  tk.Label(frame4, text='Dogecoin',font='times 35')
frame4_title.place(x=700, y=100)

img_4 = tk.PhotoImage(file="dogecoin.png")
ttk.Label(frame4, image=img_4).place(x=100, y=250)

doge_fg1 = Figure(figsize=(5,5), dpi=100)
doge_fg1_plot=doge_fg1.add_subplot(111)
doge_usd = get_doge()
doge_fg1_plot.title.set_text('Doge - USD')
doge_fg1_plot.plot(doge_usd['Close'], label='USD')
doge_fg1_plot.legend(loc='upper left')
canvas_doge1 = FigureCanvasTkAgg(doge_fg1, frame4)
canvas_doge1.draw()
canvas_doge1.get_tk_widget().place(x=600, y=200,width=800,height=250)

doge_fg2 = Figure(figsize=(5,5), dpi=100)
doge_fg2_plot=doge_fg2.add_subplot(111)
doge_thb= get_doge()
doge_fg2_plot.title.set_text('Doge - THB')
doge_fg2_plot.plot(doge_thb['Close']*32.5, label='THB', color='green')
doge_fg2_plot.legend(loc='upper left')
canvas_doge2 = FigureCanvasTkAgg(doge_fg2, frame4)
canvas_doge2.draw()
canvas_doge2.get_tk_widget().place(x=600, y=450,width=800,height=250)



frame4_btn_back = tk.Button(frame4, text='Home',command=lambda:show_frame(frame1),bg='#BFC9CA')
frame4_btn_back.pack(fill='x',ipady=15,side='bottom')

#==================Frame 5 code
frame5_title=  tk.Label(frame5)
frame_label = tk.Label(frame5, text='Record history', font='times 35')
frame_label.pack(fill='x',ipady=15,side='top')
frame5_title.place(x=700, y=100)
col=('Time','Bitcoin[USD]','Bitcoin[THB]','Ethereum[USD]','Ethereum[THB]','Dogecoin[USD]','Dogecoin[THB]')
frame5_table = ttk.Treeview(frame5, columns=col, height=10)
for i in col:
    frame5_table.heading(i, text=i, anchor='center')
    frame5_table.column(i, width=100)

frame5_table.pack(fill='both',expand=True)

frame5_btn_back = tk.Button(frame5, text='Home',command=lambda:show_frame(frame1),bg='#BFC9CA')
frame5_btn_back.pack(fill='x',ipady=15,side='bottom')

create_csv()
show_frame(frame1)
update_coin()

window.mainloop()