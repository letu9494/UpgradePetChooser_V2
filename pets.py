# Name: Le


class Pet:

    __name = ""
    __age = 0
    __owner = ""
    __animal_type = ""
    __tableID = 0

    def __init__(self,
                 pet_name="",
                 pet_age=0,
                 owner_id=0,
                 animal_type_id=0,
                 sql_ID = 0):
        self.SetPetName(pet_name)
        self.SetPetAge(pet_age)
        self.SetOwnerName(owner_id)
        self.SetType(animal_type_id)
        self.__tableID = sql_ID

    def SetPetName(self, pet_name: str) -> None:
        try:
            self.__name = pet_name
        except ValueError as e:
            print("Invalid input.")

    def SetPetAge(self, pet_age: int) -> None:
        try:
            self.__age = pet_age
        except ValueError as e:
            print("Invalid input.")

    def SetOwnerName(self, owner_name: str) -> None:
        try:
            self.__owner = owner_name
        except ValueError as e:
            print("Invalid input.")

    def SetType(self, anm_type: str) -> None:
        try:
            self.__animal_type = anm_type
        except ValueError as e:
            print("Invalid input.")

    def GetPetName(self) -> str:
        return self.__name

    def GetPetAge(self) -> int:
        return self.__age

    def GetOwnerName(self) -> str:
        return self.__owner

    def GetType(self) -> str:
        return self.__animal_type

    def GetID(self) -> str:
        return self.__tableID

