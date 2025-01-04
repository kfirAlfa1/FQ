
import requests
import ReadData
import json
import Features
import WorldTimeZones
from deep_translator import GoogleTranslator
from openpyxl import load_workbook
from openpyxl import Workbook
import tkinter as tk
from tkinter import filedialog





env_url= "https://k8-shift.tabit-dev.com"


# https://k8-shift.tabit-dev.com
# https://k8-shift.tabit-dev.com/admin
# https://k8-shift.tabit-dev.com/app/system-settings




# https://il-shift.tabit-int.com
# https://il-shift.tabit-int.com/admin




# https://il-shift.tabit-stage.com/admin
#https://il-shift.tabit-stage.com


days_of_the_week = ["ראשון", "שני", "שלישי", "רביעי", "חמישי", "שישי", "שבת"]
LIST_OF_ROLES=[]

########################################################################

def get_token():
      global  token
      tok_url = env_url+"/api/auth/token/"
      tok_data = {"username": "kfira", "password": "159753ASDF", "company": 1}
      response = requests.post(tok_url, json=tok_data)
      if response.status_code != 200:
            print(f"get_token returned error: {response.status_code}")
            print(f"Response: {response.text}")
      else:
          token= response.json().get("token")

def get_company(app_id):
    get_appliaction_request= get_app(app_id)
    company=get_appliaction_request['company']
    company_id=company.get("id")
    return company_id

def create_company():
 global company_id
 create_company_url= env_url+"/api/companies/"
 data= {
    "name":ReadData.company_name
 }
 create_company_request = requests.post(create_company_url, json=data, headers=headers)
 if create_company_request.status_code == 201:
    response_data = create_company_request.json()
    company_id = response_data.get('id')
 else:
     print("Error:create_compeny_request getting ", create_company_request.status_code)

def choose_language():
 if ReadData.language == 'עברית':
       ReadData.language='he'
 elif ReadData.language == 'אנגלית':
        ReadData.language='en'
 elif ReadData.language == 'אנגלית (ISR)':
       ReadData.language='en-il'
 elif ReadData.language == 'אנגלית (USA)':
            ReadData.language='en-us'
 elif ReadData.language == 'אנגלית (UK)':
            ReadData.language='en-gb'
 elif ReadData.language == 'אנגלית (Tabit US)':
           ReadData.language='en-tabit'
 return ReadData.language
      
def return_perrmisions_default (group):
     if ReadData.default_perrmision == group:
          return True
     else:
        return False

def return_perrmisions_id (group):
      if group=='Headquarters':
            return 10
      elif group=='Owners':
            return 7
      elif group=='Managers':
            return 2
      elif group=='Junior-Managers':
            return 9
      elif group=='Senior Sub-Managers':
            return 8
      elif group=='Sub-Managers':
            return 3
      elif group=='Senior Employees':
            return 11  
      elif group=='Employees':
            return 4
      elif group=='Junior Employees':
            return 5
      elif group=='Automation':
            return 6

def change_perrmision_to_english(index):
  if ReadData.perrmisions_list[index] == 'מטה':
      ReadData.perrmisions_list[index] = 'Headquarters'
  elif ReadData.perrmisions_list[index] == 'בעלים':
                  ReadData.perrmisions_list[index] = 'Owners'
  elif ReadData.perrmisions_list[index] == 'מנהלים':
        ReadData.perrmisions_list[index] = 'Managers' 
  elif ReadData.perrmisions_list[index] == 'מנהל מתלמד':
                  ReadData.perrmisions_list[index] = 'Junior-Managers'
  elif ReadData.perrmisions_list[index] == 'מנהלי משמרת':
        ReadData.perrmisions_list[index] = 'Senior Sub-Managers'  
  elif ReadData.perrmisions_list[index] == 'סגן מנהל משמרת':
                  ReadData.perrmisions_list[index] = 'Sub-Managers'
  elif ReadData.perrmisions_list[index] == 'עובדים':
        ReadData.perrmisions_list[index] = 'Employees' 
  elif ReadData.perrmisions_list[index] == 'עובדים עם חיתוך שעון':
                  ReadData.perrmisions_list[index] = 'Junior Employees' 
     
def organize_groups():
    global groups
    groups=[]
    for i in range(len(ReadData.perrmisions_list)):
        perrmisions_id=return_perrmisions_id(ReadData.perrmisions_list[i])
        is_default=return_perrmisions_default(ReadData.perrmisions_list[i])
        if  ReadData.language != 'he':
             change_perrmision_to_english(i)

        groups.append({
             "name": ReadData.perrmisions_list_names[i],
             "group_id": perrmisions_id,
             "is_default": is_default
              })

def return_religions_default (religion):
     if ReadData.default_religion == religion:
          return True
     else:
        return False

def return_religions_id (religion):
      if religion=='Jewish':
            return 1
      elif religion =='Christian':
            return 2
      elif religion =='Muslim':
            return 3
      elif religion =='Foreign':
            return 4
      elif religion =='Foreign 2':
            return 5

