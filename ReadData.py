from datetime import time
import TestData
import utils
import sys

general_perrmisions_list =['Headquarters','Owners','Managers','Junior-Managers','Senior Sub-Managers','Sub-Managers','Senior-employess','Senior Employees','Employees','Junior Employees','Automation']
general_religions_list =['Jewish','Christian','Muslim','Foreign']
general_languages=['עברית','אנגלית','אנגלית (USA)','אנגלית (UK)','אנגלית (ISR)','אנגלית (Tabit US)']
general_country_codes=['ישראל','ארה"ב','אנגליה','רוסיה']
general_features_list=['לייבור קוסט - LC','עלויות',"פיצ'ר ג'ירפות - הגדרה מראש עם אצבע","פיצ'ר סינטות - תכנון הפסקות",'חופשות','החלפות','היעדרויות','נסיעות','מסמכים','טפסי 101',"פיצ'ר נונו מימי - סידור מפוצל",'משימות','חיתוך שעות']
general_clock_list= ['ביומטרי','אפליקציה (Web clock)','תוכנתי (Install clock)','טאביט','ללא שעון']
general_employee_configuration_list = ['תעודת זהות','עיר','כתובת','מיקוד','תאריך תחילת עבודה','תאריך סיום עבודה','דת','מזהה שעון','מספר עובד לשכר','תפקיד ראשי']
continuously_list=[0,1,2,3]
genral_security_list=['גבוהה (שליחת פרטי התחברות)','גבוהה','נמוכה','חידוש סיסמה בהתחברות הראשונה']
days_of_week=['א','ב','ג','ד','ה','ו','ש']
full_name_days_of_week=['ראשון','שני','שלישי','רביעי','חמישי','שישי','שבת']

VALIDATE_DATA=True
ERRORS_MESSAGES=[]

def get_groups():
    global default_perrmision
    i = 5
    while i < 50:
        val = sheet.cell(row=i, column=1).value
        if val in ['דתות', 'קבוצות - הרשאות ניהול']:
            break
        i += 1

    if sheet.cell(row=i, column=1).value != 'קבוצות - הרשאות ניהול':
        TestData.error_exit("Cant find gruops!", ERRORS_MESSAGES)

    i += 2
    while i < 50 and sheet.cell(row=i, column=1).value != 'דתות':
        if sheet.cell(row=i, column=3).value == 1:
            group = sheet.cell(row=i, column=1).value
            TestData.test_in_list(group, general_perrmisions_list, "group", ERRORS_MESSAGES)
            name_of_group = TestData.test_not_none_and_strip(sheet.cell(row=i, column=2).value, "name_of_group", ERRORS_MESSAGES)
            default_perrmision = (sheet.cell(row=i, column=4).value == 'כן')
            perrmisions_list.append({
                "group": group,
                "name_of_group": name_of_group,
                "default_gruop": default_perrmision,
            })
        i += 1

    if sheet.cell(row=i, column=1).value == 'דתות':
        return

def get_religions():
    global default_religion
    i = 10
    while i < 60 and sheet.cell(row=i, column=1).value not in ('דתות', 'מגבלות בקשות'):
        i += 1
    if sheet.cell(row=i, column=1).value == 'דתות':
        i += 2
        while i < 60 and sheet.cell(row=i, column=1).value != 'מגבלות בקשות':
            if sheet.cell(row=i, column=3).value == 1:
                religion = sheet.cell(row=i, column=1).value
                TestData.test_in_list(religion,general_religions_list,"religion",ERRORS_MESSAGES)#Cheack if religion exist
                name_of_religion = sheet.cell(row=i, column=2).value
                name_of_religion=TestData.test_not_none_and_strip(name_of_religion,"Error with name_of_religion",ERRORS_MESSAGES)
                default_religion = (sheet.cell(row=i, column=4).value == 'כן')
                religions_list.append({
                    "religion": religion,
                    "name_of_religion": name_of_religion,
                    "default_religion": default_religion,
                })
            i += 1
    else:
     TestData.error_exit("Cant find religions!",ERRORS_MESSAGES)

