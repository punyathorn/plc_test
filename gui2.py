import tkinter
from tkinter import *
import customtkinter
from tkinter import messagebox
import time
import pymcprotocol
from threading import *
from queue import Queue

HOST = '192.168.3.250'
PORT = 1025
customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("dark-blue")

GUI = customtkinter.CTk()
GUI.title("PLC Boccia Throw")
GUI.geometry("1200x480")
GUI.resizable(False, False)
Big = (None, 25)
Medium = customtkinter.CTkFont(size=20, weight="bold")
small = (None, 12)
menubar = Menu(GUI, tearoff=False, background='black', fg='white')
GUI.config(menu=menubar)

# Variables
status = StringVar()
speed_a1 = IntVar()
angle_a1 = IntVar()
SD5584 = IntVar()
angle_a2 = IntVar()
SD5582 = IntVar()
SD5544 = IntVar()
SD5542 = IntVar()
SD5504 = IntVar()
SD5502 = IntVar()
S = IntVar()
S.set(0)
write_queue = Queue()
response_queue = Queue()
stop_threads = Event()

status.set("Status: Disconnected")

def con_thread():
    status.set("Status: Connecting...")
    try:
        client = pymcprotocol.Type3E()
        client.setaccessopt(commtype="binary")
        if not client._is_connected:
            client.connect(ip=HOST, port=PORT)
        status.set("Status: Connected")
        client.close()
    except Exception as e:
        status.set("Status: Connection Failed")
        messagebox.showerror(title="Connection Error", message=str(e))

def read_thread():
    while not stop_threads.is_set():
        try:
            client = pymcprotocol.Type3E()
            client.setaccessopt(commtype="binary")
            if not client._is_connected:
                client.connect(ip=HOST, port=PORT)

            SM = client.batchread_wordunits(headdevice="SM5500", readsize=4)

            SD = [
                client.batchread_wordunits(headdevice="SD5502", readsize=1),
                client.batchread_wordunits(headdevice="SD5542", readsize=1),
                client.batchread_wordunits(headdevice="SD5582", readsize=1)
            ]
            SPSD = [
                client.batchread_wordunits(headdevice="SD5504", readsize=1),
                client.batchread_wordunits(headdevice="SD5544", readsize=1),
                client.batchread_wordunits(headdevice="SD5584", readsize=1)
            ]

            SD5582.set(SD[2][0])
            SD5542.set(SD[1][0])
            SD5502.set(SD[0][0])
            SD5504.set(SPSD[0][0])
            SD5544.set(SPSD[1][0])
            SD5584.set(SPSD[2][0])

            if not write_queue.empty():
                data = write_queue.get()
                try:
                    client.randomwrite(
                        word_devices=["D0", "D2", "D4"],
                        word_values=data,
                        dword_devices=[],
                        dword_values=[]
                    )
                    response_queue.put("Write successful")
                except Exception as e:
                    response_queue.put(f"Write failed: {e}")

            client.close()

        except Exception as e:
            print(f"[Read Thread Error] {e}")
        time.sleep(0.2)

def connect():
    global t, t2
    t = Thread(target=con_thread)
    t.start()
    time.sleep(5)
    t2 = Thread(target=read_thread, daemon=True)
    t2.start()

def one_axis_arm_throw():
    q = messagebox.askyesnocancel(title="1 Axis Arm Throw", message=f" Arm Speed d2: {speed_a1.get()} \n Arm Angle d4: {angle_a1.get()} \n Plate Angle d0: 0 \n Do you want to continue?")
    if not q:
        return
    write_queue.put([0, angle_a1.get(), speed_a1.get()])
    try:
        result = response_queue.get(timeout=5)
        messagebox.showinfo("Write Status", result)
    except:
        messagebox.showerror("Timeout", "No response from write thread")

def full_throw():
    q = messagebox.askyesnocancel(title="Full Throw", message=f" Arm Speed d2: {speed_a1.get()} \n Arm Angle d4: {angle_a1.get()} \n Plate Angle d0: {angle_a2.get()} \n Do you want to continue?")
    if not q:
        return
    write_queue.put([angle_a2.get(), angle_a1.get(), speed_a1.get()])
    try:
        result = response_queue.get(timeout=5)
        messagebox.showinfo("Write Status", result)
    except:
        messagebox.showerror("Timeout", "No response from write thread")

