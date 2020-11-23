from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import multiprocessing as mp

############### start to set env ################
WIN = None
INPUT_LIST = []
BTN_LIST = []
FILE_LIST = []
FILE_INPUT_LABEL = None

TOTAL_CPU = mp.cpu_count()
MULTI_CNT = int(TOTAL_CPU*0.5)
############### end setting env #################


def get_opt_list(mult_cnt, tot_cpu):
    if tot_cpu <= 4:
        return 1, [1]
    else:
        return mult_cnt // 2, [i for i in range(1, mult_cnt + 1)]

# TODO
def upload_file(trgt_ent):
    print(trgt_ent)
    trgt_ent.delete(0, 'end')
    trgt_ent.insert(0, filedialog.askopenfilename())




def get_cpu_num(cpu_num):
    global INPUT_LIST
    global FILE_INPUT_LABEL

    input_list = FILE_INPUT_LABEL.grid_slaves()
    for tmp_input in input_list:
        print(tmp_input)
        tmp_input.destroy()

    for i in range(cpu_num):
        # st file dialog
        input_file1 = Entry(FILE_INPUT_LABEL, font='Terminal 10', width=50)
        input_file1.grid(row=i, column=0, padx=3, pady=3)
        input_file2 = Entry(FILE_INPUT_LABEL, font='Terminal 10', width=50)
        input_file2.grid(row=i, column=2, padx=3, pady=3)

        tmp_arr = [input_file1, input_file2]
        INPUT_LIST.append(tmp_arr)

        file_button1 = Button(FILE_INPUT_LABEL, text='open', font='Courier 10 bold',
                              command=lambda: upload_file(INPUT_LIST[i][0]), width=7)
        file_button1.grid(row=i, column=1, padx=3, pady=3)
        file_button2 = Button(FILE_INPUT_LABEL, text='open', font='Courier 10 bold',
                              command=lambda: upload_file(INPUT_LIST[i][1]), width=7)
        file_button2.grid(row=i, column=3, padx=3, pady=3)
        # en file dialog


def run_flash():
    global FILE_INPUT_LABEL
    global FILE_LIST

    input_list = FILE_INPUT_LABEL.grid_slaves()
    tmp_arr = []
    for idx in range(len(input_list))[::-1]:
        if idx % 2 != 0:
            fl_path = input_list[idx].get().replace(' ', '')
            tmp_arr.append(fl_path)
            if len(tmp_arr) == 2:
                FILE_LIST.append(tmp_arr)
                tmp_arr = []
    print(FILE_LIST)


def add_upload_file():
    global FILE_INPUT_LABEL
    global WIN
    _, n_row = FILE_INPUT_LABEL.grid_size()

    # st file dialog
    # if n_row < 5:
    #     input_list = FILE_INPUT_LABEL.grid_slaves()
    #     for tmp_input in input_list:
    #         tmp_input.destroy()
    #     idx = 0
    #     for tmp_input in input_list[::-1]:
    #         tmp_input.grid(row=idx, columnspan=3, padx=5, pady=5)
    #         idx += 1
    default_label = Label(FILE_INPUT_LABEL, relief=FLAT)
    default_label.grid(row=n_row, columnspan=3, padx=5, pady=5)
    default_ent1 = Entry(default_label, font='Terminal 10', width=50)
    default_ent2 = Entry(default_label, font='Terminal 10', width=50)
    default_ent1.grid(row=0, column=0, padx=3, pady=3)
    default_ent2.grid(row=0, column=2, padx=3, pady=3)

    default_btn1 = Button(default_label, text='open', font='Courier 10 bold',
                          command=lambda: upload_file(default_ent1), width=7)
    default_btn2 = Button(default_label, text='open', font='Courier 10 bold',
                          command=lambda: upload_file(default_ent2), width=7)
    default_btn1.grid(row=0, column=1, padx=3, pady=3)
    default_btn2.grid(row=0, column=3, padx=3, pady=3)
    # en file dialog


def del_upload_file():
    global FILE_INPUT_LABEL
    _, n_row = FILE_INPUT_LABEL.grid_size()
    if n_row == 1:
        messagebox.showerror('info', 'You can NOT remove the last row')
        return
    input_list = FILE_INPUT_LABEL.grid_slaves()
    input_list[0].grid_remove()


def reset():
    print('reset')

