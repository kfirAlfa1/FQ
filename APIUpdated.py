import requests
import ReadData
import json
import Features
import sys
from openpyxl import load_workbook
from openpyxl import Workbook
import tkinter as tk
from tkinter import filedialog
import utils

env_url= "https://k8-shift.tabit-dev.com"

# https://k8-shift.tabit-dev.com
# https://k8-shift.tabit-dev.com/admin
# https://k8-shift.tabit-dev.com/app/system-settings

# https://il-shift.tabit-int.com
# https://il-shift.tabit-int.com/admin

# https://il-shift.tabit-stage.com/admin
#https://il-shift.tabit-stage.com


days_of_the_week = ["ראשון", "שני", "שלישי", "רביעי", "חמישי", "שישי", "שבת"]
general_high_groups_permissions=["Headquarters","Owners","Managers"]
high_groups_permissions=[]
LIST_OF_ROLES=[]
auto_user_created=False
unplanned_shift_flag=False

########################################################################

def send_post_request(url, data, headers, request_name="request", error_message="Error occurred"):
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 201:
            json_str = response.content.decode('utf-8')
            response_data = json.loads(json_str)
            print(request_name+" " + " succseed")
            return response_data
        else:
            print(f"{error_message}: {request_name} returned status code {response.status_code}")
            print(f"{error_message}: {request_name} response content: {response.content}")
            return None
    except Exception as e:
        print(f"{error_message}: Exception in {request_name}: {e}")
        return None

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
 response=send_post_request(create_company_url,data,headers,request_name="create_company",error_message="Error with create_company - API")
 if response != None:
    company_id=response.get("id")
    
def return_perrmisions_id (group):
      if group=='Headquarters':
            high_groups_permissions.append(10)
            return 10
      elif group=='Owners':
            high_groups_permissions.append(7)
            return 7
      elif group=='Managers':
            high_groups_permissions.append(2)
            return 2
      elif group=='Junior-Managers':
            return 9
      elif group=='Senior Sub-Managers':
            return 8
      elif group=='Sub-Managers':
            return 3
      elif group=='Senior Employees' or group=='Senior-employess':
            return 11  
      elif group=='Employees':
            return 4
      elif group=='Junior Employees' or group=='Junior-employees':
            return 5
      elif group=='Automation':
            return 6
      else:
           print("Error!!")
           print("Couldent find the id of the group")
           sys.exit()

def change_perrmision_to_english(index):
  temp =ReadData.perrmisions_list[index]
  if temp['name_of_group'] == 'מטה':
      temp['name_of_group'] = 'Headquarters'
  elif temp['name_of_group'] == 'בעלים':
          temp['name_of_group'] = 'Owners'
  elif temp['name_of_group'] == 'מנהלים':
        temp['name_of_group']= 'Managers' 
  elif temp['name_of_group'] == 'מנהל מתלמד':
          temp['name_of_group'] = 'Junior-Managers'
  elif temp['name_of_group'] == 'מנהלי משמרת':
        temp['name_of_group'] = 'Senior Sub-Managers'  
  elif temp['name_of_group'] == 'סגן מנהל משמרת':
          temp['name_of_group'] = 'Sub-Managers'
  elif temp['name_of_group'] == ' עובדים' or  temp['name_of_group'] == 'עובדים'  or temp['name_of_group'] == 'עובדים '  :
        temp['name_of_group'] = 'Employees' 
  elif temp['name_of_group'] == 'עובדים עם חיתוך שעון':
          temp['name_of_group'] = 'Junior Employees'
  else:
    return 

#Organize the perrmisions in order to fit to the API of creating app
def organize_groups():
    global groups
    groups=[]
    for i in range(len(ReadData.perrmisions_list)):
        temp= ReadData.perrmisions_list[i]
        perrmisions_id=return_perrmisions_id(temp['group'])
        is_default=temp['default_gruop']
        if  ReadData.language != 'he':
             change_perrmision_to_english(i)

        groups.append({
             "name": temp['name_of_group'],
             "group_id": perrmisions_id,
             "is_default": is_default
              })
        
#     groups.append({
#              "name": "Support",
#              "group_id": 14,#Support
#              "is_default": False
#               })
     
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
      else:
          print("Error!!")
          print("Couldent find the id of the religion")
          print("API")
          sys.exit()  

