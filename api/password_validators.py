from django.core.exceptions import ValidationError
import os
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
my_file = os.path.join(THIS_FOLDER,"passwords.txt")
class CommonPasswordValidator:
    def validate(self,password,user=None):
        with open(my_file,"r") as f:
            for line in f:
                if password ==str(line):
                    raise ValidationError("the password is too common")
