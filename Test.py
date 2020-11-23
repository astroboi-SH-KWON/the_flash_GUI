from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import multiprocessing as mp
import os
import shutil

############### start to set env ################
WIN = None
INPUT_LIST = []
FILE_LIST = None
FILE_INPUT_LABEL = None
LOG_TXT = None

TOTAL_CPU = mp.cpu_count()
MULTI_CNT = int(TOTAL_CPU*0.5)
############### end setting env #################


def get_opt_list(mult_cnt, tot_cpu):
    if tot_cpu <= 4:
        return 1, [1]
    else:
        return mult_cnt // 2, [i for i in range(1, mult_cnt + 1)]


def upload_file(trgt_ent):
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


def valid_file_list(fl_list):
    non_data_flag = True
    for idx in range(len(fl_list))[::-1]:
        fl1 = fl_list[idx][::-1][0]
        fl2 = fl_list[idx][::-1][1]
        if fl1.replace(' ', '') == '' and fl2.replace(' ', '') == '':
            continue
        elif fl1.replace(' ', '') == '':
            messagebox.showerror('error', 'check row ' + str(idx + 1) + ' and the first file path')
            return False
        elif fl2.replace(' ', '') == '':
            messagebox.showerror('error', 'check row ' + str(idx + 1) + ' and the second file path')
            return False
        else:
            non_data_flag = False
    if non_data_flag:
        messagebox.showerror('error', 'check file path')
        return False
    return True


def make_dir():
    global LOG_TXT
    fq = '/FASTQ_File'
    co_pr = '/co_product_files'
    try:
        LOG_TXT.insert(CURRENT, 'make useless file folders\n\t => ' + fq + '\n\t => ' + co_pr + '\n')
        os.makedirs(fq, exist_ok=True)
        os.makedirs(co_pr, exist_ok=True)
    except Exception as err:
        LOG_TXT.insert(CURRENT, '[ERROR] during making useless file folders\n' + str(err))


def excute_flash(fq1, fq2, output_path):
    global LOG_TXT

    LOG_TXT.insert(CURRENT, 'excute_flash\n')
    try:
        # log = os.popen('cmd args').readline()
        # print(log, "::::::::::::::::::::::::::::::::::::::")
        os.system('flash {} {} -M 400 -m 10 -O -o {}'.format(fq1, fq2, output_path))
        LOG_TXT.insert(CURRENT, 'DONE :::::::::::::::::::::: \n\t' + output_path + ':'*20 + '\n')
        return

    except Exception as err:
        LOG_TXT.insert(CURRENT, '[ERROR] during flashing with \n\t' + output_path + '\n' + str(err))


def rename_FASTQ(o_path):
    os.rename(o_path + '.extendedFrags.fastq', o_path + '.fastq')


def move_useless(output):
    global LOG_TXT

    LOG_TXT.insert(CURRENT, 'move files to /co_product_files\n\t' + output + '\n')
    try:
        file1 = '{}.hist'.format(output)
        file2 = '{}.hist.innie'.format(output)
        file3 = '{}.hist.outie'.format(output)
        file4 = '{}.histogram'.format(output)
        file5 = '{}.histogram.innie'.format(output)
        file6 = '{}.histogram.outie'.format(output)
        file7 = '{}.notCombined_1.fastq'.format(output)
        file8 = '{}.notCombined_2.fastq'.format(output)
        file_list = [file1, file2, file3, file4, file5, file6, file7, file8]

        for i in file_list:
            shutil.move(i, '/co_product_files')
        LOG_TXT.insert(CURRENT, 'DONE : move files to /co_product_files\n\t' + output + '\n')
        return
    except Exception as err:
        LOG_TXT.insert(CURRENT, '[ERROR] during moving files to /co_product_files \n\t' + output + '\n' + str(err))


def move_FASTQ(output):
    global LOG_TXT

    LOG_TXT.insert(CURRENT, 'move FASTQ\n\t' + output + '\n')
    try:
        shutil.move('{}.fastq'.format(output), '/FASTQ_File')
        LOG_TXT.insert(CURRENT, 'DONE : move FASTQ\n\t' + output + '\n')
        return
    except Exception as err:
        LOG_TXT.insert(CURRENT, '[ERROR] during FASTQ \n\t' + output + '\n' + str(err))