def organize_religions():
    global religions
    religions=[]
    for i in range(len(ReadData.religions_list)):
        religion_id=return_religions_id(ReadData.religions_list[i])
        is_default=return_religions_default(ReadData.religions_list[i])
        if  ReadData.language != 'he':
             if ReadData.religions_list_names[i] == 'יהודי':
                  ReadData.religions_list_names[i] = 'Jewish'
             elif ReadData.religions_list_names[i] == 'נוצרי':
                  ReadData.religions_list_names[i] = 'Christian'
             elif ReadData.religions_list_names[i] == 'מוסלמי':
                  ReadData.religions_list_names[i] = 'Muslim'  
             else:
                   ReadData.religions_list_names[i] = 'Foreign'      
             
        religions.append({
             "name": ReadData.religions_list_names[i],
             "religion_id": religion_id,
             "is_default": is_default
            })

def choose_employee_configuration_field(name_of_attribute):
    if name_of_attribute == 'תעודת זהות':
        return 'id_number'
    elif name_of_attribute == 'עיר':
        return 'city'
    elif name_of_attribute == 'כתובת':
        return 'address'
    elif name_of_attribute == 'מיקוד':
        return 'zip_code'
    elif name_of_attribute == 'תאריך תחילת עבודה':
        return 'work_start_date'
    elif name_of_attribute == 'תאריך סיום עבודה':
        return 'work_termination_date'
    elif name_of_attribute == 'דת':
        return 'religion'
    elif name_of_attribute == 'מזהה שעון':
        return 'clock_id'
    elif name_of_attribute == 'מספר עובד לשכר':
        return 'number'
    elif   name_of_attribute == 'תפקיד ראשי':
         return 'primary_role'

def choose_password_security_level():
      if   "גבוהה (שליחת פרטי התחברות)" == ReadData.password_security_level or "גבוהה" in  ReadData.password_security_level:
            ReadData.password_security_level=3 
      elif ReadData.password_security_level == "נמוכה":
            ReadData.password_security_level=1
      else:
            ReadData.password_security_level=2     

def choose_country_code():
      if ReadData.country_code =='ישראל':
            ReadData.country_code="+972"
      elif "ארה" in ReadData.country_code : # ארה"ב
            ReadData.country_code="+1"
      elif ReadData.country_code =='אנגליה':
            ReadData.country_code="+44"
      else:
            ReadData.country_code="+7"   

def choose_holiday_area_code():
      if type( ReadData.holidays_area)== int:
           return
      if ReadData.holidays_area =='תל אביב':
            ReadData.holidays_area=676
      elif ReadData.holidays_area =='ירושלים':
            ReadData.holidays_area = 110
      elif ReadData.holidays_area =='חיפה':
            ReadData.holidays_area =1504
      else:
           ReadData.holidays_area =1507

def account_number():
 if ReadData.account_number == None:
      ReadData.account_number=0

def find_timezone(city_name, timezones):
    for tz in timezones:
        if city_name in tz:  
            return tz
    return None

def choose_time_zone():
      timezones = WorldTimeZones.TIME_ZONES
      hebrew_text = ReadData.time_zone
      translated = GoogleTranslator(source='auto', target='en').translate(hebrew_text)
      timezone = find_timezone(translated, timezones)
      ReadData.time_zone=timezone
    
def create_app():
 choose_language()
 choose_password_security_level()
 account_number()
 choose_country_code()
 choose_time_zone()
 first_day_of_week=days_of_the_week.index(ReadData.first_day_of_week)
 first_day_of_weekend=days_of_the_week.index(ReadData.first_day_of_weekend)
 last_day_for_subbmit_shifts=days_of_the_week.index(ReadData.last_day_for_subbmit_shifts)
 last_hour_for_subbmit_shifts=str(ReadData.last_hour_for_subbmit_shifts)
 organize_religions()
 organize_groups() 
 create_app_url=env_url+"/api/applications/"
 
 data={
    "company_id":company_id,
    "name": ReadData.app_name,
    "display_name": ReadData.display_name,
    "industry":'restaurants',
    "language":ReadData.language,
    "timezone":ReadData.time_zone,
    "country_code":ReadData.country_code,
    "groups": groups,
    "religions": religions,
    "week_first_day":first_day_of_week,
    "weekend_first_day":first_day_of_weekend,
    "deadline_day":last_day_for_subbmit_shifts,
    "deadline_hour":last_hour_for_subbmit_shifts,
    "type":ReadData.type,
    "stage":ReadData.stage,
    "plan":ReadData.plan,
    "max_employees":ReadData.max_employees,
    "password_security":ReadData.password_security_level,
    "color_palette":ReadData.color_palette,
    "usability_check":ReadData.usability_check,
    "account_number":ReadData.account_number,
    "is_active":True,
 } 

 create_app_request = requests.post(create_app_url, json=data, headers=headers)
 if create_app_request.status_code == 201:
    global app_id
    json_str = create_app_request.content.decode('utf-8')
    data = json.loads(json_str)
    app_id = data.get('id')
    print("This is app id")
    print(app_id)
 else:
     print("Error:create_compeny_request getting ", create_app_request.status_code)
     print("Error:create_compeny_request getting ", create_app_request.content)

