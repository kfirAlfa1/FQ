from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
import ReadData


driver_path = r"C:\Users\KfirAlfandary\OneDrive - Tabit\Desktop\chromedriver.exe"  
service = Service(driver_path)
driver = webdriver.Chrome(service=service)


new_list_of_roles=[]
new_list_of_recive_limits=ReadData.receives_limits

shifts=ReadData.shifts
names_of_shifts_final=[]



admin_compeny=1
adimin_user_name="kfira"
password_for_first_login = '159753ASD'

def do_login():
    name_of_compeny_field=driver.find_element(By.ID, "company")
    name_of_user_field=driver.find_element(By.ID, "username")
    password_field=driver.find_element(By.ID, "password")
    name_of_compeny_field.send_keys(admin_compeny)
    name_of_user_field.send_keys(adimin_user_name)
    password_field.send_keys(password_for_first_login)
    log_in_button=driver.find_element(By.ID,'log-in')
    log_in_button.click()
     

def save_and_add_another():
    save_and_add_another_button=driver.find_element(By.NAME,'_addanother')
    save_and_add_another_button.click()

# Production -- https://app.shiftorganizer.com/admin/app/application/add/

def create_app(admin_compeny,admin_user,password_for_first_login):
    #driver.get('https://app.shiftorganizer.com/admin/app/application/add/') #Production
    driver.get('https://il-shift.tabit-int.com/admin/app/application/add/')
    time.sleep(2)
    do_login()
    time.sleep(3)
    compeny_name_element=driver.find_element(By.NAME, "name")
    compeny_name_element.send_keys(ReadData.app_name)
    compeny_display_element=driver.find_element(By.NAME, "display_name")
    compeny_display_element.send_keys(ReadData.display_name)


    original_window = driver.current_window_handle
    add_compeny_button=driver.find_element(By.ID,'add_id_company')
    add_compeny_button.click()

    all_windows = driver.window_handles
    for window in all_windows:
        if window != original_window:
            driver.switch_to.window(window)
            break


    wait = WebDriverWait(driver, 10) 
    new_element = wait.until(EC.presence_of_element_located((By.NAME, "name")))
    new_element.send_keys(ReadData.company_name)
    save_button=driver.find_element(By.CLASS_NAME,'default')
    save_button.click()

    driver.switch_to.window(original_window)

    industry=driver.find_element(By.ID,'id_industry')
    select = Select(industry)
    select.select_by_visible_text("Restaurants")


    language=driver.find_element(By.ID,'id_language')
    select = Select(language)
    if ReadData.language == 'עברית':
        select.select_by_visible_text('Hebrew')

    
    country_code=driver.find_element(By.ID,'id_country_code')
    select = Select(country_code)
    if ReadData.country_code == 'ישראל':
        select.select_by_index(1)


    if ReadData.account_number !=None:
        account_number_element=driver.find_element(By.NAME,'account_number')
        account_number_element.send_keys(ReadData.account_number)


    # if ReadData.last_hour_for_subbmit_shifts != '19:00:00':
    #     last_hour_for_subbmit_shifts_element=driver.find_element(By.NAME,'deadline_hour')
    #     last_hour_for_subbmit_shifts_element.send_keys(ReadData.last_hour_for_subbmit_shifts+':00')


    for i in range(len(ReadData.perrmisions_list)):
        begining_of_id='id_applicationgroup_set-'
        end_of_id_group='-group'
        end_of_id_name='-name'
        id=i

        final_id_group=begining_of_id+str(id)+end_of_id_group
        final_id_name=begining_of_id+str(id)+end_of_id_name

        permission_group=driver.find_element(By.ID,final_id_group)
        select = Select(permission_group)
        select.select_by_visible_text(ReadData.perrmisions_list[i])

        permission_names_element=driver.find_element(By.ID,final_id_name)
        permission_names_element.send_keys(ReadData.perrmisions_list_names[i])

        #Add another app group
        if i > 2:
             {
                 driver.find_element(By.LINK_TEXT, "Add another Application group").click()

             }

        # if ReadData.default_perrmision == ReadData.perrmisions_list_names[i]:
        #         default_perrmision_id= begining_of_id+str(id)+'-is_default'
        #         default_button=driver.find_element(By.ID,default_perrmision_id)
        #         default_button.click()

        if ReadData.default_perrmision == ReadData.perrmisions_list[i]:
                default_perrmision_id= begining_of_id+str(id)+'-is_default'
                default_button=driver.find_element(By.ID,default_perrmision_id)
                default_button.click()
              


    for i in range(len(ReadData.religions_list)):
         begining_of_id='id_applicationreligion_set-'
         end_of_id_religion='-religion'
         end_of_id_religion_name='-name'
         id=i
         final_id_religions= begining_of_id+str(id)+end_of_id_religion
         religions=driver.find_element(By.ID,final_id_religions)
         select = Select(religions)
         select.select_by_visible_text(ReadData.religions_list[i])

         final_id_religions_name= begining_of_id+str(id)+end_of_id_religion_name
         religion_names_element=driver.find_element(By.ID,final_id_religions_name)
         religion_names_element.send_keys(ReadData.religions_list_names[i])

        #  if ReadData.default_religion == ReadData.religions_list_names[i]:
        #     default_religion_id= begining_of_id+str(id)+'-is_default'
        #     default_button=driver.find_element(By.ID,default_religion_id)
        #     default_button.click()

         if ReadData.default_religion == ReadData.religions_list[i]:
            default_religion_id= begining_of_id+str(id)+'-is_default'
            default_button=driver.find_element(By.ID,default_religion_id)
            default_button.click()

    final_save_button= driver.find_element(By.NAME,'_save')
    final_save_button.click()
         
