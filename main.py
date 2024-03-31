import pyfirmata2
import pandas as pd
import time
import customtkinter as ctk
import ast

from PIL import Image
from servo_motors import *
from stepper_function import nano_sleep



ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Robot Arm")
root.geometry("1350x600")

# with open('list_of_moves.xlsx', sheet='Sheet1')


frame = ctk.CTkFrame(master=root, fg_color="#1F1F1F")
frame.pack(padx=20, pady=20, fill="both", expand=True)

#configure grid system for frame
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)

#display robot image right side
image_robot = ctk.CTkImage(dark_image=Image.open("robot_photo.jpg"), size=(200,550))
label_image = ctk.CTkLabel(frame, image=image_robot, text="")
label_image.grid( column=3, rowspan=6, padx=5, pady=5)

# arduino_port = ctk.CTkInputDialog(text = "Type Arduino Port - COM3, COM4..", title="Arduino Port")
# port = arduino_port.get_input()
# board = pyfirmata2.Arduino(port)


board = pyfirmata2.Arduino('COM4')
it = pyfirmata2.util.Iterator(board)
it.start()


pin_button = board.get_pin('d:13:i')
button_status = 0
def break_while(value):
    global button_status
    if value:
       button_status = 1

    else:
        button_status = 0


pin_button.register_callback(break_while)
pin_button.enable_reporting()

#################################################################################

def f_51_360(x, haf):
    return ((25 - 0) / (haf) ** 2) * (x - haf) ** 2 + 0
def f_21_60(x, haf):
    return ((30 - 15) / (haf) ** 2) * (x - haf) ** 2 + 15
def f_11_20(x, haf):
    return ((50 - 30) / (haf) ** 2) * (x - haf) ** 2 + 30
def f_1_10(x, haf):
    return ((120 - 100) / (haf) ** 2) * (x - haf) ** 2 + 100

def stepper_right(y):
    board.digital[12].write(0)
    board.digital[11].write(1)
    nano_sleep(y)
    board.digital[11].write(0)
def stepper_left(y):
    board.digital[12].write(1)
    board.digital[11].write(1)
    nano_sleep(y)
    board.digital[11].write(0)

crt_pos = 0
def motors_moves(value_stepper, value_servo1, value_servo2, value_servo3, value_servo4, value_servo5):

    global crt_pos

    dif = abs(value_stepper - crt_pos)
    half_dif = abs((value_stepper - crt_pos) / 2)
    step = 0

    while crt_pos < value_stepper:

        if dif <= 10:
            y = f_1_10(step, half_dif)
            stepper_right(y)

        elif dif <= 20:
            y = f_11_20(step, half_dif)
            stepper_right(y)

        elif dif <= 50:
            y = f_21_60(step, half_dif)
            stepper_right(y)

        elif dif <= 360:
            y = f_51_360(step, half_dif)
            stepper_right(y)

        crt_pos += 0.25
        step += 0.25

    while crt_pos > value_stepper:

        if dif <= 10:
            y = f_1_10(step, half_dif)
            stepper_left(y)

        elif dif <= 20:
            y = f_11_20(step, half_dif)
            stepper_left(y)

        elif dif <= 50:
            y = f_21_60(step, half_dif)
            stepper_left(y)

        elif dif <= 360:
            y = f_51_360(step, half_dif)
            stepper_left(y)

        crt_pos -= 0.25
        step += 0.25

    board.servo_config(6, min_pulse=0, max_pulse=180, angle=value_servo1)
    board.servo_config(7, min_pulse=0, max_pulse=180, angle=value_servo2)
    board.servo_config(8, min_pulse=0, max_pulse=180, angle=value_servo3)
    board.servo_config(9, min_pulse=0, max_pulse=180, angle=value_servo4)
    board.servo_config(10, min_pulse=0, max_pulse=180, angle=value_servo5)

    textbox_stepper_var.set(value_stepper)
    textbox_servo1_var.set(value_servo1)
    textbox_servo2_var.set(value_servo2)
    textbox_servo3_var.set(value_servo3)
    textbox_servo4_var.set(value_servo4)
    textbox_servo5_var.set(value_servo5)

def get_values_motors():
    value_stepper = int(stepper_slider.get())
    value_servo1 = int(servo1_slider.get())
    value_servo2 = int(servo2_slider.get())
    value_servo3 = int(servo3_slider.get())
    value_servo4 = int(servo4_slider.get())
    value_servo5 = int(servo5_slider.get())
    return value_stepper, value_servo1, value_servo2, value_servo3, value_servo4, value_servo5

