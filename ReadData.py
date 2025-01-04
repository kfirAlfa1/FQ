
import sys

general_perrmisions_list =['Headquarters','Owners','Managers','Junior-Managers','Senior Sub-Managers','Sub-Managers','Employees','Junior Employees']
days_of_week=['א','ב','ג','ד','ה','ו','ש']
days_of_week_shabat=['ראשון','שני','שלישי','רביעי','חמישי','שישי','שבת']



#Compeny and app details 
def get_application():
    global app_name
    global display_name
    global company_name
    global language
    global time_zone
    global country_code
    global first_day_of_week
    global first_day_of_weekend
    global last_day_for_subbmit_shifts
    global last_hour_for_subbmit_shifts
    global password_security_level
    global account_number
    global industry
    global default_perrmision
    global default_religion
    global type
    global stage    
    global plan
    global max_employees
    global color_palette
    global usability_check
    global active 

    #From Excel
    app_name=sheet.cell(row=13, column=2).value
    display_name=sheet.cell(row=14, column=2).value
    company_name=sheet.cell(row=12, column=2).value
    language=sheet.cell(row=15, column=2).value
    time_zone=sheet.cell(row=16, column=2).value
    country_code=sheet.cell(row=17, column=2).value
    first_day_of_week=sheet.cell(row=18, column=2).value
    first_day_of_weekend=sheet.cell(row=19, column=2).value
    last_day_for_subbmit_shifts=sheet.cell(row=20, column=2).value
    last_hour_for_subbmit_shifts=sheet.cell(row=21, column=2).value
    password_security_level=sheet.cell(row=22, column=2).value
    account_number=sheet.cell(row=23, column=2).value

    #From webstie

    industry='Restaurants' 
    type= 'P'
    stage= 0
    plan= 0
    max_employees= -1
    color_palette='palette-blue'
    usability_check= True
    active= True

    #Permissions
    for i in range(27,36):
        temp=sheet.cell(row=i, column=3).value
        if temp == 1:
            perrmisions_list.append(i)

    if  len(perrmisions_list) != 0:
        for i in range(len(perrmisions_list)):
            j=perrmisions_list[i]
            perrmisions_list[i]=sheet.cell(row=j, column=1).value
            perrmisions_list_names.append(sheet.cell(row=j, column=2).value)
            #Check if default
            if sheet.cell(row=j, column=4).value == 'כן':
                default_perrmision=sheet.cell(row=j, column=1).value

    #Religion
    for i in range(39,41):
        temp=sheet.cell(row=i, column=3).value
        if temp == 1:
            religions_list.append(i)

    if  len(religions_list) != 0:
        for i in range(len(religions_list)):
            j=religions_list[i]
            religions_list[i]=sheet.cell(row=j, column=1).value
            religions_list_names.append(sheet.cell(row=j, column=2).value)
            #Check if default
            if sheet.cell(row=j, column=4).value == 'כן':
                default_religion=sheet.cell(row=j, column=1).value

def get_owners():
 i=3
 while sheet.cell(row=i, column=1).value != 'שם חברה' and sheet.cell(row=i, column=1).value !='שם משתמש' and i<30:
        i+=1
 if sheet.cell(row=i, column=1).value =='שם חברה' or i== 30:
     return "Couldnt find owner details "
 if sheet.cell(row=i, column=1).value =='שם משתמש': 
    j=2 
    for x in range(2):
     if sheet.cell(row=i, column=j+x).value != None:
        full_name =sheet.cell(row=i+3, column=j).value.split(' ')
        first_name=full_name[0]
        if len (full_name) == 1:
            last_name=None
        else:
            last_name=full_name[1]
        owner_details.append(
        {
            "user_name":sheet.cell(row=i, column=j).value,
            "password":sheet.cell(row=i+1+x, column=j).value,
            "group":sheet.cell(row=i+2+x, column=j).value,
            "first_name":first_name,
            "last_name":last_name,
            "email":sheet.cell(row=i+4+x, column=2).value,
            "phone_number":sheet.cell(row=i+5+x, column=2).value
        })
  
# Tow validations: 
# 1- Checking if the first value is not NULL
# 2- Checking if the role does not already exist
def get_roles():
 i=7
 if sheet.cell(row=i, column=8).value == None:
     print("Error!!! no roles found")
     quit
 while sheet.cell(row=i, column=8).value != None:
        if sheet.cell(row=i, column=8).value not in roles:
            roles.append(sheet.cell(row=i, column=8).value)
            i+=2
            continue
        else:
            print(sheet.cell(row=i, column=8).value)
            print("Error!!! This role is allready in the list!!!")
            break