# Production -- https://app.shiftorganizer.com/admin/app/application/     
  
def get_the_last_app_id():
     driver.get('https://il-shift.tabit-int.com/admin/app/application/')
    #driver.get('https://app.shiftorganizer.com/admin/app/application/') #Prod
    #  do_login()
    #  time.sleep(2)
     id_navbar_element = driver.find_element(By.PARTIAL_LINK_TEXT,"ID")
     id_navbar_element.click()
     time.sleep(2)
     id_navbar_element = driver.find_element(By.PARTIAL_LINK_TEXT,"ID")
     id_navbar_element.click()
     time.sleep(2)
     xpath_expression_compeny = "//td[@class='field-company nowrap']"
     xpath_expression_date = "//td[@class='field-created_at nowrap']"
     apps_names=driver.find_elements(By.CLASS_NAME,"field-name")
     apps_ids=driver.find_elements(By.CLASS_NAME,"field-id")
     dates=driver.find_elements(By.XPATH, xpath_expression_date)
     compenys=driver.find_elements(By.XPATH, xpath_expression_compeny)
     compeny=compenys[0].text
     date=dates[0].text
     app_name=apps_names[0].text
     app_id=apps_ids[0].text

    #  print("This is the app name: "+ app_name)
    #  print("This is the app id: "+ app_id)
    #  print("This is the app company: "+ company)
    #  print("This is the app date: "+ date)
     return app_id

# Production -- driver.get('https://app.shiftorganizer.com/admin/app/role/add/?app='+(app_id))   

def add_roles(app_id):
    #driver.get('https://il-shift.tabit-int.com/admin/app/role/add/?app='+str(app_id))
    driver.get('https://app.shiftorganizer.com/admin/app/role/add/?app='+str(app_id)) #--Prod
    do_login()
    time.sleep(5)
    for i in range(len(ReadData.roles)):
        name_input= driver.find_element(By.CLASS_NAME,'vTextField')
        name_input.clear()
        name_input.send_keys(ReadData.roles[i])
        priority=driver.find_element(By.CLASS_NAME,'vIntegerField')
        priority.clear()
        priority.send_keys(i+1)
        save_and_Add_Another_button=driver.find_element(By.NAME,'_addanother')
        save_and_Add_Another_button.click()
        driver.back()


def change_roles(list1,list2):
    temp_list = [0] * len(list2)
    for index1, value in enumerate(list1):
        if value in list2:
            index2 = list2.index(value)
            temp_list[index2]=new_list_of_roles[index1]
    return temp_list


def change_recive_limits(list1,list2):
    temp_list = [0] * len(list2)
    for index1, value in enumerate(list1):
        if value in list2:
            index2 = list2.index(value)
            temp_list[index2]=new_list_of_recive_limits[index1]
    return temp_list


def get_and_chagne_values_for_roles():
    #driver.get('https://il-shift.tabit-int.com/admin/app/shift/add/?app='+(app_id))
    # do_login()
    # time.sleep(2)
    global shifts
    roles_group=driver.find_element(By.ID,'id_roles')
    select = Select(roles_group)
    for option in select.options:
        new_list_of_roles.append(option.text)
    for key,value in shifts.items():
        shifts[key]=change_roles(ReadData.roles,value)


