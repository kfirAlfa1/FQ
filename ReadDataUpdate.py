
import sys
from datetime import time
import TestData

general_perrmisions_list =['Headquarters','Owners','Managers','Junior-Managers','Senior Sub-Managers','Sub-Managers','Senior-employess','Senior Employees','Employees','Junior Employees','Automation']
general_religions_list =['Jewish','Christian','Muslim','Foreign']
general_languages=['עברית','אנגלית','אנגלית (USA)','אנגלית (UK)','אנגלית (ISR)','אנגלית (Tabit US)']
general_features_list=['לייבור קוסט - LC','עלויות',"פיצ'ר ג'ירפות - הגדרה מראש עם אצבע","פיצ'ר סינטות - תכנון הפסקות",'חופשות','החלפות','היעדרויות','נסיעות','מסמכים','טפסי 101',"פיצ'ר נונו מימי - סידור מפוצל",'משימות','חיתוך שעות']
general_clock_list= ['ביומטרי','אפליקציה (Web clock)','תוכנתי (Install clock)','טאביט','ללא שעון']
general_employee_configuration_list= ['תעודת זהות','עיר','כתובת','מיקוד','תאריך תחילת עבודה','תאריך סיום עבודה','דת','מזהה שעון','מספר עובד לשכר','תפקיד ראשי']
continuously_list=[0,1,2,3]
days_of_week=['א','ב','ג','ד','ה','ו','ש']
full_name_days_of_week=['ראשון','שני','שלישי','רביעי','חמישי','שישי','שבת']

######################################################

def get_groups():
    global default_perrmision
    i=5
    while sheet.cell(row=i, column=1).value != 'דתות' and i<50 and sheet.cell(row=i, column=1).value != 'קבוצות - הרשאות ניהול' :
        i+=1
    if sheet.cell(row=i, column=1).value == 'קבוצות - הרשאות ניהול' :
        i+=2
        while sheet.cell(row=i, column=1).value != 'דתות' and i<50:
            temp=sheet.cell(row=i, column=3).value
            if temp == 1:
                j=i
                group=sheet.cell(row=j, column=1).value
                if group not in general_perrmisions_list: #Cheack if permission exist
                    print("Error with permission: " + str(group))
                    print("ReadData")
                    sys.exit()

                name_of_group=sheet.cell(row=j, column=2).value
                if  None == name_of_group or ' ' == name_of_group:
                    print("Error with name_of_group in ReadData")
                    sys.exit()
                #Check if default
                if sheet.cell(row=j, column=4).value == 'כן':
                    default_perrmision=True
                else:
                    default_perrmision=False
            
                perrmisions_list.append( {
                "group":group,
                "name_of_group":name_of_group,
                "default_gruop":default_perrmision,
                })
                
                i+=1
            else:
                i+=1   

        if sheet.cell(row=i, column=1).value == 'דתות':
                return 
    else:
        print("There are no gruops!")
        print("ReadData")
        sys.exit()

def get_religions():
    global default_religion
    i=10
    while sheet.cell(row=i, column=1).value != 'דתות' and i<60 and sheet.cell(row=i, column=1).value != 'מגבלות בקשות' :
        i+=1
    if sheet.cell(row=i, column=1).value == 'דתות':
      i+=2
      while sheet.cell(row=i, column=1).value != 'מגבלות בקשות' and i<60:
        temp=sheet.cell(row=i, column=3).value 
        if temp == 1:
            j=i
            religion=sheet.cell(row=j, column=1).value
            if religion not in general_religions_list:
                print("Error with religion: " + str(religion))
                print("ReadData")
                sys.exit()

            name_of_religion= sheet.cell(row=j, column=2).value
            #Validtion for religions
            if  None == name_of_religion or ' ' == name_of_religion:
             print("Error with name_of_religion in ReadData")
             sys.exit()
            #Check if default
            if sheet.cell(row=j, column=4).value == 'כן':
                default_religion=True
            else:
                default_religion=False

            religions_list.append({
            "religion":religion,
            "name_of_religion":name_of_religion,
            "default_religion":default_religion,
            })

            i+=1

        else:
           i+=1  
    # else:
    #     print("There are no religions!")
    #     print("ReadData")
    #     sys.exit()