# 1- Checking if the total number of shifts is correct
def get_shifts():
    i = 4
    j = 9
    flag = True

    while flag:
        roles_per_shift = []  
        
        if sheet.cell(row=i, column=j).value is None or sheet.cell(row=i, column=j).value =='' or sheet.cell(row=i, column=j).value == "משמרת1":
            flag = False
            break  

        shift_name = sheet.cell(row=i, column=j).value 
        continuously=sheet.cell(row=i+2, column=j).value
        loop_on_roles=i+3
        for counter in range(len(roles)):
         if sheet.cell(row=loop_on_roles, column=j).value is not None:
            role = sheet.cell(row=loop_on_roles, column=8).value 
            roles_per_shift.append(role)
            loop_on_roles+= 2 
         else:
             loop_on_roles+=2 

        shifts.append(
            {
             "name":shift_name,
             "roles":roles_per_shift,
             "continuously":continuously
             })
        j += 1 
        i = 4
    i=5
    j=6
    if sheet.cell(row=i, column=j).value == "רשימת משמרות":
        number_of_shifts=0
        while sheet.cell(row=i, column=j).value != None and sheet.cell(row=i, column=j).value != '':
            i+=1
            if sheet.cell(row=i, column=j).value != None and sheet.cell(row=i, column=j).value != '':
                number_of_shifts+=1
        if len(shifts)== number_of_shifts:
            print()
        else:
            print("Number of shifts is not match!!")
            quit()

    else:
        print("couldent find validation on shifts") 

def get_locations():
 i=8
 j=8
 if sheet.cell(row=i, column=j).value == None and i==8:
     locations.clear()
     return "No locations"
 while sheet.cell(row=i, column=j).value != None:
        name_of_location= sheet.cell(row=i, column=j).value
        roles_per_location=[]
        role = sheet.cell(row=i-1, column=j).value
        roles_per_location.append(role)
        i+=2
        
        while name_of_location == sheet.cell(row=i, column=j).value:
            role = sheet.cell(row=i-1, column=j).value
            roles_per_location.append(role)
            i+=2
        locations.append(
         {
            "name": name_of_location,
            "roles":roles_per_location,
         }) 
            
def split_shifts_for_limits(shifts):
     if ',' in shifts:
        return shifts.split(',')
     else:
        return shifts.split('/') 

def convert_days_to_range_for_limist(days_for_requests_limits):
   days= []
   temp1=days_for_requests_limits[0]
   temp2=days_for_requests_limits[1]
   index = days_of_week.index(temp1)
   days.append(index+1)
   index = days_of_week.index(temp2)
   days.append(index+1)
   days=list(range(days[0], days[-1] + 1))
   return days

def convert_days_for_shabat(day):
   index = days_of_week_shabat.index(day)
   return index

def get_requests_limits():
 i=37
 global days_for_request_limit 
 days_for_request_limit=[]
 while sheet.cell(row=i, column=1).value != 'מגבלות בקשות' and sheet.cell(row=i, column=1).value !='הגדרת דוחות':
        i+=1
 if sheet.cell(row=i, column=1).value =='הגדרת דוחות':
     return "Couldnt find requests limits "
 if sheet.cell(row=i, column=1).value == 'מגבלות בקשות':      
    i+=2
    j=1
    flag = True
    while flag:
        if sheet.cell(row=i, column=j).value != None and sheet.cell(row=i, column=j).value !=''and 'הגדרת דוחות' != sheet.cell(row=i, column=1).value and  'מגבלות קבלות' != sheet.cell(row=i, column=1).value:
         limit_name = sheet.cell(row=i, column=j).value 
         if '-' in limit_name:
             days_for_request_limit= limit_name.split('-')
             days_for_request_limit[0]=days_for_request_limit[0][-1]
             days_for_request_limit=convert_days_to_range_for_limist(days_for_request_limit)
         elif 'מינימום בקשות סופש'== limit_name:
             if  not requests_limits:  
              days_for_request_limit=[6,7]
             else:
              temp=requests_limits[-1]
              last_day_of_requests=temp["days"]
              last_day_of_requests=last_day_of_requests[-1]
              if int(last_day_of_requests) == 7:
                days_for_request_limit= [1,2]
              else:
                 days_for_request_limit= [int(last_day_of_requests)+1,int(last_day_of_requests)+2]  

         shift_daily=sheet.cell(row=i, column=j+4).value
         if shift_daily == 'יומי':
             shift_daily='D'
         else:
             shift_daily='S'
         
         scala=sheet.cell(row=i, column=j+2).value
         if '-' in scala:
            split_scala= scala.split('-')
            min=int(split_scala[0])
            max=int(split_scala[1])

         default=sheet.cell(row=i, column=j+3).value
        
         requests_limits.append(
         {
            "name": limit_name,
            "type":'Req',
            "days":days_for_request_limit ,
            "shift_daily":shift_daily,
            "min":min,
            "max":max,
            "default":default,
         }) 

         j=1 
         i+=1
        elif i > 74 or  'הגדרת דוחות' == sheet.cell(row=i, column=1).value or 'מגבלות קבלות' == sheet.cell(row=i, column=1).value:
            flag=False
            return 
        else:
            i+=1
      
 else:
        print("Error!!")
        print("Couldnt find receives limits")
        quit

