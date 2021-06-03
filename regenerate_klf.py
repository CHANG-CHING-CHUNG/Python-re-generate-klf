import os
from db_class import db
from dotenv import load_dotenv

load_dotenv()
lines = []
input_klf_backup_path = os.getenv("INPUT_KLF_BACKUP")

with open(f"{input_klf_backup_path}48430$$48533$$J0H989-CP-01.txt") as file_in:
    for line in file_in:
        lines.append(line.rstrip().split(" "))
        
    rough_bin_number_index = None
    for n in range(len(lines)):
      if "DefectRecordSpec" in lines[n]:
        print(lines[n])
        rough_bin_number_index = lines[n].index("ROUGHBINNUMBER")
      if "TiffFileName" in lines[n]:
        print(lines[n])
      if "DefectList" in lines[n]:
        lines[n+1][rough_bin_number_index]="106"
        print(lines[n+1])

# print(lines[-8])
# print(lines[-7])
# print(lines[-6])