import sys
import imaplib, getpass
from bs4 import BeautifulSoup

if len(sys.argv) < 3:
    print("Error! Email and IMAP configuration is required as command line arguments")
    exit()

email = sys.argv[1]
imap_address = sys.argv[2]

mail = imaplib.IMAP4_SSL(imap_address) # Replace this!
mail.login(email, getpass.getpass())
mail.select("Inbox") # connect to inbox.

print("Please wait...")
result, data = mail.search(None, '(FROM "receipts-nigeria@taxify.eu")' )

id_list = data[0].split()

total, discount = 0, 0

for id in id_list:
    typ, data = mail.fetch(id, '(UID BODY[1])')
    soup = BeautifulSoup(data[0][1], 'lxml')
    fees = soup.find_all("td", {"style":"text-align:right; color:rgb(153, 153, 153);"})
    ride_total = soup.find("td", {"style":"text-align:right; color:black;"}) # Unique styling for the total amount paid
    total+=int(ride_total.text[1:]) # Remove the Naira sign in front of the ride total
    if (fees[3].text[0] == "-"): # Discounted trip
    	discount+=float(fees[3].text)

print("Total Payment Made to Taxify = N{}".format(total))
print("Total Discount from Taxify = N{}".format(discount))
mail.close()
mail.logout()