def get_receives_limits():
 i=45
 while sheet.cell(row=i, column=1).value != 'מגבלות קבלות' and sheet.cell(row=i, column=1).value !='הגדרת דוחות':
        i+=1
 if sheet.cell(row=i, column=1).value =='הגדרת דוחות':
     return "Couldnt find receives limits "
 if sheet.cell(row=i, column=1).value =='מגבלות קבלות':      
    i+=2
    j=1
    flag = True
    while flag:
        if sheet.cell(row=i, column=j).value != None and sheet.cell(row=i, column=j).value !=''and 'הגדרת דוחות' != sheet.cell(row=i, column=1).value:
         limit_name = sheet.cell(row=i, column=j).value 
         shift_for_limit=sheet.cell(row=i, column=j+1).value
         if shift_for_limit == None or shift_for_limit =='':
             print("Error, coludent find shifts for limits") 
             sys.exit()
         if ',' in shifts or '/'in shifts:
          shift_for_limit = split_shifts_for_limits(shift_for_limit)     
         elif shift_for_limit == "כולם":
             shift_for_limit = [item["name"] for item in shifts if "name" in item]
         else:
            for t in range(len(shifts)):
                temp_shifts=shifts[t]
                name_of_shift= temp_shifts["name"]
                if shift_for_limit == name_of_shift:
                    shift_for_limit=[name_of_shift]
                    shift_daily = 'S'
                    break
         if shift_daily == None:
             print("Error, coludent find shifts for limits") 
             sys.exit()
         
         scala=sheet.cell(row=i, column=j+2).value
         if '-' in scala:
            split_scala= scala.split('-')
            min=int(split_scala[0])
            max=int(split_scala[1])
         default=sheet.cell(row=i, column=j+3).value
         is_global =sheet.cell(row=i, column=j+4).value
         if is_global == None:
             is_global=False
         elif is_global == "כן" or "כן" in is_global:
             shift_daily='D'
             is_global=True         
         
         receives_limits.append(
         {
            "name": limit_name,
            "shifts": shift_for_limit,
            "type":'Rec',
            "shift_daily":shift_daily,
            "min":min,
            "max":max,
            "default":default,
            "is_global":is_global
         }) 

         j=1 
         i+=1
        elif i > 84  or  'הגדרת דוחות' == sheet.cell(row=i, column=1).value:
            flag=False
            return 
        else:
            i+=1
      
 else:
        print("Error!!")
        print("Couldnt find receives limits")
        quit

def get_employee_configurations_fields():
 i=121
 while sheet.cell(row=i, column=1).value != 'שדות נוספים בכרטיס העובד' and sheet.cell(row=i, column=1).value !='הרשאות':
        i+=1
 if sheet.cell(row=i, column=1).value =='הרשאות':
     return "Couldnt find employee configurations "
 if sheet.cell(row=i, column=1).value =='שדות נוספים בכרטיס העובד':      
    i+=2
    j=1
    flag = True
    while flag:
        if sheet.cell(row=i, column=j).value != None and sheet.cell(row=i, column=j).value !=''and 'הרשאות' != sheet.cell(row=i, column=j).value:
         configuration_name = sheet.cell(row=i, column=j).value 
         document=False
         if configuration_name == "מספר עובד לשכר":
            document=True
         excel = sheet.cell(row=i, column=j+1).value
         if excel== "כן":
            excel=True
         else:
            excel=False
         report =sheet.cell(row=i, column=j+2).value
         if report== "כן":
            report=True
         else:
            report=False
         if report == False and excel == False:
            j=1 
            i+=1
            continue
            
         employee_configurations.append(
            {
                "name":configuration_name,
                "excel": excel,
                "report":report,
                "document":document
            }
         )
         j=1 
         i+=1
        elif sheet.cell(row=i, column=j).value == None or  'הרשאות' == sheet.cell(row=i, column=1).value or sheet.cell(row=i, column=j).value == '':
            flag=False
            return 