def get_application_and_company():
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
    global type
    global stage    
    global plan
    global max_employees
    global color_palette
    global usability_check
    global active 

    #From Excel
    app_name=sheet.cell(row=13, column=2).value
    if app_name == None:
        print( "ReadData")
        print( "No app_name")
        sys.exit()
    app_name=app_name.strip()
    display_name=sheet.cell(row=14, column=2).value
    if display_name == None:
        print( "ReadData")
        print( "No display_name")
        sys.exit()
    display_name=display_name.strip()
    company_name=sheet.cell(row=12, column=2).value
    if company_name != None:
        company_name=company_name.strip()
    language=sheet.cell(row=15, column=2).value
    if language not in general_languages:
        print( "ReadData")
        print( "No language")
        sys.exit()
    time_zone=sheet.cell(row=16, column=2).value
    time_zone=time_zone.strip()
    country_code=sheet.cell(row=17, column=2).value
    first_day_of_week=sheet.cell(row=18, column=2).value
    if first_day_of_week not in full_name_days_of_week:
        print( "ReadData")
        print( "No first_day_of_week")
        sys.exit()
    first_day_of_weekend=sheet.cell(row=19, column=2).value
    if first_day_of_weekend not in full_name_days_of_week:
        print( "ReadData")
        print( "No first_day_of_weekend")
        sys.exit()
    last_day_for_subbmit_shifts=sheet.cell(row=20, column=2).value
    if last_day_for_subbmit_shifts not in full_name_days_of_week:
        print( "ReadData")
        print( "No first_day_of_weekend")
        sys.exit()
    last_hour_for_subbmit_shifts=sheet.cell(row=21, column=2).value
    if not isinstance(last_hour_for_subbmit_shifts, time): 
        print( "ReadData")
        print( "last_hour_for_subbmit_shifts is not in time format")
        sys.exit()
    password_security_level=sheet.cell(row=22, column=2).value
    account_number=sheet.cell(row=23, column=2).value

    #From webstie
    industry='Restaurants' 
    type= 'P' #Planned work scedule
    stage= 0
    plan= 0
    max_employees= -1
    color_palette='palette-blue'
    usability_check= True
    active= True

    #Permissions
    get_groups()
    TestData.test_groups(perrmisions_list)

   #Religions
    get_religions()
    TestData.test_religions(religions_list)
     
def get_owners():
 i=3
 while sheet.cell(row=i, column=1).value != 'שם חברה' and sheet.cell(row=i, column=1).value !='שם משתמש' and i<30:
        i+=1
 if sheet.cell(row=i, column=1).value =='שם חברה' or i== 30:
     return "Couldnt find owner details " #Not necessarily an error- sheet2
 if sheet.cell(row=i, column=1).value =='שם משתמש': 
    j=2 
    for x in range(2):
     if sheet.cell(row=i, column=j+x).value != None and sheet.cell(row=i, column=j+x).value != ' ' : #Check if user name exist

        password=sheet.cell(row=i+1, column=j+x).value
        if password == None or password == ' ' or len(password)<8: #Password validation
            print("No password for owner OR invalid password, its mandatory")
            print("ReadData")
            sys.exit()

        full_name =sheet.cell(row=i+3, column=j+x).value
        if full_name == None:
            print("No name for owner, its mandatory")
            print("ReadData")
            sys.exit()
        full_name =full_name.split(' ')
        first_name=full_name[0]
        if len (full_name) == 1:
            last_name=None
        elif len (full_name) == 2:
            last_name=full_name[1]
        elif len (full_name) > 2:
            last_name=full_name[1] + ' ' + full_name[2]
    

        phone_number=sheet.cell(row=i+5, column=2+x).value
        if phone_number == None:
            print("No phone for owner, its mandatory")
            print("ReadData")
            sys.exit()

        owner_details.append(
        {
            "user_name":sheet.cell(row=i, column=j+x).value,
            "password":password,
            "group":sheet.cell(row=i+2, column=j+x).value,
            "first_name":first_name,
            "last_name":last_name,
            "email":sheet.cell(row=i+4, column=2+x).value,
            "phone_number":phone_number
        })
  
def get_roles():
 i=7
 if sheet.cell(row=i, column=8).value == None:
     print("ReadData")
     print("No roles found")
     print ("i = "+str(i)+ " j=8")
     sys.exit()
 while sheet.cell(row=i, column=8).value != None:
        if sheet.cell(row=i, column=8).value not in roles:
            roles.append(sheet.cell(row=i, column=8).value)
            i+=2
            continue
        else:
            print(sheet.cell(row=i, column=8).value)
            print("Error!!! This role is allready in the list!!!")
            print("ReadData")
            sys.exit()
 if sheet.cell(row=i+2, column=8).value != None and sheet.cell(row=i+2, column=8).value != ' ':
            print("Error!!! There are spaces with roles!!!")
            print("ReadData")
            sys.exit()
     