def create_attendance_app():
 choose_language()
 choose_password_security_level()
 account_number()
 choose_country_code()
 choose_time_zone()
 first_day_of_week=days_of_the_week.index(ReadData.first_day_of_week)
 first_day_of_weekend=days_of_the_week.index(ReadData.first_day_of_weekend)
 last_day_for_subbmit_shifts=days_of_the_week.index(ReadData.last_day_for_subbmit_shifts)
 last_hour_for_subbmit_shifts=str(ReadData.last_hour_for_subbmit_shifts)
 organize_religions()
 organize_groups() 

 create_app_url=env_url+"/api/applications/"
 
 data={
    "company_id":company_id,
    "name": ReadData.app_name,
    "display_name": ReadData.display_name,
    "industry":'restaurants',
    "language":ReadData.language,
    "timezone":ReadData.time_zone,
    "country_code":ReadData.country_code,
    "groups": groups,
    "religions": religions,
    "week_first_day":first_day_of_week,
    "weekend_first_day":first_day_of_weekend,
    "deadline_day":last_day_for_subbmit_shifts,
    "deadline_hour":last_hour_for_subbmit_shifts,
    "type":'A',
    "stage":ReadData.stage,
    "plan":ReadData.plan,
    "max_employees":ReadData.max_employees,
    "password_security":ReadData.password_security_level,
    "color_palette":ReadData.color_palette,
    "usability_check":False,
    "account_number":ReadData.account_number,
    "is_active":True,
 } 

 create_app_request = requests.post(create_app_url, json=data, headers=headers)
 if create_app_request.status_code == 201:
    global app_id
    json_str = create_app_request.content.decode('utf-8')
    data = json.loads(json_str)
    app_id = data.get('id')
    print("This is app id")
    print(app_id)
 else:
     print("Error:create_compeny_request getting ", create_app_request.status_code)
     print("Error:create_compeny_request getting ", create_app_request.content)

def get_app(app_id):
 get_appliaction_url=env_url+"/api/applications/"+str(app_id)
 headers = {"Authorization": f"Token {token}"}
 get_appliaction_request = requests.get(get_appliaction_url,json=None,headers=headers)
 if get_appliaction_request.status_code == 200:
      response_data = get_appliaction_request.json()
#     local_account_number=response_data.get("account_number")
#     print("This is account number: ")
#     print(local_account_number)
#     print(json.dumps(response_data, indent=4, ensure_ascii=False))
      return response_data

 else:
     print("Error:get_appliaction_request ", get_appliaction_request.status_code)

def get_groups(app_id):
 get_appliaction_url=env_url+"/api/applications/"+str(app_id)
 headers = {"Authorization": f"Token {token}"}
 get_appliaction_request = requests.get(get_appliaction_url,json=None,headers=headers)
 if get_appliaction_request.status_code == 200:
    response_data = get_appliaction_request.json()
    groups=response_data.get("groups")
    return groups
 else:
     print("Error:get_appliaction_request ", get_appliaction_request.status_code)
  
def convert_role_name_to_id(role_name,role_id,list):
     for i in range(len(list)):
       temp_list=list[i]
       roles=temp_list["roles"]
       for j in range(len(roles)):
            if roles[j]==role_name:
                 roles[j]=role_id
                 break  

def convert_group_name_to_id(list_target,list_sorce):
 if isinstance(list_target, list):
     for i in range(len(list_sorce)):
       temp_sorce=list_sorce[i]
       group_id=temp_sorce["id"]
       group_name=temp_sorce["name"]
       for j in range(len(list_target)):
            if list_target[j]==group_name:
                 list_target[j]=group_id
                 break  
 else:
   for i in range(len(list_sorce)):
       temp_sorce=list_sorce[i]
       group_id=temp_sorce["id"]
       group_name=temp_sorce["name"]
       for j in range(len(list_sorce)):
            if list_target == group_name:
                 return group_id
             
def convert_shift_name_to_id(shift_name,shift_id):
     for i in range(len(ReadData.receives_limits)):
       temp_limit=ReadData.receives_limits[i]
       shifts_in_limit=temp_limit["shifts"]
       for j in range(len(shifts_in_limit)):
            if shifts_in_limit[j]==shift_name:
                 shifts_in_limit[j]=shift_id
                 break   

def create_role(index,roles,app_id):
 create_role_url=env_url+"/api/roles/"
 data={
    "name": roles[index], 
    "application":app_id,
    "priority": index+1
 }
 create_role_request = requests.post(create_role_url, json=data, headers=headers)
 if create_role_request.status_code == 201:
    json_str = create_role_request.content.decode('utf-8')
    data = json.loads(json_str)
    convert_role_name_to_id(data.get("name"),data.get("id"),ReadData.shifts)

    if len(ReadData.locations) !=0 :
      convert_role_name_to_id(data.get("name"),data.get("id"),ReadData.locations)
    print(data)
    LIST_OF_ROLES.append(data.get("id"))
    
 else:
     print("Error:create_role_request getting ", create_role_request.status_code)
     print("Error:create_role_request getting ", create_role_request.content)

