import API
import ReadData
from openpyxl import load_workbook
from openpyxl import Workbook
import tkinter as tk
from tkinter import filedialog
import Features
import utils
import TokenAndCats



token_and_cats = TokenAndCats.TokenAndCats()

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
    #root.destroy()

def execute_system():
    choice = system_choice.get()
    if choice == 1:
        create_one_system()
    elif choice == 2:
        create_two_systems_with_one_company()
    elif choice == 3:
        create_attendance_system()
    root.destroy()

###########################################
def create_system(two_systems_boolean):
 if two_systems_boolean == False: 
     API.create_company()
     print("Company created")
 API.create_app()
 print("App created")
 token_and_cats.get_cats(API.app_id)
 API.create_roles(ReadData.roles,API.app_id)
 print("Roles created")
 API.create_shifts(ReadData.shifts,API.app_id)
 print("Shifts created")
 API.create_requests_limits(ReadData.requests_limits,API.app_id)
 print("requests_limits created")
 API.create_recives_limits(ReadData.receives_limits,API.app_id)
 print("recives_limits created")
 API.create_clock(API.app_id)
 print("Clock created")
 API.create_features(ReadData.features,API.app_id)
 if len(ReadData.cutting_hours) != 0: #Specific for cutting hours
   Features.create_cutting_hours_feature(API.app_id,ReadData.cutting_hours) 
 print("Features created")
 if ReadData.shabat is not None and len(ReadData.shabat) != 0:
      API.create_shabat(API.app_id)

 if ReadData.holidays == "כן":
      ReadData.holidays_area = utils.choose_holiday_area_code(ReadData.holidays_area)
      API.create_automatic_holiday(API.app_id)

 if ReadData.automatic_holidays_special_cost == "כן":
      API.create_report_attribute(API.app_id)
      Features.create_special_holiday(API.app_id)
      if ReadData.language != "he":
          API.create_report_coulmn(API.app_id,["1","2"],'special_holiday_100',"Speciel 200%")
      else:          
          API.create_report_coulmn(API.app_id,["1","2"],'special_holiday_100',"מיוחד 200%")

 API.create_employee_configurations(ReadData.employee_configurations,API.app_id)
 print("Employee configurations created")

 API.create_employees(ReadData.owner_details,API.app_id)
 print("Owners created")

 print("\n\n System created successfully\n\n")

def create_attendance_system():
 ReadData.read_all_data(sheet1)
 API.create_company()
 API.create_attendance_app()
 headers=TokenAndCats.TokenAndCats().get_cats(API.app_id)
 API.create_roles(ReadData.roles,API.app_id)
 unplanned_shift_flag=True
 API.create_unplanned_shift(API.app_id,unplanned_shift_flag)
 API.create_clock(API.app_id)
 if ReadData.shabat is not None and len(ReadData.shabat) != 0:
      API.create_shabat(API.app_id)

 if ReadData.automatic_holidays_special_cost == "כן":
      API.create_report_attribute(API.app_id)#Spacial holiday regular hours rate
      Features.create_special_holiday(API.app_id)
      if ReadData.language != "he":
          API.create_report_coulmn(API.app_id,["1","2"],'special_holiday_100',"Speciel 200%")
      else:          
          API.create_report_coulmn(API.app_id,["1","2"],'special_holiday_100',"מיוחד 200%")

 if ReadData.holidays == "כן":
      ReadData.holidays_area = utils.choose_holiday_area_code(ReadData.holidays_area)
      API.create_automatic_holiday(API.app_id)
 
 for i in range(len(ReadData.features)):
  API.create_features(i,API.app_id)
 if len(ReadData.cutting_hours) != 0:
   Features.create_cutting_hours_feature(API.app_id,ReadData.cutting_hours)
   
 Features.delete_auto_populate_rota(API.app_id)

 for i in range(len(ReadData.employee_configurations)):
     API.create_employee_configuration(i,API.app_id,ReadData.employee_configurations[i])

 for i in range(len(ReadData.owner_details)):
      API.create_employee(i,ReadData.owner_details,API.app_id)

 print("\n\n System created successfully\n\n")

def create_one_system():
 ReadData.read_all_data(sheet1)
 create_system(False)

def create_two_systems_with_one_company():
  ReadData.read_all_data(sheet1)
  create_system(False) 
  ReadData.read_all_data(sheet2)  
  create_system(True) 

##############################################
##############  GUI ###########################
##############################################
root = tk.Tk()
root.title("FQ system")
root.geometry("400x300")
load_button = tk.Button(root, text="Load Excel File", command=load_and_convert_excel_to_values_only)
load_button.pack(pady=60)

system_choice = tk.IntVar()
system_choice.set(1) 

tk.Radiobutton(root, text="Create one system", variable=system_choice, value=1).pack(anchor="w", padx=20)
tk.Radiobutton(root, text="Create two systems with one company", variable=system_choice, value=2).pack(anchor="w", padx=20)
tk.Radiobutton(root, text="Create attendance system", variable=system_choice, value=3).pack(anchor="w", padx=20)

execute_button = tk.Button(root, text="Execute", command=execute_system, width=20, height=2, font=("Helvetica", 14))
execute_button.pack(pady=20)

root.mainloop()

###################################
###################################

#For Motti
# Support gruop in  organize_groups() 