def get_holidays():
 global shabat
 global holidays
 global automatic_holidays_special_cost
 global holidays_area
 i=60
 j=1
 while sheet.cell(row=i, column=j).value != '''פיצ'רים נוספים'''and sheet.cell(row=i, column=j).value !='הגדרת חגים וימי מנוחה':
  i+=1
  if sheet.cell(row=i, column=j).value =='חוקי עבודה':
     print("Error, no holidays!!")
     quit 
      
  if sheet.cell(row=i, column=j).value =='הגדרת חגים וימי מנוחה':
      i+=1
      j+=1
      shabat=sheet.cell(row=i, column=j).value
      if shabat == 'שנתי':
            t=j 
            while sheet.cell(row=i, column=t).value != "יום התחלה" and t<20:
                t+=1
            
            if t==20:
                return "Error!! couldent find start day of Shabat (שנתית) "
            t+=1
            shabat_start_day=convert_days_for_shabat(sheet.cell(row=i, column=t).value)
            shabat_start_hour=sheet.cell(row=i+1, column=t).value
            shabat_end_day=convert_days_for_shabat(sheet.cell(row=i+2, column=t).value)
            shabat_end_hour=sheet.cell(row=i+3, column=t).value  
            shabat= {  
                "name":"שבת",
                "start_day":shabat_start_day,
                "start_time":shabat_start_hour,
                "end_day": shabat_end_day,
                "end_time": shabat_end_hour,
                "period":'Y',
                "religions":[1],
                "special_type":"AS",
                "type":"R"
            }     
      if shabat == 'חורף/קיץ':
            shabat=[]
            t=j 
            while sheet.cell(row=i, column=t).value != "יום התחלה" and t<20:
                t+=1
            
            if t==20:
                return "Error!! couldent find start day of Shabat (חורף/קיץ) "
            t+=1
            for x in range(2):
                t+=1
                if x == 0:
                    period='W'
                else:
                    period='S'
                shabat_start_day=convert_days_for_shabat(sheet.cell(row=i, column=t).value)
                shabat_start_hour=sheet.cell(row=i+1, column=t).value
                shabat_end_day=sheet.cell(row=i+2, column=t).value
                shabat_end_hour=sheet.cell(row=i+3, column=t).value  
                shabat.append = [{  
                    "name":"שבת",
                    "start_day":shabat_start_day,
                    "start_time":shabat_start_hour,
                    "end_day": shabat_end_day,
                    "end_time": shabat_end_hour,
                    "period":period,
                    "religions":[1],
                    "special_type":"AS",
                    "type":"R"
                } ]           
      holidays=sheet.cell(row=i+1, column=j).value
      automatic_holidays_special_cost=sheet.cell(row=i+2, column=j).value
      holidays_area=sheet.cell(row=i+3, column=j).value
      return

def get_clock():
 global clock
 global clock_number
 global permissions_for_web_clock
 i=108
 j=1
 while sheet.cell(row=i, column=j).value != 'סוג שעון' and sheet.cell(row=i, column=1).value !='פושים':
        i+=1
 if sheet.cell(row=i, column=j).value =='פושים':
     return "Error, no clock!!"
 if sheet.cell(row=i, column=j).value == 'סוג שעון':
     clock=sheet.cell(row=i, column=j+1).value
     if 'אפליקציה' in clock:
        permissions_for_web_clock= sheet.cell(row=i, column=j+2).value
        if ',' in permissions_for_web_clock:
           permissions_for_web_clock = permissions_for_web_clock.split(',')
        else:
           permissions_for_web_clock=[]
           permissions_for_web_clock.append(sheet.cell(row=i, column=j+2).value)    

     clock_number=sheet.cell(row=i+1, column=j+1).value
 else:
     return "Error, no clock!!"

def get_features():
 global features
 global vacation_days
 vacation_days=None
 i=75
 j=1
 while sheet.cell(row=i, column=j).value != '''פיצ'רים נוספים'''and sheet.cell(row=i, column=1).value !='חוקי עבודה':
        i+=1
 if sheet.cell(row=i, column=j).value =='חוקי עבודה':
     return "Error, no features!!"
 if sheet.cell(row=i, column=j).value == '''פיצ'רים נוספים''':
     i+=1
     while sheet.cell(row=i, column=1).value !='חוקי עבודה' and i < 100:
        if sheet.cell(row=i, column=2).value == 'כן':
            if sheet.cell(row=i, column=1).value == 'חופשות':
                if sheet.cell(row=i, column=3).value != None:
                    vacation_days=14  
            if sheet.cell(row=i, column=1).value == 'מסמכים':
                if any( d.get('name') == 'תאריך תחילת עבודה' for d in employee_configurations):
                    if any( d.get('name') == 'תעודת זהות' for d in employee_configurations):
                        print()
                    else:
                        print("Error!!")
                        print("There is no employee_configurations תעודת זהות'!!")
                else:
                    print("Error!!")
                    print("There is no employee_configurations of תאריך תחילת עבודה !!")
            features.append(sheet.cell(row=i, column=1).value)

            i+=1
        else:
            i+=1
 else:
     return  "Error, no features!!"
 if "פיצ'ר נונו מימי - סידור מפוצל" in features: 
     if len (locations)==0:
         print()
     else:# Case when there is no locations for נונו מימי
         print("Error!!")
         print("נונו מימי without locations!!")
     
