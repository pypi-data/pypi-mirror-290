import random
import time
import json
from .country_code import code

class GenKit:
    class PhoneGen:
        def __init__(self, country="IN"):
            """
            Initialize the PhoneGen class with a specific country code.
            
            Parameters:
            country (str): The country code to use for generating phone numbers. 
                           Defaults to 'IN' for India. (Optional)
            """
            # Country codes based on the country
            self.codes = code
            # Set the country code or default to India
            self.code = self.codes.get(country.upper(), "+91")

        def generate(self, length=10):
            """
            Generate a random phone number with the specified length.
            
            Parameters:
            length (int): The length of the phone number to generate. 
                          Defaults to 10. (Optional)
            
            Returns:
            str: A phone number with the specified length and country code.
            """
            if self.code == "+91":
                # For Indian numbers, ensure the number starts with a digit between 6 and 9
                number = str(random.randint(6, 9)) + ''.join([str(random.randint(0, 9)) for _ in range(length - 1)])
            else:
                # Generate a random phone number for other countries
                number = ''.join([str(random.randint(0, 9)) for _ in range(length)])
                
            return f"{self.code}{number}"

    @staticmethod
    def phonenumber(country="IN", n=1, type="string", save=False):
        """
        Generate a specified number of phone numbers for a given country.
        
        Parameters:
        country (str): The country code to use for generating phone numbers. 
                       Defaults to 'IN'. (Optional)
        n (int): The number of phone numbers to generate. 
                 Defaults to 1. (Optional)
        type (str): The format of the output.  'string' (default), 
                    'list', or 'dict'. Defaults to 'string'. (Optional)
        save (bool): Whether to save the generated phone numbers to a file. 
                     Defaults to False. (Optional)
        
        Returns:
        str | list | dict: The generated phone numbers in the specified format.
        """
        phone_gen = GenKit.PhoneGen(country)
        numbers = [phone_gen.generate() for _ in range(n)]

        if type == "list":
            result = numbers
        elif type == "dict":
            result = {"phone_numbers": numbers}
        else:  # default to "string"
            result = "\n".join(numbers)
        
        if save:
            timestamp = int(time.time())
            filename = f"genkit_{timestamp}.txt"
            with open(filename, "w") as file:
                if type == "dict":
                    json.dump(result, file, indent=4)
                elif type == "list":
                    file.write("\n".join(result))  # Convert list to string format
                else:
                    file.write(result)
            print(f"Data saved to file: {filename}")       
        
        return result
