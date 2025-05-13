import tkinter
from tkinter import *
import customtkinter
from tkinter import messagebox
import sys
import rk_mcprotocol as mc
from threading import *

HOST = '192.168.3.250'
PORT = 1025
customtkinter.set_appearance_mode("light")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

GUI = customtkinter.CTk()  # create CTk window like you do with the Tk window
GUI.title("PLC Boccia Throw")
GUI.geometry("1200x480")
GUI.resizable(False, False)
Big = (None,25)
Medium = customtkinter.CTkFont(size=20, weight="bold")
small = (None, 12)
menubar = Menu(GUI, tearoff=False, background='black', fg='white')
GUI.config(menu=menubar)

#Variables
status = StringVar()
speed_a1 = IntVar()
angle_a1 = IntVar()
SD5584 = IntVar()
angle_a2 = IntVar()
SD5582 = IntVar()
SD5544 = IntVar()
SD5542 = IntVar()

status.set("Status: Disconnected")
def con_thread():
    global s
    status.set("Status: Connecting...")
    try:
        s = mc.open_socket(HOST,PORT) 
    except Exception as e:
        status.set("Status: Connection Failed")
        if TimeoutError:
            messagebox.showerror(title="Connection Error", message="Connection timed out. Make sure the PLC is on and connected to the PC.")
        else:
            messagebox.showerror(title="Connection Error", message=e)
        return
    status.set("Status: Connected")

def read_thread():
    speed_a2.set(mc.read_sign_word(s,headdevice = 'SM5582' , length = 2, signed_type=True))

def connect():
    global t
    t = Thread(target=con_thread)
    t.start()
    

def one_axis_arm_throw():
    q = messagebox.askyesnocancel(title="1 Axis Arm Throw", message=f" Arm Speed d2: {speed_a1.get()} \n Arm Angle d4: {angle_a1.get()} \n Plate Angle d0: 0 \n Do you want to continue?")
    if q == None:
        return
    if q == False:
        return
    try:
        r = mc.write_sign_word(s,headdevice = 'd2' , data_list = [angle_a1.get()], signed_type =True)
        r2 = mc.write_sign_word(s,headdevice = 'd4' , data_list = [speed_a1.get()], signed_type =True)
        r3 = mc.write_sign_word(s,headdevice = 'd0' , data_list = [0], signed_type =True)
        if r != 'ok':
            messagebox.showerror(title="D2 Arm Angle Write Error", message=r)
            return
        if r2 != 'ok':
            messagebox.showerror(title="D4 Arm Speed Write Error", message=r2)
            return
        if r3 != 'ok':
            messagebox.showerror(title="D0 Arm Start Write Error", message=r3)
            return
    except Exception as e:
        if NameError:
            messagebox.showerror(title="Connection Error", message="Please connect to the PLC first")
        else:
           messagebox.showerror(title="Write Error", message=e)

    try:
        r = mc.write_sign_word(s,headdevice = 'x1' , data_list = angle_a1, signed_type =True)
        if r != 'ok':
            messagebox.showerror(title="Throw Error", message=r)
            return
        
    except Exception as e:
        if NameError:
            messagebox.showerror(title="Connection Error", message="Please connect to the PLC first")
        else:
           messagebox.showerror(title="Error", message=e)

def full_throw():
    q = messagebox.askyesnocancel(title="1 Axis Arm Throw", message=f" Arm Speed d2: {speed_a1.get()} \n Arm Angle d4: {angle_a1.get()} \n Plate Angle d0: {angle_a2.get()} \n Do you want to continue?")
    if q == None:
        return
    if q == False:
        return    
    try:
        r = mc.write_sign_word(s,headdevice = 'd2' , data_list = [angle_a1.get()], signed_type =True)
        r2 = mc.write_sign_word(s,headdevice = 'd4' , data_list = [speed_a1.get()], signed_type =True)
        r3 = mc.write_sign_word(s,headdevice = 'd0' , data_list = [angle_a2.get()], signed_type =True)
        if r != 'ok':
            messagebox.showerror(title="D2 Arm Angle Write Error", message=r)
            return
        if r2 != 'ok':
            messagebox.showerror(title="D4 Arm Speed Write Error", message=r2)
            return
        if r3 != 'ok':
            messagebox.showerror(title="D0 Arm Start Write Error", message=r3)
            return
    except Exception as e:
        if NameError:
            messagebox.showerror(title="Connection Error", message="Please connect to the PLC first")
        else:
           messagebox.showerror(title="Write Error", message=e)

    try:
        r = mc.write_sign_word(s,headdevice = 'x1' , data_list = angle_a1, signed_type =True)
        if r != 'ok':
            messagebox.showerror(title="Throw Error", message=r)
            return
        
    except Exception as e:
        if NameError:
            messagebox.showerror(title="Connection Error", message="Please connect to the PLC first")
        else:
           messagebox.showerror(title="Error", message=e)

