import os
from os import walk
from db_class import db
import re
import json
from dotenv import load_dotenv

load_dotenv()

class RegenerateKlf:
  __lines = []
  __input_klf_backup_path = os.getenv("INPUT_KLF_BACKUP")
  __ai_to_oqa_path = os.getenv("AI_TO_OQA_PATH")

  def extract_startId_endId(self, klf_file_name):
    klf_file_name_arr = klf_file_name.split("$$")
    return [klf_file_name_arr[0],klf_file_name_arr[1]]

  def rewrite_file(self,lines,klf_file_name):
    filepath = f'{ self.__ai_to_oqa_path }{ klf_file_name.split("$$")[2] }'
    try:
      if os.path.isfile(filepath):
        os.remove(filepath)
      file_write =  open(filepath,"a")
      for line in lines:
        file_write.write(line)
        file_write.write("\n")

      file_write.close()
      lines.clear()
    except:
      print("有地方出錯了，請檢查")

  def get_all_filenames(self, directory_path, klf_filename):
    filenames_list = []
    result_filenames = []
    for (dirpath, dirnames, filenames) in walk(directory_path):
      result_filenames = filenames
    for filename in result_filenames:
      regexStr = f"^.*{klf_filename}$"
      match = re.findall(regexStr, filename)
      if match:
        filenames_list.append(filename)
      
    return filenames_list

  def get_user_confirmed_img_data(self,start_id, end_id):
    select_query = """select id, c_type_ai2, c_type_user, img_path, c_line_type from classification_c_img_data where c_type_user is not null and id between %s and %s;"""
    query_var = (start_id, end_id,)
    db.execute_query(select_query, query_var)
    all_img_data = db.fetchall()
    return  all_img_data

  def new_get_user_confirmed_img_data(self,lot_id, wafer_id, upload_time):
    select_query = """select DISTINCT ON (img_path) img_path, c_type_user from classification_c_img_data 
                      where c_type_user is not null 
                      and lot_id = %s 
                      and wafer_id  = %s
                      and upload_time = %s
                      order by img_path;"""
    query_var = (lot_id, wafer_id,upload_time)
    db.execute_query(select_query, query_var)
    all_img_data = db.fetchall()
    return  all_img_data

  def get_wafer_id(self,lot_id, upload_time):
    select_query = """select wafer_id from classification_c_img_data 
                      where lot_id = %s 
                      and c_type_user is not null 
                      and upload_time = %s 
                      group by wafer_id;"""
    query_var = (lot_id,upload_time)
    db.execute_query(select_query, query_var)
    wafer_id_list = db.fetchall()
    return  wafer_id_list

  def get_subfolder_name(self,lot_id,wafer_id, upload_time):
    select_query = """select c_line_type from classification_c_img_data 
                      where lot_id = %s 
                      and wafer_id = %s 
                      and c_type_user is not null 
                      and upload_time = %s 
                      group by c_line_type;"""
    query_var = (lot_id,wafer_id, upload_time)
    db.execute_query(select_query, query_var)
    subfolder_name = db.fetchall()
    return  subfolder_name

  def get_klf_filename(self, lot_id, wafer_id):
    select_query = """select filename from classification_klf_info as k
                      left join classification_wafer_info as w 
                      on k.id = w.klf_id
                      where k.lot_id = %s 
                      and w.wafer_id = %s
                      group by filename;"""
    query_var = (lot_id,wafer_id)
    db.execute_query(select_query, query_var)
    klf_filename = db.fetchall()
    return klf_filename

  def re_generate_klf(self,subfolder_name,klf_file_name,img_data_list):
    with open(f"{self.__input_klf_backup_path}{subfolder_name}/{klf_file_name}") as file_in:
        for line in file_in:
            self.__lines.append(line.rstrip().split(" "))  
        rough_bin_number_index = None
        for n in range(len(self.__lines)):
          if "TiffFileName" in self.__lines[n]:
            for img_data in img_data_list:
              img_path = img_data[0].replace(".jpeg",".jpg;")
              c_type_user = img_data[1]

              if img_path in self.__lines[n]:
                if "DefectRecordSpec" in self.__lines[n+1]:
                  rough_bin_number_index = self.__lines[n+1].index("ROUGHBINNUMBER")
                if "DefectList" in self.__lines[n+1]:
                  self.__lines[n+2][rough_bin_number_index]=c_type_user
                if "DefectList" in self.__lines[n+2]:
                  self.__lines[n+3][rough_bin_number_index]=c_type_user
                if "DefectList" in self.__lines[n+3]:
                  self.__lines[n+4][rough_bin_number_index]=c_type_user
          if "SummarySpec" in self.__lines[n]:
            self.__lines[n][-1] = self.__lines[n][-1] + " "
          self.__lines[n] = " ".join(self.__lines[n])
    self.rewrite_file(self.__lines,klf_file_name)

  def new_re_generate_klf(self, lot_id, upload_time):
    try:
      wafer_id_list = self.get_wafer_id(lot_id, upload_time)
      for wafer_id in wafer_id_list:
        subfolder_name_list = self.get_subfolder_name(lot_id, wafer_id,upload_time)
        for subfolder_name in subfolder_name_list:
          subfolder_name = subfolder_name[0]
          klf_file_name = self.get_klf_filename(lot_id,wafer_id)[0][0]
          all_img_data = self.new_get_user_confirmed_img_data(lot_id, wafer_id, upload_time)
          directory_path = self.__input_klf_backup_path + subfolder_name + "/"
          filename_list = self.get_all_filenames(directory_path,klf_file_name)
          for filename in filename_list:
            self.re_generate_klf(subfolder_name,filename,all_img_data)
      return json.dumps({'action':'rewrite_klf', 'status':'success'})
    except:
      return json.dumps({'action':'rewrite_klf', 'status':'failed'})

lot_id = 'J0H989-CP'
upload_time = '2020-08-04 19:03:19+08'
re_generate_klf = RegenerateKlf()
print(re_generate_klf.new_re_generate_klf(lot_id,upload_time))