def get_shifts():
    i = 4
    j = 9
    flag = True

    while flag:
        roles_per_shift = []  
        if (sheet.cell(row=i, column=j).value is None 
            or sheet.cell(row=i, column=j).value =='' 
            or sheet.cell(row=i, column=j).value == "משמרת1"):

            flag = False 
            break   

        shift_name = sheet.cell(row=i, column=j).value 
        shift_name=shift_name.strip()
        continuously=sheet.cell(row=i+2, column=j).value
        if continuously not in continuously_list:
            print("Error, continuously is not correct")
            print("ReadData")
            sys.exit()
        loop_on_roles=i+3
        for counter in range(len(roles)):
         if sheet.cell(row=loop_on_roles, column=j).value is not None : #check if the shift is the same shift
            if shift_name != sheet.cell(row=loop_on_roles, column=j).value.strip():
                        print("Error, the shifts are not coordinate")
                        print("ReadData")
                        sys.exit()
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
    
    #Checking whether the existing number of shifts matches the list of shifts on the right side of the table
    TestData.test_shifts(shifts,sheet)

def get_locations():
 global sum_of_roles_for_locations
 sum_of_roles_for_locations=0
 i=8
 j=8
 if sheet.cell(row=i, column=j).value == None and i==8:
     locations.clear()
     print() #No locations 
 while sheet.cell(row=i, column=j).value != None:
        name_of_location= sheet.cell(row=i, column=j).value
        name_of_location=name_of_location.strip()
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
        sum_of_roles_for_locations+=len(roles_per_location)  

 TestData.test_locations(locations,features,sum_of_roles_for_locations,roles)

def split_shifts_for_limits(shifts):
     if ',' in shifts:
        return shifts.split(',')
     else:
        return shifts.split('/') 

def convert_days_to_range_for_limist(days_for_requests_limits):
   days= []
   temp1=days_for_requests_limits[0]
   temp2=days_for_requests_limits[1]
   try:
    index = days_of_week.index(temp1)
    days.append(index+1)
    index = days_of_week.index(temp2)
    days.append(index+1)
    days=list(range(days[0], days[-1] + 1))
    return days
   except Exception as e:  # Catches any exception and stores it in 'e'
    print(f"An error occurred: {e}")

def convert_days_for_shabat(day):
   index = full_name_days_of_week.index(day)
   return index

def get_requests_limits():
 i=30
 global days_for_request_limit 
 global shift_daily
 days_for_request_limit=[]
 while sheet.cell(row=i, column=1).value != 'מגבלות בקשות' and sheet.cell(row=i, column=1).value !='הגדרת דוחות':
        i+=1
 if sheet.cell(row=i, column=1).value =='הגדרת דוחות':
        print("Error!!")
        print("Couldnt find requests limits")
        print("ReadData")
        sys.exit()

 if sheet.cell(row=i, column=1).value == 'מגבלות בקשות':      
    i+=2 # To get to the line of the first recive
    j=1
    flag = True
    while flag:
     if(sheet.cell(row=i, column=j).value != None 
        and sheet.cell(row=i, column=j).value !=''
        and  'משמרות לא רצויות' != sheet.cell(row=i, column=1).value
        and  'מגבלות קבלות' != sheet.cell(row=i, column=1).value):
         
         limit_name = sheet.cell(row=i, column=j).value.strip()

         if not isinstance(limit_name, str):
            print("Error!!")
            print("limit_name is not string")
            print("ReadData")
            sys.exit()

         
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

         if shift_daily == None or shift_daily == ' ' or not isinstance(shift_daily, str) :
            print("Error!!")
            print("shift / daily is not defined / type of string")
            print("ReadData")
            sys.exit()

             
         shift_daily=shift_daily.strip()
         if shift_daily == 'יומי':
             shift_daily='D'
         elif shift_daily =='משמרתי' :
             shift_daily='S'
         else:
            print("Error!!")
            print("shift / daily is not in the right format")
            print("ReadData")
            sys.exit()

         
         scala=sheet.cell(row=i, column=j+2).value
         
         if  scala == None or scala == ' ' or isinstance(scala, int) or  '-' not in scala:
            print("Error!!")
            print("scala is not defined - requests_limits")
            print("ReadData")
            sys.exit()            
           
         else:
            split_scala= scala.split('-')
            min=int(split_scala[0])
            max=int(split_scala[1])
         

         default=sheet.cell(row=i, column=j+3).value
         if  default == None or default == ' ' or not isinstance(default, int):
            print("Error!!")
            print("default  - requests_limits")
            print("ReadData")
            sys.exit() 

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

     elif( i > 74 or  'הגדרת דוחות' == sheet.cell(row=i, column=1).value
              or 'מגבלות קבלות' == sheet.cell(row=i, column=1).value
              or 'משמרות לא רצויות' == sheet.cell(row=i, column=1).value):
            flag=False
            return 
     else:
            i+=1
      
    else:
        print("Error!!")
        print("Couldnt find requests limits")
        print("ReadData")
        sys.exit()

