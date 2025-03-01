import requests
import json
import sys

env_url= "https://k8-shift.tabit-dev.com/"

create_application_group_feature_url=env_url+"api/application-group-feature/"
create_application_group_attribute_url=env_url+"api/application-group-attribute/"
create_messages_configuration_url=env_url+"api/messages-configuration/"
create_location_url =env_url+"api/location/"
temp_high_groups=["Headquarters","Owners","Managers"]
temp_low_groups=["Junior-Managers","Senior Sub-Managers","Senior Employees","Employees","Junior Employees"]
CLOCK = False
AUTOMATION=False
HOURLY_COST=False
high_groups_id=[]
low_groups_id=[]

def get_token():
      global  token
      tok_url = env_url+"api/auth/token/"
      tok_data = {"username": "kfira", "password": "159753ASDF", "company": 1}
      response = requests.post(tok_url, json=tok_data)
      if response.status_code == 200:  
        token = response.json().get('token')
      else:
          print("get_token in Features file is getting error")
          print(response.status_code)
          print(response.content)

def get_cats(app_id):
      cats_url = env_url+"api/auth/switch-application/"
      get_token()
      global headers
      headers={"Authorization": f"Token {token}"}
      data ={
          "application": app_id
         }
      response = requests.post(cats_url, json=data,headers=headers)
      if response.status_code == 200:
          headers={"Authorization": f"Token {token}", "Cats": response.json().get('cats')}
          return response.json().get('cats')
      else:
          print("ERROR!")
          print(" response.status_code "+str(response.status_code))
          print(" response.content "+str(response.content))
        
def get_groups(app_id):
 get_appliaction_url=env_url+"api/applications/"+str(app_id)
 headers = {"Authorization": f"Token {token}"}
 get_appliaction_request = requests.get(get_appliaction_url,json=None,headers=headers)
 if get_appliaction_request.status_code == 200:
    response_data = get_appliaction_request.json()
    groups=response_data.get("groups")
    return groups
 else:
     print("Error:get_appliaction_request ", get_appliaction_request.status_code)

def get_company(app_id):
 get_appliaction_url=env_url+"api/applications/"+str(app_id)
 headers = {"Authorization": f"Token {token}"}
 get_appliaction_request = requests.get(get_appliaction_url,json=None,headers=headers)
 if get_appliaction_request.status_code == 200:
    response_data = get_appliaction_request.json()
    company=response_data.get("company")
    return company
 else:
     print("Error:get_appliaction_request ", get_appliaction_request.status_code)

def get_group_features(feature_id):
  requst_url= "https://k8-shift.tabit-dev.com/api/application-group-feature/"+str(feature_id)
  request = requests.post(requst_url, headers=headers)
  if request.status_code ==200:
       print(request.content)
  else:
       print("Error!! create_costs_request ")
       print(request.content) 

def convert_role_name_to_id(role_name,role_id,list):
     for i in range(len(list)):
       temp_list=list[i]
       roles=temp_list["roles"]
       for j in range(len(roles)):
            if roles[j]==role_name:
                 roles[j]=role_id
                 break  

def organize_groups(groups):
    global automation_group 
    automation_group=False
    for dictionary in groups:
        if dictionary.get("original_name") in temp_high_groups and dictionary.get("id") not in high_groups_id:
            high_groups_id.append(dictionary.get("id"))
        elif dictionary.get("original_name") in temp_low_groups and dictionary.get("id") not in low_groups_id:
            low_groups_id.append(dictionary.get("id"))
        elif dictionary.get("original_name") == 'Automation':
            automation_group=True

def send_application_group_feature_request(app_id, group,feature,is_active):
      data= (
            {
                "application":app_id,
                "group":group,
                 "feature": feature, 
                 "is_active":is_active
                }) 
      request = requests.post(create_application_group_feature_url, json=data, headers=headers)
      if request.status_code == 201:  
         json_str = request.content.decode('utf-8')
         data = json.loads(json_str)
         print(data)
         return request
      else:
        print("Error!!!")
        json_str = request.content.decode('utf-8')
        print(json_str)
        return request
          
def send_application_group_attribute_request(app_id, group,feature,value):
      data= (
            {
                "application":app_id,
                "group":group,
                 "attribute":feature, 
                 "value": value
                }) 
      request = requests.post(create_application_group_attribute_url, json=data, headers=headers)
      if request.status_code == 201:  
         json_str = request.content.decode('utf-8')
         data = json.loads(json_str)
         print(data)
         return request
      else:
        print("Error!!!")
        json_str = request.content.decode('utf-8')
        print(json_str)
        return request

