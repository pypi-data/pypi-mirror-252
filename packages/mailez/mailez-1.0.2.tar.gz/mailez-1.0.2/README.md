A package to make sending mails to multiple people while adding their names to each message automaticly easy. I tested it with Gmail but it might work with some other e-mail service providers.
Usage:
```
import mailez.functions as mz
my_gmail_address = "supercoolemailofsupercoolperson@gmail.com"
my_password = "heyheyheyiamverycool12345"
my_subject = "Asking How The Recipient Is Feeling At The Moment"
my_csv_path = "path/to/csv/file.csv"
my_message = "Dear {name},\nHow are you?"
obj = mz.Mail(my_gmail_address, my_password, my_subject, my_csv_path, my_message)
obj.Send()
```
The format for CSV file is given below:
```
email, name
supercoolguy@coolmail.com, Jake Peralta
anothersupercoolguy@mail.com, Joey Tribbiani
supercoolbusinessmail@coolbusiness.com, CoolBusiness LTD.
```