def start_position():
    board.servo_config(6, min_pulse=0, max_pulse=180, angle=140)
    board.servo_config(7, min_pulse=0, max_pulse=180, angle=170)
    board.servo_config(8, min_pulse=0, max_pulse=180, angle=140)
    board.servo_config(9, min_pulse=0, max_pulse=180, angle=90)
    board.servo_config(10, min_pulse=0, max_pulse=180, angle=90)
    while True:
        board.digital[12].write(1)
        nano_sleep(30)
        board.digital[11].write(1)
        board.digital[11].write(0)

        if button_status == 1:
            break
    motors_moves(90, 139, 170, 140, 90, 90)

def update_values(*args):

    value_stepper, value_servo1, value_servo2, value_servo3, value_servo4, value_servo5 = get_values_motors()
    motors_moves(value_stepper, value_servo1, value_servo2, value_servo3, value_servo4, value_servo5)


moves_list = []
def save_moves():
    value_stepper, value_servo1, value_servo2, value_servo3, value_servo4, value_servo5 = get_values_motors()
    moves_list.append((value_stepper, value_servo1, value_servo2, value_servo3, value_servo4, value_servo5))
    print(moves_list)


def add_moves():
    global combobox_list
    name_set_of_moves = ctk.CTkInputDialog(text="Type Name")
    name_set = name_set_of_moves.get_input()

    table = pd.read_excel("list_of_moves.xlsx")
    new_moves = pd.DataFrame([{"Name": name_set, "Moves": moves_list}])
    table = pd.concat([table, new_moves], ignore_index=True)

    table.to_excel("list_of_moves.xlsx", index=False)
    combobox_list = table['Name'].tolist()
    combobox_moves.configure(values=combobox_list)





table = pd.read_excel("list_of_moves.xlsx")
combobox_list = table['Name'].tolist()
def delete_moves():
    moves_list.clear()

def combobox_value(choice):
    table = pd.read_excel("list_of_moves.xlsx")
    index_choice = table[table["Name"] == choice].index
    moves_list = ast.literal_eval(table.loc[index_choice[0], "Moves"]) #evalueaza stringul ca o expresie Python


    speed_choice = combobox_speed.get()

    moves = list_of_moves(moves_list)
    for set_moves in moves:
        value_stepper, value_servo1, value_servo2, value_servo3, value_servo4, value_servo5 = set_moves
        motors_moves(value_stepper, value_servo1, value_servo2, value_servo3, value_servo4, value_servo5)

        if speed_choice == "1":
            time.sleep(0.08)
        elif speed_choice == "2":
            time.sleep(0.05)
        elif speed_choice == "3":
            time.sleep(0.03)
        elif speed_choice == "4":
            time.sleep(0.01)
        elif speed_choice == "5":
            time.sleep(0)


##########################################################################################################################

    #define labels
stepper_label = ctk.CTkLabel(frame, width=20, height=190, text="Stepper", font=('Comic Sans MS Bold', 20), text_color="#CDC6E1")
stepper_label.grid(row=5, column=0, padx=5, pady=0)

servo1_label = ctk.CTkLabel(frame, width=20, height=20, text="Servo1", font=('Comic Sans MS Bold', 20), text_color="#CDC6E1")
servo1_label.grid(row=4, column=0, padx=5, pady=0)

servo2_label = ctk.CTkLabel(frame, width=20, height=170, text="Servo2", font=('Comic Sans MS Bold', 20), text_color="#CDC6E1")
servo2_label.grid(row=3, column=0, padx=5, pady=0)

servo3_label = ctk.CTkLabel(frame, width=20, height=40, text="Servo3", font=('Comic Sans MS Bold', 20), text_color="#CDC6E1")
servo3_label.grid(row=2, column=0, padx=5, pady=0)

servo4_label = ctk.CTkLabel(frame, width=20, height=30, text="Servo4", font=('Comic Sans MS Bold', 20), text_color="#CDC6E1")
servo4_label.grid(row=1, column=0, padx=5, pady=0)

servo5_label = ctk.CTkLabel(frame, width=20, text="Servo5", font=('Comic Sans MS Bold', 20), text_color="#CDC6E1")
servo5_label.grid(row=0, column=0, padx=5, pady=0)


#define sliders
stepper_slider = ctk.CTkSlider(frame, width=640, height=30, from_=0, to=320, number_of_steps=320, command=update_values)
stepper_slider.set(90)
stepper_slider.grid(row=5, column=1, pady=0)

