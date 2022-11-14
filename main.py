# Name: Le Tu
# Assignment upgrade pet chooser


import pymysql.cursors
from creds import *
from pets import Pet


def main_menu():
    exit_cond = False
    print("Welcome to the Pet Chooser!")
    while not exit_cond:
        try:
            i = 1
            print("Please choose a pet from the list below:")
            for pet in pets_list:
                print(f"[{i}] {pet.GetPetName()}")
                i += 1
            print("[Q] Quit")

            user_input = input("Choice: ")
            if user_input == "q" or user_input == "Q":
                print("Exiting the Pet Chooser...")
                exit_cond = True
            elif not user_input.isnumeric():
                print("You did not enter in a valid number. Please choose again.")
                input("Press [ENTER] to continue.")
            elif int(user_input) <= 0 or int(user_input) > i-1:
                print(f"Please enter in a number between 1 and {i-1}")
                input("Press [ENTER] to continue.")
            else:
                print_quit = printPet(pets_list[int(user_input)-1], user_input)
                # Break out of this loop and function if user previously quit in another function
                if print_quit:
                    return

        except Exception as e:
            raise e

def editing(chosen_pet: Pet):
    print(f"You have chosen to edit {chosen_pet.GetPetName()}.")
    print("Press the enter key at the prompt if you would like to keep the current value.")
    new_name = input("New name: ")
    if new_name.upper() == "Q":
        print("Exiting the Pet Chooser...")
        return True
    new_age = input("New age: ")
    if new_age.upper() == "Q":
        print("Exiting the Pet Chooser...")
        return True

    if new_name == "":
        print("Name of pet not changed.")
    # Do not allow integer names
    elif new_name.isnumeric() == True:
        print("Name of pet must not be a number. Name not changed.")
    else:
        print(chosen_pet.GetID())
        name_update = f"update pets set name = '{new_name}' where id = {chosen_pet.GetID()};"
        myConnection.cursor().execute("use pets;")
        myConnection.cursor().execute(name_update)
        myConnection.commit()
        print(f"Pet's name successfully updated to {new_name}")

    if new_age == "":
        print("Age of pet not changed.")
    # Do not allow non positive integer ages
    elif new_age.isnumeric() == False:
        print("Invalid age entered. Age not updated.")
    else:
        age_update = f"update pets set age = '{new_age}' where id = {chosen_pet.GetID()};"
        myConnection.cursor().execute(age_update)
        myConnection.commit()
        print(f"Pet's age successfully updated to {new_age}")

    # Update class object by pulling updated information from sql server
    sqlSelect = f"select id, name, age from pets where id = {chosen_pet.GetID()};"
    with myConnection.cursor() as cursor:
        cursor.execute(sqlSelect)
        for row in cursor:
            chosen_pet.SetPetName(row['name'])
            chosen_pet.SetPetAge(row['age'])

    # Return false as user did not choose to quit
    return False

def printPet(chosen_pet: Pet, pet_number : int):
        print_exit = False
        print(f"You have chosen {chosen_pet.GetPetName()}, the {chosen_pet.GetType()}. "
              f"{chosen_pet.GetPetName()} is {chosen_pet.GetPetAge()} years old. "
              f"{chosen_pet.GetPetName()}'s owner is {chosen_pet.GetOwnerName()}.\n")

        while print_exit == False:
            edit_choice = input("Would you like to [C]ontinue, [Q]uit, or [E]dit this pet? ")
            if edit_choice.lower() == "q":
                print("Exiting the Pet Chooser...")
                return True

            elif edit_choice.lower() == "c":
                print_exit = True
            elif edit_choice.lower() == "e":
                quiting = editing(pets_list[int(pet_number)-1])
                # Break out of this loop and function if user previously quit in another function
                if quiting == True:
                    return True
                print_exit = True
            else:
                print("Invalid choice. Please try again.")

        input("Press [ENTER] to continue. ")
        # Return false as user did not choose to quit
        return False


# Connect to the database
try:
    myConnection = pymysql.connect(host=hostname,
                                   user=username,
                                   password=password,
                                   db=database,
                                   charset='utf8mb4',
                                   cursorclass=pymysql.cursors.DictCursor)

except Exception as e:
    print(f"An error has occurred.  Exiting: {e}")
    print()
    exit()

# Now that we are connected, execute a query
#  and do something with the result set.
try:
    with myConnection.cursor() as cursor:
        # ==================

        # Create list holding each pet object
        pets_list = []

        sqlSelect = """select pets.id, pets.name, pets.age,
             owners.name, types.animal_type 
            from pets join owners on pets.owner_id=owners.id 
            join types on pets.animal_type_id=types.id;"""

        # Execute select
        cursor.execute(sqlSelect)
        for row in cursor:
            # Create pet object for each returned row from sql server and append it to the list
            pets_list.append(Pet(row['name'], row['age'], row['owners.name'], row['animal_type'], row['id']))

        main_menu()


except Exception as e:
    print(f"An error has occurred.  Exiting: {e}")
    print("Thank you for using the Pet Chooser!")
    print()

finally:
    myConnection.close()
    print("Connection closed.")