def get_receives_limits():
 global shift_daily
 i=45
 while sheet.cell(row=i, column=1).value != 'מגבלות קבלות' and sheet.cell(row=i, column=1).value !='הגדרת דוחות':
        i+=1
 if sheet.cell(row=i, column=1).value =='הגדרת דוחות':
        print("Error!!")
        print("Couldnt find receives limits")
        print("ReadData")
        sys.exit()
 if sheet.cell(row=i, column=1).value =='מגבלות קבלות':      
    i+=2
    j=1
    flag = True
    while flag:
        if sheet.cell(row=i, column=j).value != None and sheet.cell(row=i, column=j).value !=''and 'הגדרת דוחות' != sheet.cell(row=i, column=1).value:
         limit_name = sheet.cell(row=i, column=j).value.strip()

         if not isinstance(limit_name, str):
            print("Error!!")
            print("limit_name is not string")
            print("ReadData")
            sys.exit()

         shift_for_limit=sheet.cell(row=i, column=j+1).value

         if shift_for_limit == None or shift_for_limit =='':
             print("Error, coludent find shifts for limits") 
             print("i="+str(i)+" , j = "+ str(j))
             print("ReadData")
             sys.exit()

         shift_for_limit=shift_for_limit.strip()
         
         shift_daily=None # To cancel the previous setting from requests limits

         if ',' in shift_for_limit or '/'in shift_for_limit:
          shift_for_limit = split_shifts_for_limits(shift_for_limit)  
          TestData.test_shift_for_receives_limits(shift_for_limit,shifts)
         elif shift_for_limit == "כולם" or shift_for_limit == "כל המשמרות" :
             shift_for_limit = [item["name"] for item in shifts if "name" in item]
             shift_daily='S'
         else: #Only one shift 
            for t in range(len(shifts)):
                temp_shifts=shifts[t]
                name_of_shift= temp_shifts["name"]
                if shift_for_limit == name_of_shift:
                    shift_for_limit=[name_of_shift]
                    shift_daily = 'S'
                    break

         if shift_daily == None:
             print("Error, coludent find shifts for limits") 
             print("ReadData")
             sys.exit()
         

         scala=sheet.cell(row=i, column=j+2).value
         if scala == None or scala == ' ' or isinstance(scala, int) or  '-' not in scala:
            print("Error!!")
            print("scala is not defined - requests_limits")
            print("ReadData")
            sys.exit()            

         else: 
            split_scala= scala.split('-')
            min=int(split_scala[0])
            max=int(split_scala[1])


         default=sheet.cell(row=i, column=j+3).value
         if  default == None or default == ' ' or not isinstance(default, int):
            print("Error!!")
            print("default  - requests_limits")
            print("ReadData")
            sys.exit() 



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
        sys.exit()

def get_employee_configurations_fields():
 i=100
 while sheet.cell(row=i, column=1).value != 'שדות נוספים בכרטיס העובד' and sheet.cell(row=i, column=1).value !='הרשאות':
        i+=1
 if sheet.cell(row=i, column=1).value =='הרשאות':
     print("Error!")
     print("Couldnt find employee configurations")
     print("ReadData")
     sys.exit()

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

         configuration_name=configuration_name.strip()

         if configuration_name not in general_employee_configuration_list:
            print("Error")
            print("Cant find the configurationname ")
            sys.exit()  

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
 while sheet.cell(row=i, column=j).value != '''פיצ'רים נוספים'''and sheet.cell(row=i, column=j).value !='הגדרת חגים וימי מנוחה' and i<150:
  i+=1
      
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
      if shabat == 'חורף/קיץ' or shabat == "חורף / קיץ":
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
                shabat_end_day=convert_days_for_shabat(sheet.cell(row=i+2, column=t).value)
                shabat_end_hour=sheet.cell(row=i+3, column=t).value  
                shabat.append(
                {  
                    "name":"שבת",
                    "start_day":shabat_start_day,
                    "start_time":shabat_start_hour,
                    "end_day": shabat_end_day,
                    "end_time": shabat_end_hour,
                    "period":period,
                    "religions":[1],
                    "special_type":"AS",
                    "type":"R"
                }  )         
      holidays=sheet.cell(row=i+1, column=j).value
      automatic_holidays_special_cost=sheet.cell(row=i+2, column=j).value
      holidays_area=sheet.cell(row=i+3, column=j).value
      if holidays =="כן" or shabat == "אוטומטי":
          if holidays_area == None :
              print("Error! There is automatic holiday or Shabat and there is no area code")
              print("ReadData")
              sys.exit()
      return
 else:
     print("Error, no holidays!!")
     print("ReadData")
     sys.exit() 