servo1_slider = ctk.CTkSlider(frame, width=640, height=30, from_=5, to=140, number_of_steps=135, command=update_values)
servo1_slider.set(140)
servo1_slider.grid(row=4, column=1, pady=0)

servo2_slider = ctk.CTkSlider(frame, width=640, height=30, from_=5, to=170, number_of_steps=165, command=update_values)
servo2_slider.set(170)
servo2_slider.grid(row=3, column=1, pady=0)

servo3_slider = ctk.CTkSlider(frame, width=640, height=30, from_=50, to=170, number_of_steps=120, command=update_values)
servo3_slider.set(140)
servo3_slider.grid(row=2, column=1, pady=0)

servo4_slider = ctk.CTkSlider(frame, width=640, height=30, from_=0, to=180, number_of_steps=180, command=update_values)
servo4_slider.set(90)
servo4_slider.grid(row=1, column=1, pady=0)

servo5_slider = ctk.CTkSlider(frame, width=640, height=30, from_=5, to=120, number_of_steps=115, command=update_values)
servo5_slider.set(90)
servo5_slider.grid(row=0, column=1, pady=0)

#define textbox
textbox_stepper_var = ctk.StringVar()
textbox_stepper = ctk.CTkEntry(frame, width=90, height=30, textvariable=textbox_stepper_var, font=('Comic Sans MS Bold', 15), justify="center" )
textbox_stepper.insert(ctk.END,"160")
textbox_stepper.grid(row=5, column=2, padx=20)

textbox_servo1_var = ctk.StringVar()
textbox_servo1 = ctk.CTkEntry(frame, width=90, height=30, textvariable=textbox_servo1_var, font=('Comic Sans MS Bold', 15), justify="center" )
textbox_servo1.insert(ctk.END,"140")
textbox_servo1.grid(row=4, column=2, padx=20)

textbox_servo2_var = ctk.StringVar()
textbox_servo2 = ctk.CTkEntry(frame, width=90, height=30, textvariable=textbox_servo2_var, font=('Comic Sans MS Bold', 15), justify="center" )
textbox_servo2.insert(ctk.END,"170")
textbox_servo2.grid(row=3, column=2, padx=20)

textbox_servo3_var = ctk.StringVar()
textbox_servo3 = ctk.CTkEntry(frame, width=90, height=30, textvariable=textbox_servo3_var, font=('Comic Sans MS Bold', 15), justify="center" )
textbox_servo3.insert(ctk.END,"140")
textbox_servo3.grid(row=2, column=2, padx=20)

textbox_servo4_var = ctk.StringVar()
textbox_servo4 = ctk.CTkEntry(frame, width=90, height=30, textvariable=textbox_servo4_var, font=('Comic Sans MS Bold', 15), justify="center" )
textbox_servo4.insert(ctk.END,"90")
textbox_servo4.grid(row=1, column=2, padx=20)

textbox_servo5_var = ctk.StringVar()
textbox_servo5 = ctk.CTkEntry(frame, width=90, height=30, textvariable=textbox_servo5_var, font=('Comic Sans MS Bold', 15), justify="center" )
textbox_servo5.insert(ctk.END,"90")
textbox_servo5.grid(row=0, column=2, padx=20)


save_button = ctk.CTkButton(frame, width=90, height=30, text="Save", font=('Comic Sans MS Bold', 15), command=save_moves)
save_button.grid(row=6, column=0, padx=20)
play_stop_button = ctk.CTkButton(frame, width=90, height=30, text="Add move", font=('Comic Sans MS Bold', 15), command=add_moves)
play_stop_button.grid(row=6, column=1, padx=20)
delete_button = ctk.CTkButton(frame, width=90, height=30, text="Delete", font=('Comic Sans MS Bold', 15),  command=delete_moves)
delete_button.grid(row=6, column=2, padx=20)



combobox_moves_var = ctk.StringVar(value="Choose move")
combobox_moves = ctk.CTkComboBox(frame, values=combobox_list, state="readonly", command=combobox_value, variable=combobox_moves_var)
combobox_moves.grid(row=0, column=4, padx=20)

combobox_speed_var = ctk.StringVar(value="Choose speed")
combobox_speed = ctk.CTkComboBox(frame, values=['1', '2', '3', '4', '5'], state="readonly", variable=combobox_speed_var)
# combobox_speed_var.set('3')
combobox_speed.grid(row=6, column=4, padx=20)


##########################################
#All motors take initial position
start_position()
##########################################



