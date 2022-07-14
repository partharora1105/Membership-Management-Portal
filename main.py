import os
import csv
from datetime import datetime
from werkzeug.utils import secure_filename

from flask import Flask, redirect, url_for, request, render_template, send_from_directory

app = Flask(__name__, static_folder="static")
localDomain = "http://localhost:5000"
publicDomain = "http://www.gtxr.club"
DOMAIN = localDomain

localPath = ""
publicPath = "/home/GTXR/mysite/"
PATH = localPath

@app.route("/")
def openHomeDefault():
    dataDict = {"Email": "", "Info": "", "Interests": "", "Major": "", "Name": "", "Year": None}
    return render_template("index.html", isSubmitted=False, errorMessage="", dataDict=dataDict, domain=DOMAIN)


@app.route("/home")
def openHome():
    dataDict = {"Email": "", "Info": "", "Interests": "", "Major": "", "Name": "", "Year": None}
    return render_template("index.html", isSubmitted=False, errorMessage="", dataDict=dataDict, domain=DOMAIN)


@app.route("/projects")
def openProjects():
    projectData = []
    with open(PATH + 'static/data/projectData.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            projectData.append(row)
    projectData.reverse()
    return render_template("projects.html", projectData=projectData, domain=DOMAIN)


@app.route("/admin")
def openAdmin():
    count = 0
    memberData = []
    with open(PATH + 'static/data/memberData.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            memberData.append(row)
            if row["Status"] == "Member":
                count += 1;
    memberData.reverse()
    projectData = []
    with open(PATH + 'static/data/projectData.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            projectData.append(row)
    projectData.reverse()
    return render_template("admin.html", memberData=memberData, projectData=projectData, count=count, domain=DOMAIN)


@app.route("/application", methods=["POST", "GET"])
def appliedForm():
    errorMessage = ""
    dataDict = {"Email": request.form["email"].strip().lower(), "Info": request.form["info"].strip(), "Interests": "",
                "Major": request.form["major"].strip().upper(), "Name": request.form["name"].strip(),
                "Year": request.form.get("year")}
    for item in ["events", "projects", "mentorship"]:
        if dataDict["Interests"] == "":
            dataDict["Interests"] += item[0].upper() if request.form.get(item) else ""
        else:
            dataDict["Interests"] += "," + item[0].upper() if request.form.get(item) else ""
    for key, value in dataDict.items():
        if (value == "" or value is None) and errorMessage == "":
            errorMessage = "Please enter your " + key
        elif (value == "" or value is None) and errorMessage != "":
            errorMessage += ", " + key
    if errorMessage == "":
        isSubmitted = True
        dataDict["Status"] = "Applied"
        dataDict["Date"] = (datetime.now()).strftime("%d/%m/%y");
        largestSNo = 0
        with open(PATH + 'static/data/memberData.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                largestSNo = int(row['SNo'])
        dataDict['SNo'] = largestSNo + 1
        with open(PATH + 'static/data/memberData.csv', 'a') as csvfile:
            fieldnames = ["SNo", "Name", "Email", "Status", "Interests", "Year", "Major", "Date", "Info"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(dataDict)
        dataDict = {"Email": "", "Info": "", "Interests": "", "Major": "", "Name": "", "Year": None}
    else:
        isSubmitted = False
    return render_template("index.html", isSubmitted=isSubmitted, errorMessage=errorMessage, dataDict=dataDict)


@app.route("/admin/accepted", methods=["POST", "GET"])
def accept():
    SNo = request.form['decision']
    # Read Data
    memberData = []
    with open(PATH + 'static/data/memberData.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(row)
            if row['SNo'] == SNo:
                row['Status'] = "Member"
            memberData.append(row)
    # #Write Data
    with open(PATH + 'static/data/memberData.csv', 'w') as csvfile:
        fieldnames = ["SNo", "Name", "Email", "Status", "Interests", "Year", "Major", "Date", "Info"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for dataDict in memberData:
            writer.writerow(dataDict)
    return redirect(url_for('openAdmin'))


@app.route("/admin/rejected", methods=["POST", "GET"])
def reject():
    SNo = request.form['decision']
    # Read Data
    memberData = []
    with open(PATH + 'static/data/memberData.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['SNo'] == SNo:
                row['Status'] = "Rejected"
            memberData.append(row)
    # #Write Data
    with open(PATH + 'static/data/memberData.csv', 'w') as csvfile:
        fieldnames = ["SNo", "Name", "Email", "Status", "Interests", "Year", "Major", "Date", "Info"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for dataDict in memberData:
            writer.writerow(dataDict)
    return redirect(url_for('openAdmin'))


@app.route("/admin/newProject", methods=["POST", "GET"])
def updateProject():
    projectDict = {}
    input = request.form["project"].split(";")
    projectDict["Name"] = input[0]
    projectDict["Description"] = input[1]
    file = request.files['image']
    if file.filename != '':
        filename = PATH + "static/uploads/" + secure_filename(file.filename)
        file.save(filename)
    projectDict["ImgURL"] = filename[len("static/"):]
    print(projectDict)
    with open(PATH + 'static/data/projectData.csv', 'a') as csvfile:
        fieldnames = ["Name", "Description", "ImgURL"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(projectDict)
    return redirect(url_for('openAdmin'))


@app.route("/admin/delete", methods=["POST", "GET"])
def deleteProject():
    projectName = request.form["name"]
    # Read Data
    projectData = []
    with open(PATH + 'static/data/projectData.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Name'] != projectName:
                projectData.append(row)
            else:
                os.remove(PATH + "static/" + row['ImgURL'])
    # #Write Data
    with open(PATH + 'static/data/projectData.csv', 'w') as csvfile:
        fieldnames = ["Name", "Description", "ImgURL"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for dataDict in projectData:
            writer.writerow(dataDict)
    return redirect(url_for('openAdmin'))


@app.route("/admin/download/master-data", methods=["POST", "GET"])
def downloadMasterData():
    return send_from_directory(app.static_folder, "data/memberData.csv")

@app.route("/admin/download/email-data", methods=["POST", "GET"])
def downloadEmailData():
    return send_from_directory(app.static_folder, "data/emailData.csv")

@app.route("/admin/download/member-data", methods=["POST", "GET"])
def downloadMemberData():
    memberData = []
    with open(PATH + 'static/data/memberData.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        memberData = [row for row in reader if row['Status'] != "Rejected"]
    # #Write Data
    with open(PATH + 'static/data/member-data.csv', 'w') as csvfile:
        fieldnames = ["SNo", "Name", "Email", "Status", "Interests", "Year", "Major", "Date", "Info"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for dataDict in memberData:
            writer.writerow(dataDict)
    return send_from_directory(app.static_folder, "data/member-data.csv")

@app.route("/email")
def openEmailDrop():
    return render_template("email.html", domain=DOMAIN)

@app.route("/emailDrop", methods=["POST", "GET"])
def submitEmail():
    with open(PATH + 'static/data/emailData.csv', 'a') as csvfile:
        fieldnames = ["Email"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        email =  request.form["email"]
        if email != "":
            writer.writerow({"Email" : email})
            return redirect(url_for('openHomeDefault'))
        else:
            return redirect(url_for('openEmailDrop'))


if __name__ == "__main__":
    app.debug = True
    app.run()