def get_clock():
 global clock
 global clock_number
 global permissions_for_web_clock
 i=108
 j=1
 while sheet.cell(row=i, column=j).value != 'סוג שעון' and sheet.cell(row=i, column=1).value !='פושים' and i<200:
        i+=1
 if sheet.cell(row=i, column=j).value =='פושים':
     print("Error, couldent find clock")
     print("ReadData")
     sys.exit()

 if sheet.cell(row=i, column=j).value == 'סוג שעון':
     clock=sheet.cell(row=i, column=j+1).value
     if clock in general_clock_list:
      if 'אפליקציה' in clock:
            permissions_for_web_clock= sheet.cell(row=i, column=j+2).value
            if permissions_for_web_clock == None or permissions_for_web_clock==' ' :
             permissions_for_web_clock=perrmisions_list # Case when the web clock is not spesific for groups
            elif ',' in permissions_for_web_clock:
             permissions_for_web_clock = permissions_for_web_clock.split(',')
             TestData.test_web_clock(permissions_for_web_clock,perrmisions_list)
            elif ',' not in permissions_for_web_clock :
             permissions_for_web_clock=[]
             permissions_for_web_clock.append(sheet.cell(row=i, column=j+2).value) 

      clock_number=sheet.cell(row=i+1, column=j+1).value
     else:
      print("Error, couldent find clock")
      print("ReadData")
      sys.exit()   
     

 else:
     print("Error, couldent find clock")
     print("ReadData")
     sys.exit()

def get_features():
 global features
 global vacation_days
 vacation_days=None
 i=70
 j=1
 while sheet.cell(row=i, column=j).value != '''פיצ'רים נוספים'''and sheet.cell(row=i, column=1).value !='חוקי עבודה' and i < 180:
        i+=1

 if sheet.cell(row=i, column=j).value == '''פיצ'רים נוספים''':
     i+=1
     while sheet.cell(row=i, column=1).value !='חוקי עבודה' and i < 180:
        if sheet.cell(row=i, column=2).value == 'כן':
            if sheet.cell(row=i, column=1).value == 'חופשות':
                if sheet.cell(row=i, column=3).value != None:
                    vacation_days=14  
            if sheet.cell(row=i, column=1).value == 'מסמכים':
                if any( d.get('name') == 'תאריך תחילת עבודה' for d in employee_configurations):
                    if any( d.get('name') == 'תעודת זהות' for d in employee_configurations):
                        print()
                    else:
                        print("Warning!!")
                        print("There is no employee_configurations תעודת זהות'!!")
                        print("ReadData")
                else:
                    print("Warning!!")
                    print("There is no employee_configurations of תאריך תחילת עבודה !!")
                    print("ReadData")
            if sheet.cell(row=i, column=1).value in general_features_list:
                features.append(sheet.cell(row=i, column=1).value)
            else:
             print("Error, couldent find feature")
             print("ReadData")
             sys.exit() 

            i+=1
        else:
            i+=1
 else:
     print("Error, couldent find features")
     print("ReadData")
     sys.exit()

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
 while (sheet.cell(row=i, column=j).value is None or 
       ('חיתוך שעות' not in str(sheet.cell(row=i, column=j).value))) and i < 300:
        
        i+=1
 if sheet.cell(row=i, column=j).value =='הערות':
     print("Error, didnt find cutting houers!!")
     print("ReadData")
     sys.exit()
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
         group= return_perrmisions_id(group)
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
     print("Error, couldent find cutting hours in the table")
     print("ReadData")
     sys.exit()

def read_all_data(sheet_from_API):
    global sheet
    global perrmisions_list
    global religions_list
    global locations
    global  owner_details
    global roles
    global shifts
    global requests_limits
    global receives_limits
    global employee_configurations
    global features

    sheet=sheet_from_API
    perrmisions_list=[]
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
    TestData.test_the_sheet(sheet)
    get_application_and_company()
    get_owners()
    get_roles()
    get_shifts()
    get_requests_limits()
    get_receives_limits()
    get_holidays()
    get_features()
    TestData.test_features(features,perrmisions_list)
    get_locations()
    get_clock()
    get_employee_configurations_fields()
    get_cutting_hours()
