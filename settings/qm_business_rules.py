"""
This file contains only constance variables for the test project
QA_API : http://10.10.10.61:8081/qm/cam
ID : contains given ID's to test data decided by the team positive scenarios followed by negative
DOA : contains given definition of Accounts combination defined by the project owner and arranged by positive followed by negative

"""

import random

# Application variables
APP_URL = "http://10.10.10.60:8083/qm/iam/login"
USERNAME = "anandaraj.pandiri@gmail.com"
PASSWORD = "anand"

# API variables
QA_API = "http://10.10.10.61:8081/qm/cam"

ID = dict(PA1="Personal_Revenue_Prepaid_Non_visitor", PA2="Personal_Revenue_Prepaid_Visitor",
          PA3="Personal_Non_Revenue_Postpaid_Non_visitor", PA4="Personal_Revenue_Postpaid_Visitor",
          PA5="Personal_Non_Revenue_Prepaid_Non_Visitor", PA6="Personal_Non_Revenue_Postpaid_Visitor",
          BA1="Business_Revenue_Prepaid_Non_Visitor", BA2="Business_Non_Revenue_Postpaid_Non_Visitor",
          BA3="Business_Revenue_Postpaid_Visitor",BA4="Business_Non_Revenue_Prepaid_Non_Visitor",
          FB1 = "Fleet_Business_Revenue_Postpaid_As_Non_Visitor_SubFleet_LeaseOrDealership_None_RentalType",
          FB2 = "Fleet_Business_Revenue_Postpaid_As_Non_Visitor_SubFleet_Rental_Any_RentalType",
          FB3 = "Fleet_Business_Revenue_Postpaid_As_Non_Visitor_SubFleet_None_Rental_Any_RentalType",
          FB4 = "Fleet_Business_Revenue_Postpaid_As_Visitor_Any_SubFleet_None_RentalType"
)

""" 
Personal account types 
    +ve scenarios 
        PA1- PA3
    -ve scenarios 
        PA4- PA6
-----------------------
Business non-fleet account types 
    +ve scenarios 
        BA1- BA2
    -ve scenarios 
        BA3- BA4
-----------------------
Business fleet account types 
    +ve scenarios 
        FB1- FB2
    -ve scenarios 
        FB3- FB4
"""
DOA = dict(Personal_Revenue_Prepaid_Non_visitor={
    "accountType": "PERSONAL",
    "revenueCategory": "REVENUE",
    "paymentModel": "PREPAID",
    "visitor": False,
}, Personal_Revenue_Prepaid_Visitor={
    "accountType": "PERSONAL",
    "revenueCategory": "REVENUE",
    "paymentModel": "PREPAID",
    "visitor": True,
}, Personal_Non_Revenue_Postpaid_Non_visitor={
    "accountType": "PERSONAL",
    "revenueCategory": "NON_REVENUE",
    "paymentModel": "POSTPAID",
    "visitor": False,
}, Personal_Revenue_Postpaid_Visitor={
    "accountType": "PERSONAL",
    "revenueCategory": "REVENUE",
    "paymentModel": "POSTPAID",
    "visitor": True,
}, Personal_Non_Revenue_Prepaid_Non_Visitor={
    "accountType": "PERSONAL",
    "revenueCategory": "NON_REVENUE",
    "paymentModel": "PREPAID",
    "visitor": False,
}, Personal_Non_Revenue_Postpaid_Visitor={
    "accountType": "PERSONAL",
    "revenueCategory": "NON_REVENUE",
    "paymentModel": "POSTPAID",
    "visitor": True,
},
Business_Revenue_Prepaid_Non_Visitor={
    "accountType": "BUSINESS",
    "revenueCategory": "REVENUE",
    "paymentModel": "PREPAID",
    "isFleet": False,
    "visitor": False,
},
Business_Revenue_Postpaid_Visitor ={
    "accountType": "BUSINESS",
    "revenueCategory": "REVENUE",
    "paymentModel": "POSTPAID",
    "isFleet": False,
    "visitor": True,
 },
Business_Non_Revenue_Postpaid_Non_Visitor ={
    "accountType": "BUSINESS",
    "revenueCategory": "NON_REVENUE",
    "paymentModel": "POSTPAID",
    "isFleet": False,
    "visitor": False,
},
Business_Non_Revenue_Prepaid_Non_Visitor ={
    "accountType": "BUSINESS",
    "revenueCategory": "NON_REVENUE",
    "paymentModel": "PREPAID",
    "isFleet": False,
    "visitor": False,
},
Fleet_Business_Revenue_Postpaid_As_Non_Visitor_SubFleet_LeaseOrDealership_None_RentalType ={
        "accountType": "BUSINESS",
        "revenueCategory": "REVENUE",
        "paymentModel": "POSTPAID",
        "visitor": False,
        "isFleet": True,
        "subFleet": random.choice(["LEASE", "DEALERSHIP"]),
    },
Fleet_Business_Revenue_Postpaid_As_Non_Visitor_SubFleet_Rental_Any_RentalType ={
    "accountType": "BUSINESS",
    "revenueCategory": "REVENUE",
    "paymentModel": "POSTPAID",
    "visitor": False,
    "isFleet": True,
    "subFleet": "RENTAL",
    "rentalType": random.choice(["BILL_THE_CUSTOMER", "CUSTOMER_PAYS"]),
},
Fleet_Business_Revenue_Postpaid_As_Non_Visitor_SubFleet_None_Rental_Any_RentalType ={
    "accountType": "BUSINESS",
    "revenueCategory": "REVENUE",
    "paymentModel": "POSTPAID",
    "visitor": False,
    "isFleet": True,
    "subFleet": random.choice(["LEASE", "DEALERSHIP"]),
    "rentalType": random.choice(["BILL_THE_CUSTOMER", "CUSTOMER_PAYS"]),
},
Fleet_Business_Revenue_Postpaid_As_Visitor_Any_SubFleet_None_RentalType ={
    "accountType": "BUSINESS",
    "revenueCategory": "REVENUE",
    "paymentModel": "POSTPAID",
    "visitor": True,
    "isFleet": True,
    "subFleet": random.choice(["LEASE", "DEALERSHIP", "RENTAL"]),
}
)