#Organize the religions in order to fit to the API of creating app
def organize_religions():
    global religions
    religions=[]
    for i in range(len(ReadData.religions_list)):
        temp=ReadData.religions_list[i]
        religion_id=return_religions_id(temp['religion'])
        if  ReadData.language != 'he':
             if temp['name_of_religion'] == 'יהודי':
                 temp['name_of_religion'] = 'Jewish'
             elif temp['name_of_religion'] == 'נוצרי':
                  temp['name_of_religion'] = 'Christian'
             elif temp['name_of_religion'] == 'מוסלמי':
                  temp['name_of_religion'] = 'Muslim'  
             else:
                  temp['name_of_religion'] = 'Foreign'      
             
        religions.append({
             "name": temp['name_of_religion'],
             "religion_id": religion_id,
             "is_default": temp['default_religion']
            })
 
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
           ReadData.holidays_area =1507 #באר שבע כדיפולט 
 
def create_app():
 global app_id
 ReadData.language = utils.choose_language(ReadData.language)
 ReadData.password_security_level = utils.choose_password_security_level(ReadData.password_security_level)
 ReadData.account_number = utils.account_number(ReadData.account_number)
 ReadData.country_code = utils.choose_country_code(ReadData.country_code)
 ReadData.time_zone = utils.choose_time_zone(ReadData.time_zone)
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

 response=send_post_request(create_app_url,data,headers,request_name="create_app",error_message="Error with create_app - API")
 if response != None:
    app_id=response.get("id")

def create_attendance_app():
 global app_id
 ReadData.language = utils.choose_language(ReadData.language)
 ReadData.password_security_level = utils.choose_password_security_level(ReadData.password_security_level)
 ReadData.account_number = utils.account_number(ReadData.account_number)
 ReadData.country_code = utils.choose_country_code(ReadData.country_code)
 ReadData.time_zone = utils.choose_time_zone(ReadData.time_zone)
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
 response=send_post_request(create_app_url,data,headers,request_name="create_attendance_app",error_message="Error with create_attendance_app - API")
 if response != None:
   app_id=response.get("id")

def get_app(app_id):
 get_appliaction_url=env_url+"/api/applications/"+str(app_id)
 headers = {"Authorization": f"Token {token}"}
 get_appliaction_request = requests.get(get_appliaction_url,json=None,headers=headers)
 if get_appliaction_request.status_code == 200:
      response_data = get_appliaction_request.json()
      return response_data

 else:
     print("Error:get_appliaction_request ", get_appliaction_request.status_code)
     print("API file")

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
    
def convert_name_of_group_from_hebrew_to_english(name_of_group):
  if name_of_group == 'מטה':
      name_of_group = 'Headquarters'
      return name_of_group
  elif name_of_group == 'בעלים':
      name_of_group = 'Owners'
      return name_of_group
  elif name_of_group == 'מנהלים':
        name_of_group= 'Managers' 
        return name_of_group
  else:
    return

def convert_group_name_to_id(list_target, list_source):
    # If the input is a single element (string, int, or dict), convert it to a list for uniform processing
    if isinstance(list_target, (str, int, dict)):
        list_target = [list_target]

    group_ids = []

    for item in list_target:
        found = False  # Flag to check if we found a match

        for temp_source in list_source:
            group_id = temp_source.get("id") or temp_source.get("group_id")
            group_name = temp_source["name"]
            group_original_name = temp_source.get("original_name", group_name)

            # Handle dictionaries (extract name_of_group)
            if isinstance(item, dict):
                item_name = item.get("name_of_group")
            else:
                item_name = item  # Direct string or number

            # Match names and append group_id
            if item_name in (group_name, group_original_name):
                group_ids.append(group_id)
                found = True
                break

        # If no match is found, raise an error
        if not found:
            print(f"Error! Could not find group name or ID for: {item}")
            sys.exit()

    # If there's only one ID, return it as an integer, otherwise return the list of IDs
    return group_ids[0] if len(group_ids) == 1 else group_ids

def convert_shift_name_to_id_for_receives_limits(shift_name, shift_id):
    for i in range(len(ReadData.receives_limits)):
        temp_limit = ReadData.receives_limits[i]
        shifts_in_limit = temp_limit["shifts"]
        if isinstance(shifts_in_limit, list):
            for j in range(len(shifts_in_limit)):
                if shifts_in_limit[j] == shift_name:
                    shifts_in_limit[j] = shift_id
                    break
        elif isinstance(shifts_in_limit, str):
            if shifts_in_limit == shift_name:
                temp_limit["shifts"] = [shift_id]