def find_groups_for_cutting_hours(y,x):
    while sheet.cell(row=y, column=x).value not in general_perrmisions_list and y > 120:
        y-=1
    if sheet.cell(row=y, column=x).value in general_perrmisions_list:
           return  sheet.cell(row=y, column=x).value
    else:
          return "Error!! "

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

def get_cutting_hours():
 global cutting_hours
 cutting_hours=[]
 i=150
 j=1
 while sheet.cell(row=i, column=j).value == None or 'חיתוך שעות' not in sheet.cell(row=i, column=j).value :
        i+=1
 if sheet.cell(row=i, column=j).value =='הערות':
     return "Error, didnt find cutting houers!!"
 if 'חיתוך שעות' in sheet.cell(row=i, column=j).value:
     for counter in range (3):
        j=1
        attribute=[57,58,59,60]
        while j<10 :
         if sheet.cell(row=i, column=j+1).value == -1:
             j+=1
             continue
         value=sheet.cell(row=i, column=j+1).value 
         group= find_groups_for_cutting_hours(i,j+1)
         group=return_perrmisions_id(group)
         cutting_hours.append(
            {
                "group_id":group,
                "attribute":attribute[counter],
                "value": value
            }
         )
         j+=1
        
        if j == 10:
            i+=1
 else:
     return "No cutting hours"

def read_data_for_regular_system(sheet_from_API):
    global sheet
    sheet=sheet_from_API

    ###############################################
    global perrmisions_list_names
    global perrmisions_list
    global religions_list_names
    global religions_list
    global locations
    global  owner_details
    global roles
    global shifts
    global requests_limits
    global   receives_limits
    global employee_configurations
    global features
    
    perrmisions_list_names=[]
    perrmisions_list=[]
    religions_list_names=[]
    religions_list=[]
    locations=[]
    owner_details=[]
    roles=[]
    shifts=[]
    requests_limits=[]
    receives_limits=[]
    employee_configurations=[]
    features=[]
#################################################
    get_application()
    get_owners()
    get_roles()
    get_shifts()
    get_requests_limits()
    get_receives_limits()
    get_employee_configurations_fields()
    get_holidays()
    get_features()
    get_locations()
    get_cutting_hours()
    get_clock()



# def print_compeny_details():
#     print('Compeny details')
#     print('company name')
#     print(company_name)
#     print('app name')
#     print(app_name)
#     print('display name')
#     print(display_name)
#     print('language')
#     print(language)
#     print('country code')
#     print(country_code)
#     print('time zone')
#     print(time_zone)
#     print('last hour for subbmit shifts')
#     print(last_hour_for_subbmit_shifts)
#     print('account number')
#     print(account_number)
#     print('first day of week')
#     print(first_day_of_week)
#     print('first day of weekend')
#     print(first_day_of_weekend)
#     print('last day for subbmit shifts')
#     print(last_day_for_subbmit_shifts)

# def print_perrmisions_list_names():
#     print('Perrmisions names')
#     print(perrmisions_list_names)

# def print_religions():
#  print("Religions")
#  print(religions_list_names)

# def print_roles():
#     print('Roles')
#     print(roles)

# def print_shifts():
#  print("Shifts")
#  print(shifts)

# def print_receives_limits():
#  print("Receives limits")
#  for key,value in receives_limits.items():
#      print(f"Key = {key} and value: {value}")

# def print_employee_configurations():
#  print("Employee configurations")
#  for key,value in employee_configurations.items():
#      print(f"Key = {key} and value: {value}")

# def print_clock():
#  print("Clock")
#  print(clock)

# def print_features():
#  print("Features")
#  print(features)

# #print_shifts()
#print_employee_configurations()
#print_compeny_details()
# print_perrmisions_list_names()
# print_religions()
# print_roles()
# print_shifts()
# print_clock()
# print_receives_limits()
# print_employee_configurations()
#print_features()
