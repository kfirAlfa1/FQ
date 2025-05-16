import TestData
import WorldTimeZones
from deep_translator import GoogleTranslator
import sys
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

def retrun_permission_id_to_group(permission_id):
    mapping = {
        10: 'Headquarters',
        7: 'Owners',
        2: 'Managers',
        9: 'Junior-Managers',
        8: 'Senior Sub-Managers',
        3: 'Sub-Managers',
        11: 'Senior Employees',
        4: 'Employees',
        5: 'Junior Employees',
        6: 'Automation'
    }
    return mapping.get(permission_id, "Unknown")
     
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
   temp1 = temp1[-1] 
   temp2 = temp2[0]
   try:
    index = days_of_week.index(temp1)
    days.append(index+1)
    index = days_of_week.index(temp2)
    days.append(index+1)
    days=list(range(days[0], days[-1] + 1))
    return days
   except Exception as e: 
    TestData.error_exit("Error with converting days to range for limits - utils.py",ERRORS_MESSAGES)

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
# groups.append({
#            "name":'Support',
#           "group_id": 14,
#          "is_default": False
#     })


    return groups

def return_religions_id(religion):
    religion_ids = {
        "Jewish": 1,
        "Christian": 2,
        "Muslim": 3,
        "Foreign": 4,
        "Foreign 2": 5,
    }
    if religion in religion_ids:
        return religion_ids[religion]

    print("Error!!")
    print("Could not find the id of the religion")

def change_religion_to_english(religions_list, index):
    temp = religions_list[index]
    translation_map = {
        "יהודי": "Jewish",
        "נוצרי": "Christian",
        "מוסלמי": "Muslim"
    }
    temp["name_of_religion"] = translation_map.get(temp["name_of_religion"], "Foreign")

def organize_religions(religions_list, language):
    religions = []
    for i, temp in enumerate(religions_list):
        religion_id = return_religions_id(temp["religion"])

        if language != "he":
            change_religion_to_english(religions_list, i)

        religions.append({
            "name": temp["name_of_religion"],
            "religion_id": religion_id,
            "is_default": temp["default_religion"]
        })
    
    return religions

def choose_holiday_area_code(holidays_area):
    # If it's already an int, return it unchanged
    if isinstance(holidays_area, int):
        return holidays_area
    if holidays_area == 'תל אביב':
        return 676
    elif holidays_area == 'ירושלים':
        return 110
    elif holidays_area == 'חיפה':
        return 1504
    else:
        return 1507  # Default to באר שבע
    
def convert_name_of_group_from_hebrew_to_english(name_of_group):
    mapping = {
        'מטה': 'Headquarters',
        'בעלים': 'Owners',
        'מנהלים': 'Managers'
    }
    return mapping.get(name_of_group)
   
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

def convert_shift_name_to_id_for_receives_limits(receives_limits, shift_name, shift_id):
    for i in range(len(receives_limits)):
        temp_limit = receives_limits[i]
        shifts_in_limit = temp_limit["shifts"]
        if isinstance(shifts_in_limit, list):
            for j in range(len(shifts_in_limit)):
                if shifts_in_limit[j] == shift_name:
                    shifts_in_limit[j] = shift_id
                    break
        elif isinstance(shifts_in_limit, str):
            if shifts_in_limit == shift_name:
                temp_limit["shifts"] = [shift_id]


################ Features ##############################
#######################################################

# def organize_groups_Features(groups, temp_high_groups, temp_low_groups, high_groups_id, low_groups_id):
#     global automation_group # Declare it as global so it can be used outside the function
#     automation_group_Features = False  # Reset before processing

#     for dictionary in groups:
#         if dictionary.get("original_name") in temp_high_groups and dictionary.get("id") not in high_groups_id:
#             high_groups_id.append(dictionary.get("id"))
#         elif dictionary.get("original_name") in temp_low_groups and dictionary.get("id") not in low_groups_id:
#             low_groups_id.append(dictionary.get("id"))
#         elif dictionary.get("original_name") == 'Automation':
#             automation_group_Features = True  # Set it if condition matches