def create_role(index,roles,app_id):
 create_role_url=env_url+"/api/roles/"
 data={
    "name": roles[index], 
    "application":app_id,
    "priority": index+1
 }
 response=send_post_request(create_role_url,data,headers,request_name="create_role "+str(roles[index]),error_message="Error with create_role - API")
 if response != None:
    utils.convert_role_name_to_id(response.get("name"),response.get("id"),ReadData.shifts)
    if len(ReadData.locations) !=0 :
       utils.convert_role_name_to_id(response.get("name"),response.get("id"),ReadData.locations)
    LIST_OF_ROLES.append(response.get("id")) # For create_hourly_cost 

def create_shifts(index,shifts,app_id):
 create_shift_url=env_url+"/api/shifts/"
 temp_shifts=shifts[index]
 name= temp_shifts["name"]
 roles=temp_shifts["roles"]
 continuously=temp_shifts["continuously"]  
 data= {
   "name":name,
    "application": app_id,
    "roles": roles,
    "continuously": continuously,
    "order": index+1
  }
 response=send_post_request(create_shift_url,data,headers,request_name="create_shift "+ str(name),error_message="Error with create_shift - API")
 if response !=None:
    convert_shift_name_to_id_for_receives_limits(response.get("name"),response.get("id"))
    if response.get("id") != None:
        return 1
    else:
        return 0
 
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
 response=send_post_request(create_limit_url,data,headers,request_name="create_request_limits "+str(name),error_message="Error with create_request_limits - API")
 if response !=None:
    if response.get("id") != None:
        return 1
    else:
        return 0
 
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
 
 response=send_post_request(create_limit_url,data,headers,request_name="create_recive_limits "+str(name),error_message="Error with create_recive_limits - API")
 if response !=None:
    if response.get("id") != None:
        return 1
    else:
        return 0

def create_employee_configuration(index,app_id,attribute,headers):
 create_employee_configuration_url=env_url+"/api/employee-configuration/"
 if attribute != None:
      if  attribute == 'primary_role' or attribute == "תפקיד ראשי":
           attribute ='primary_role'
           mandatory=True
           data= {
               "attribute":attribute,
               "application": app_id,
               "excel": True,
               "report":False,
               "document":False,
               "is_active":True,
               "mandatory":mandatory
               } 

           send_post_request(create_employee_configuration_url,data,headers,request_name="create_employee_configuration",error_message="Error with create_employee_configuration - API")
           return
      else:
           mandatory=False
 
      if (len(ReadData.employee_configurations) == 0):
           return 
      temp=ReadData.employee_configurations[index]
      name_of_attribute=utils.choose_employee_configuration_field(temp["name"])
      if name_of_attribute == 'number':
           create_report_coulmn(app_id,["2"],'number',"מספר עובד לשכר")

      report=temp["report"]
      document=temp["document"]
      data= {
      "attribute":name_of_attribute,
      "application": app_id,
      "excel": True,
      "report":report,
      "document":document,
      "is_active":True,
      "mandatory":mandatory
      }
      send_post_request(create_employee_configuration_url,data,headers,request_name="create_employee_configuration",error_message="Error with create_employee_configuration - API")
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
      send_post_request(create_employee_configuration_url,data,headers,request_name="create_employee_configuration",error_message="Error with create_employee_configuration - API")

def create_automation_user(app_id):
  groups=get_groups(app_id)
  automation_id = None
  for item in groups:
    if item["name"] == "Automation":
        automation_id = item["id"]
        break
  create_automation_user=env_url+"/api/employees/"
  data = {
      "application" :app_id,
      "group":automation_id,
      "limits":[],
      "user":
      {
        "company":company_id,
        "username":"tabit_auto",
        "password":"tabit"+str(company_id),
        "first_name" :'טאביט' ,
        "last_name":'אוטומציה',
        "email":"",
        "phone_number":"0511111111",
        }
      }

  response= send_post_request(create_automation_user,data,headers,request_name="create_automation_user",error_message="Error with create_automation_user - API")
  if response != None:
            global auto_user_created
            print("\n Automation user created \n\n")
            print("API: LC + Attendance")
            print("username : tabit_auto")
            print("password : tabit"+ str(company_id))
            print("company :"+ str(company_id))
            print("app id  :"+ str(app_id))
            print()
            auto_user_created=True

