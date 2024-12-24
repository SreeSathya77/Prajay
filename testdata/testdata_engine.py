#######################################################################################################################
# Package Title: Test Data Generator for QM ETC APIs and Application.
# Revision: 1.0.
# Date: 22 Oct 2024
# Author(s): Anand
# Contributor : Renu
# Approve(s): Anand & Renu
#######################################################################################################################

import json
import csv
import random
from typing import Any
from faker.contrib.pytest.plugin import Faker
from datetime import datetime, timedelta

from gevent.greenlet import joinall

import settings.qm_business_rules as doa_rules
from testdata.fetch_master_db_details import QMMasterTables
from src.utils.logger import logger

class FakeDataGenerator():
    fake = Faker()
    master_db = QMMasterTables()
    vehicle_repo = {"Toyota": ["Camry", "Corolla", "RAV4", "Tacoma"],
                    "Ford": ["F-150", "Mustang", "Explorer", "Escape"],
                    "Honda": ["Civic", "Accord", "CR-V", "HR-V"],
                    "Chevrolet": ["Silverado", " Malibu", "Equinox", "Corvette"],
                    "Nissan": ["Al-tima", "Rogue", "Sen-tra", "Pathfinder"],
                    "BMW": ["3 Series", "5 Series", "X5", "X3"],
                    "Mercedes-Benz": ["C-Class", "E-Class", "GLE", "S-Class"],
                    "Volkswagen": ["Jetta", "Pass-at", "Tiguan", "Golf"],
                    "Subaru": ["Outback", "Forester", "WRX", "Ascent"],
                    "Hyundai": ["Sonata", "El-antra", "Tucson", "Santa Fe"],
                    "Kia": ["Optima", "So-rent-o", "Sport-age", "Forte"],
                    "Lexus": ["ES", "RX", "NX", "GS"],
                    "Audi": ["A4", "A6", "Q5", " Q7"],
                    "Tesla": ["Model S", " Model 3", "Model X", "Model Y"],
                    "Subaru	": ["Forester", "Outback", "Im-pre-za", "Cross-trek"]}
    colors = ["Red", "Blue", "Green", "Black", "White"]
    vehicle_class = ["2 Axle", "3 Axle", "4 Axle", "5 Axle", "6-plus Axles"]

    def __init__(self, **config: "Any"):
        super().__init__(**config)
        self.country="United States"

    def set_doa_key(self,doa_key):
        if doa_key =="":
            doa_key = random.choice(list(doa_rules.ID.keys()))
            logger.info(f"Generating TestData : {doa_key}")
            doa_id = doa_rules.ID.get(doa_key)
            logger.info(f"Generating TestData for DOA ID is : {doa_id}")
            doa_data = doa_rules.DOA.get(doa_id)
            logger.info("TestData for DOA: { doa_data }")
        else:
            doa_key = doa_key
            logger.info(f"Generating TestData : {doa_key}")
            doa_id = doa_rules.ID.get(doa_key)
            logger.info(f"Generating TestData for DOA ID is : {doa_id}")
            doa_data = doa_rules.DOA.get(doa_id)
        return doa_data

    def generate_random_date(self, start_year, end_year, format_type="%Y-%m-%d"):
        """
        Generates a random date between the start year and the end year in the format 'YYYY-MM-DD'.

        :param start_year: The starting year for the random date.
        :param end_year: The ending year for the random date.
        :param format_type: The date format
        :return: A random date as a string in the format 'YYYY-MM-DD'.
        """
        # Define the start and end dates
        start_date = datetime(start_year, 1, 1)
        end_date = datetime(end_year, 12, 31)

        # Calculate the range of days between the start and end dates
        days_range = (end_date - start_date).days

        # Generate a random number of days to add to the start date
        random_days = random.randint(0, days_range)
        random_date = start_date + timedelta(days=random_days)

        # Return the date as a formatted string
        return random_date.strftime(format_type)

    # TODO: get address will be clean the plate @sowjanya
    def get_address(self):
        return {
                "country": self.fake.country(),
                "address1": self.fake.street_address(),
                "address2": self.fake.street_name(),
                "city": self.fake.city(),
                "state": self.fake.city(),
                "zipCode": self.fake.zipcode(),
                #"isCurrentAddress": random.choice([True,False]),
                 "isCurrentAddress": False,
                 "lastUpdatedDate": "2024-09-01T12:00:00"
                }

    def get_vehicle_information(self,account_ref,country="United States"):
        self.country=country
        address_country = self.master_db.get_states_by_country(self.country)
        state_name = address_country['state_name']
        state_code = address_country['state_code']
        country_name = address_country['country_name']
        country_code = address_country['country_code']
        vehicle_make = random.choice(list(self.vehicle_repo.keys()))
        vehicle_model = random.choice(list(self.vehicle_repo.get(vehicle_make)))
        return {
                "accountRefId": account_ref,
                "isHamRadioOperator": random.choice([True, False]),  # Randomly set True or False
                "temporary": random.choice([True, False]),  # Randomly set True or False
                "plateNumber": self.get_plate_number,
                "plateState": state_code,
                "plateStateDesc": state_name,
                "plateCountry":country_code,
                "plateCountryDesc": country_name,
                "plateType": random.choice(["COMMERCIAL", "PERSONAL", "ELECTRIC"]),
                "year": self.generate_random_date(2013,2025,"%Y"),
                "vehicleMake": vehicle_make,
                "vehicleModel": vehicle_model,
                "vehicleColor": random.choice(self.colors),
                "vehicleClass": random.choice(self.vehicle_class),
                "plateRegistrationStartDate": self.generate_random_date(2013,2025),
                "plateRegistrationEndDate": self.generate_random_date(2013,2025),
                "tagid": random.randint(10000000,99999999),
                "tagAgencyId": random.randint(1000,9999),
                "requestTag": random.choice([True,False]),
                "hasTag": random.choice([True,False]),
                "itemType": "Tolling Device",
                "tagType": "RFID",
                "mounting": "Windshield",
                "tagDeliveryMethod": self.get_plate_tag_delivery_method,
                "tagAliasName": self.fake.first_name(),

                "shippingAddress":
                {
                "country": country_name,
                "state": state_name,
                "city": self.fake.city(),
                "addressline1": self.fake.street_name(),
                "addressline2": self.fake.street_address(),
                "zipCode": self.fake.zipcode(),
                "sameAddressForBilling": random.choice([True,False]),
                "sameAddressForShipping": True,
                "sameAddressForMailing": random.choice([True,False]),
                "addressType": "SHIPPING",
                "isprimaryAddress": random.choice([True,False])
                },
                "comments": "This tag information is generated by the automation"
                }

    @property
    def generate_toll_info(self):
        locations = ["Highway 1", "Bridge A", "Tunnel 5", "Toll Plaza 3"]
        return {
            "location": random.choice(locations),
            "amount": round(random.uniform(1.0, 50.0), 2),
            "date": "2023-10-{} {}:{}:{}".format(random.randint(1, 31), random.randint(0, 23), random.randint(0, 59),
                                                 random.randint(0, 59))
        }

    def get_full_address(self, country="United States"):
        self.country = country
        address_country = self.master_db.get_states_by_country(self.country)
        return {"addressline1": self.fake.street_address(),
                "addressline2": self.fake.street_address(),
                "city": self.fake.city(),
                "state": address_country['state_name'],
                "country": self.country,
                "zipCode": self.fake.zipcode(),
                "sameAddressForBilling": random.choice([True, False]),
                "sameAddressForShipping": random.choice([True, False]),
                "sameAddressForMailing": random.choice([True, False]),
                "addressType": random.choice(["BILLING", "MAILING", "SHIPPING"]),
                "isPrimaryAddress": random.choice([True, False])
                # "isCurrentAddress":  status,
                # "lastUpdatedDate": "2024-09-01T12:00:00"
                }

    def get_demographic_info(self, doa_key ):
        # fetch DOA for given key
        doa_data = self.set_doa_key(doa_key)
        email = self.fake.email()
        demographic = {
            "prefix": random.choice(["MR", "MISS", "MRS", "MS","DR"]),
            "suffix":random.choice(["JR","SR","PHD","OTHER"]),
            "firstName": self.fake.first_name(),
            "middleName": self.fake.name().split(" ")[0],
            "lastName": self.fake.last_name(),
            "accountTypeDesc": self.fake.sentence(),
            "emailList": [
                {
                    "emailAddress": email,
                    "confirmEmailAddress": email,
                    "isPrimaryEmail": True,
                    "emailType": random.choice(["PRIMARYMAIL", "ALTERNATEMAIL"]),
                }
            ],
            "phoneList": [
                {
                    "countryCode": str(random.randint(100, 999)),
                    "phoneNumber": str(random.randint(6000500000, 9999999999)),
                    "isPrimaryPhone": True,
                    "phoneType": random.choice(["PHONENUM", "WORKPHONE", "HOMEPHONE"])

                }
            ],
            "addressList":[
                self.get_full_address(country='Canada')
            ],
            "vehicleDataassociteWithTag":[
                {
                    "vehicleId":"string",
                    "tagSerialNum":"string"
                }
            ]
        }
        if doa_key[0:2] == "FB":
                demographic = demographic| {
                    "companyName": self.fake.company(),
                    "companyCode": self.fake.random_number(5)
                 }
        return doa_data | demographic

    def get_vendor_details(self, country="United States"):
        self.country = country
        address_country = self.master_db.get_states_by_country(self.country)
        state_name = address_country['state_name']
        state_code = address_country['state_code']
        country_name = address_country['country_name']
        country_code = address_country['country_code']
        company_name = self.fake.company()
        site = self.fake.name().replace(" ","")
        return {
            "vendorCompanyName": company_name,
            "vendorCompanyOwnerName": self.fake.name(),
            "vendorCompanyWebsite": "https://www.{0}.com".format(site),
            "vendorCompanyDemographicInformation": {
                "address": {
                    "addressLine1": self.fake.street_name(),
                    "addressLine2": self.fake.street_address(),
                    "city": self.fake.city(),
                    "stateCode": state_code,
                    "stateDesc": state_name,
                    "countryCode": country_code,
                    "countryDesc": country_name,
                    "zipCode": self.fake.zipcode(),
                    "zipPlusFour": "10001",
                    "addressType": "BILLING"
                },
                "phoneInformation": [
                    {
                        "phoneNumber": self.fake.phone_number(),
                        "phoneType": "MOBILE",
                        "isPrimaryPhone": True
                    },
                    {
                        "phoneNumber": f"{random.randint(100,999)}-{random.randint(1000,10000)}",
                        "phoneType": "PERSONAL",
                        "isPrimaryPhone": False
                    }
                ],
                "faxNumber": f"{random.randint(100,999)}-{random.randint(1000,10000)}",
                "emailInformation": [
                    {
                        "emailAddress": self.fake.email(),
                        "emailType": "PRIMARY",
                        "isPrimaryEmail": True
                    },
                    {
                        "emailAddress": self.fake.email(),
                        "emailType": "SECONDARY",
                        "isPrimaryEmail": False
                    }
                ],
            },
            "status": "ACTIVE",
            "createdBy": "admin",
            "createdDateTime": "2024-11-02T10:00:00",
            "updatedBy": "admin",
            "updatedDateTime": "2024-11-02T10:00:00"
        }

    def get_add_inventory_type(self, inventory_type):
        return {
              "inventoryType": inventory_type,
              "inventoryDesc": self.fake.text(8),
              "createdOn": self.fake.date_time().isoformat() + "Z",
              "createdBy": self.fake.first_name(),
              "lastModifiedOn": self.fake.date_time().isoformat() + "Z",
              "lastModifiedBy":  self.fake.first_name(),
              "status": random.choice(["ACTIVE", "INACTIVE"])
            }

    @property
    def generate_payment_card_info(self):
        card_types = ["CREDIT", "DEBIT"]
        return {

            "cardId": "{}{}{}{}".format(random.randint(1000, 9999), random.randint(1000, 9999),
                                             random.randint(1000, 9999), random.randint(1000, 9999)),
            "paymentMethod": random.choice(card_types),
            "cardAlias": " ".join(self.fake.words())
        }

    def address_details(self):
        return {
            "billingAddress": [ self.get_address() ],
            "mailingAddress": [ self.get_address() ],
            "shippingAddress": [ self.get_address() ] }

    @property
    def get_plate_number(self):
        plat_number = "{} {}".format((self.fake.state()[:2]).upper(), random.randint(100, 9999))
        return plat_number

    @property
    def get_plate_item_type(self):
        return random.choice(["STICKER_TAG", "LICENSE_PLATE_TAG", "HARD_CASE_TAG", "INTEGRATED"])

    @property
    def get_plate_tag_type(self):
        return random.choice(["STICKER", "MOUNTED"])
    @property
    def get_plate_tag_delivery_method(self):
        return random.choice(["HAND_TO_CUSTOMER", "MAIL_TO_CUSTOMER", "CUSTOMER_ALREADY_HAS_TRANSPONDER"])

    def tag_information(self, tags=1):
        tag_info = list()
        for t in range(tags):
            tag_details = {
                "hasTag": True,
                "tagAgencyId": "Agt{}".format(random.randint(10,20)),
                "tagId": "RENU{}".format(random.randint(10,99)),
                "itemType": random.choice(["STICKER_TAG", "LICENSE_PLATE_TAG", "HARD_CASE_TAG", "INTEGRATED"]),
                "tagType": random.choice(["STICKER", "MOUNTED"]),
                "mounting": random.choice(["YES","NO"]),
                "tagDeliveryMethod": random.choice(["HAND_TO_CUSTOMER", "MAIL_TO_CUSTOMER", "CUSTOMER_ALREADY_HAS_TRANSPONDER"]),
                "tagAliasName": self.fake.first_name()
            }
            tag_info.append(tag_details)
        return tag_info


class TestDataDriver(FakeDataGenerator):

    def __init__(self):
        pass
