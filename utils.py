import TestData


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

   