def create_features(index,app_id):
 global unplanned_shift_flag
 global auto_user_created
 if ReadData.features[index] == 'לייבור קוסט - LC':
      Features.create_labor_cost_feature(app_id)
      if  unplanned_shift_flag != True :
        create_unplanned_shift(app_id,False)
        unplanned_shift_flag= True
      create_hourly_cost(app_id)
      if auto_user_created == False:
           create_automation_user(app_id)
           auto_user_created=True
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
           if any( d.get('name') == 'תפקיד ראשי' for d in ReadData.employee_configurations):
             print() #No  
           else:
             create_employee_configuration(0,app_id,'primary_role',headers)
 elif   ReadData.features[index] == 'משימות' :
         Features.create_tasks_feature(app_id)
 elif   ReadData.features[index] == 'איוש עובדים מוגדרים מראש' :
         Features.create_predefined_rota_feature(app_id)
 elif   ReadData.features[index] == 'נסיעות' :
         create_travel_cost(app_id,"עלות נסיעות שעתית ",'H',1)
         create_travel_cost(app_id,"עלות נסיעות יומית",'D',2)
         create_travel_cost(app_id,"עלות חופשי חודשי",'M',3) 
         create_report_coulmn(app_id,["1","2"],'auto_travel_cost',None)  

def create_unplanned_shift(app_id,attendnce):
      global unplanned_shift_id
      unplanned_shift_id=[]
      if attendnce == True:
           name= "נוכחות"
           if ReadData.language != 'he':
              name= "Attendnce" 
      else:
          name= "בלת''מ" 
      create_unplannedshift_url=env_url+"/api/unplanned-shifts/"
      data= {
      "name":name,
      "application": app_id,
      "type": 1,
      "work_code":0,
      "order":1,
      "is_active":True
      }
      response=send_post_request(create_unplannedshift_url,data, headers,request_name="create_unplannedshift",error_message="Error with create_unplanned_shift - API")
      if response !=None:
         unplanned_shift_id.append(response.get("id"))

def create_clock(app_id):
 global unplanned_shift_flag
 if ReadData.clock == 'ללא שעון':
      return
 if any( d.get('name') == 'מזהה שעון' for d in ReadData.employee_configurations):#Check if clock id inside employee configuration
        print() #clock id NOT inside employee configuration
 else:
      create_employee_configuration(0,app_id,'מזהה שעון',headers)
 if unplanned_shift_flag==False:
       create_unplanned_shift(app_id,False)  
       unplanned_shift_flag=True
 Features.create_clock_feature(app_id)
 if ReadData.clock == 'ביומטרי':
    Features.create_clock_feature(app_id)
    return 
 if ReadData.clock == 'טאביט':
      if auto_user_created == False:
         create_automation_user(app_id)
         return
 elif  'אפליקציה' in ReadData.clock:
      if ReadData.permissions_for_web_clock != None: #For part of the groups
         permissions_after_convert= convert_group_name_to_id(ReadData.permissions_for_web_clock, groups)
         Features.create_web_clock_attribute(app_id,permissions_after_convert)
         return
 elif  'תוכנתי' in ReadData.clock:
        Features.create_install_clock_attribute(app_id,high_groups_permissions)
        return 

def create_employee(index,headers,employee_details,app_id):
  groups=get_groups(app_id)
  create_employee_url=env_url+"/api/employees/"
  headers=headers
  temp=employee_details[index]
  user_name=temp["user_name"]
  password=temp["password"]
  first_name=temp["first_name"]
  last_name=temp["last_name"]
  if last_name == None:
       last_name=""
  email=  temp["email"]
  if  email == None:
       email=""
  phone_number=  temp["phone_number"]
  if  phone_number == None:
       return 
  phone_number=str(phone_number)
  if phone_number.startswith('5'):
       phone_number='0'+phone_number
  elif phone_number.startswith('972'):
        phone_number='0'+ phone_number[3:]
  group =temp["group"]
  group= convert_name_of_group_from_hebrew_to_english(group)
  group=convert_group_name_to_id(group,groups) 
  if group == None:
       print("Couldent find group id of owners")
       print("The owner has not been established in the system")
       return

  data = {
      "application" : app_id,
      "group":group,
      "limits":[],
      "user":
      {
        "company":company_id,
        "username":user_name,
        "password":password,
        "first_name" :first_name,
        "last_name":last_name,
        "email":email,
        "phone_number":phone_number,
        }
      }
  send_post_request(create_employee_url,data, headers,request_name="create_employee",error_message="Error with create_employee - API")