def create_shifts(index,shifts,app_id):
 create_shift_url=env_url+"/api/shifts/"
 temp_shifts=shifts[index]
 name= temp_shifts["name"]
 roles=temp_shifts["roles"]
 continuesly=temp_shifts["continuously"]
 data= {
   "name":name,
    "application": app_id,
    "roles": roles,
    "continuesly": continuesly,
    "order": index+1
  }
 
 create_shift_request = requests.post(create_shift_url, json=data, headers=headers)
 if create_shift_request.status_code == 201:
    json_str = create_shift_request.content.decode('utf-8')
    data = json.loads(json_str)
    convert_shift_name_to_id(data.get("name"),data.get("id"))
    print(data)
 else:
     print("Error:create_compeny_request getting ", create_shift_request.status_code)
     print("Error:create_compeny_request getting ", create_shift_request.content)

def create_request_limits(index,app_id):
 create_limit_url=env_url+"/api/limits/"
 temp=ReadData.requests_limits[index]
 name=temp["name"]
 days=temp["days"]
 type=temp["type"]
 min=temp["min"]
 max=temp["max"]
 default=temp["default"]
 shift_daily =temp["shift_daily"]

 data= {
   "name":name,
    "application": app_id,
    "type": type,
    "days":days,
    "shift_daily":shift_daily,
    "min": min,
    "max":max,
    "default":default,
    "order":index+1,
  }
 
 create_request_limit_request = requests.post(create_limit_url, json=data, headers=headers)
 if create_request_limit_request.status_code == 201:
    json_str = create_request_limit_request.content.decode('utf-8')
    data = json.loads(json_str)
    print(data)
 else:
     print("Error:create_compeny_request getting ", create_request_limit_request.status_code)
     print("Error:create_compeny_request getting ", create_request_limit_request.content)

def create_recive_limits(index,app_id):
 create_limit_url=env_url+"/api/limits/"
 temp=ReadData.receives_limits[index]
 name=temp["name"]
 shift=temp["shifts"]
 _type=temp["type"]
 _min=temp["min"]
 _max=temp["max"]
 default=temp["default"]
 shift_daily =temp["shift_daily"]
 is_global=temp["is_global"]

 data= {
   "name":name,
    "application": app_id,
    "type": _type,
    "shift_daily":shift_daily,
    "min": _min,
    "max":_max,
    "default":default,
    "order":index+1,
    "shifts":shift,
    "is_global":is_global
  }
 
 create_recive_limit_request = requests.post(create_limit_url, json=data, headers=headers)
 if create_recive_limit_request.status_code == 201:
    json_str = create_recive_limit_request.content.decode('utf-8')
    data = json.loads(json_str)
    print(data)
 else:
     print("Error:create_compeny_request getting ", create_recive_limit_request.status_code)
     print("Error:create_compeny_request getting ", create_recive_limit_request.content)

def create_employee_configuration(index,app_id,attribute,headers):
 create_employee_configuration_url=env_url+"/api/employee-configuration/"
 headers = headers
 if attribute != None:
      temp=ReadData.employee_configurations[index]
      name_of_attribute=choose_employee_configuration_field(temp["name"])
      if name_of_attribute == 'number':
           create_report_coulmn(app_id,["2"],'number',"מספר עובד לשכר")     
      excel=temp["excel"] 
      report=temp["report"]
      document=temp["document"]
      data= {
      "attribute":name_of_attribute,
      "application": app_id,
      "excel": True,
      "report":report,
      "document":document,
      "is_active":True,
      "mandatory":False
      }
      create_employee_configuration_request = requests.post(create_employee_configuration_url, json=data, headers=headers)
      if create_employee_configuration_request.status_code == 201:
        json_str = create_employee_configuration_request.content.decode('utf-8')
        data = json.loads(json_str)
        print(data)
      else:
            print("Error:create_compeny_request getting ", create_employee_configuration_request.status_code)
            print("Error:create_compeny_request getting ", create_employee_configuration_request.content)
 else:
      data= {
      "mandatory":False,
      "attribute":'clock_id',
      "application": app_id,
      "excel": True,
      "report":False,
      "document":False,
      "is_active":True
      }
      create_employee_configuration_request = requests.post(create_employee_configuration_url, json=data, headers=headers)
      if create_employee_configuration_request.status_code == 201:
        json_str = create_employee_configuration_request.content.decode('utf-8')
        data = json.loads(json_str)
        print(data)
      else:
            print("Error:create_employee_configuration getting ", create_employee_configuration_request.status_code)
            print("Error:create_employee_configuration getting ", create_employee_configuration_request.content)