def send_messages_configuration_request(app_id, name,in_app,notification,value):
      data= (
            {
                "application":app_id,
                "name":name,
                "in_app":in_app,
                "notification":notification, 
                "value": value
                }) 
      request = requests.post(create_messages_configuration_url, json=data, headers=headers)
      if request.status_code == 201:  
         json_str = request.content.decode('utf-8')
         data = json.loads(json_str)
         print(data)
         return request
      else:
        print("Error!!!")
        json_str = request.content.decode('utf-8')
        data = json.loads(json_str)
        error_message = data.get("non_field_errors", [])[0]
        return error_message

def create_special_holiday(app_id):
   get_cats(app_id)
   groups= get_groups(app_id)
   organize_groups(groups)
   for i in range((len(high_groups_id))):
    send_application_group_attribute_request(app_id,high_groups_id[i],101,"True")#	Special_holiday

def create_clock_feature(app_id):
    get_cats(app_id)
    global CLOCK
    groups= get_groups(app_id)
    if CLOCK == False:
        for dictionary in groups:
         if dictionary.get('original_name') != "Automation":
            group_id=dictionary.get("id")
            send_application_group_feature_request(app_id,group_id,14,True)# clock feature 
    CLOCK =True

def create_web_clock_attribute(app_id, permissions_for_web_clock):
    get_cats(app_id)
    if CLOCK:
        if isinstance(permissions_for_web_clock, dict):
            for dictionary in permissions_for_web_clock.values():  # Ensure iterating over values
                group_id = dictionary.get("id") or dictionary.get("group_id")  # Get group_id safely
                original_name = dictionary.get("original_name", dictionary["name"])  # Use default if missing
                if original_name != "Automation":
                    send_application_group_attribute_request(app_id, group_id, 21, "True")  # Web clock attribute 

        elif isinstance(permissions_for_web_clock, list):
            if all(isinstance(item, int) for item in permissions_for_web_clock):
                for group_id in permissions_for_web_clock:
                    send_application_group_attribute_request(app_id, group_id, 21, "True")  # Reports cost
            else:
                print("Error!!")
                print("Couldn't find permissions for clock ")
                print("Features")
                sys.exit()

        elif isinstance(permissions_for_web_clock, int):  # Handle integer input
            send_application_group_attribute_request(app_id, permissions_for_web_clock, 21, "True")        

    else: 
        create_clock_feature(app_id)
        if not hasattr(create_web_clock_attribute, "retry"):
            create_web_clock_attribute.retry = True  # Prevent infinite recursion
            create_web_clock_attribute(app_id, permissions_for_web_clock)

def create_install_clock_attribute(app_id,permissions_for_install_clock):
    get_cats(app_id)
    if CLOCK:
        if isinstance(permissions_for_install_clock, dict):
            for dictionary in permissions_for_install_clock.values():  # Ensure iterating over values
                group_id = dictionary.get("id") or dictionary.get("group_id")  # Get group_id safely
                original_name = dictionary.get("original_name", dictionary["name"])  # Use default if missing
                if original_name != "Automation":
                    send_application_group_attribute_request(app_id, group_id, 42, "True")  # Web clock attribute 

        elif isinstance(permissions_for_install_clock, list):
            if all(isinstance(item, int) for item in permissions_for_install_clock):
                for group_id in permissions_for_install_clock:
                    send_application_group_attribute_request(app_id, group_id, 42, "True")  # Reports cost
            else:
                print("Error!!")
                print("Couldn't find permissions for install clock ")
                print("Features")
                sys.exit()

    else: 
        create_clock_feature(app_id)
        if not hasattr(create_web_clock_attribute, "retry"):
            create_web_clock_attribute.retry = True  # Prevent infinite recursion
            create_web_clock_attribute(app_id, permissions_for_install_clock)

def create_automation_user(app_id):
  get_cats(app_id)
  global company_id
  company_id= get_company(app_id)
  company_id=company_id.get('id')
  groups=get_groups(app_id)
  automation_id = None
  for item in groups:
    if item["name"] == "Automation":
        automation_id = item["id"]
        break
  create_automation_user=env_url+"/api/employees/"
  data = {
      "application" : app_id,
      "group":automation_id,
      "limits":[],
      "user":
        {
        "company":company_id,
        "username":"tabit_auto",
        "password":"tabit"+str(company_id),
        "group":automation_id,
        "first_name" :'טאביט' ,
        "last_name":'אוטומציה',
        "phone":'0501111111',
        "id_number":""
        }
     } 
  create_automation_user = requests.post(create_automation_user, json=data, headers=headers)
  if create_automation_user.status_code == 201:
            json_str = create_automation_user.content.decode('utf-8')
            data = json.loads(json_str)
            print(data)
  else:
            print("Features File")
            print("Error:create_automation_user getting ", create_automation_user.status_code)
            print("Error:create_automation_user getting ", create_automation_user.content)

