import API
import ReadData
from openpyxl import load_workbook
from openpyxl import Workbook
import tkinter as tk
from tkinter import filedialog
import Features
import utils
############################################# 
def load_and_convert_excel_to_values_only():
    global sheet1 
    global sheet2

    file_path = filedialog.askopenfilename(
    title="Select an Excel file",
    filetypes=[("Excel files", "*.xlsx;*.xls")]
    )

    if file_path:
        wb = load_workbook(file_path, data_only=True) #Open the excel and copies the values (not formulas)
        new_wb = Workbook() # Create new Workbook 

    for idx, sheet_name in enumerate(wb.sheetnames):
            original_ws = wb[sheet_name]
            if idx == 0:
                new_ws = new_wb.active
            else:
                new_ws = new_wb.create_sheet(title=sheet_name)
            
            new_ws.title = sheet_name

            for row in original_ws.iter_rows(values_only=True): # Add as values only
                new_ws.append(row)

    sheet1 = new_wb.worksheets[0]
    sheet2 = new_wb.worksheets[1]
    root.destroy()

def create_system(two_systems_boolean):
 API.get_token()
 global headers
 headers = {"Authorization": f"Token {API.token}"}
 if two_systems_boolean == False: 
     API.create_company(headers)
 API.create_app(headers)
 Cats = Features.get_cats(635)
 headers = {"Authorization": f"Token {API.token}", "Cats": Cats}

 for i in range(len(ReadData.roles)):
  API.create_role(i,ReadData.roles,API.app_id,headers)
 if len(API.LIST_OF_ROLES) == len(ReadData.roles):
      print("\n All roles were created successfully \n")
 
 counter_of_shifts=0
 for i in range(len(ReadData.shifts)):
  counter_of_shifts += API.create_shifts(i,ReadData.shifts,API.app_id,headers)
  if counter_of_shifts == len(ReadData.shifts):
       print("\n All shifts were created successfully \n")

 counter_of_requests_limits=0     
 for i in range(len(ReadData.requests_limits)):
  counter_of_requests_limits+=API.create_request_limits(i,API.app_id,headers)
  if counter_of_requests_limits == len(ReadData.requests_limits):
       print("\n All requests limits were created successfully \n") 

 counter_of_recive_limits=0 
 for i in range(len(ReadData.receives_limits)):
  API.create_recive_limits(i,API.app_id,headers)
  if counter_of_recive_limits == len(ReadData.receives_limits):
       print("\n All recive limits were created successfully \n") 

 API.create_clock(API.app_id,headers)

 for i in range(len(ReadData.features)):
  API.create_features(i,API.app_id,headers)

 if len(ReadData.cutting_hours) != 0: #Specific for cutting hours
   Features.create_cutting_hours_feature(API.app_id,ReadData.cutting_hours) 
   API.create_report_coulmn(API.app_id,["3"],'exit_cut',None,headers)
   API.create_report_coulmn(API.app_id,["3"],'entry_cut',None,headers)

 if ReadData.shabat is not None and len(ReadData.shabat) != 0:
      API.create_shabat(API.app_id,headers)

 if ReadData.holidays == "כן":
      ReadData.holidays_area = utils.choose_holiday_area_code(ReadData.holidays_area)
      API.create_automatic_holiday(API.app_id,headers)

 if ReadData.automatic_holidays_special_cost == "כן":
      API.create_report_attribute(API.app_id,headers)
      Features.create_special_holiday(API.app_id)
      if ReadData.language != "he":
          API.create_report_coulmn(API.app_id,["1","2"],'special_holiday_100',"Speciel 200%",headers)
      else:          
          API.create_report_coulmn(API.app_id,["1","2"],'special_holiday_100',"מיוחד 200%",headers)

 for i in range(len(ReadData.employee_configurations)):
     API.create_employee_configuration(i,API.app_id,ReadData.employee_configurations[i],headers)

 for i in range(len(ReadData.owner_details)):
      API.create_employee(i,headers,ReadData.owner_details,API.app_id)

 print("\n\n System created successfully\n\n")
##############################################
def attendance_system():
 ReadData.read_all_data(sheet1)
 API.get_token()
 global headers
 headers = {"Authorization": f"Token {API.token}"}
 API.create_company(headers)
 API.create_attendance_app(headers)
 Cats = Features.get_cats(API.app_id)
 headers = {"Authorization": f"Token {API.token}", "Cats": Cats}

 API.create_role(0,ReadData.roles,API.app_id,headers)

 unplanned_shift_flag=True
 API.create_unplanned_shift(API.app_id,unplanned_shift_flag,headers)

 API.create_clock(API.app_id,headers)

 if ReadData.shabat is not None and len(ReadData.shabat) != 0:
      API.create_shabat(API.app_id,headers)

 if ReadData.automatic_holidays_special_cost == "כן":
      API.create_report_attribute(API.app_id,headers)#Spacial holiday regular hours rate
      Features.create_special_holiday(API.app_id)
      if ReadData.language != "he":
          API.create_report_coulmn(API.app_id,["1","2"],'special_holiday_100',"Speciel 200%",headers)
      else:          
          API.create_report_coulmn(API.app_id,["1","2"],'special_holiday_100',"מיוחד 200%",headers)

 if ReadData.holidays == "כן":
      ReadData.holidays_area = utils.choose_holiday_area_code(ReadData.holidays_area)
      API.create_automatic_holiday(API.app_id,headers)
 
 for i in range(len(ReadData.features)):
  API.create_features(i,API.app_id,headers)
 if len(ReadData.cutting_hours) != 0:
   Features.create_cutting_hours_feature(API.app_id,ReadData.cutting_hours)
   
 Features.delete_auto_populate_rota(API.app_id)

 for i in range(len(ReadData.employee_configurations)):
     API.create_employee_configuration(i,API.app_id,ReadData.employee_configurations[i],headers)

 for i in range(len(ReadData.owner_details)):
      API.create_employee(i,headers,ReadData.owner_details,API.app_id)

 print("\n\n System created successfully\n\n")

def one_system():
 ReadData.read_all_data(sheet1)
 create_system(False)

def two_systems_with_one_company():
  ReadData.read_all_data(sheet1)
  create_system(False) 
  ReadData.read_all_data(sheet2)  
  create_system(True) 

################################################################################
################################################################################
root = tk.Tk()
root.title("FQ system")
root.geometry("400x250")
load_button = tk.Button(root, text="Load Excel File", command=load_and_convert_excel_to_values_only)
load_button.pack(pady=50)
root.mainloop()

one_system()
#two_systems_with_one_company()
#attendance_system()


#For Motti
# Support gruop in  organize_groups() 