def keys_keybord(event):
    key = event.keysym
    step_speed = 1

    if key == "s":
        save_moves()
    elif key == "d":
        delete_moves()
    elif key == "a":
        add_moves()

    elif key == "7":
        value_stepper, value_servo1, value_servo2, value_servo3, value_servo4, value_servo5 = get_values_motors()
        motors_moves(value_stepper, value_servo1 + step_speed , value_servo2, value_servo3, value_servo4, value_servo5)
        servo1_slider.set(value_servo1 + step_speed)

    elif key == "4":
        value_stepper, value_servo1, value_servo2, value_servo3, value_servo4, value_servo5 = get_values_motors()
        motors_moves(value_stepper, value_servo1 - step_speed, value_servo2, value_servo3, value_servo4, value_servo5)
        servo1_slider.set(value_servo1 - step_speed)

    elif key == "5":
        value_stepper, value_servo1, value_servo2, value_servo3, value_servo4, value_servo5 = get_values_motors()
        motors_moves(value_stepper, value_servo1, value_servo2 + step_speed, value_servo3, value_servo4, value_servo5)
        servo2_slider.set(value_servo2 + step_speed)

    elif key == "8":
        value_stepper, value_servo1, value_servo2, value_servo3, value_servo4, value_servo5 = get_values_motors()
        motors_moves(value_stepper, value_servo1, value_servo2 - step_speed, value_servo3, value_servo4, value_servo5)
        servo2_slider.set(value_servo2 - step_speed)

    elif key == "9":
        value_stepper, value_servo1, value_servo2, value_servo3, value_servo4, value_servo5 = get_values_motors()
        motors_moves(value_stepper, value_servo1, value_servo2, value_servo3 + step_speed, value_servo4, value_servo5)
        servo3_slider.set(value_servo3 + step_speed)

    elif key == "6":
        value_stepper, value_servo1, value_servo2, value_servo3, value_servo4, value_servo5 = get_values_motors()
        motors_moves(value_stepper, value_servo1, value_servo2, value_servo3 - step_speed, value_servo4, value_servo5)
        servo3_slider.set(value_servo3 - step_speed)

    elif key == "1":
        value_stepper, value_servo1, value_servo2, value_servo3, value_servo4, value_servo5 = get_values_motors()
        motors_moves(value_stepper, value_servo1, value_servo2, value_servo3, value_servo4 + step_speed, value_servo5)
        servo4_slider.set(value_servo4 + step_speed)

    elif key == "2":
        value_stepper, value_servo1, value_servo2, value_servo3, value_servo4, value_servo5 = get_values_motors()
        motors_moves(value_stepper, value_servo1, value_servo2, value_servo3, value_servo4 - step_speed, value_servo5)
        servo4_slider.set(value_servo4 - step_speed)

    elif key == "3":
        value_stepper, value_servo1, value_servo2, value_servo3, value_servo4, value_servo5 = get_values_motors()
        motors_moves(value_stepper, value_servo1, value_servo2, value_servo3, value_servo4, value_servo5 + step_speed)
        servo5_slider.set(value_servo5 + step_speed)

    elif key == "0":
        value_stepper, value_servo1, value_servo2, value_servo3, value_servo4, value_servo5 = get_values_motors()
        motors_moves(value_stepper, value_servo1, value_servo2, value_servo3, value_servo4, value_servo5 - step_speed)
        servo5_slider.set(value_servo5 - step_speed)

    elif key == "Left":
        value_stepper, value_servo1, value_servo2, value_servo3, value_servo4, value_servo5 = get_values_motors()
        motors_moves(value_stepper + step_speed, value_servo1, value_servo2, value_servo3, value_servo4, value_servo5)
        stepper_slider.set(value_stepper + step_speed)

    elif key == "Right":
        value_stepper, value_servo1, value_servo2, value_servo3, value_servo4, value_servo5 = get_values_motors()
        motors_moves(value_stepper - step_speed, value_servo1, value_servo2, value_servo3, value_servo4, value_servo5)
        stepper_slider.set(value_stepper - step_speed)




root.bind("<KeyPress>",keys_keybord)


root.mainloop()


























# # Configurare port serial
# port = 'COM4'
# baud_rate = 115200
#
# # Inițializare conexiune serială
# arduino = serial.Serial(port, baud_rate)
# time.sleep(2)  # așteaptă câteva secunde pentru stabilizarea conexiunii
#
# # # Trimite comenzi la Arduino pentru a mișca servo motoarele la pozițiile dorite
# # arduino.close()