def create_labor_cost_feature(app_id):
  get_cats(app_id)
  groups= get_groups(app_id)
  organize_groups(groups)
  if automation_group == True:
        create_labor_cost_request = send_application_group_feature_request(app_id,6,39,True)#labor cost 
        if create_labor_cost_request.status_code == 201: 
            print("Labor cost created successfully")
            #create_automation_user(app_id)
        else:
            print("create_labor_cost_request  didnt work" )
            #create_automation_user(app_id)
  else:
     print("Error!! There is no automation group")

def create_costs_feature(app_id):
 get_cats(app_id)
 groups= get_groups(app_id)
 organize_groups(groups)
 for i in range((len(high_groups_id))):
   send_application_group_attribute_request(app_id,high_groups_id[i],69,"1")#reports cost
 if automation_group == True:
    send_application_group_attribute_request(app_id,6,69,"1")#Automation group + reports cost
 create_report_coulmn(app_id,['1','2'],'cost',None)
 create_report_coulmn(app_id,['2'],'cost_rate',None)
           
def create_giraffes_feature(app_id):
    get_cats(app_id)
    groups=get_groups(app_id)
    if CLOCK == False:
        create_clock_feature(app_id)#clock feature
    for dictionary in groups:
        group_id=dictionary.get("id")
        original_name=dictionary.get("original_name")
        if original_name != "Automation":
            send_application_group_attribute_request(app_id,group_id,151,"True")#create predefined rota
            send_application_group_feature_request(app_id,group_id,8,False)#auto populate rota
            if group_id in high_groups_id:
                send_application_group_attribute_request(app_id,group_id,68,"True")# predefined rota            
#הגדרת איוש עובדים מוגדרים מראש 
def create_predefined_rota_feature(app_id):
    get_cats(app_id)
    groups=get_groups(app_id)
    if CLOCK == False:
        create_clock_feature(app_id)#clock feature
    for dictionary in groups:
        group_id=dictionary.get("id")
        original_name=dictionary.get("original_name")
        if original_name != "Automation":
            send_application_group_attribute_request(app_id,group_id,151,"True")#create predefined rota
            send_application_group_feature_request(app_id,group_id,8,False)#auto populate rota

def create_sintot_feature(app_id):
    get_cats(app_id)
    groups=get_groups(app_id)
    for dictionary in groups:
        group_id=dictionary.get("id")
        original_name=dictionary.get("original_name")
        if original_name != "Automation":
            if CLOCK == False:
                 create_clock_feature(app_id)
            send_application_group_attribute_request(app_id,group_id,147,"3")# clock mode attribute 

def create_vacations_feature(app_id,bool):
     get_cats(app_id)
     groups=get_groups(app_id)
     organize_groups(groups)
     for dictionary in groups:
        group_id=dictionary.get("id")
        original_name=dictionary.get("original_name")
        if original_name != "Automation":
            send_application_group_feature_request(app_id,group_id,20,True)# vacation feature 
            send_application_group_attribute_request(app_id,group_id,194,"True")# vacation_type
            send_application_group_attribute_request(app_id,group_id,195,"False")# old_interface
     if bool == True:
      for dictionary in groups:
        group_id=dictionary.get("id")
        if group_id in low_groups_id:
             send_application_group_attribute_request(app_id,group_id,114,"14")# min request days

def create_replacements_feature(app_id):
     get_cats(app_id)
     groups=get_groups(app_id)
     for dictionary in groups:
        group_id=dictionary.get("id")
        original_name=dictionary.get("original_name")
        if original_name != "Automation":
            send_application_group_feature_request(app_id,group_id,18,True)# replacements feature 
       
def create_absences_feature(app_id):
    get_cats(app_id)
    groups=get_groups(app_id)
    organize_groups(groups)
    for dictionary in groups:
        group_id=dictionary.get("id")
        if group_id in high_groups_id:
            send_application_group_attribute_request(app_id,group_id,130,"2")# Show Absence Reasons
            send_application_group_attribute_request(app_id,group_id,54,"True") #Update Absence Reasons  
            send_application_group_attribute_request(app_id,group_id,53,"True") #absence report
    create_report_coulmn(app_id,['1'],'absence_0',None)