def get_application_and_company():
    global app_name, display_name, company_name, language, time_zone, country_code, first_day_of_week, first_day_of_weekend
    global last_day_for_subbmit_shifts, last_hour_for_subbmit_shifts, password_security_level, account_number
    global industry, type, stage, plan, max_employees, color_palette, usability_check, active
     
    app_name=sheet.cell(row=13, column=2).value
    app_name=TestData.test_not_none_and_strip(app_name, "app_name",ERRORS_MESSAGES)
    display_name=sheet.cell(row=14, column=2).value
    display_name=TestData.test_not_none_and_strip(display_name, "display_name",ERRORS_MESSAGES)
    company_name=sheet.cell(row=12, column=2).value
    if company_name != None : #Case of 2 applicaitons - If its 2 apps, in API it will not create another comapny
        company_name=TestData.test_not_none_and_strip(company_name, "company_name",ERRORS_MESSAGES)
    language=sheet.cell(row=15, column=2).value
    TestData.test_in_list(language,general_languages,"language",ERRORS_MESSAGES)
    time_zone=sheet.cell(row=16, column=2).value
    time_zone=TestData.test_not_none_and_strip(time_zone, "time_zone",ERRORS_MESSAGES)
    country_code=sheet.cell(row=17, column=2).value
    TestData.test_in_list(country_code,general_country_codes,"country_code",ERRORS_MESSAGES)
    first_day_of_week=sheet.cell(row=18, column=2).value
    TestData.test_in_list(first_day_of_week,full_name_days_of_week,"first_day_of_week",ERRORS_MESSAGES)
    first_day_of_weekend=sheet.cell(row=19, column=2).value
    TestData.test_in_list(first_day_of_weekend,full_name_days_of_week,"first_day_of_weekend",ERRORS_MESSAGES)
    last_day_for_subbmit_shifts=sheet.cell(row=20, column=2).value
    TestData.test_in_list(first_day_of_weekend,full_name_days_of_week,"first_day_of_weekend",ERRORS_MESSAGES)
    last_hour_for_subbmit_shifts=sheet.cell(row=21, column=2).value
    TestData.test_type(last_hour_for_subbmit_shifts, time, "last_hour_for_subbmit_shifts",ERRORS_MESSAGES)
    password_security_level=sheet.cell(row=22, column=2).value
    password_security_level=TestData.test_not_none_and_strip(password_security_level,"password_security_level",ERRORS_MESSAGES)
    TestData.test_in_list(password_security_level,genral_security_list,"password_security_level",ERRORS_MESSAGES)
    account_number=sheet.cell(row=23, column=2).value
    if account_number != None:
         TestData.test_type(account_number, int, "account_number",ERRORS_MESSAGES)
    
    #From webstie- default
    industry='Restaurants' 
    type= 'P' #Planned work scedule
    stage= 0
    plan= 0
    max_employees= -1
    color_palette='palette-blue'
    usability_check= True
    active= True

    get_groups()
    TestData.test_groups(perrmisions_list,ERRORS_MESSAGES)

    get_religions()
    TestData.test_religions(religions_list,ERRORS_MESSAGES)
     
def get_owners():
    i = 3
    while i < 30 and sheet.cell(row=i, column=1).value not in ['שם חברה', 'שם משתמש']:
        i += 1
    if sheet.cell(row=i, column=1).value == 'שם חברה' or i == 30:
        return "Couldnt find owner details "
    if sheet.cell(row=i, column=1).value == 'שם משתמש':
        j = 2
        for x in range(2):
            user = sheet.cell(row=i, column=j+x).value
            if user  is not None:
                user = TestData.test_not_none_and_strip(user, "user", ERRORS_MESSAGES)
                password = TestData.test_not_none_and_strip(sheet.cell(row=i+1, column=j+x).value, "password", ERRORS_MESSAGES)
                if len(password) < 8:
                    TestData.error_exit("Password to short", ERRORS_MESSAGES)
                full_name = TestData.test_not_none_and_strip(sheet.cell(row=i+3, column=j+x).value, "full_name", ERRORS_MESSAGES)
                names = full_name.split() if full_name else []
                first_name = names[0] if names else ""
                last_name = None if len(names) == 1 else (names[1] if len(names) == 2 else f"{names[1]} {names[2]}")
                phone_number = TestData.test_not_none_and_strip(sheet.cell(row=i+5, column=2+x).value, "phone_number", ERRORS_MESSAGES)
                if phone_number is not None:
                    phone_number = str(phone_number)
                    if phone_number.startswith("5"):
                        phone_number = "0" + phone_number
                    elif phone_number.startswith("972"):
                        phone_number = "0" + phone_number[3:]
                owner_details.append({
                    "user_name": user,
                    "password": password,
                    "group": sheet.cell(row=i+2, column=j+x).value,
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": sheet.cell(row=i+4, column=2+x).value,
                    "phone_number": phone_number
                })
 