def create_automation_user():
  create_employee_url=env_url+"/api/employee-details/"
  automation_details=[                   
      {
      "user_name":"tabit_auto",
      "password":"tabit"+str(company_id),
      "group":7,
      "first_name" :'טאביט' ,
      "last_name":'אוטומציה',
      "phone":'0501111111'
     } ]

  create_employee_url = requests.post(create_employee_url, json=automation_details, headers=headers)
  if create_employee_url.status_code == 201:
            json_str = create_employee_url.content.decode('utf-8')
            data = json.loads(json_str)
            print(data)
  else:
            print("Error:create_employee_url getting ", create_employee_url.status_code)
            print("Error:create_employee_url getting ", create_employee_url.content)

def create_features(index,app_id,unplanned_shift_flag):
 if ReadData.features[index] == 'לייבור קוסט - LC':
      Features.create_labor_cost_feature(app_id)
      if  unplanned_shift_flag != True :
        create_unplanned_shift(app_id)
        unplanned_shift_flag= True
      create_hourly_cost(app_id)
 elif ReadData.features[index] == 'עלויות':
      Features.create_costs_feature(app_id)
 elif   "פיצ'ר ג'ירפות" in ReadData.features[index] :
      Features.create_giraffes_feature(app_id)
 elif  'סינטות' in ReadData.features[index] :
      Features.create_sintot_feature(app_id)
 elif  ReadData.features[index] == 'חופשות' :
      if ReadData.vacation_days != None:
        Features.create_vacations_feature(app_id,True)
      else:
        Features.create_vacations_feature(app_id,False)
 elif  ReadData.features[index] == 'החלפות' :
      Features.create_replacements_feature(app_id)        
 elif  ReadData.features[index] == 'היעדרויות' :
      Features.create_absences_feature(app_id)      
 elif  ReadData.features[index] == 'מסמכים' :
         Features.create_documents_feature(app_id)    
         for item in ReadData.employee_configurations:
            if item.get("name")== 'תעודת זהות' :
               ReadData.employee_configurations.remove(item)
         for item in ReadData.employee_configurations:
            if item.get("name") == 'תאריך תחילת עבודה' :
               ReadData.employee_configurations.remove(item)              
 elif  ReadData.features[index] == 'טפסי 101' :
         Features.create_101_feature(app_id)      
 elif  'נונו מימי' in ReadData.features[index] :
          if len(ReadData.locations) != 0:
           Features.create_multi_rota_feature(app_id,ReadData.locations)  
 elif   ReadData.features[index] == 'משימות' :
         Features.create_tasks_feature(app_id)
 elif   ReadData.features[index] == 'נסיעות' :
         create_travel_cost(app_id,"עלות נסיעות יומית",'D',1)
         create_travel_cost(app_id,"עלות חופשי חודשי",'M',2) 
         create_report_coulmn(app_id,["1","2"],'auto_travel_cost',None)  

def create_unplanned_shift(app_id):
      global unplanned_shift_id
      create_unplannedshift_url=env_url+"/api/unplanned-shifts/"
      data= {
      "name":"בלת''מ",
      "application": app_id,
      "type": 1,
      "work_code":0,
      "order":1,
      "is_active":True
      }
      create_unplannedshift_url = requests.post(create_unplannedshift_url, json=data, headers=headers)
      if create_unplannedshift_url.status_code == 201:
            json_str = create_unplannedshift_url.content.decode('utf-8')
            data = json.loads(json_str)
            unplanned_shift_id=[]
            unplanned_shift_id.append(data.get("id"))
            print(data)
      else:
            print("Error:create_unplannedshift_url getting ", create_unplannedshift_url.status_code)
            print("Error:create_unplannedshift_url getting ", create_unplannedshift_url.content)

def create_attendance_unplanned_shift(app_id):
      create_unplannedshift_url=env_url+"/api/admin/app/unplannedshifts/"
      headers = {"Authorization": f"Token {token}"}
      baltam="נוכחות"
      data= {
      "name":baltam,
      "application": app_id,
      "type": 1,
      "work_code":0,
      "order":1,
      "is_active":True
      }
      create_unplannedshift_url = requests.post(create_unplannedshift_url, json=data, headers=headers)
      if create_unplannedshift_url.status_code == 201:
            json_str = create_unplannedshift_url.content.decode('utf-8')
            data = json.loads(json_str)
            print(data)
      else:
            print("Error:create_unplannedshift_url getting ", create_unplannedshift_url.status_code)
            print("Error:create_unplannedshift_url getting ", create_unplannedshift_url.content)