def setupGUI():
    global WIN
    global FILE_INPUT_LABEL
    global INPUT_LIST
    global BTN_LIST

    WIN = Tk()
    WIN.title('the FLASH for GUI')

    notebk = ttk.Notebook(WIN)
    notebk.pack()

    frame1 = Frame(WIN)
    notebk.add(frame1, text='the FLASH')

    spec_label = Label(frame1)
    spec_label.grid(row=0, columnspan=3, padx=3, pady=3)
    # st drop down selection box
    default_cpu, cpu_list = get_opt_list(MULTI_CNT, TOTAL_CPU)
    variable = StringVar(spec_label)
    variable.set(default_cpu)
    opt = OptionMenu(spec_label, variable, *cpu_list, command=get_cpu_num)
    opt.config(font=('Terminal bold', 11))
    opt.grid(row=0, column=0, padx=5, pady=3)
    cpu_label = Label(spec_label, text='CPU', font='Courier 15 bold')
    cpu_label.grid(row=0, column=1, padx=5, pady=3)
    Button(spec_label, text='+', font='Courier 15 bold', command=add_upload_file, width=7).grid(row=0, column=2, padx=3, pady=3)
    Button(spec_label, text='-', font='Courier 15 bold', command=del_upload_file, width=7).grid(row=0, column=3, padx=3, pady=3)
    # en drop down selection box

    # st file_input_label
    FILE_INPUT_LABEL = Label(frame1, relief=RAISED)
    FILE_INPUT_LABEL.grid(row=1, columnspan=3, padx=5, pady=5)

    # st file dialog
    default_label = Label(FILE_INPUT_LABEL, relief=FLAT)
    default_label.grid(row=0, columnspan=3, padx=5, pady=5)
    default_ent1 = Entry(default_label, font='Terminal 10', width=50)
    default_ent2 = Entry(default_label, font='Terminal 10', width=50)
    default_ent1.grid(row=0, column=0, padx=3, pady=3)
    default_ent2.grid(row=0, column=2, padx=3, pady=3)

    default_btn1 = Button(default_label, text='open', font='Courier 10 bold',
                          command=lambda: upload_file(default_ent1), width=7)
    default_btn2 = Button(default_label, text='open', font='Courier 10 bold',
                          command=lambda: upload_file(default_ent2), width=7)
    default_btn1.grid(row=0, column=1, padx=3, pady=3)
    default_btn2.grid(row=0, column=3, padx=3, pady=3)
    # en file dialog

    # Text for log
    log_text = Text(frame1, font='Terminal 10', relief=RAISED, width=100, height=20)
    log_text.grid(row=2, columnspan=1, padx=3, pady=3)

    btn_label = Label(frame1, relief=FLAT)
    btn_label.grid(row=2, column=2, padx=3, pady=3)
    reset_btn = Button(btn_label, text='reset', font='Courier 10 bold', fg='red', command=reset, width=10)
    reset_btn.grid(row=0, column=2, padx=3, pady=5)
    flash_btn = Button(btn_label, text='run\nthe FLASH', font='Courier 15 bold', command=run_flash, width=10, height=8)
    flash_btn.grid(row=1, column=2, padx=3, pady=5)

    frame2 = Frame(WIN)
    notebk.add(frame2, text='about')
    about = """
    
THIS APP WAS MADE WITH pairwise2 FROM biopython.
IT IS A FREE APP LIKE biopython.
YOU CAN DOWNLOAD AND EDIT THE ORIGINAL 
BY FOLLOWING THE LINK BELOW.
WE ARE NOT RESPONSIBLE FOR ANY DAMAGE AFTER DOWNLOAD AND USE.
_________________________________________________
https://github.com/astroboi-SH-KWON/the_flash_GUI
_________________________________________________

이 app은 biopython 기반의 pairwise2를 사용하였습니다.
biopython처럼 이 app은 완전 무료 제품입니다.
github에 원래 소스를 받아서 수정하셔도 됩니다.
우리는 이 app에 의해 생기는 
사용자의 어떠한 손해도 책임지지 않습니다.
        """
    about_label = Label(frame2, font='Terminal 15', text=about, relief=FLAT, width=95, height=15)
    about_label.grid(row=1, columnspan=2, padx=5, pady=5)




if __name__ == '__main__':
    setupGUI()
    WIN.mainloop()