def change_shifts_keys_and_recive_limits(app_id):
    #driver.get('https://il-shift.tabit-int.com/admin/app/limit/add/?app='+str(app_id))
    #driver.get('https://app.shiftorganizer.com/admin/app/limit/add//?app='+str(app_id))#Prod
    # do_login()
    time.sleep(3)
    global shifts
    shifts_element= driver.find_element(By.NAME,'shifts')
    select = Select(shifts_element)
    temp = []
    for option in select.options:
         temp.append(option.text) 
    for i, key in enumerate(new_list_of_recive_limits):
        if i < len(temp):
            new_list_of_recive_limits[key][0] = temp[i]
        
# Production --> driver.get('https://app.shiftorganizer.com/admin/app/shift/add/?app='+app_id)    
def add_shifts(app_id):
    #driver.get('https://il-shift.tabit-int.com/admin/app/shift/add/?app='+str(app_id))
    driver.get('https://app.shiftorganizer.com/admin/app/shift/add/?app='+str(app_id)) #--Prod
    do_login()
    time.sleep(5)
    get_and_chagne_values_for_roles()
    keys=list (shifts.keys())
    for i in range(len(shifts)):
        shift_name_elemnt=driver.find_element(By.CLASS_NAME,'vTextField')
        shift_name_elemnt.clear()
        time.sleep(1)
        roles_group=driver.find_element(By.ID,'id_roles')
        select = Select(roles_group)
        select.deselect_all()
        shift_name_elemnt.send_keys(keys[i])
        roles_list=shifts[keys[i]] 
        for item in roles_list:
            roles_group=driver.find_element(By.ID,'id_roles')
            select = Select(roles_group)
            substring=item
            for option in select.options:
             if substring == option.text:
                select.select_by_visible_text(option.text)
                break
        order=driver.find_element(By.CLASS_NAME,'vIntegerField')
        order.clear()
        time.sleep(1)
        order.send_keys(i+1)
        continuously=driver.find_element(By.ID,'id_continuously')
        select = Select(continuously)
        continuously= str(ReadData.continuously[i]).strip()
        select.select_by_visible_text(continuously)
        save_and_Add_Another_button=driver.find_element(By.NAME,'_addanother')
        save_and_Add_Another_button.click()
        time.sleep(1)
        driver.back()
            
# Production --> driver.get('https://app.shiftorganizer.com/admin/app/limit/add/?app='+app_id) 

def add_receives_limits(app_id):
    #driver.get('https://il-shift.tabit-int.com/admin/app/limit/add/?app='+str(app_id))
    driver.get('https://app.shiftorganizer.com/admin/app/limit/add/?app='+str(app_id)) #--Prod
    #do_login()
    time.sleep(3)
    change_shifts_keys_and_recive_limits(app_id)
    keys=list (new_list_of_recive_limits.keys())
    for i in range(len(new_list_of_recive_limits)):
        current_key=keys[i]
        limit_name_elemnt=driver.find_element(By.NAME,'name')
        limit_name_elemnt.clear()
        limit_name_elemnt.send_keys(keys[i])
        time.sleep(2)
        if i == 0:
         type_of_limit=driver.find_element(By.NAME,'type')
         select = Select(type_of_limit)
         select.select_by_value('Rec')
        daily_or_shift_elemnt=driver.find_element(By.NAME,'shift_daily')
        if new_list_of_recive_limits[current_key][-1]=='כן':
         select = Select(daily_or_shift_elemnt)
         select.select_by_value('D')
         global_element=driver.find_element(By.ID,'id_is_global')
         global_element.click()
        shifts_element= driver.find_element(By.NAME,'shifts')
        #↓↓↓For Global limit- all shifts need to be selected ↓↓
        if new_list_of_recive_limits[current_key][0]=='כולם':
            select=Select(shifts_element)
            for option in select.options:
             select.select_by_visible_text(option.text) 
        else:
            select = Select(daily_or_shift_elemnt)
            select.select_by_value('S')
        
        before_split= new_list_of_recive_limits[current_key][1].split('-')
        min=before_split[0]
        max=before_split[1]
        min_element= driver.find_element(By.NAME,'min')
        min_element.clear()
        min_element.send_keys(min)
        max_element= driver.find_element(By.NAME,'max')
        max_element.clear()
        max_element.send_keys(max)
        default_element= driver.find_element(By.NAME,'default')
        default_element.clear()
        default_element.send_keys(ReadData.receives_limits[current_key][2])
        order=driver.find_element(By.NAME,'order')
        order.clear()
        order.send_keys(i+1)
        if new_list_of_recive_limits[current_key][0]!='כולם':
            shifts_element= driver.find_element(By.NAME,'shifts')
            select=Select(shifts_element)
            select.deselect_all()
            for option in select.options:
                if new_list_of_recive_limits[current_key][0] == option.text:
                    select.select_by_visible_text(option.text)
                    break
        save_and_add_another_button=driver.find_element(By.NAME,'_addanother')
        save_and_add_another_button.click()
        time.sleep(2)
        driver.back()