def create_clock(app_id):
 global unplanned_shift_flag
 unplanned_shift_flag=False
 if ReadData.clock == 'ללא שעון':
      return
 if any( d.get('name') == 'מזהה שעון' for d in ReadData.employee_configurations):
        print() #No 
 else:
      create_employee_configuration(0,app_id,'מזהה שעון')
 if unplanned_shift_flag==False:
       create_unplanned_shift(app_id)  
       unplanned_shift_flag=True
 Features.create_clock_feature(app_id)
 if ReadData.clock == 'ביומטרי':
    Features.create_clock_feature(app_id)
 if ReadData.clock == 'טאביט':
      Features.create_automation_user(app_id)
 elif  'אפליקציה' in ReadData.clock:
      if ReadData.permissions_for_web_clock != None: #For part of the groups
         convert_group_name_to_id(ReadData.permissions_for_web_clock, groups)
         Features.create_web_clock_attribute(app_id,ReadData.permissions_for_web_clock)
      else:
         Features.create_web_clock_attribute(app_id,ReadData.permissions_for_web_clock) #For all  groups   
 elif  'תוכנתי' in ReadData.clock:  
      if ReadData.permissions_for_web_clock != None:
        convert_group_name_to_id(ReadData.permissions_for_web_clock, groups)   
        Features.create_install_clock_attribute(app_id,ReadData.permissions_for_web_clock)#For part of the groups
      else:
            Features.create_install_clock_attribute(app_id,ReadData.permissions_for_web_clock) #For all  groups  

def create_attendance_clock(app_id):
 if ReadData.clock == 'ללא שעון':
      Features.create_clock_feature(app_id)
      return "Erorr!!, attendance system with no clock!!"    
 if any( d.get('name') == 'מזהה שעון' for d in ReadData.employee_configurations):
        print() #No 
 else:
      create_employee_configuration(0,app_id,'מזהה שעון')
 Features.create_clock_feature(app_id)
 create_attendance_unplanned_shift(app_id)
 if ReadData.clock == 'טאביט':
        Features.AUTOMATION=True    
 elif  'אפליקציה' in ReadData.clock:
      if ReadData.permissions_for_web_clock != None: #For part of the groups
         convert_group_name_to_id(ReadData.permissions_for_web_clock, groups)
         Features.create_web_clock_attribute(app_id,ReadData.permissions_for_web_clock)
      else:
         Features.create_web_clock_attribute(app_id,ReadData.permissions_for_web_clock) #For all  groups   
 elif  'תוכנתי' in ReadData.clock:  
      if ReadData.permissions_for_web_clock != None:
        convert_group_name_to_id(ReadData.permissions_for_web_clock, groups)   
        Features.create_install_clock_attribute(app_id,ReadData.permissions_for_web_clock)#For part of the groups
      else:
            Features.create_install_clock_attribute(app_id,ReadData.permissions_for_web_clock) #For all  group

def create_employee(index,headers,employee_details,app_id):
  groups=get_groups(app_id)
  create_employee_url=env_url+"/api/employee-details/"
  headers=headers
  temp=employee_details[index]
  user_name=temp["user_name"]
  password=temp["password"]
  first_name=temp["first_name"]
  last_name=temp["last_name"]
  if last_name == None:
       last_name=""
  email=  temp["email"] 
  phone_number=   temp["phone_number"]
  group =temp["group"]
  group=convert_group_name_to_id(group,groups) 
  data = {
      "application":app_id,
      "username":user_name,
      "password":password,
      "group":group,
      "first_name" :first_name,
      "last_name":last_name,
      "email":email,
      "phone":phone_number,
      "id_number":"" 
      }
  create_employee_url = requests.post(create_employee_url, json=data, headers=headers)
  if create_employee_url.status_code == 201:
            json_str = create_employee_url.content.decode('utf-8')
            data = json.loads(json_str)
            print(data)
  else:
            print("Error:create_employee_url getting ", create_employee_url.status_code)
            print("Error:create_employee_url getting ", create_employee_url.content)

def create_report_attribute(app_id):
 report_attribute_url= env_url+"/api/report-attribute/"
 headers = {"Authorization": f"Token {token}"}
 data={
          "application" : app_id,
          "name":"special_holiday_100_rate",#Spacial holiday regular hours rate
          "contract": 0,
          "value": 2.0      
     }
 report_attribute_url=requests.post(report_attribute_url, json=data, headers=headers)
 if report_attribute_url.status_code == 201:
            print(report_attribute_url.content)
 else:
            print("Error:report_attribute_url getting ", report_attribute_url.status_code)
            print("Error:report_attribute_url getting ", report_attribute_url.content)
     
