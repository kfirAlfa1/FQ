import requests
import ReadData
import json
import Features
import utils
import sys
import TokenAndCats

env_url= ""

days_of_the_week = ["ראשון", "שני", "שלישי", "רביעי", "חמישי", "שישי", "שבת"]
general_high_groups_permissions=["Headquarters","Owners","Managers"]
LIST_OF_ROLES=[]
auto_user_created=False
unplanned_shift_flag=False

token_and_cats = TokenAndCats.TokenAndCats()

def send_post_request(url, data, request_name, error_message="Error occurred"):
    try:
        response = requests.post(url, json=data, headers=token_and_cats.headers)
        if response.status_code == 201:
            json_str = response.content.decode('utf-8')
            response_data = json.loads(json_str)
            return response_data
        else:
            print(f"{error_message}: {request_name} returned status code {response.status_code}")
            print(f"{error_message}: {request_name} response content: {response.content}")
            return None
    except Exception as e:
        print(f"{error_message}: Exception in {request_name}: {e}")
        return None

def get_company(app_id):
    get_appliaction_request= get_app(app_id)
    company=get_appliaction_request['company']
    company_id=company.get("id")
    return company_id

def get_app(app_id):
 get_appliaction_url=env_url+"/api/applications/"+str(app_id)
 get_appliaction_request = requests.get(get_appliaction_url,json=None,headers=token_and_cats.headers)
 if get_appliaction_request.status_code == 200:
      response_data = get_appliaction_request.json()
      return response_data

 else:
     print("Error:get_appliaction_request ", get_appliaction_request.status_code)
     print("API file")

def get_groups(app_id):
 get_appliaction_url=env_url+"/api/applications/"+str(app_id)
 get_appliaction_request = requests.get(get_appliaction_url,json=None,headers=token_and_cats.headers)
 if get_appliaction_request.status_code == 200:
    response_data = get_appliaction_request.json()
    groups=response_data.get("groups")
    return groups
 else:
     print("Error:get_appliaction_request ", get_appliaction_request.status_code)

def create_company():
 global company_id
 create_company_url= env_url+"/api/companies/"
 data= {
    "name":ReadData.company_name
 }
 response=send_post_request(create_company_url,data,request_name="create_company",error_message="Error with create_company - API")
 if response != None:
    company_id=response.get("id")
    print("Company created")
 else:
     print("Error!! ,create_company request failed")
     sys.exit()
   
def create_app():
 global app_id
 global groups
 global religions
 create_app_url=env_url+"/api/applications/"
 ReadData.language = utils.choose_language(ReadData.language)
 ReadData.password_security_level = utils.choose_password_security_level(ReadData.password_security_level)
 ReadData.account_number = utils.account_number(ReadData.account_number)
 ReadData.country_code = utils.choose_country_code(ReadData.country_code)
 ReadData.time_zone = utils.choose_time_zone(ReadData.time_zone)
 first_day_of_week=days_of_the_week.index(ReadData.first_day_of_week)
 first_day_of_weekend=days_of_the_week.index(ReadData.first_day_of_weekend)
 last_day_for_subbmit_shifts=days_of_the_week.index(ReadData.last_day_for_subbmit_shifts)
 last_hour_for_subbmit_shifts=str(ReadData.last_hour_for_subbmit_shifts)
 religions = utils.organize_religions(ReadData.religions_list, ReadData.language)
 groups = utils.organize_groups(ReadData.perrmisions_list, ReadData.language)

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
 response=send_post_request(create_app_url,data,request_name="create_app",error_message="Error with create_app - API")
 if response != None:
    app_id=response.get("id")
    print("Application created")
 else:
     print("Error!!, create_app request failed")
     sys.exit()

def create_attendance_app():
 global app_id
 create_app_url=env_url+"/api/applications/"
 ReadData.language = utils.choose_language(ReadData.language)
 ReadData.password_security_level = utils.choose_password_security_level(ReadData.password_security_level)
 ReadData.account_number = utils.account_number(ReadData.account_number)
 ReadData.country_code = utils.choose_country_code(ReadData.country_code)
 ReadData.time_zone = utils.choose_time_zone(ReadData.time_zone)
 first_day_of_week=days_of_the_week.index(ReadData.first_day_of_week)
 first_day_of_weekend=days_of_the_week.index(ReadData.first_day_of_weekend)
 last_day_for_subbmit_shifts=days_of_the_week.index(ReadData.last_day_for_subbmit_shifts)
 last_hour_for_subbmit_shifts=str(ReadData.last_hour_for_subbmit_shifts)
 religions = utils.organize_religions(ReadData.religions_list, ReadData.language)
 groups = utils.organize_groups(ReadData.perrmisions_list, ReadData.language) 
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
 response=send_post_request(create_app_url,data,request_name="create_attendance_app",error_message="Error with create_attendance_app - API")
 if response != None:
   app_id=response.get("id")