def run_flash(fq1, fq2, output_path):
    global LOG_TXT

    LOG_TXT.insert(CURRENT, 'RUN the FLASH\n')
    make_dir()
    excute_flash(fq1, fq2, output_path)
    rename_FASTQ(output_path)
    move_useless(output_path)
    move_FASTQ(output_path)
    LOG_TXT.insert(CURRENT, 'DONE ::::::::::::::::: \nRUN the FLASH\n')
    return


def click_flash():
    global FILE_INPUT_LABEL
    global FILE_LIST
    input_list = FILE_INPUT_LABEL.grid_slaves()
    FILE_LIST = []
    for tmp_arr in input_list:
        tmp_ent_arr = []
        for btn_ent in tmp_arr.grid_slaves():
            if 'Entry' in str(type(btn_ent)):
                tmp_ent_arr.append(btn_ent.get())
                if len(tmp_ent_arr) == 2:
                    FILE_LIST.append(tmp_ent_arr)
                    tmp_ent_arr = []

    if valid_file_list(FILE_LIST):
        for tmp in FILE_LIST[::-1]:
            if '.gz' in tmp[::-1][0].lower():
                output_path, f_ex = os.path.splitext(tmp[::-1][0])
                output_path, f_ex = os.path.splitext(output_path)
            else:
                output_path, f_ex = os.path.splitext(tmp[::-1][0])
            proc = mp.Process(target=run_flash, args=(tmp[::-1][0], tmp[::-1][1], output_path.split('/')[-1]))
            proc.start()


def add_upload_file():
    global FILE_INPUT_LABEL
    global WIN

    _, n_row = FILE_INPUT_LABEL.grid_size()
    default_cpu, cpu_list = get_opt_list(MULTI_CNT, TOTAL_CPU)

    if cpu_list[-1] < n_row + 1:
        messagebox.showerror('warning', 'too many CPU')
        return
    elif default_cpu <= n_row + 1:
        if not messagebox.askyesno('alert', 'Recommend ' + str(default_cpu) + ' CPU.\nYour computer could get slow\n, if you use too many CPU.\nDo you want to use more CPU?'):
            return

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
    input_list[0].destroy()
    # FILE_INPUT_LABEL[0].grid_remove()


def reset():
    global FILE_INPUT_LABEL
    input_list = FILE_INPUT_LABEL.grid_slaves()
    for tmp_arr in input_list:
        for btn_ent in tmp_arr.grid_slaves():
            if 'Entry' in str(type(btn_ent)):
                btn_ent.delete(0, 'end')


def setupGUI():
    global WIN
    global FILE_INPUT_LABEL
    global LOG_TXT

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
    recmd_cpu = ' Recommend ' + str(default_cpu) + ' CPU, Max ' + str(cpu_list[-1]) + ' CPU '
    cpu_label = Label(spec_label, text=recmd_cpu, font='Courier 20 bold', relief=RAISED)
    cpu_label.grid(row=0, column=0, padx=5, pady=3)

    Button(spec_label, text='+', font='Courier 15 bold', command=add_upload_file, width=5).grid(row=0, column=2, padx=3,
                                                                                                pady=3)
    Button(spec_label, text='-', font='Courier 15 bold', command=del_upload_file, width=5).grid(row=0, column=3, padx=3,
                                                                                                pady=3)
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
    LOG_TXT = Text(frame1, font='Terminal 10', relief=RAISED, width=100, height=20)
    LOG_TXT.grid(row=2, columnspan=1, padx=3, pady=3)

    btn_label = Label(frame1, relief=FLAT)
    btn_label.grid(row=2, column=2, padx=3, pady=3)
    reset_btn = Button(btn_label, text='reset', font='Courier 10 bold', fg='red', command=reset, width=10)
    reset_btn.grid(row=0, column=2, padx=3, pady=5)
    flash_btn = Button(btn_label, text='run\nthe FLASH', font='Courier 15 bold', command=click_flash, width=10, height=8)
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