def create_shabat(app_id):
  shabat_url=env_url+"/api/holidays/"
  if ReadData.shabat == "ללא הגדרת שבת":
       return 
  else:
       if isinstance(ReadData.shabat, list):# חורף וקיץ
            for i in range(len(ReadData.shabat)): # חורף וקיץ
             temp=ReadData.shabat[i]
             end_time=temp["shabat_end_hour"]
             shabat_start_day=temp["shabat_start_day"] 
             shabat_start_hour=temp["shabat_start_hour"]
             shabat_end_day=temp["shabat_end_day"]
             period=temp["period"]
            data = {
                 "application":app_id,
                    "name":"שבת",
                    "start_day":shabat_start_day,
                    "start_time":shabat_start_hour,
                    "end_day": shabat_end_day,
                    "end_time": end_time,
                    "period":period,
                    "religions":[1],
                    "special_type":"AS",
                    "type":"R"
                  }
            shabat_url = requests.post(shabat_url, json=data, headers=headers)
            if shabat_url.status_code == 201:
                  json_str = shabat_url.content.decode('utf-8')
                  data = json.loads(json_str)
                  print(data)
            else:
                  print("Error:shabat_url getting ", shabat_url.status_code)
                  print("Error:shabat_url getting ", shabat_url.content)
       if "start_day" in ReadData.shabat:#שנתי
             end_time=temp["shabat_end_hour"]
             shabat_start_day=temp["shabat_start_day"] 
             shabat_start_hour=temp["shabat_start_hour"]
             shabat_end_day=temp["shabat_end_day"]
             period=temp["period"]
             data = {
                    "name":"שבת",
                    "start_day":shabat_start_day,
                    "start_time":shabat_start_hour,
                    "end_day": shabat_end_day,
                    "end_time": end_time,
                    "period":period,
                    "religions":[1],
                    "special_type":"AS",
                    "type":"R"
                  }
             shabat_url = requests.post(shabat_url, json=data, headers=headers)
             if shabat_url.status_code == 201:
                  json_str = shabat_url.content.decode('utf-8')
                  data = json.loads(json_str)
                  print(data)
             else:
                  print("Error:shabat_url getting ", shabat_url.status_code)
                  print("Error:shabat_url getting ", shabat_url.content)

       else: #אוטומטי
          choose_holiday_area_code()
          data = { 
                  "application":app_id, 
                   "name":"שבת",
                   "period":'A',
                   "religions":[1],
                   "special_type":"AS",
                   "type":"R",
                   "location":ReadData.holidays_area

                }   
          shabat_url = requests.post(shabat_url, json=data, headers=headers)
          if shabat_url.status_code == 201:
                  json_str = shabat_url.content.decode('utf-8')
                  data = json.loads(json_str)
                  print(data)
          else:
                  print("Error:shabat_url getting ", shabat_url.status_code)
                  print("Error:shabat_url getting ", shabat_url.content)  

def create_automatic_holiday(app_id):
  holiday_url=env_url+"/api/holidays/"
  if ReadData.automatic_holidays_special_cost ==  "כן":
      data = {  
                   "application":app_id,
                   "name":"חגים",
                   "period":'A',
                   "religions":[1],
                   "special_type":"AS",
                   "type":"H",
                   "location":ReadData.holidays_area

                }   
      holiday_url = requests.post(holiday_url, json=data, headers=headers)
      if holiday_url.status_code == 201:
                  json_str = holiday_url.content.decode('utf-8')
                  data = json.loads(json_str)
                  print(data)
      else:
                  print("Error:holiday_url getting ", holiday_url.status_code)
                  print("Error:holiday_url getting ", holiday_url.content) 
  else:# ללא חגים מיוחדים
      data = {  
                   "name":"חגים",
                   "period":'A',
                   "religions":[1],
                   "special_type":"WS",
                   "type":"H",
                   "location":ReadData.holidays_area,
                }   
      holiday_url = requests.post(holiday_url, json=data, headers=headers)
      if holiday_url.status_code == 201:
                  json_str = holiday_url.content.decode('utf-8')
                  data = json.loads(json_str)
                  print(data)
      else:
                  print("Error:holiday_url getting ", holiday_url.status_code)
                  print("Error:holiday_url getting ", holiday_url.content) 
        
def create_hourly_cost(app_id):
 hourly_cost_url=env_url+"/api/costs/"
 data= {
      "name":'עלות שעתית',
      "application": app_id,
      "type": 'C',
      "input_type ":1, #text
      "order":1,
      "hourly_daily":'H',
      "roles": LIST_OF_ROLES,
     "unplanned_shifts": unplanned_shift_id,
      "is_active":True,
      "order":1
      }
 hourly_cost_url = requests.post(hourly_cost_url, json=data, headers=headers)
 if hourly_cost_url.status_code == 201:
            json_str = hourly_cost_url.content.decode('utf-8')
            data = json.loads(json_str)
            print(data)
 else:
            print("Error:hourly_cost_url getting ", hourly_cost_url.status_code)
            print("Error:hourly_cost_url getting ", hourly_cost_url.content)

def create_travel_cost(app_id,name,hourly_daily,order):
 travel_cost_url=env_url+"/api/costs/"
 data= {
      "name":name,
      "application": app_id,
      "hourly_daily":hourly_daily,
      "type":'V',
      "order":order
      }
 travel_cost_url = requests.post(travel_cost_url, json=data, headers=headers)
 if travel_cost_url.status_code == 201:
            json_str = travel_cost_url.content.decode('utf-8')
            data = json.loads(json_str)
            print(data)
 else:
            print("Error:travel_cost_url getting ", travel_cost_url.status_code)
            print("Error:travel_cost_url getting ", travel_cost_url.content)

