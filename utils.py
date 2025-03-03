import TestData
import WorldTimeZones
from deep_translator import GoogleTranslator
import requests
import json

################ ReadData ##########################
####################################################
def return_perrmisions_id_ReadData (group):
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
      
def split_shifts_for_limits(shifts):
     if ',' in shifts:
        return shifts.split(',')
     else:
        return shifts.split('/') 
     
def find_groups_for_cutting_hours(y,x,sheet,general_perrmisions_list,ERRORS_MESSAGES):
    while sheet.cell(row=y, column=x).value not in general_perrmisions_list and y > 120:
        y-=1
    if sheet.cell(row=y, column=x).value in general_perrmisions_list:
           return  sheet.cell(row=y, column=x).value
    else:
          TestData.error_exit("Couldent find groups for cutting houres",ERRORS_MESSAGES)

def convert_days_for_shabat(day,full_name_days_of_week):
   index = full_name_days_of_week.index(day)
   return index

def convert_days_to_range_for_limist(days_for_requests_limits,days_of_week,ERRORS_MESSAGES):
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
   except Exception as e: 
    TestData.error_exit("Error with converting days to range for limits",ERRORS_MESSAGES)


################ API ##############################
#################################################### 
high_groups_permissions = []

def choose_language(language):
    if language == 'עברית':
        return 'he'
    elif language == 'אנגלית':
        return 'en'
    elif language == 'אנגלית (ISR)':
        return 'en-il'
    elif language == 'אנגלית (USA)':
        return 'en-us'
    elif language == 'אנגלית (UK)':
        return 'en-gb'
    elif language == 'אנגלית (Tabit US)':
        return 'en-tabit'
    return language  

def choose_password_security_level(security_level_str):
    if "גבוהה (שליחת פרטי התחברות)" == security_level_str or "גבוהה" in security_level_str:
        return 3
    elif security_level_str == "נמוכה":
        return 1
    else:
        return 2

def account_number(value):
    if value is None:
        return 0
    return value

def choose_country_code(country_code):
    if country_code == 'ישראל':
        return "+972"
    elif "ארה" in country_code:  # ארה"ב
        return "+1"
    elif country_code == 'אנגליה':
        return "+44"
    else:
        return "+7"

def find_timezone(city_name, timezones):
    for tz in timezones:
        if city_name in tz:
            return tz
    return None

def choose_time_zone(hebrew_text):
    # Get the list of time zones from the WorldTimeZones module
    timezones = WorldTimeZones.TIME_ZONES
    
    # Translate the Hebrew time zone text to English
    translated = GoogleTranslator(source='auto', target='en').translate(hebrew_text)
    
    # Determine the time zone based on the translated text
    if '5' in translated or '4' in translated:
        tz = 'Asia/Jerusalem'
    else:
        tz = find_timezone(translated, timezones)
    
    # Fallback if no time zone was determined
    if tz is None:
        tz = 'Asia/Jerusalem'
    
    return tz

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
    
def convert_role_name_to_id(role_name,role_id,list):
     for i in range(len(list)):
       temp_list=list[i]
       roles=temp_list["roles"]
       for j in range(len(roles)):
            if roles[j]==role_name:
                 roles[j]=role_id
                 break

def return_perrmisions_id(group):
    if group == 'Headquarters':
        high_groups_permissions.append(10)
        return 10
    elif group == 'Owners':
        high_groups_permissions.append(7)
        return 7
    elif group == 'Managers':
        high_groups_permissions.append(2)
        return 2
    elif group == 'Junior-Managers':
        return 9
    elif group == 'Senior Sub-Managers':
        return 8
    elif group == 'Sub-Managers':
        return 3
    elif group == 'Senior Employees' or group == 'Senior-employess':
        return 11  
    elif group == 'Employees':
        return 4
    elif group == 'Junior Employees' or group == 'Junior-employees':
        return 5
    elif group == 'Automation':
        return 6
    else:
        print("Error!!")
        print("Could not find the id of the group")

def change_perrmision_to_english(permissions_list, index):
    temp = permissions_list[index]
    if temp['name_of_group'] == 'מטה':
        temp['name_of_group'] = 'Headquarters'
    elif temp['name_of_group'] == 'בעלים':
        temp['name_of_group'] = 'Owners'
    elif temp['name_of_group'] == 'מנהלים':
        temp['name_of_group'] = 'Managers'
    elif temp['name_of_group'] == 'מנהל מתלמד':
        temp['name_of_group'] = 'Junior-Managers'
    elif temp['name_of_group'] == 'מנהלי משמרת':
        temp['name_of_group'] = 'Senior Sub-Managers'
    elif temp['name_of_group'] == 'סגן מנהל משמרת':
        temp['name_of_group'] = 'Sub-Managers'
    elif temp['name_of_group'] in [' עובדים', 'עובדים', 'עובדים ']:
        temp['name_of_group'] = 'Employees'
    elif temp['name_of_group'] == 'עובדים עם חיתוך שעון':
        temp['name_of_group'] = 'Junior Employees'
    else:
        return

def organize_groups(permissions_list, language):
    groups = []
    for i, temp in enumerate(permissions_list):
        perrmisions_id = return_perrmisions_id(temp['group'])
        is_default = temp['default_gruop']
        if language != 'he':
            change_perrmision_to_english(permissions_list, i)
        groups.append({
            "name": temp['name_of_group'],
            "group_id": perrmisions_id,
            "is_default": is_default
        })
    return groups