def on_closing():
    stop_threads.set()
    GUI.destroy()

GUI.protocol("WM_DELETE_WINDOW", on_closing)

sidebar_frame = customtkinter.CTkFrame(GUI, width=140, corner_radius=0)
sidebar_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")

Content_Label = customtkinter.CTkLabel(sidebar_frame, text="Arm Speed (pulse):", font=Medium)
Content_Label.grid(row=0, column=0, padx=10, pady=25)

Content_Entry = customtkinter.CTkEntry(sidebar_frame, textvariable=speed_a1, font=Medium, width=100)
Content_Entry.grid(row=1, column=0, padx=10, pady=25)

Content_Label = customtkinter.CTkLabel(sidebar_frame, text="Arm Angle (pulse):", font=Medium)
Content_Label.grid(row=2, column=0, padx=10, pady=25)

Content_Entry = customtkinter.CTkEntry(sidebar_frame, textvariable=angle_a1, font=Medium, width=100)
Content_Entry.grid(row=3, column=0, padx=10, pady=25)

Content_Label = customtkinter.CTkLabel(sidebar_frame, text="Plate Angle (pulse):", font=Medium)
Content_Label.grid(row=4, column=0, padx=10, pady=25)

Content_Entry = customtkinter.CTkEntry(sidebar_frame, textvariable=angle_a2, font=Medium, width=100)
Content_Entry.grid(row=5, column=0, padx=10, pady=25)

Content_Label = customtkinter.CTkLabel(sidebar_frame, text="Plate Angle (read) (pulse):", font=Medium)
Content_Label.grid(row=0, column=1, padx=10, pady=25)

Content_Entry = customtkinter.CTkEntry(sidebar_frame, textvariable=SD5582, font=Medium, width=50, state='disabled')
Content_Entry.grid(row=1, column=1, padx=10, pady=25)

Content_Label = customtkinter.CTkLabel(sidebar_frame, text="Plate Speed (read) (pulse):", font=Medium)
Content_Label.grid(row=2, column=1, padx=10, pady=25)

Content_Entry = customtkinter.CTkEntry(sidebar_frame, textvariable=SD5584, font=Medium, width=100, state='disabled')
Content_Entry.grid(row=3, column=1, padx=10, pady=25)

Content_Label = customtkinter.CTkLabel(sidebar_frame, text="Arm Angle (read) (pulse):", font=Medium)
Content_Label.grid(row=0, column=2, padx=10, pady=25)

Content_Entry = customtkinter.CTkEntry(sidebar_frame, textvariable=SD5542, font=Medium, width=50, state='disabled')
Content_Entry.grid(row=1, column=2, padx=10, pady=25)

Content_Label = customtkinter.CTkLabel(sidebar_frame, text="Arm Speed (read) (pulse):", font=Medium)
Content_Label.grid(row=2, column=2, padx=10, pady=25)

Content_Entry = customtkinter.CTkEntry(sidebar_frame, textvariable=SD5544, font=Medium, width=50, state='disabled')
Content_Entry.grid(row=3, column=2, padx=10, pady=25)

Content_Label = customtkinter.CTkLabel(sidebar_frame, textvariable=status, font=Medium)
Content_Label.grid(row=0, column=3, padx=10, pady=25)

sidebar_button_1 = customtkinter.CTkButton(sidebar_frame, text="Connect", command=connect)
sidebar_button_1.grid(row=1, column=3, padx=10, pady=25)

sidebar_button_1 = customtkinter.CTkButton(sidebar_frame, text="1 Axis Arm Throw", command=one_axis_arm_throw)
sidebar_button_1.grid(row=2, column=3, padx=10, pady=25)

sidebar_button_2 = customtkinter.CTkButton(sidebar_frame, text="Full Throw", command=full_throw)
sidebar_button_2.grid(row=3, column=3, padx=10, pady=25)

GUI.mainloop()