def get_roles():
 i=7
 if sheet.cell(row=i, column=8).value == None:
     TestData.error_exit("No roles found i = "+str(i)+ " j=8",ERRORS_MESSAGES)
     return
 while sheet.cell(row=i, column=8).value != None:
        if sheet.cell(row=i, column=8).value not in roles:
            roles.append(sheet.cell(row=i, column=8).value)
            i+=2
            continue
        else:
             TestData.error_exit(str(sheet.cell(row=i, column=8).value)+ "This role is allready in the list: " ,ERRORS_MESSAGES)
             return
 if sheet.cell(row=i+2, column=8).value != None and sheet.cell(row=i+2, column=8).value != ' ':
            TestData.error_exit(" There are spaces with roles!!! " ,ERRORS_MESSAGES)

def get_shifts():
    i = 4
    j = 9
    flag = True

    while flag:
        shift_name = sheet.cell(row=i, column=j).value
        if shift_name in (None, '', "משמרת1"):
            break

        shift_name = shift_name.strip()
        continuously = sheet.cell(row=i+2, column=j).value
        TestData.test_in_list(continuously, continuously_list, "continuously", ERRORS_MESSAGES)

        roles_per_shift = []
        loop_on_roles = i + 3
        for _ in range(len(roles)):
            cell_shift = sheet.cell(row=loop_on_roles, column=j).value
            if cell_shift and isinstance(cell_shift, str):
                if shift_name != cell_shift.strip():#Case when shift_name not the same shift of cell_shift
                    TestData.error_exit("Shifts are not coordinate", ERRORS_MESSAGES)
                    
                roles_per_shift.append(sheet.cell(row=loop_on_roles, column=8).value)
            loop_on_roles += 2

        shifts.append({
            "name": shift_name,
            "roles": roles_per_shift,
            "continuously": continuously
        })
        j += 1
        i = 4
    TestData.test_shifts(shifts, sheet,ERRORS_MESSAGES)
    
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

 TestData.test_locations(locations,features,sum_of_roles_for_locations,roles,ERRORS_MESSAGES)

def get_requests_limits():
    global days_for_request_limit, shift_daily
    i = 30
    days_for_request_limit = []
    while i < 100 and sheet.cell(row=i, column=1).value not in ('מגבלות בקשות', 'הגדרת דוחות'):
        i += 1
    if sheet.cell(row=i, column=1).value == 'הגדרת דוחות' or i == 100:
        TestData.error_exit("Couldnt find requests limits", ERRORS_MESSAGES)
        return
    if sheet.cell(row=i, column=1).value != 'מגבלות בקשות':
        TestData.error_exit("Couldnt find requests limits", ERRORS_MESSAGES)
        return

    i += 2  # Move to the first record
    while True:
        limit_name = sheet.cell(row=i, column=1).value
        if i > 74 or limit_name in ('הגדרת דוחות', 'מגבלות קבלות', 'משמרות לא רצויות'):
            return
        if not limit_name or limit_name == '':
            i += 1
            continue
        if isinstance(limit_name, str):
            limit_name = limit_name.strip()
        if '-' in limit_name:
            days_for_request_limit = limit_name.split('-')
            days_for_request_limit[0] = days_for_request_limit[0][-1]
            days_for_request_limit = utils.convert_days_to_range_for_limist(days_for_request_limit,days_of_week,ERRORS_MESSAGES)
        elif limit_name == 'מינימום בקשות סופש':
            if not requests_limits:
                days_for_request_limit = [6, 7]
            else:
                last_day = requests_limits[-1]["days"][-1]
                days_for_request_limit = [1, 2] if int(last_day) == 7 else [int(last_day) + 1, int(last_day) + 2]

        shift_daily = sheet.cell(row=i, column=5).value  # column j+4 where j is 1
        shift_daily = TestData.test_not_none_and_strip(shift_daily, "shift_daily", ERRORS_MESSAGES)
        if shift_daily == 'יומי':
            shift_daily = 'D'
        elif shift_daily == 'משמרתי':
            shift_daily = 'S'
        else:
            TestData.error_exit("shift / daily is not in the right format-requests_limits", ERRORS_MESSAGES)

        scala = sheet.cell(row=i, column=3).value  # column j+2 where j is 1
        if scala and isinstance(scala, str) and '-' in scala:
            min_val, max_val = map(int, scala.split('-'))
        else:
            TestData.error_exit("Scala is not defined - requests_limits", ERRORS_MESSAGES)
            min_val, max_val = None, None

        default = sheet.cell(row=i, column=4).value  # column j+3 where j is 1
        if default is None or default == ' ' or not isinstance(default, int):
            TestData.error_exit("default  - requests_limits", ERRORS_MESSAGES)

        requests_limits.append({
            "name": limit_name,
            "type": 'Req',
            "days": days_for_request_limit,
            "shift_daily": shift_daily,
            "min": min_val,
            "max": max_val,
            "default": default,
        })
        i += 1