def create_roles(roles,app_id):
 for i in range(len(roles)):
   create_role(i,roles,app_id)
 print(str(len(roles))+ " roles created")

def create_role(index,roles,app_id):
 create_role_url=env_url+"/api/roles/"
 data={
    "name": roles[index], 
    "application":app_id,
    "priority": index+1
 }
 response=send_post_request(create_role_url,data,request_name="create_role "+str(roles[index]),error_message="Error with create_role - API")
 if response != None:
    utils.convert_role_name_to_id(response.get("name"),response.get("id"),ReadData.shifts)
    if len(ReadData.locations) !=0 :
       utils.convert_role_name_to_id(response.get("name"),response.get("id"),ReadData.locations)
    LIST_OF_ROLES.append(response.get("id")) # For create_hourly_cost 

def create_shifts(shifts,app_id):
 for i in range(len(shifts)):
  create_shift(i,shifts,app_id)
 print(str(len(shifts))+ " shifts created")

def create_shift(index,shifts,app_id):
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
 response=send_post_request(create_shift_url,data,request_name="create_shift "+ str(name),error_message="Error with create_shift - API")
 if response !=None:
    utils.convert_shift_name_to_id_for_receives_limits(ReadData.receives_limits,response.get("name"),response.get("id"))
    return 1
 else:
     print("Error, create_shift request failed")
  
def create_requests_limits(requests_limits,app_id):
 for i in range(len(requests_limits)):
   create_request_limit(i,requests_limits,app_id)
 print(str(len(requests_limits))+ " requests limits created")

def create_request_limit(index,requests_limits,app_id):
 create_limit_url=env_url+"/api/limits/"
 temp=requests_limits[index]
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
 send_post_request(create_limit_url,data,request_name="create_request_limits "+str(name),error_message="Error with create_request_limits - API")

def create_recives_limits(recives_limits,app_id):
 for i in range(len(recives_limits)):
   create_recive_limit(i,recives_limits,app_id)
 print(str(len(recives_limits))+ " recives limits created")

def create_recive_limit(index,recives_limits,app_id):
 create_limit_url=env_url+"/api/limits/"
 temp=recives_limits[index]
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
 send_post_request(create_limit_url,data,request_name="create_recive_limits "+str(name),error_message="Error with create_recive_limits - API")

def create_features(features,app_id):
 for i in range(len(features)):
   create_feature(i,features,app_id)
 print(str(len(features))+ " features created")