def create_report_coulmn(app_id,reports,coulmn_name,name):
     create_report_coulmn_url=env_url+"/api/report-column/"
     if name == None:
          data= {
          "application": app_id,
          "reports":reports,
          "column":coulmn_name,
          }
     else:
        data= {
            "name": name,
            "application": app_id,
            "reports":reports,
            "column":coulmn_name,
            }
     
     create_report_coulmn_url = requests.post(create_report_coulmn_url, json=data, headers=headers)
     if create_report_coulmn_url.status_code == 201:
               json_str = create_report_coulmn_url.content.decode('utf-8')
               data = json.loads(json_str)
               print(data)
     else:
               print("Error:create_report_coulmn_url getting ", create_report_coulmn_url.status_code)
               print("Error:create_report_coulmn_url getting ", create_report_coulmn_url.content)


###Excel 
######################################################
def load_excel_file():
    global sheet 
    global sheet2
    global root
    file_path = filedialog.askopenfilename(
    title="Select an Excel file",
    filetypes=[("Excel files", "*.xlsx;*.xls")]
    )
    if file_path:
        wb = load_workbook(file_path, data_only=True)
        new_wb = Workbook()

        for idx, sheet_name in enumerate(wb.sheetnames):
            original_ws = wb[sheet_name]
            # Create a new sheet for each sheet, except the first one
            if idx == 0:
                new_ws = new_wb.active  # Use the default active sheet
            else:
                new_ws = new_wb.create_sheet(title=sheet_name)
            
            new_ws.title = sheet_name

            for row in original_ws.iter_rows(values_only=True):
                new_ws.append(row)

        new_file = 'values_only_file.xlsx'
        new_wb.save(new_file)

        # Access the first and second sheets
        sheet = new_wb.worksheets[0]
        sheet2 = new_wb.worksheets[1]
        root.destroy()

#####################################################

def create_system(two_systems_boolean):
 get_token()
 global headers
 headers = {"Authorization": f"Token {token}"}
 if two_systems_boolean == False:
     create_company()
 create_app()
 Cats = Features.get_cats(app_id)
 headers = {"Authorization": f"Token {token}", "Cats": Cats}

 for i in range(len(ReadData.roles)):
  create_role(i,ReadData.roles,app_id)

 for i in range(len(ReadData.shifts)):
  create_shifts(i,ReadData.shifts,app_id)

 for i in range(len(ReadData.requests_limits)):
  create_request_limits(i,app_id)

 for i in range(len(ReadData.receives_limits)):
  create_recive_limits(i,app_id)

 create_clock(app_id)

 for i in range(len(ReadData.features)):
  create_features(i,app_id,unplanned_shift_flag)
 if len(ReadData.cutting_hours) != 0:
   Features.create_cutting_hours_feature(app_id,ReadData.cutting_hours) 

 if ReadData.holidays == "כן":
      choose_holiday_area_code()
      create_automatic_holiday(app_id)
      create_shabat(app_id)

 if ReadData.automatic_holidays_special_cost == "כן":
      create_report_attribute(app_id)
      Features.create_special_holiday(app_id)
      create_report_coulmn(app_id,["1","2"],'special_holiday_100',None)

 for i in range(len(ReadData.employee_configurations)):
     create_employee_configuration(i,app_id,ReadData.employee_configurations[i],headers)

#  for i in range(len(ReadData.owner_details)):
#       create_employee(i,headers,ReadData.owner_details,app_id)
    

root = tk.Tk()
root.title("FQ system")
root.geometry("400x250")
load_button = tk.Button(root, text="Load Excel File", command=load_excel_file)
load_button.pack(pady=50)
root.mainloop()


##### ATTENDANCE SYSTEM ###

def create_attendance_system():
 get_token()
 global headers
 headers = {"Authorization": f"Token {token}"}
 create_company()
 Cats = Features.get_cats(app_id)
 headers = {"Authorization": f"Token {token}", "Cats": Cats}
 create_attendance_app()
 create_role()
 if ReadData.automatic_holidays_special_cost == "כן":
      create_report_attribute(app_id)
      Features.create_special_holiday(app_id)
      print("Report columns")
 if ReadData.holidays == "כן":
      choose_holiday_area_code()
      create_automatic_holiday(app_id)
      create_shabat(app_id)
 for i in range(len(ReadData.features)):
  create_features(i,app_id)
 if len(ReadData.cutting_hours) != 0:
   Features.create_cutting_hours_feature(278,ReadData.cutting_hours) 
 create_attendance_clock(app_id)
 
##### Regular SYSTEM ###
def create_regular_system():
 ReadData.read_data_for_regular_system(sheet)
 create_system(False)

##### 2 applications with one company SYSTEM ###

def create_two_systems_with_one_company():
  ReadData.read_data_for_regular_system(sheet)
  create_system(False) 
  ReadData.read_data_for_regular_system(sheet2)
  if len (ReadData.shifts) != 0:   
   create_system(True) 




create_two_systems_with_one_company()