def get_receives_limits():
    global shift_daily
    i = 45
    while i < 100 and sheet.cell(row=i, column=1).value not in ('מגבלות קבלות', 'הגדרת דוחות'):
        i += 1
    if i == 100 or sheet.cell(row=i, column=1).value == 'הגדרת דוחות':
        TestData.error_exit("Couldnt find receives limits", ERRORS_MESSAGES)
        return
    if sheet.cell(row=i, column=1).value != 'מגבלות קבלות':
        TestData.error_exit("Couldnt find recives limits", ERRORS_MESSAGES)
        return

    i += 2  
    j = 1
    while True:
        if i > 84 or sheet.cell(row=i, column=1).value == 'הגדרת דוחות':
            return
        limit_name = sheet.cell(row=i, column=j).value
        if limit_name:
            if isinstance(limit_name, str):
                limit_name = limit_name.strip()

            shift_for_limit = TestData.test_not_none_and_strip(sheet.cell(row=i, column=j+1).value, "shift_for_limit", ERRORS_MESSAGES)
            shift_daily = None
            if ',' in shift_for_limit or '/' in shift_for_limit:
                shift_for_limit = utils.split_shifts_for_limits(shift_for_limit)
                shift_daily = TestData.test_shift_for_receives_limits(shift_for_limit, shifts, ERRORS_MESSAGES)
            elif shift_for_limit in ("כולם", "כל המשמרות"):
                shift_for_limit = [item["name"] for item in shifts if "name" in item]
                shift_daily = 'S'
            else:
                shift_daily = TestData.test_shift_for_receives_limits(shift_for_limit, shifts, ERRORS_MESSAGES)

            if shift_daily is None:
                TestData.error_exit("Coludent find shift_daily for limits - receives_limits", ERRORS_MESSAGES)

            scala = sheet.cell(row=i, column=j+2).value
            if scala and isinstance(scala, str) and '-' in scala:
                min_val, max_val = map(int, scala.split('-'))
            else:
                TestData.error_exit("Scala is not defined - receives_limits", ERRORS_MESSAGES)
                min_val, max_val = None, None

            default = sheet.cell(row=i, column=j+3).value
            if default is None or default == ' ' or not isinstance(default, int):
                TestData.error_exit("default  - requests_limits", ERRORS_MESSAGES)

            is_global = sheet.cell(row=i, column=j+4).value
            if is_global is None:
                is_global = False
            elif "כן" in str(is_global):
                shift_daily = 'D'
                is_global = True

            receives_limits.append({
                "name": limit_name,
                "shifts": shift_for_limit,
                "type": 'Rec',
                "shift_daily": shift_daily,
                "min": min_val,
                "max": max_val,
                "default": default,
                "is_global": is_global
            })
            i += 1
        else:
            i += 1
