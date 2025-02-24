import sys
from datetime import time
############ Tests ###################

def error_exit(msg):
    print(msg)
    print("ReadData")
    sys.exit()

def test_the_sheet(sheet):
    if ('שם אפליקציה' == sheet.cell(row=13, column=1).value 
        and 'שם תצוגה'== sheet.cell(row=14, column=1).value
         and 'שם משתמש'== sheet.cell(row=5, column=1).value):
            return
    else:
         error_exit("Not right format of sheet")

def test_groups(perrmisions_list):
    default=0
    if len(perrmisions_list) == 0:      
         error_exit("There are no gruops!")

    for temp in perrmisions_list:
     if temp.get('default_gruop') == True:
       default+=1
    if default > 1:
         error_exit("There is more than 1 deafult group")

def test_religions(religions_list):
    default=0
    if len(religions_list) == 0:
         error_exit("There are no religions!")  

    for temp in religions_list:
     if temp.get('default_religion') == True:
       default+=1
    if default > 1:
         error_exit("There is more than 1 deafult religion")

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

def test_shift_for_receives_limits(list_of_shifts,shifts):
        counter=0
        for i in range(len(list_of_shifts)):
          if any(shift["name"] == list_of_shifts[i] for shift in shifts):
                counter+=1
                continue
        if counter == len(list_of_shifts): #All the sifts inside the limit are in the shift list
            return
        else:
         error_exit("Couldnt find shifts of receives limits")

def test_features(features,perrmisions_list):
    if 'לייבור קוסט - LC' in features:
        if any(group["group"] == "Automation" for group in perrmisions_list):
            return
        else:
         error_exit("There is labor cost but not Automation group")

def test_locations(locations,features,sum_of_roles_for_locations,roles):
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
          error_exit("There are roles without locations!!")

    if nono_test == False and locations_test == False:
        return
    else:
        if len(locations) >0 :
         error_exit("There are locations but NONO MIMI feature is not True!!")
        else:
         error_exit(" NONO MIMI feature is True but there are no locations!!")

def test_web_clock(list_of_permission,perrmisions_list):
  counter=0
  for i in range(len(list_of_permission)):
      if any(group["name_of_group"] == list_of_permission[i] for group in perrmisions_list):
       counter+=1

  if counter == len(list_of_permission):
      return
  else:
     error_exit("permissions for web clock are not inside perrmisions names")

#Must be not None
def test_not_none(variable, name):
    if variable is not None:
        error_exit(f"No {name}")
#Must not None
def test_none(variable, name):
    if variable is None:
        error_exit(f"No {name}")

# When element must be in list, if its not, it returns error.
def test_in_list(variable, valid_list, name):
    if variable not in valid_list:
        error_exit(f"No {name}")

# When element must NOT be in list, if it is, it returns error.
def test_not_in_list(variable, valid_list, name):
    if variable  in valid_list:
        error_exit(f" {name}  is allredy on the list: {valid_list}")

def test_type(variable, expected_type, name):
  if not isinstance(variable, expected_type):
    error_exit(f"{name} is not in {expected_type.__name__} format")