def create_report_attribute(app_id):
 report_attribute_url= env_url+"/api/report-attribute/"
 headers = {"Authorization": f"Token {token}"}
 data={
          "application" : app_id,
          "name":"special_holiday_100_rate",#Spacial holiday regular hours rate
          "contract": 0,
          "value": 2.0      
     }
 send_post_request(report_attribute_url,data, headers,request_name="report_attribute",error_message="Error with create_report_attribute - API")

def create_shabat(app_id):
    shabat_url = env_url + "/api/holidays/"
    if ReadData.shabat == "ללא הגדרת שבת":
        return

    if isinstance(ReadData.shabat, list):  # חורף וקיץ
        for temp in ReadData.shabat:
            data = {
                "application": app_id,
                "name": "שבת",
                "start_day": temp["start_day"],
                "start_time": str(temp["start_time"]),
                "end_day": temp["end_day"],
                "end_time": str(temp["end_time"]),
                "period": temp["period"],
                "religions": [1],
                "special_type": "AS",
                "type": "R"
            }
            send_post_request(shabat_url,data,headers,request_name="shabat - Summer and winter ",error_message="Error with create_shabat - API" )
        return

    if "start_day" in ReadData.shabat:  # שנתי
        temp = ReadData.shabat
        data = {
            "application": app_id,
            "name": "שבת",
            "start_day": temp["start_day"],
            "start_time": str(temp["start_time"]),
            "end_day": temp["end_day"],
            "end_time": str(temp["end_time"]),
            "period": temp["period"],
            "religions": [1],
            "special_type": "AS",
            "type": "R"
        }
        send_post_request(shabat_url,data, headers,request_name="shabat - Yearly ",error_message="Error with create_shabat - API")
    else:  # אוטומטי
        choose_holiday_area_code()
        data = {
            "application": app_id,
            "name": "שבת",
            "period": 'A',
            "religions": [1],
            "special_type": "AS",
            "type": "R",
            "location": ReadData.holidays_area
        }
        send_post_request(shabat_url,data,headers, request_name="shabat - Automatic ",error_message="Error with create_shabat - API")

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
      send_post_request(holiday_url,data, headers,request_name="create_automatic_holiday -> חגים + חגים מיוחדים",error_message="Error with create_automatic_holiday - API")
  else:# הגדרת חגים ללא חגים מיוחדים
      data = {     "application":app_id,
                   "name":"חגים",
                   "period":'A',
                   "religions":[1],
                   "special_type":"WS",
                   "type":"H",
                   "location":ReadData.holidays_area,
                }   
      send_post_request(holiday_url,data, headers,request_name="create_automatic_holiday -> חגים + ללא חגים מיוחדים",error_message="Error with create_automatic_holiday - API") 

