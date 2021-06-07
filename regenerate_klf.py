import os
from db_class import db
from dotenv import load_dotenv

load_dotenv()
lines = []
input_klf_backup_path = os.getenv("INPUT_KLF_BACKUP")
klf_file_name = "48430$$48533$$J0H989-CP-01.txt"

class RegenerateKlf:
  

  def get_user_confirmed_img_data(self,start_id, end_id):
    select_query = "select id, c_type_ai2, c_type_user, img_path, c_line_type from classification_c_img_data where c_type_user != c_type_ai2 and id between %s and %s;"
    query_var = (start_id, end_id,)
    db.execute_query(select_query, query_var)
    all_img_data = db.fetchall()
    # print(all_img_data)

    return  all_img_data

  def re_generate_klf(self,input_klf_backup_path,klf_file_name):
    img_data_list = self.get_user_confirmed_img_data("48430","48533")
    c_line_type  = img_data_list[0][4] + "/"
    with open(f"{input_klf_backup_path}{c_line_type}{klf_file_name}") as file_in:
        for line in file_in:
            lines.append(line.rstrip().split(" "))
            
        rough_bin_number_index = None
        for n in range(len(lines)):
          if "TiffFileName" in lines[n]:
            for img_data in img_data_list:
              img_id = img_data[0]
              c_type_ai2 = img_data[1]
              c_type_user = img_data[2]
              img_path = img_data[3].replace(".jpeg",".jpg;")
              if img_path in lines[n]:
                if "DefectRecordSpec" in lines[n+1]:
                  rough_bin_number_index = lines[n+1].index("ROUGHBINNUMBER")
                if "DefectList" in lines[n+1]:
                  lines[n+2][rough_bin_number_index]=c_type_user
                if "DefectList" in lines[n+2]:
                  lines[n+3][rough_bin_number_index]=c_type_user
                if "DefectList" in lines[n+3]:
                  lines[n+4][rough_bin_number_index]=c_type_user
          lines[n] = " ".join(lines[n])

    file_write =  open(klf_file_name.split("$$")[2],"a")

    for line in lines:
      file_write.write(line)
      file_write.write("\n")

    file_write.close()

re_generate_klf = RegenerateKlf()
re_generate_klf.re_generate_klf(input_klf_backup_path, klf_file_name)