#This function is for yearly or summer and winter Shabat
def get_shabat_details(i, j, shabat_value, ERRORS_MESSAGES):
    t = j
    while sheet.cell(row=i, column=t).value != "יום התחלה" and t < 20:
        t += 1
    if t == 20:
        TestData.error_exit(f"Couldn't find start day of Shabat ({shabat_value})", ERRORS_MESSAGES)
        return None
    t += 1
    if shabat_value == 'שנתי':
        return {
            "name": "שבת",
            "start_day": utils.convert_days_for_shabat(sheet.cell(row=i, column=t).value,full_name_days_of_week),
            "start_time": sheet.cell(row=i+1, column=t).value,
            "end_day": utils.convert_days_for_shabat(sheet.cell(row=i+2, column=t).value,full_name_days_of_week),
            "end_time": sheet.cell(row=i+3, column=t).value,
            "period": 'Y',
            "religions": [1],
            "special_type": "AS",
            "type": "R"
        }
    elif shabat_value in ('חורף/קיץ', "חורף / קיץ"):
        shabat_list = []
        for period in ['W', 'S']:
            t += 1
            shabat_list.append({
                "name": "שבת",
                "start_day": utils.convert_days_for_shabat(sheet.cell(row=i, column=t).value),
                "start_time": sheet.cell(row=i+1, column=t).value,
                "end_day": utils.convert_days_for_shabat(sheet.cell(row=i+2, column=t).value),
                "end_time": sheet.cell(row=i+3, column=t).value,
                "period": period,
                "religions": [1],
                "special_type": "AS",
                "type": "R"
            })
        return shabat_list
    else:
        return None

def get_holidays():
    global shabat, holidays, automatic_holidays_special_cost, holidays_area
    i, j = 60, 1
    while sheet.cell(row=i, column=j).value not in ("'''פיצ'רים נוספים'''", 'הגדרת חגים וימי מנוחה') and i < 150:
        i += 1
      
    if sheet.cell(row=i, column=j).value != 'הגדרת חגים וימי מנוחה':
        TestData.error_exit("Error, no holidays!!", ERRORS_MESSAGES)
        return

    i, j = i + 1, j + 1 
    shabat_value = sheet.cell(row=i, column=j).value
    if shabat_value in ('שנתי', 'חורף/קיץ', "חורף / קיץ"):
        shabat = get_shabat_details(i, j, shabat_value, ERRORS_MESSAGES)
    else: #Automatic or without shabat 
         shabat=shabat_value
    holidays = sheet.cell(row=i+1, column=j).value
    automatic_holidays_special_cost = sheet.cell(row=i+2, column=j).value
    holidays_area = sheet.cell(row=i+3, column=j).value
    if holidays == "כן" or shabat_value == "אוטומטי":
        if holidays_area is None:
            TestData.error_exit("Error! There is automatic holiday or Shabat and there is no area code", ERRORS_MESSAGES)
    return

def get_clock():
    global clock, clock_number, permissions_for_web_clock
    i, j = 108, 1
    while sheet.cell(row=i, column=j).value not in ['סוג שעון', 'פושים'] and i < 200:
        i += 1
    if sheet.cell(row=i, column=j).value == 'פושים':
        TestData.error_exit("Error, couldent find clock",ERRORS_MESSAGES)
        return
    
    if sheet.cell(row=i, column=j).value == 'סוג שעון':
        clock = sheet.cell(row=i, column=j+1).value
        if clock in general_clock_list:
            if 'אפליקציה' in clock:
                permissions_for_web_clock = sheet.cell(row=i, column=j+2).value
                if not permissions_for_web_clock or permissions_for_web_clock == ' ':
                    permissions_for_web_clock = perrmisions_list
                elif ',' in permissions_for_web_clock:
                    permissions_for_web_clock = permissions_for_web_clock.split(',')
                    TestData.test_web_clock(permissions_for_web_clock, perrmisions_list)
                else:
                    permissions_for_web_clock = [sheet.cell(row=i, column=j+2).value]
            clock_number = sheet.cell(row=i+1, column=j+1).value
        else:
            TestData.error_exit("Error, couldent find clock",ERRORS_MESSAGES)
    else:
        TestData.error_exit("Error, couldent find clock",ERRORS_MESSAGES)

