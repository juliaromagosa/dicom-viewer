import os
import pydicom
import numpy as np
import collections


def fast_scandir_folder(dirname):
    subfolders = [f.path for f in os.scandir(dirname) if f.is_dir()]
    im_folder = []
    im_folder.append(subfolders)
    return im_folder

path = 'assets/Base_de_Datos/'
############ Create a list of all the files ###############
filelist_patient = fast_scandir_folder(path)
patient_identification = [];
patient_dictionary = {}
for i in range(len(filelist_patient[0])):
    id = filelist_patient[0][i][21:]
    patient_identification.append(id)
    patient_dictionary[id] = i

patient_identification_default = patient_identification[0]
# PARTE READER
# Create files_3DT2,  files_ADC, files_Perfusion, list of the name of the images inside the folder
filelist_3DT2 = []
filelist_ADC = []
filelist_Perfusion = []

c=0
filelist=[]
for root, dirs, files in os.walk(path):
    for p in range(len(patient_identification)):
        list=[]
        for d in dirs:
            if "3DT2" in d:
                list2=[]
                filelist.append(os.path.join(root,d))
            if "ADC" in d:
                list3=[]
                filelist.append(os.path.join(root, d))
            if "Perfusion" in d:
                list4=[]
                filelist.append(os.path.join(root, d))


    list.append(list2,list3,list4)




filelist=[]
n=[1,2,3,4,5]
for root, dirs, files in os.walk(path):
    for d in n:
        list=[]
        for d in n:
            list2=[]
            for file in files:
                if ".DS_Store" not in file:
                    list2.append(os.path.join(root, file))
                list.append(list2)
            filelist.append(list2)




list_patients = []
for root, dirs, files in os.walk(path):
        for d in dirs:
            if "Patient" in d:
                list_patients.append(os.path.join(root,d))


list8=[]
for i in list_patients:
    list7 = []
    for root, dirs, files in os.walk(i):
        for d in dirs:

            list7.append(os.path.join(root,d))
        list8.append(list7)



filelist_sorted=filelist.sort()

def classificar(filelist_sorted):
    for i in range(len(filelist_sorted)):
        if '3DT2' in filelist_sorted[i]:
            filelist_3DT2.append(filelist_sorted[i])
        if 'ADC' in filelist_sorted[i]:
            filelist_ADC.append(filelist_sorted[i])
        if 'Perfusion' in filelist_sorted[i]:
            filelist_Perfusion.append(filelist_sorted[i])
    return filelist_3DT2, filelist_Perfusion, filelist_ADC


filelist_3DT2, filelist_Perfusion, filelist_ADC = classificar(filelist)

"""
def definition_filelist(babies_identification, weeks, planes):
    file_list_all = []
    filelist_cont = []
    for i in babies_identification:
      file_list_baby = []
      for ii in weeks:
        file_list_week = []
        for iii in planes:
          file_list_week.append(path+i+"/"+i+"_"+ii+"EG_SELECCION ESTANDAR/"+i+"_"+iii+"_M_CUT.bmp")
          filelist_cont.append(path+i+"/"+i+"_"+ii+"EG_SELECCION ESTANDAR/"+i+"_"+iii+"_M_CUT.bmp")

        file_list_baby.append(file_list_week)
      file_list_all.append(file_list_baby)

    return (file_list_all, filelist_cont)
    """


my_dict={}
for file in filelist_Perfusion:
    key = pydicom.dcmread(file).AcquisitionNumber
    my_dict.setdefault(key,[])
    my_dict[key].append(file)

filelist=[]
DEFAULT_IMAGE_PATH='assets/Base_de_Datos/Patient 870/'
for (dirpath, dirnames, filenames) in os.walk(os.path.join(os.getcwd(), DEFAULT_IMAGE_PATH), topdown=False):
    for name in filenames:
        if ".DS_Store" not in name:
            filelist.append(os.path.join( dirpath,name))
            filelist.sort()