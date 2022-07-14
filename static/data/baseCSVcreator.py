import csv

def memberData():
    with open('memberData.csv', 'w') as csvfile:
        fieldnames = ["SNo", "Name","Email","Status", "Interests", "Year", "Major" , "Date", "Info"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
def projectData():
    with open('projectData.csv', 'w') as csvfile:
        fieldnames = ["SNo", "Name","Description","ImgURL"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

def emailData():
    with open('emailData.csv', 'w') as csvfile:
        fieldnames = ["Emails"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

if __name__ == "__main__":
    #memberData()
    #projectData()
    emailData()