#######################################################################
#Finding an app in Select that includes all apps

def find_the_app(app_id):
    apps_options = driver.find_element(By.ID, 'id_application')
    select = Select(apps_options)
    for option in select.options:
        app_id_str='('+str(app_id)+')'
        if option.text.strip().endswith(app_id_str):
            option.click() 
            break 


def choose_employee_configuration_field(name_of_filed):
    if name_of_filed == 'תעודת זהות':
        return 'id_number'
    elif name_of_filed == 'עיר':
        return 'city'
    elif name_of_filed == 'כתובת':
        return 'address'
    elif name_of_filed == 'מיקוד':
        return 'zip_code'
    elif name_of_filed == 'תאריך תחילת עבודה':
        return 'work_start_date'
    elif name_of_filed == 'תאריך סיום עבודה':
        return 'work_termination_date'
    elif name_of_filed == 'דת':
        return 'religion'
    elif name_of_filed == 'מזהה שעון':
        return 'clock_id'
    elif name_of_filed == 'מספר עובד לשכר':
        return 'number'

def add_employee_configuration_field(app_id):
    driver.get('https://il-shift.tabit-int.com/admin/app/employeeconfiguration/add/?app='+str(app_id))
    do_login()
    time.sleep(3)
    find_the_app(app_id)
    for key,value in ReadData.employee_configurations.items():
        if value[0]=='כן':
            attribute_element=driver.find_element(By.ID,'id_attribute')
            select=Select(attribute_element)
            attribute=choose_employee_configuration_field(f'{key}')
            select.select_by_value(attribute)
            active_checkbox_element=driver.find_element(By.ID,'id_is_active')
            if active_checkbox_element.is_selected():
                print()
            else:
                active_checkbox_element.click()

            excel_checkbox_element=driver.find_element(By.ID,'id_excel')
            if excel_checkbox_element.is_selected():
                print()
            else:
                excel_checkbox_element.click()
            if attribute == 'number':
                name_elemnt=driver.find_element(By.ID,'id_name')
                name_elemnt.send_keys(ReadData.employee_configurations[key])
                url='https://il-shift.tabit-int.com/admin/app/reportcolumn/add/?app='+ str(app_id)
                driver.execute_script(f"window.open('{url}', '_blank');")
                time.sleep(3)
                driver.switch_to.window(driver.window_handles[1])
                select_report=driver.find_element(By.ID,'id_reports')
                select_report=Select(select_report)
                select_report.select_by_value("2")
                select_column=driver.find_element(By.ID,'id_column')
                select_column=Select(select_column)
                select_column.select_by_value('number')
                name_elemnt=driver.find_element(By.ID,'id_name')
                name_elemnt.send_keys("מספר עובד לשכר")
                save_and_add_another()
                time.sleep(5)
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
  
        if ReadData.employee_configurations[key][1]=='כן':
            reprot_checkbox_element=driver.find_element(By.ID,'id_report')
            if reprot_checkbox_element.is_selected():
                print()
            else:
                reprot_checkbox_element.click()
        if ReadData.employee_configurations[key][0]!='כן' and ReadData.employee_configurations[key][1]!='כן':
            continue
        save_and_add_another()
        time.sleep(2)
        driver.back()



# create_app(adimin_user_name,admin_compeny,password_for_first_login)
# app_id = get_the_last_app_id()
app_id=5012
#add_roles(app_id)
#add_shifts(app_id)
add_receives_limits(app_id)
#add_employee_configuration_field(app_id)
time.sleep(5000)

