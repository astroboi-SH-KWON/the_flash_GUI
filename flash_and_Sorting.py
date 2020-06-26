import os
import shutil


class clsFLASH:
    def __init__ (self,file_number,output):
        self.file_No = file_number
        self.output  = output





    def Make_Dir(self):

        if not (os.path.isdir('FASTQ_File')):
            os.mkdir('FASTQ_File')
        else:
            pass

        if not (os.path.isdir('co_product_files')):
            os.mkdir('co_product_files')
        else:
            pass
        return





## flash 1_S1_L001_R1_001.fastq.gz 1_S1_L001_R2_001.fastq.gz -M 400 -m 10 -O -o 18
    def execute (self):
        os.system('flash {}_S{}_L001_R1_001.fastq.gz {}_S{}_L001_R2_001.fastq.gz -M 400 -m 10 -O -o {}'.
                  format(self.file_No,self.file_No,self.file_No, self.file_No, self.output))

        return

    def Rename_FASTQ(self):
        os.rename('{}.extendedFrags.fastq'.format(self.output),'{}.fastq'.format(self.output))

        return

    def Move_useless(self):

        file1 = '{}.hist'.format(self.output)
        file2 = '{}.hist.innie'.format(self.output)
        file3 = '{}.hist.outie'.format(self.output)
        file4 = '{}.histogram'.format(self.output)
        file5 = '{}.histogram.innie'.format(self.output)
        file6 = '{}.histogram.outie'.format(self.output)
        file7 = '{}.notCombined_1.fastq'.format(self.output)
        file8 = '{}.notCombined_2.fastq'.format(self.output)
        file_list = [file1,file2,file3,file4,file5,file6,file7,file8]


        for i in file_list:
            shutil.move(i,'co_product_files')
        return


    def Move_FASTQ(self):
        shutil.move('{}.fastq'.format(self.output), 'FASTQ_File')
        return






def flash(a,b):
    a = clsFLASH(a,b)
    a.Make_Dir()
    a.execute()
    a.Rename_FASTQ()
    a.Move_useless()
    a.Move_FASTQ()

    return



def main():
    print('Input Index_Number(ex. 33) and press Enter Key')
    print('If you input every index number, Input "done" then press Enter key')
    b = []
    while True:
        a = input('Index_Number: ')
        if a == 'done':
            break
        else:
            b.append(a)


    for i in b:
        flash(i,i)

    return

if __name__ == '__main__':
    main()