def create_feature(index,features,app_id):
 global unplanned_shift_flag
 global auto_user_created
 if features[index] == 'לייבור קוסט - LC':
      Features.create_labor_cost_feature(app_id)
      if  unplanned_shift_flag != True :
        create_unplanned_shift(app_id,False)
        unplanned_shift_flag= True
      create_hourly_cost(app_id)
      if auto_user_created == False:
           create_automation_user(app_id)
           auto_user_created=True
      print("Labor cost created")
 elif features[index] == 'עלויות':
      Features.create_costs_feature(app_id)
      print("Costs created")
 elif   "פיצ'ר ג'ירפות" in ReadData.features[index] :
      Features.create_giraffes_feature(app_id)
      print("Giraff created")
 elif  'סינטות' in ReadData.features[index] :
      Features.create_sintot_feature(app_id)
      print("Sintot created")
 elif  features[index] == 'חופשות' :
      if ReadData.vacation_days != None:
        Features.create_vacations_feature(app_id,True)
        print("Vications created")
      else:
        Features.create_vacations_feature(app_id,False)
        print("Vications created")
 elif  features[index] == 'החלפות' :
      Features.create_replacements_feature(app_id) 
      print("Replacments created")     
 elif  features[index] == 'היעדרויות' :
      Features.create_absences_feature(app_id) 
      print("Absences created")     
 elif  features[index] == 'מסמכים' :
         Features.create_documents_feature(app_id)    
         for item in ReadData.employee_configurations:
            if item.get("name")== 'תעודת זהות' :
               ReadData.employee_configurations.remove(item)
         for item in ReadData.employee_configurations:
            if item.get("name") == 'תאריך תחילת עבודה' :
               ReadData.employee_configurations.remove(item)   
         print("Documents created")           
 elif  features[index] == 'טפסי 101' :
         Features.create_101_feature(app_id)
         print("101 created")      
 elif  'נונו מימי' in ReadData.features[index] :
          if len(ReadData.locations) != 0:
           Features.create_multi_rota_feature(app_id,ReadData.locations)
           if any( d.get('name') == 'תפקיד ראשי' for d in ReadData.employee_configurations):
             print() #No  
           else:
             create_employee_configuration(0,app_id,'primary_role')
          print("NONO MIMI created")
 elif   features[index] == 'משימות' :
         Features.create_tasks_feature(app_id)
         print("Tasks created")
 elif   features[index] == 'איוש עובדים מוגדרים מראש' :
         Features.create_predefined_rota_feature(app_id)
         print("Predefined created")
 elif   features[index] == 'נסיעות' :
         create_travel_cost(app_id,"עלות נסיעות שעתית ",'H',1)
         create_travel_cost(app_id,"עלות נסיעות יומית",'D',2)
         create_travel_cost(app_id,"עלות חופשי חודשי",'M',3) 
         create_report_coulmn(app_id,["1","2"],'auto_travel_cost',None)  

def create_employee_configurations(employee_configurations,app_id):
 for i in range(len(employee_configurations)):
   create_employee_configuration(i,app_id,employee_configurations[i])

def create_employee_configuration(index, app_id, attribute):
    url = env_url + "/api/employee-configuration/"
    if attribute:
        mandatory = attribute in ['primary_role', "תפקיד ראשי"]
        attribute = 'primary_role' if mandatory else attribute

        if mandatory:
            data = {"attribute": attribute,
                     "application": app_id,
                       "excel": True, 
                       "report": False,
                    "document": False,
                      "is_active": True, 
                      "mandatory": mandatory}
            send_post_request(url, data, request_name="create_employee_configuration",
                              error_message="Error with create_employee_configuration - API")
            return

        if not ReadData.employee_configurations:
            return

        temp = ReadData.employee_configurations[index]
        name_of_attribute = utils.choose_employee_configuration_field(temp["name"])

        if name_of_attribute == 'number':
            create_report_coulmn(app_id, ["2"], 'number', "מספר עובד לשכר")

        data = {"attribute": name_of_attribute,
                 "application": app_id,
                   "excel": True,
                "report": temp["report"], 
                "document": temp["document"], 
                "is_active": True,
                  "mandatory": mandatory}
    else:
        data = {"mandatory": False, 
                "attribute": 'clock_id', 
                "application": app_id,
                "excel": True,
                "report": False, 
                 "document": False, 
                "is_active": True}

    send_post_request(url, data, request_name="create_employee_configuration",error_message="Error with create_employee_configuration - API")

def create_employees(owner_details,app_id):
 for i in range(len(owner_details)):
   create_employee(i,app_id,owner_details)
 print(str(len(owner_details))+ " owner created")
    
def create_employee(index,app_id,owner_details):
  groups=get_groups(app_id)
  create_employee_url=env_url+"/api/employees/"
  temp=owner_details[index]
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
  group= utils.convert_name_of_group_from_hebrew_to_english(group)
  group=utils.convert_group_name_to_id(group,groups) 
  if group == None:
       print("Couldent find group id of owners\n")
       print("The owner has not been established in the system\n")
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
  send_post_request(create_employee_url,data,request_name="create_employee",error_message="Error with create_employee - API")

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
  response= send_post_request(create_automation_user,data,request_name="create_automation_user",error_message="Error with create_automation_user - API")
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

def create_unplanned_shift(app_id,attendnce):
      global unplanned_shift_flag
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
      response=send_post_request(create_unplannedshift_url,data,request_name="create_unplannedshift",error_message="Error with create_unplanned_shift - API")
      if response !=None:
         unplanned_shift_id.append(response.get("id"))
         unplanned_shift_flag=True
      else:
          print("ERROR!! create_unplanned_shift ,request failed")