def get_features():
    global features, vacation_days
    vacation_days = None
    i, j = 70, 1

    while sheet.cell(row=i, column=j).value not in ("פיצ'רים נוספים", "חוקי עבודה") and i < 180:
        i += 1

    if sheet.cell(row=i, column=j).value == "פיצ'רים נוספים":
        i += 1
        while sheet.cell(row=i, column=1).value != 'חוקי עבודה' and i < 180:
            if sheet.cell(row=i, column=2).value == 'כן':
                feature = sheet.cell(row=i, column=1).value
                if feature == 'חופשות' and sheet.cell(row=i, column=3).value is not None:
                    vacation_days = 14
                elif feature == 'מסמכים':
                    names = {d.get('name') for d in employee_configurations}
                    if 'תאריך תחילת עבודה' not in names:
                        print("Warning!!\n There is no employee_configurations of תאריך תחילת עבודה \nReadData")
                    elif 'תעודת זהות' not in names:
                        print("Warning!!\n There is no employee_configurations תעודת זהות' \nReadData")
                elif feature in general_features_list:
                    features.append(feature)
                else:
                    TestData.error_exit("Couldent find feature", ERRORS_MESSAGES)
            i += 1
    else:
        TestData.error_exit("Couldent find features", ERRORS_MESSAGES)

def get_employee_configurations_fields():
    i = 100
    while sheet.cell(row=i, column=1).value not in ['שדות נוספים בכרטיס העובד', 'הרשאות']:
        i += 1
    if sheet.cell(row=i, column=1).value == 'הרשאות':
        TestData.error_exit("Couldnt find employee configurations",ERRORS_MESSAGES)

    if sheet.cell(row=i, column=1).value == 'שדות נוספים בכרטיס העובד':
        i += 2
        while True:
            if sheet.cell(row=i, column=1).value in [None, 'הרשאות', '']:
                return
            configuration_name = sheet.cell(row=i, column=1).value
            if configuration_name:
                configuration_name = configuration_name.strip()
                document = configuration_name == "מספר עובד לשכר"
                excel = sheet.cell(row=i, column=2).value == "כן"
                report = sheet.cell(row=i, column=3).value == "כן"
                if report or excel:
                    if configuration_name not in general_employee_configuration_list:
                        TestData.error_exit("Error\nCant find the configuration name",ERRORS_MESSAGES)
  
                    employee_configurations.append({
                        "name": configuration_name,
                        "excel": excel,
                        "report": report,
                        "document": document
                    })
            i += 1

def get_cutting_hours():
    global cutting_hours
    cutting_hours = []
    i, j = 150, 1
    while (sheet.cell(row=i, column=j).value is None or 'חיתוך שעות' not in str(sheet.cell(row=i, column=j).value)) and i < 300:
        i += 1
    if sheet.cell(row=i, column=j).value == 'הערות':
        TestData.error_exit("Didnt find cutting houers",ERRORS_MESSAGES)
    if 'חיתוך שעות' in sheet.cell(row=i, column=j).value:
        attribute = [57, 58, 59, 60]
        for counter in range(3):
            j = 1
            while j < 10:
                if sheet.cell(row=i, column=j+1).value == -1:
                    j += 1
                    continue
                value = sheet.cell(row=i, column=j+1).value
                #  group get the id number of the permission group 
                group = utils.return_perrmisions_id_ReadData(utils.find_groups_for_cutting_hours(i, j+1,sheet,general_perrmisions_list,ERRORS_MESSAGES))
                if any( d.get("group") == utils.retrun_permission_id_to_group(group) for d in perrmisions_list): #Cheack if its relevant to the groups allready added
                    cutting_hours.append({
                        "group_id": group,
                        "attribute": attribute[counter],
                        "value": value
                    })
                    j += 1
                else:
                    TestData.error_exit("Error, mismatch between cutting hours and groups in perrmisions_list ",ERRORS_MESSAGES)
                    return
            if j == 10:
                i += 1
    else:
         TestData.error_exit("Error, couldent find cutting hours in the table",ERRORS_MESSAGES)

def read_all_data(sheet_from_API):
    global sheet, perrmisions_list, religions_list, locations, owner_details, roles, shifts, requests_limits, receives_limits
    global employee_configurations, features

    sheet=sheet_from_API
    perrmisions_list, religions_list, locations, owner_details, roles = [], [], [], [], []  
    shifts, requests_limits, receives_limits, employee_configurations, features = [], [], [], [], []  

    TestData.test_the_sheet(sheet)
    get_application_and_company()
    get_owners()
    get_roles()
    get_shifts()
    get_requests_limits()
    get_receives_limits()
    get_holidays()
    get_features()
    TestData.test_features(features,perrmisions_list,ERRORS_MESSAGES)
    get_locations()
    get_clock()
    get_employee_configurations_fields()
    get_cutting_hours()
    if len(ERRORS_MESSAGES) != 0:
        print(ERRORS_MESSAGES)
        sys.exit()
