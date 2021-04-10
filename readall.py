import os
def fast_scandir_folder(dirname):
    subfolders= [f.path for f in os.scandir(dirname) if f.is_dir()]
    im_folder = []
    im_folder.append(subfolders)
    return im_folder

path = "assets/Base_de_Datos/"
filelist_baby = fast_scandir_folder(path)

patient_identification = [];
patient_dictionary = {}
for i in range(len(filelist_baby[0])):
    id = filelist_baby[0][i][21:]
    patient_identification.append(id)
    patient_dictionary[id] = i

babies_identification_default = patient_identification[0]


def dictionary_function(vector):
    vector_dictionary = {}
    for i in range(len(vector)):
        id = vector[i]
        vector_dictionary[id] = i
    return vector_dictionary

techniques = ["ADC", "3DT2", "Perfusion"]
techniques_default = techniques[0]

techniques_dictionary = dictionary_function(techniques)


def definition_filelist(patient_identification, techniques, filelist):
    file_list_all = []
    filelist_cont = []
    for i in patient_identification:
      file_list_patient = []
      for ii in techniques:
        file_list_week = []
        for d in range(len(filelist)):
            if filelist[0][2]
        file_list_week.append(path+i+"/"+ii+"/"+"")
        filelist_cont.append(path+i+"/"+ii+"/"+"")

        file_list_patient.append(file_list_week)
      file_list_all.append(file_list_patient)

    return file_list_all, filelist_cont

filelist, filelist_cont = definition_filelist(patient_identification, techniques)