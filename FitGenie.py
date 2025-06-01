print("\t\t\t____   ____\t______\n\t\t\t____\\  ____\\t___  \n\t\t\t____ \\ ____\\t__   \n\t\t\t____  \\____\\t_    \n\t\t\t\t    FIT    \\tGENIE®\n")
print("\n\n\t\t\tMeet the Better You.\n")

import mysql.connector as mc, random, pickle

def thediagnosis():
    cho=input("1.Generate new diagnosis\n2.Check previous diagnosis\n3.Book A Mentor\n4.Feedback\n")
    if cho=='1':
        d={}
        print("Let's start your diagnosis :")
        w=float(input("\n\tPlease enter your weight(in kg): "))
        h=float(input("\n\tPlease enter your height(in m): "))
        bmi=w/((h)**2)
        d['Height']=h
        d['Weight']=w
        if bmi<18.5:
            d['BMI']=[bmi,"Looks like you are underweight."]
        elif bmi>30:
            d['BMI']=[bmi,"You seem to be obese."]
        elif bmi>25 and bmi<29.9:
            d['BMI']=[bmi,"Looks like you are overweight"]
        else:
            d['BMI']=[bmi,"You are within the normal BMI range."]
        food=input("Breakfast?\n1.Fruits/Dairy\n2.Just carbs\n3.Skip\n")
        d['Food'] = {
            '1': "Fresh produce is great! Keep it up.",
            '2': "Try more fiber and veggies in the morning.",
            '3': "Don't skip! Breakfast boosts metabolism."
        }.get(food, "No input")
        sleep=input("Sleep?\n1.8hrs\n2.10-12hrs\n3.Barely any\n")
        d['Sleep'] = {
            '1': "Perfect amount!",
            '2': "Oversleeping? Monitor energy levels.",
            '3': "Lack of sleep harms focus and immunity."
        }.get(sleep, "No input")
        ex=input("Exercise in last 7 days?\n1.None\n2.1-3 days\n3.More than 3\n")
        d['Exercise'] = {
            '1': "Physical activity is crucial!",
            '2': "Decent. Try to do more!",
            '3': "Awesome job!"
        }.get(ex, "No input")
        vice=input("Drugs or Alcohol?\n1.Yes\n2.No\n3.Only alcohol\n")
        d['Vices'] = {
            '1': "Seek help. Mentor service is available.",
            '2': "Great job avoiding harmful substances.",
            '3': "Limit alcohol for long-term health."
        }.get(vice, "No input")

        fi=open('MemberDiagnosis.dat','rb+')
        try:
            while True:
                pos=fi.tell()
                m=pickle.load(fi)
                if m['FitGenieID']==fitid:
                    m['Diagnosis']=d
                    fi.seek(pos)
                    pickle.dump(m,fi)
                    print("\nDiagnosis Saved!\n")
                    for k, v in m.items():
                        if k != 'Diagnosis':
                            print(f"{k}: {v}")
                    print("\nDiagnosis:")
                    for k, v in d.items():
                        print(f"\t{k}: {v}")
        except EOFError:
            fi.close()

    elif cho=='2':
        fi=open('MemberDiagnosis.dat','rb')
        try:
            while True:
                m=pickle.load(fi)
                if m['FitGenieID']==fitid:
                    print("\nYour Previous Diagnosis:\n")
                    for k, v in m['Diagnosis'].items():
                        print(f"\t{k}: {v}")
        except EOFError:
            fi.close()

    elif cho=='3':
        print("\nMentor Booking:\n\tStreet: 408, Mango Grove\n\tCity: Mumbai\n\tContact: 8769678546\n\tEmail: fitgenie@gmail.com\n")
    elif cho=='4':
        fb=input("How was your experience with FitGenie?\n")
        print("Thanks! We appreciate your feedback.")
    else:
        print("Invalid Choice")

def startdiagnosis():
    global fitid
    fitid=int(input("Enter your FitGenieID (or 0 to retrieve): "))
    if fitid==0:
        pn=int(input("Enter your Phone Number: "))
        co=mc.connect(host='localhost',user="root",passwd='')
        cur=co.cursor()
        cur.execute("use FitGenie")
        cur.execute('select * from Members WHERE PhoneNo=%s', (pn,))
        rec=cur.fetchall()
        for r in rec:
            print("FitGenieID:",r[0])
            print("Name:",r[1], r[2])
        fitid=int(input("Now enter your FitGenieID again: "))
        thediagnosis()
    else:
        thediagnosis()

def AccountCreate():
    con=mc.connect(host='localhost',user="root",passwd='')
    cur=con.cursor()
    cur.execute("Create database if not exists FitGenie")
    cur.execute("use FitGenie")
    cur.execute('''Create table if not exists Members(
        FitGenieID int primary key,
        FirstName varchar(15),
        LastName varchar(15),
        PhoneNo bigint,
        DateofBirth date
    )''')
    fna=input("First Name: ")
    lna=input("Last Name: ")
    phno=int(input("Phone Number: "))
    dob=input("Date of Birth (YYYY-MM-DD): ")
    i=random.randint(0,9)
    memID=(phno%100000)+(67*i)
    cur.execute("insert into Members values(%s,%s,%s,%s,%s)", (memID,fna,lna,phno,dob))
    con.commit()
    print("Account created. Your FitGenieID is:",memID)
    st={'First Name':fna,'Last Name':lna,'Phone No.':phno,'Date of Birth':dob,'FitGenieID':memID}
    with open('MemberDiagnosis.dat','ab') as f:
        pickle.dump(st,f)
    if input("Login now? (y/n): ")=='y':
        startdiagnosis()

def Login():
    ch=input("Welcome to FitGenie!\n1. Existing User\n2. New User\n")
    if ch=='1':
        startdiagnosis()
    else:
        AccountCreate()

ans='y'
while ans.lower()=='y':
    ch=input("1. Login\n2. About FitGenie\n")
    if ch=='2':
        print("FitGenie™ offers personalized fitness diagnostics and mentor support using lifestyle inputs, helping you lead a healthier life!")
        if input("Login now? (y/n): ")=='y':
            Login()
    else:
        Login()
    ans=input("Do you want to continue? (y/n): ")