def create_clock(app_id):
 global unplanned_shift_flag
 if ReadData.clock == 'ללא שעון':
      return
 if any( d.get('name') == 'מזהה שעון' for d in ReadData.employee_configurations):#Check if clock id inside employee configuration
        print() #clock id NOT inside employee configuration
 else:
      create_employee_configuration(0,app_id,'מזהה שעון')
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
         permissions_after_convert= utils.convert_group_name_to_id(ReadData.permissions_for_web_clock, groups)
         Features.create_web_clock_attribute(app_id,permissions_after_convert)
         return
 elif  'תוכנתי' in ReadData.clock:
        Features.create_install_clock_attribute(app_id,utils.high_groups_permissions)
        return 

def create_report_attribute(app_id):
 report_attribute_url= env_url+"/api/report-attribute/"
 data={
          "application" : app_id,
          "name":"special_holiday_100_rate",#Spacial holiday regular hours rate
          "contract": 0,
          "value": 2.0      
     }
 send_post_request(report_attribute_url,data,request_name="report_attribute",error_message="Error with create_report_attribute - API")

def create_shabat(app_id):
    shabat_url = env_url + "/api/holidays/"
    if ReadData.shabat == "ללא הגדרת שבת":
        return
    
    if isinstance(ReadData.shabat, list):  # חורף וקיץ
        for temp in ReadData.shabat:
            temp["start_time"], temp["end_time"] = str(temp["start_time"]), str(temp["end_time"])
            send_post_request(shabat_url, {
                "application": app_id,
                "name": "שבת",
                "start_day": temp["start_day"],
                "start_time": temp["start_time"],
                "end_day": temp["end_day"],
                "end_time": temp["end_time"],
                "period": temp["period"],
                "religions": [1],
                "special_type": "AS",
                "type": "R"
            }, request_name="shabat - Summer and winter", error_message="Error with create_shabat - API")
        return

    if "start_day" in ReadData.shabat:  # שנתי
        ReadData.shabat["start_time"], ReadData.shabat["end_time"] = str(ReadData.shabat["start_time"]), str(ReadData.shabat["end_time"])
        send_post_request(shabat_url, {
            "application": app_id,
            "name": "שבת",
            "start_day": ReadData.shabat["start_day"],
            "start_time": ReadData.shabat["start_time"],
            "end_day": ReadData.shabat["end_day"],
            "end_time": ReadData.shabat["end_time"],
            "period": ReadData.shabat["period"],
            "religions": [1],
            "special_type": "AS",
            "type": "R"
        }, request_name="shabat - Yearly", error_message="Error with create_shabat - API")
    else:  # אוטומטי
        ReadData.holidays_area = utils.choose_holiday_area_code(ReadData.holidays_area)
        send_post_request(shabat_url, {
            "application": app_id,
            "name": "שבת",
            "period": "A",
            "religions": [1],
            "special_type": "AS",
            "type": "R",
            "location": ReadData.holidays_area
        }, request_name="shabat - Automatic", error_message="Error with create_shabat - API")

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
      send_post_request(holiday_url,data,request_name="create_automatic_holiday -> חגים + חגים מיוחדים",error_message="Error with create_automatic_holiday - API")
  else:# הגדרת חגים ללא חגים מיוחדים
      data = {     "application":app_id,
                   "name":"חגים",
                   "period":'A',
                   "religions":[1],
                   "special_type":"WS",
                   "type":"H",
                   "location":ReadData.holidays_area,
                }   
      send_post_request(holiday_url,data,request_name="create_automatic_holiday -> חגים + ללא חגים מיוחדים",error_message="Error with create_automatic_holiday - API") 

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
 send_post_request(hourly_cost_url,data,request_name="create_hourly_cost -> עלות שעתית",error_message="Error with create_hourly_cost - API")

def create_travel_cost(app_id,name,hourly_daily,order):
 travel_cost_url=env_url+"/api/costs/"
 data= {
      "name":name,
      "application": app_id,
      "hourly_daily":hourly_daily,
      "type":'V',
      "order":order
      }
 send_post_request(travel_cost_url,data,request_name="create_travel_cost"+str(name),error_message="Error with create_travel_cost - API")

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
     send_post_request(create_report_coulmn_url,data,request_name="create_report_coulmn "+str(coulmn_name),error_message="Error with create_report_coulmn - API")
