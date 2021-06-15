import os
from db_class import db
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
    if os.path.isfile(filepath):
      os.remove(filepath)
    file_write =  open(filepath,"a")
    for line in lines:
      file_write.write(line)
      file_write.write("\n")

    file_write.close()
    lines.clear()


  def get_user_confirmed_img_data(self,start_id, end_id):
    select_query = "select id, c_type_ai2, c_type_user, img_path, c_line_type from classification_c_img_data where c_type_user is not null and id between %s and %s;"
    query_var = (start_id, end_id,)
    db.execute_query(select_query, query_var)
    all_img_data = db.fetchall()
    return  all_img_data

  def re_generate_klf(self,klf_file_name):
    klf_file_name_arr = re_generate_klf.extract_startId_endId(klf_file_name)
    [star_id, end_id] = klf_file_name_arr
    img_data_list = self.get_user_confirmed_img_data(star_id,end_id)
    c_line_type  = img_data_list[0][4] + "/"

    with open(f"{self.__input_klf_backup_path}{c_line_type}{klf_file_name}") as file_in:
        for line in file_in:
            self.__lines.append(line.rstrip().split(" "))  
        rough_bin_number_index = None
        for n in range(len(self.__lines)):
          if "TiffFileName" in self.__lines[n]:
            for img_data in img_data_list:
              img_id = img_data[0]
              c_type_ai2 = img_data[1]
              c_type_user = img_data[2]
              img_path = img_data[3].replace(".jpeg",".jpg;")
              if img_path in self.__lines[n]:
                if "DefectRecordSpec" in self.__lines[n+1]:
                  rough_bin_number_index = self.__lines[n+1].index("ROUGHBINNUMBER")
                if "DefectList" in self.__lines[n+1]:
                  self.__lines[n+2][rough_bin_number_index]=c_type_user
                if "DefectList" in self.__lines[n+2]:
                  self.__lines[n+3][rough_bin_number_index]=c_type_user
                if "DefectList" in self.__lines[n+3]:
                  self.__lines[n+4][rough_bin_number_index]=c_type_user
          self.__lines[n] = " ".join(self.__lines[n])
    self.rewrite_file(self.__lines,klf_file_name)

klf_file_name = "48430$$48533$$J0H989-CP-01.txt"
re_generate_klf = RegenerateKlf()
re_generate_klf.re_generate_klf(klf_file_name)