def create_documents_feature(app_id):
    get_cats(app_id)
    groups=get_groups(app_id)
    organize_groups(groups)
    for dictionary in groups:
        group_id=dictionary.get("id")
        original_name=dictionary.get("original_name")
        if original_name != "Automation":
            send_application_group_feature_request(app_id,group_id,36,True)# documents feature 
            if group_id in high_groups_id:
              send_application_group_attribute_request(app_id,group_id,155,"True")# create_documents attribute
     
              send_application_group_attribute_request(app_id,group_id,156,"True")# edit_documents attribute
    for i in range (2):
     if i == 0:
        attribute=  'id_number' 
     else:
         attribute=  'work_start_date' 
     create_employee_configuration_url=env_url+"api/employee-configuration/"
     data= {
        "attribute":attribute,
        "application": app_id,
        "mandatory":False,
        "excel": True,
        "report":True,
        "document":False,
        "is_active":True
        }
     create_employee_configuration_request = requests.post(create_employee_configuration_url, json=data, headers=headers)
     if create_employee_configuration_request.status_code == 201:
          print(create_employee_configuration_request.content)
     else:
         print(create_employee_configuration_request.status_code )
         print(create_employee_configuration_request.content )

def create_101_feature(app_id):
    get_cats(app_id)
    groups=get_groups(app_id)
    for dictionary in groups:
        group_id=dictionary.get("id")
        original_name=dictionary.get("original_name")
        if original_name != "Automation":
            send_application_group_feature_request(app_id,group_id,42,True)# payroll feature 
            send_application_group_attribute_request(app_id,group_id,109,"2")# edit_payrolls attribute
            send_application_group_attribute_request(app_id,group_id,158,"True")# update_payrolls attribute
    create_employee_configuration_url=env_url+"api/employee-configuration/"
    data= {
        "attribute":'payroll_form',
        "application": app_id,
        "mandatory":False,
        "excel": True,
        "report":False,
        "document":False,
        "is_active":True
        }
    create_employee_configuration_request = requests.post(create_employee_configuration_url, json=data, headers=headers)
    if create_employee_configuration_request.status_code == 201:
          print(" payroll_form employee configureaiton created sucssefuly")
    else:
         print(create_employee_configuration_request.status_code )

def create_tasks_feature(app_id):
    get_cats(app_id)
    groups=get_groups(app_id)
    for dictionary in groups:
        group_id=dictionary.get("id")
        original_name=dictionary.get("original_name")
        if original_name != "Automation":
            send_application_group_feature_request(app_id,group_id,40,True)# Tasks feature 
            if group_id in high_groups_id:
             send_application_group_attribute_request(app_id,group_id,192,"True")# tasks_creator attribute

    #Moti said that he will make al the messages_configurations as ture
# נונו מימי NONO MIMI
def create_multi_rota_feature(app_id,locations):
    get_cats(app_id)
    groups=get_groups(app_id)
    for dictionary in groups:
        group_id=dictionary.get("id")
        original_name=dictionary.get("original_name")
        if original_name != "Automation":
            send_application_group_attribute_request(app_id,group_id,162,"True")# multi_rota attribute 
    for i in range(len(locations)):
        create_location_url = env_url+"api/locations/"
        temp=locations[i]
        name_of_location= temp["name"]
        roles_for_location= temp["roles"]
        
        data= {
            "name":name_of_location,
            "application": app_id,
            "roles": roles_for_location,
            "order":i+1,
        }
        create_location_url = requests.post(create_location_url, json=data, headers=headers)
        if create_location_url.status_code == 201:
            json_str = create_location_url.content.decode('utf-8')
            data = json.loads(json_str)
            print(data)
        else:
            print("Error:create_compeny_request getting ", create_location_url.status_code)
            print("Error:create_compeny_request getting ", create_location_url.content)

def create_report_coulmn(app_id,reports,coulmn_name,name):
    get_cats(app_id)
    create_report_coulmn_url=env_url+"api/report-column/"
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

def create_cutting_hours_feature(app_id,cutting_hours):
    get_cats(app_id)
    for item in cutting_hours :
        group_id=item.get("group_id")
        attribute=item.get("attribute")
        value= item.get("value")
        send_application_group_attribute_request(app_id,group_id,attribute,value)# All cutting houres

def delete_auto_populate_rota(app_id):
    groups=get_groups(app_id)
    organize_groups(groups)
    for dictionary in groups:
         group_id=dictionary.get("id")
         send_application_group_feature_request (app_id,group_id,8,False)
