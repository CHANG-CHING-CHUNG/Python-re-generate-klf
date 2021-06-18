import os
from os import walk
from db_class import db
import re
import json
from dotenv import load_dotenv
from datetime import datetime, timezone
load_dotenv()



class RegenerateKlf:
  __lines = []
  __input_klf_backup_path = os.getenv("INPUT_KLF_BACKUP")
  __directory_path = os.getenv("DIRECTORY_PATH")
  __insert_query_list = []
  def re_generate_klf(self,subfolder_name,klf_file_name,c_line_type):
    with open(f"{self.__input_klf_backup_path}{subfolder_name}/{klf_file_name}") as file_in:
        insert_query = [None] * 8
        for line in file_in:
            self.__lines.append(line.rstrip().split(" "))
        dt = datetime.now(tz=timezone.utc)
        dt = dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        print(dt)
        insert_query[7] = dt
        insert_query[1] = c_line_type
        insert_query[2] = True
        InspectionStationID = None
        LotID = None
        WaferID = None
        for n in range(len(self.__lines)):
          
          # print(self.__lines[n])
          if "InspectionStationID" in self.__lines[n]:
            # print(self.__lines[n])
            InspectionStationID = self.__lines[n][3].replace('"',"").replace(";","")
            insert_query[3] = InspectionStationID
          if "LotID" in self.__lines[n]:
            LotID = self.__lines[n][1].replace('"',"").replace(";","")
            insert_query[4] = LotID
          if "WaferID" in self.__lines[n]:
            WaferID = self.__lines[n][1].replace('"',"").replace(";","")
            insert_query[5] = WaferID
          if "TiffFileName" in self.__lines[n]:
            insert_query[6] = self.__lines[n][1].replace('"',"").replace(";","")
            if "DefectList" in self.__lines[n+1]:
              insert_query[0] = self.__lines[n+2][12]
            if "DefectList" in self.__lines[n+2]:
              insert_query[0] = self.__lines[n+3][12]
            if "DefectList" in self.__lines[n+3]:
              insert_query[0] = self.__lines[n+4][12]

          if any(x is None for x in insert_query) == False:
            # print(insert_query)
            self.__insert_query_list.append(insert_query)
            insert_query = [None] * 8
            insert_query[7] = dt
            insert_query[1] = c_line_type
            insert_query[2] = True
            insert_query[3] = InspectionStationID
            insert_query[4] = LotID
            insert_query[5] = WaferID
        
        for insert_query_var in self.__insert_query_list:
          self.insert_data_to_c_img_data(insert_query_var)
        
        klf_id = self.insert_data_to_klf_info(klf_file_name,LotID)

        for insert_query_var in self.__insert_query_list:
          self.insert_data_to_wafer_info(klf_id,insert_query_var[5])
  def insert_data_to_c_img_data(self,insert_query_var):
    insert_query = """insert into classification_c_img_data 
                (c_type_ai2, c_line_type, c_ai2_right,c_inspection_tool, lot_id, wafer_id,img_path, upload_time)
                values ( %s,%s,%s,%s,%s, %s, %s, %s);"""
    query_var = tuple(insert_query_var)
    result = db.execute_query(insert_query, query_var)

  def insert_data_to_klf_info(self,filename,lot_id):
    insert_query = """insert into classification_klf_info (filename, lot_id) values(%s, %s) RETURNING id;"""
    filename = filename.split("$$")[2]
    query_var = (filename,lot_id,)
    # print(filename)
    db.execute_query(insert_query, query_var)
    id_of_new_row = db.fetchone()[0]
    return id_of_new_row

  def insert_data_to_wafer_info(self,klf_id,wafer_id):
    insert_query = """insert into classification_wafer_info (klf_id, wafer_id) values(%s,%s)"""
    query_var = (klf_id,wafer_id,)
    db.execute_query(insert_query, query_var)

  def get_all_filenames(self, subfolder_name):
    filenames_list = []
    result_filenames = []
    for (dirpath, dirnames, filenames) in walk(self.__directory_path + subfolder_name + "/"):
      result_filenames = filenames
    for filename in result_filenames:
        filenames_list.append(filename)
      
    return filenames_list

r = RegenerateKlf()
# filenames_list = r.get_all_filenames('t1')
# for filename in filenames_list:
#   # print(filename)
#   r.re_generate_klf('t1',filename,"t1")

filenames_list = r.get_all_filenames('b2')
for filename in filenames_list:
  # print(filename)
  r.re_generate_klf('b2',filename,"b2")

# filenames_list = r.get_all_filenames('c3')
# for filename in filenames_list:
#   # print(filename)
#   r.re_generate_klf('c3',filename,"c3")