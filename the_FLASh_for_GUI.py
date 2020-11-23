from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import os
import shutil

############### start to set env ################
WIN = None
FILE_LIST = None
FILE_INPUT_LABEL = None
log_txt = None

FLASH_RESULT = '../FLASh_RESULT'
CO_PRODUCT_FILES = '../co_product_files'

############### end setting env #################


def get_opt_list(mult_cnt, tot_cpu):
    if tot_cpu <= 4:
        return 1, [1]
    else:
        return mult_cnt // 2, [i for i in range(1, mult_cnt + 1)]


def upload_file(trgt_ent):
    trgt_ent.delete(0, 'end')
    trgt_ent.insert(0, filedialog.askopenfilename())


def valid_file_list(fl_list):
    tot_len = len(fl_list)
    for idx in range(tot_len):
        fl1 = fl_list[idx][::-1][0]
        fl2 = fl_list[idx][::-1][1]
        if fl1.replace(' ', '') == '' or fl2.replace(' ', '') == '':
            messagebox.showerror('error', 'check file path')
            return False
    return True


def make_dir():
    global log_txt
    try:
        os.makedirs(FLASH_RESULT, exist_ok=True)
        os.makedirs(CO_PRODUCT_FILES, exist_ok=True)
    except Exception as err:
        log_txt.insert(CURRENT, '[-ERROR-] during making useless file folders\n' + str(err) + '\n')


def excute_flash(fq1, fq2, output_path):
    global log_txt
    try:
        log_txt.insert(CURRENT, 'FLAShing ==========\n\t' + output_path + '\n')
        os.system('flash {} {} -M 400 -m 10 -O -o {}'.format(fq1, fq2, output_path))
        return

    except Exception as err:
        log_txt.insert(CURRENT, '[-ERROR-] during FLAShing \n' + str(err) + '\n')


def rename_FASTQ(o_path):
    global log_txt
    try:
        os.remove(o_path + '.fastq')
    except Exception as err:
        log_txt.insert(CURRENT, '[-ERROR-] os.remove(' + o_path + '.fastq)\n' + str(err) + '\n')
    os.rename(o_path + '.extendedFrags.fastq', o_path + '.fastq')


def move_useless(output):
    global log_txt
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
            shutil.move(i, CO_PRODUCT_FILES)
        return
    except Exception as err:
        log_txt.insert(CURRENT, '[-ERROR-] during moving files to /co_product_files \n' + str(err) + '\n')


def move_FASTQ(output):
    global log_txt
    try:
        shutil.move('{}.fastq'.format(output), FLASH_RESULT)
        return
    except Exception as err:
        log_txt.insert(CURRENT, '[-ERROR-] during moving FASTQ\n' + str(err) + '\n')


def run_flash(fq1, fq2, output_path):
    global log_txt
    log_txt.insert(CURRENT, 'make dir\n')
    make_dir()
    excute_flash(fq1, fq2, output_path)
    log_txt.insert(CURRENT, 'move files\n')
    rename_FASTQ(output_path)
    move_useless(output_path)
    move_FASTQ(output_path)
    log_txt.insert(CURRENT, '\nthe FLASh is DONE\n')
    return


def clear_res_text(res_txt):
    if res_txt.get('1.0', END) != '':
        res_txt.delete('1.0', END)


def click_flash():
    global FILE_INPUT_LABEL
    global FILE_LIST
    global log_txt

    clear_res_text(log_txt)
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
            log_txt.insert(CURRENT, 'start FLASh\n\t' + output_path + '\n')
            run_flash(tmp[::-1][0], tmp[::-1][1], output_path.split('/')[-1])


def add_upload_file():
    global FILE_INPUT_LABEL
    global WIN

    _, n_row = FILE_INPUT_LABEL.grid_size()
    default_cpu, cpu_list = get_opt_list(MULTI_CNT, TOTAL_CPU)

    if cpu_list[-1] < n_row + 1:
        messagebox.showerror('warning', 'too many CPU')
        return
    elif default_cpu <= n_row + 1:
        if not messagebox.askyesno('alert', 'Recommend ' + str(
                default_cpu) + ' CPU.\nYour computer could get slow\n, if you use too many CPU.\nDo you want to use more CPU?'):
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
    global log_txt

    WIN = Tk()
    WIN.title('FLASh for GUI')

    notebk = ttk.Notebook(WIN)
    notebk.pack()

    frame1 = Frame(WIN)
    notebk.add(frame1, text='FLASh')

    spec_label = Label(frame1)
    spec_label.grid(row=0, columnspan=3, padx=3, pady=3)

    # st notice
    recmd_cpu = ' [ + strand ] | [ - strand ] '
    cpu_label = Label(spec_label, text=recmd_cpu, font='Courier 20 bold', relief=RAISED)
    cpu_label.grid(row=0, column=0, padx=5, pady=3)
    # en notice

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
    log_txt = Text(frame1, font='Terminal 10', relief=RAISED, width=100, height=20)
    log_txt.grid(row=2, columnspan=1, padx=3, pady=3)

    btn_label = Label(frame1, relief=FLAT)
    btn_label.grid(row=2, column=2, padx=3, pady=3)
    reset_btn = Button(btn_label, text='reset', font='Courier 10 bold', fg='red', command=reset, width=10)
    reset_btn.grid(row=0, column=2, padx=3, pady=5)
    flash_btn = Button(btn_label, text='run\nFLASh', font='Courier 15 bold', fg='dark blue', command=click_flash,
                       width=10, height=8)
    flash_btn.grid(row=1, column=2, padx=3, pady=5)

    frame2 = Frame(WIN)
    notebk.add(frame2, text='about')
    about = """

THIS APP WAS MADE WITH FLASh FROM The Center for Computational Biology at Johns Hopkins University.
IT IS A FREE APP LIKE FLASh.
YOU CAN DOWNLOAD AND EDIT THE ORIGINAL 
BY FOLLOWING THE LINK BELOW.
WE ARE NOT RESPONSIBLE FOR ANY DAMAGE AFTER DOWNLOAD AND USE.
_________________________________________________
https://github.com/astroboi-SH-KWON/the_flash_GUI
_________________________________________________

이 app은 존 홉킨스 대학 CCB의 FLASh를 사용하였습니다.
FLASh처럼 이 app은 완전 무료 제품입니다.
github에 원래 소스를 받아서 수정하셔도 됩니다.
우리는 이 app에 의해 생기는 
사용자의 어떠한 손해도 책임지지 않습니다.

        """
    about_label = Label(frame2, font='Terminal 15', text=about, relief=FLAT, width=95, height=15)
    about_label.grid(row=1, columnspan=2, padx=5, pady=5)


if __name__ == '__main__':
    setupGUI()
    WIN.mainloop()
