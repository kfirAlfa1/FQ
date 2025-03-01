import sys
from datetime import time
############ Tests ###################

def error_exit(msg,ERRORS_MESSAGES):
    ERRORS_MESSAGES.append(msg + " \n"+"ReadData")
   
def test_the_sheet(sheet):
    valid = (
        sheet.cell(row=13, column=1).value == 'שם אפליקציה' and
        sheet.cell(row=14, column=1).value == 'שם תצוגה' and
        sheet.cell(row=5, column=1).value == 'שם משתמש'
    )
    
    if not valid:
         print("Not right format of sheet")
         sys.exit()

def test_groups(perrmisions_list,ERRORS_MESSAGES):
    default=0
    if len(perrmisions_list) == 0:      
         error_exit("There are no gruops!",ERRORS_MESSAGES)

    for temp in perrmisions_list:
     if temp.get('default_gruop') == True:
       default+=1
    if default > 1:
         error_exit("There is more than 1 deafult group",ERRORS_MESSAGES)

def test_religions(religions_list,ERRORS_MESSAGES):
    default=0
    if len(religions_list) == 0:
         error_exit("There are no religions!", ERRORS_MESSAGES)  

    for temp in religions_list:
     if temp.get('default_religion') == True:
       default+=1
    if default > 1:
         error_exit("There is more than 1 deafult religion", ERRORS_MESSAGES)

def test_shifts(shifts,sheet):
    #Checking whether the existing number of shifts matches the list of shifts on the right side of the table
    i=5
    j=6
    if sheet.cell(row=i, column=j).value == "רשימת משמרות":
        number_of_shifts=0
        while sheet.cell(row=i, column=j).value != None and sheet.cell(row=i, column=j).value != '':
            i+=1
            if sheet.cell(row=i, column=j).value != None and sheet.cell(row=i, column=j).value != '':
                number_of_shifts+=1
        if len(shifts)== number_of_shifts:
            # Test pass
            #Checking if there are continuesly shifts if they valid or not
            continuously_of_0= False
            continuously_of_2= False

            for temp in shifts:
                if temp.get('continuously') == 0 :
                    continuously_of_0 =True

                if temp.get('continuously') == 2 :
                        continuously_of_2=True
            
            if (continuously_of_0 == True and continuously_of_2==True) or (continuously_of_0 == False and continuously_of_2==False):
                return #Test pass
            else:
                print("Continuously of shifts are worng!!") 
                print("ReadData")
                sys.exit()               


        else:
            print("Number of shifts is not match!!")
            sys.exit()
    else:
        print("Couldent find validation on shifts") 
        print("ReadData")
        sys.exit()

def test_shift_for_receives_limits(shifts_received, shifts, ERRORS_MESSAGES):

    if not isinstance(shifts_received, list):
        shifts_received = [shifts_received]

    counter = 0
    for shift_name in shifts_received:
        if any(shift["name"] == shift_name for shift in shifts):
            counter += 1
            continue

    if counter == len(shifts_received):  # All shifts inside the limit exist in the shift list
        return 'S'
    else:
        error_exit("Couldnt find shifts of receives limits", ERRORS_MESSAGES)

def test_features(features,perrmisions_list,ERRORS_MESSAGES):
    if 'לייבור קוסט - LC' in features:
        if any(group["group"] == "Automation" for group in perrmisions_list):
            return
        else:
         error_exit("There is labor cost but not Automation group",ERRORS_MESSAGES)

def test_locations(locations,features,sum_of_roles_for_locations,roles,ERRORS_MESSAGES):
    nono_test = False
    locations_test=False

    if len(locations)>0 :
        locations_test=True

    if any("נונו מימי"  in feature for feature in features): 
        nono_test = True
    
    if nono_test == True and locations_test == True: 
        if sum_of_roles_for_locations == len(roles): #Cheack that all the roles have location
             return
        else:
          error_exit("There are roles without locations",ERRORS_MESSAGES)

    if nono_test == False and locations_test == False:
        return
    else:
        if len(locations) >0 :
         error_exit("There are locations but NONO MIMI feature is not True",ERRORS_MESSAGES)
        else:
         error_exit(" NONO MIMI feature is True but there are no locations",ERRORS_MESSAGES)

def test_web_clock(list_of_permission,perrmisions_list):
  counter=0
  for i in range(len(list_of_permission)):
      if any(group["name_of_group"] == list_of_permission[i] for group in perrmisions_list):
       counter+=1

  if counter == len(list_of_permission):
      return
  else:
     error_exit("permissions for web clock are not inside perrmisions names")

#This function checks if variable is not none and than do strip it its string
def test_not_none_and_strip(variable,name,ERRORS_MESSAGES):
    if test_not_none(variable) == True:
       if isinstance (variable,str):
           return variable.strip()
       else:
           return variable
           
    else:
        error_exit(name + " is None",ERRORS_MESSAGES)    

#Must be not None
def test_not_none(variable):
    if variable ==  None:
        return False
    else:
        return True

# When element must be in list, if its not, it returns error.
def test_in_list(variable, valid_list, name,ERRORS_MESSAGES):
    if variable not in valid_list:
        error_exit(f"No {name} in list: {valid_list}",ERRORS_MESSAGES) 
    
def test_type(variable, expected_type, name,ERRORS_MESSAGES):
  if not isinstance(variable, expected_type):
    error_exit(f"{name} is not in {expected_type.__name__} format",ERRORS_MESSAGES)