def create_hourly_cost(app_id):
 hourly_cost_url=env_url+"/api/costs/"
 name ='עלות שעתית'
 if ReadData.language != "he":
      name="hourly cost"
 data= {
      "name":name,
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
 send_post_request(hourly_cost_url,data, headers,request_name="create_hourly_cost -> עלות שעתית",error_message="Error with create_hourly_cost - API")

def create_travel_cost(app_id,name,hourly_daily,order):
 travel_cost_url=env_url+"/api/costs/"
 data= {
      "name":name,
      "application": app_id,
      "hourly_daily":hourly_daily,
      "type":'V',
      "order":order
      }
 
 send_post_request(travel_cost_url,data, headers,request_name="create_travel_cost"+str(name),error_message="Error with create_travel_cost - API")

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
     send_post_request(create_report_coulmn_url,data, headers,request_name="create_report_coulmn"+str(coulmn_name),error_message="Error with create_report_coulmn - API")
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
 get_token()
 global headers
 headers = {"Authorization": f"Token {token}"}
 if two_systems_boolean == False: 
     create_company()
 create_app()
 Cats = Features.get_cats(635)
 headers = {"Authorization": f"Token {token}", "Cats": Cats}

 for i in range(len(ReadData.roles)):
  create_role(i,ReadData.roles,app_id)
 if len(LIST_OF_ROLES) == len(ReadData.roles):
      print("\n All roles were created successfully \n")
 
 counter_of_shifts=0
 for i in range(len(ReadData.shifts)):
  counter_of_shifts += create_shifts(i,ReadData.shifts,app_id)
  if counter_of_shifts == len(ReadData.shifts):
       print("\n All shifts were created successfully \n")

 counter_of_requests_limits=0     
 for i in range(len(ReadData.requests_limits)):
  counter_of_requests_limits+=create_request_limits(i,app_id)
  if counter_of_requests_limits == len(ReadData.requests_limits):
       print("\n All requests limits were created successfully \n") 

 counter_of_recive_limits=0 
 for i in range(len(ReadData.receives_limits)):
  create_recive_limits(i,app_id)
  if counter_of_recive_limits == len(ReadData.receives_limits):
       print("\n All recive limits were created successfully \n") 

 create_clock(app_id)

 for i in range(len(ReadData.features)):
  create_features(i,app_id)

 if len(ReadData.cutting_hours) != 0: #Specific for cutting hours
   Features.create_cutting_hours_feature(app_id,ReadData.cutting_hours) 
   create_report_coulmn(app_id,["3"],'exit_cut',None)
   create_report_coulmn(app_id,["3"],'entry_cut',None)


 if ReadData.shabat is not None and len(ReadData.shabat) != 0:
      create_shabat(app_id)

 if ReadData.holidays == "כן":
      choose_holiday_area_code()
      create_automatic_holiday(app_id)

 if ReadData.automatic_holidays_special_cost == "כן":
      create_report_attribute(app_id)
      Features.create_special_holiday(app_id)
      if ReadData.language != "he":
          create_report_coulmn(app_id,["1","2"],'special_holiday_100',"Speciel 200%")
      else:          
          create_report_coulmn(app_id,["1","2"],'special_holiday_100',"מיוחד 200%")

 for i in range(len(ReadData.employee_configurations)):
     create_employee_configuration(i,app_id,ReadData.employee_configurations[i],headers)

 for i in range(len(ReadData.owner_details)):
      create_employee(i,headers,ReadData.owner_details,app_id)

 print("\n\n System created successfully\n\n")
##############################################

def attendance_system():
 ReadData.read_all_data(sheet1)
 get_token()
 global headers
 headers = {"Authorization": f"Token {token}"}
 create_company()
 create_attendance_app()
 Cats = Features.get_cats(app_id)
 headers = {"Authorization": f"Token {token}", "Cats": Cats}

 create_role(0,ReadData.roles,app_id)
 unplanned_shift_flag=True
 create_unplanned_shift(app_id,unplanned_shift_flag)

 create_clock(app_id,True)

 if ReadData.shabat is not None and len(ReadData.shabat) != 0:
      create_shabat(app_id)

 if ReadData.automatic_holidays_special_cost == "כן":
      create_report_attribute(app_id)#Spacial holiday regular hours rate
      Features.create_special_holiday(app_id)
      if ReadData.language != "he":
          create_report_coulmn(app_id,["1","2"],'special_holiday_100',"Speciel 200%")
      else:          
          create_report_coulmn(app_id,["1","2"],'special_holiday_100',"מיוחד 200%")

 if ReadData.holidays == "כן":
      choose_holiday_area_code()
      create_automatic_holiday(app_id)
 
 for i in range(len(ReadData.features)):
  create_features(i,app_id)
 if len(ReadData.cutting_hours) != 0:
   Features.create_cutting_hours_feature(278,ReadData.cutting_hours)
   
 Features.delete_auto_populate_rota(app_id)

 for i in range(len(ReadData.employee_configurations)):
     create_employee_configuration(i,app_id,ReadData.employee_configurations[i],headers)

 for i in range(len(ReadData.owner_details)):
      create_employee(i,headers,ReadData.owner_details,app_id)

 print("\n\n System created successfully\n\n")

def one_system():
 ReadData.read_all_data(sheet1)
 create_system(False)

def two_systems_with_one_company():
  ReadData.read_all_data(sheet1)
  create_system(False) 
  ReadData.read_all_data(sheet2)  
  create_system(True) 

########################################
########################################
########################################
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
# Support gruop in  organize_groups() function
 