sidebar_frame = customtkinter.CTkFrame(GUI, width=140, corner_radius=0)
sidebar_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")

#COLUMN 0
Content_Label = customtkinter.CTkLabel(sidebar_frame, text="Arm Speed (pulse):", font=Medium)
Content_Label.grid(row=0, column=0, padx=10, pady=25)

Content_Entry = customtkinter.CTkEntry(sidebar_frame, textvariable= speed_a1, font= Medium, width= 100)
Content_Entry.grid(row=1, column=0, padx=10, pady=25)

Content_Label = customtkinter.CTkLabel(sidebar_frame, text="Arm Angle (pulse):", font=Medium)
Content_Label.grid(row=2, column=0, padx=10, pady=25)

Content_Entry = customtkinter.CTkEntry(sidebar_frame, textvariable= angle_a1, font= Medium, width= 100)
Content_Entry.grid(row=3, column=0, padx=10, pady=25)

Content_Label = customtkinter.CTkLabel(sidebar_frame, text="Plate Angle (pulse):", font=Medium)
Content_Label.grid(row=4, column=0, padx=10, pady=25)

Content_Entry = customtkinter.CTkEntry(sidebar_frame, textvariable= angle_a2, font= Medium, width= 100)
Content_Entry.grid(row=5, column=0, padx=10, pady=25)


#COLUMN 1
Content_Label = customtkinter.CTkLabel(sidebar_frame, text="Plate Angle (read) (pulse):", font=Medium)
Content_Label.grid(row=0, column=1, padx=10, pady=25)

Content_Entry = customtkinter.CTkEntry(sidebar_frame, textvariable= SD5582, font= Medium, width= 50, state='disabled')
Content_Entry.grid(row=1, column=1, padx=10, pady=25)

Content_Label = customtkinter.CTkLabel(sidebar_frame, text="Plate Speed (read) (pulse):", font=Medium)
Content_Label.grid(row=2, column=1, padx=10, pady=25)

Content_Entry = customtkinter.CTkEntry(sidebar_frame, textvariable= SD5584, font= Medium, width= 100, state='disabled')
Content_Entry.grid(row=3, column=1, padx=10, pady=25)


#COLUMN 2
Content_Label = customtkinter.CTkLabel(sidebar_frame, text="Arm Angle (read) (pulse):", font=Medium)
Content_Label.grid(row=0, column=2, padx=10, pady=25)

Content_Entry = customtkinter.CTkEntry(sidebar_frame, textvariable= SD5542, font= Medium, width= 50, state='disabled')
Content_Entry.grid(row=1, column=2, padx=10, pady=25)

Content_Label = customtkinter.CTkLabel(sidebar_frame, text="Arm Speed (read) (pulse):", font=Medium)
Content_Label.grid(row=2, column=2, padx=10, pady=25)

Content_Entry = customtkinter.CTkEntry(sidebar_frame, textvariable= SD5544, font= Medium, width= 50, state='disabled')
Content_Entry.grid(row=3, column=2, padx=10, pady=25)


#COLUMN 3
Content_Label = customtkinter.CTkLabel(sidebar_frame, textvariable = status, font=Medium)
Content_Label.grid(row=0, column=3, padx=10, pady=25)

sidebar_button_1 = customtkinter.CTkButton(sidebar_frame, text="Connect", command=connect)
sidebar_button_1.grid(row=1, column=3, padx=10, pady=25)

sidebar_button_1 = customtkinter.CTkButton(sidebar_frame, text="1 Axis Arm Throw", command=one_axis_arm_throw)
sidebar_button_1.grid(row=2, column=3, padx=10, pady=25)

sidebar_button_2 = customtkinter.CTkButton(sidebar_frame, text="Full Throw", command=full_throw)
sidebar_button_2.grid(row=3, column=3, padx=10, pady=25)


GUI.mainloop()
try:
    s.close()
    t.join()
except:
    pass