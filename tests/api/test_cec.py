import json
from typing import Match
import pytest
from http import HTTPStatus
from src.utils.logger import logger
from testdata.testdata_engine import TestDataDriver

@pytest.mark.smoke
@pytest.mark.openaccount
class TestOpenAccountCreation:
    # Class properties
    # To store account reference ids
    temp_account_ref_ids = {"Dummy1": {"accountRefId": 123123}}

    def __get_payload(self, testdata_set, country="United States"):
        payload = dict()
        logger.info(f"Testing account creation with type: {testdata_set}")
        testdata = TestDataDriver()
        for api_name in testdata_set.keys():
            match api_name:
                case "create_or_draft":
                    payload = testdata.get_demographic_info(doa_key=testdata_set["create_or_draft"])
                case "vehicle_tag_add":
                    payload = testdata.get_vehicle_information(account_ref=testdata_set["vehicle_tag_add"]['accountRefId'], country=country)
        return payload


    @pytest.mark.smoke
    @pytest.mark.parametrize("account_type,expected_status", [
        pytest.param("PA1", HTTPStatus.CREATED,
                     id="POST Personal_Revenue_Prepaid_Non_visitor"),
        pytest.param("PA2", HTTPStatus.CREATED,
                     id="POST Personal Revenue Prepaid Visitor"),
        pytest.param("PA3", HTTPStatus.CREATED,
                     id="POST Personal Non Revenue Postpaid Non visitor"),
        pytest.param("BA1", HTTPStatus.CREATED,
                     id="POST Business Revenue Prepaid Non Visitor"),
        pytest.param("BA2", HTTPStatus.CREATED,
                     id="POST Business Non Revenue Postpaid Non Visitor"),
        pytest.param("FB1", HTTPStatus.CREATED,
                     id="POST Fleet Business Revenue Postpaid As Non Visitor SubFleet Rental Any RentalType"),
        pytest.param("FB2", HTTPStatus.CREATED,
                     id="POST Fleet_Business_Revenue_Postpaid_As_Non_Visitor_SubFleet_Rental_Any_RentalType")
    ])
    def test_account_create_or_draft_for_doa(self, api_client, account_type, expected_status):
        """Validating API - create or draft with different DOA account types
        args:
            api_client :  API fixtures with scope to session
            account_type : DOA account type
            expected_status : HTTPStatus constants
        """
        logger.info(f"Testing account creation with type: {account_type}")
        base_account_payload = self.__get_payload(testdata_set = {"create_or_draft":account_type})
        try:
            response = api_client.post("/api/accounts/demographics/createOrDraft", data=base_account_payload)
            assert response.status_code == expected_status
            if expected_status == HTTPStatus.CREATED:
                self.temp_account_ref_ids[account_type] = {'accountRefId': response.json()['accountRefId']}
                logger.info(
                    f"Account Reference ID {response.json()['accountRefId']} is created for the account type: {account_type}")
                logger.info(f"Successfully created account with type: {account_type}")
                assert response.json()["status"]== "Created"
                logger.info(f"status : Created")
                assert response.json()["message"]== "Temporary Account successfully created"
                logger.info(f"Message : Temporary Account successfully created")
            else:
                logger.info(f"Successfully validated rejection of invalid account type: {account_type}")
                logger.info(f"Here the payload for the same: {base_account_payload}")

        except Exception as e:
            logger.error(f"Error testing account type {account_type}", exc_info=e)
            raise

    @pytest.mark.smoke
    @pytest.mark.parametrize("account_type,expected_status", [
        pytest.param("PA1", HTTPStatus.OK,
                     id="TC_Validate Demographics Get API Personal_Revenue_Prepaid_Non_visitor"),
        pytest.param("PA2", HTTPStatus.OK,
                     id="TC Validate Demographics Get API Personal Revenue Prepaid Visitor"),
        pytest.param("PA3", HTTPStatus.OK,
                     id="TC Validate Demographics Get Personal Non Revenue Postpaid Non visitor"),
        pytest.param("BA1", HTTPStatus.OK,
                     id="TC Validate Demographics Get Business Revenue Prepaid Non Visitor"),
        pytest.param("BA2", HTTPStatus.OK,
                     id="TC Validate Demographics Get Business Non Revenue Postpaid Non Visitor"),
        pytest.param("FB1", HTTPStatus.OK,
                     id="TC Validate Demographics Get Fleet Business Revenue Postpaid As Non Visitor SubFleet Rental Any RentalType"),
        pytest.param("FB2", HTTPStatus.OK,
                     id="TC Validate Demographics Get Fleet Business Revenue Postpaid As Non Visitor SubFleet Rental Any RentalType")
    ])
    def test_account_demographics_get_for_doa(self,api_client, account_type, expected_status):
        """Validating API - demographics get with different DOA account types
        args:
            api_client :  API fixtures with scope to session
            account_type : DOA account type
            expected_status : HTTPStatus constants
        """
        logger.info(f"Testing account creation with type: {self.temp_account_ref_ids[account_type]}")
        base_account_payload = self.temp_account_ref_ids[account_type]

        try:
            response = api_client.post("/api/accounts/demographics/get", data=base_account_payload)
            assert response.status_code == expected_status

            if expected_status == HTTPStatus.OK:
                assert response.json()["accountStatus"]== "SAVED"
                logger.info(f"Message : Account RefID. Status as SAVED")
            else:
                logger.info(f"Account RefID is not invalid or available", self.temp_account_ref_ids[account_type])

        except Exception as e:
            logger.error(f"Error testing account type {account_type}", exc_info=e)
            raise


    @pytest.mark.smoke
    @pytest.mark.parametrize("account_type,expected_status", [
        pytest.param("PA1", HTTPStatus.CREATED,
                     id="POST Personal_Revenue_Prepaid_Non_visitor"),
        pytest.param("PA2", HTTPStatus.CREATED,
                     id="POST API Personal Revenue Prepaid Visitor"),
        pytest.param("PA3", HTTPStatus.CREATED,
                     id="POST Personal Non Revenue Postpaid Non visitor"),
        pytest.param("BA1", HTTPStatus.CREATED,
                     id="POST  Business Revenue Prepaid Non Visitor"),
        pytest.param("BA2", HTTPStatus.CREATED,
                     id="POST  Business Non Revenue Postpaid Non Visitor"),
        pytest.param("FB1", HTTPStatus.CREATED,
                     id="POST Fleet Business Revenue Postpaid As Non Visitor SubFleet Rental Any RentalType"),
        pytest.param("FB2", HTTPStatus.CREATED,
                     id="POST Fleet Business Revenue Postpaid As Non Visitor SubFleet Rental Any RentalType")
    ])
    def test_account_vehicle_tag_add_for_doa(self,api_client, account_type, expected_status):
        """Validating API - demographics get with different DOA account types
        args:
            api_client :  API fixtures with scope to session
            account_type : DOA account type
            expected_status : HTTPStatus constants
        """
        logger.info(f"Testing account creation with type: {self.temp_account_ref_ids[account_type]}")
        base_account_payload = self.__get_payload(testdata_set={"vehicle_tag_add": self.temp_account_ref_ids[account_type]},country="United States")

        try:
            response = api_client.post("/api/accounts/VehicleTag/add", data=base_account_payload)
            assert response.status_code == expected_status
            if expected_status == HTTPStatus.CREATED:
                self.temp_account_ref_ids[account_type]['vehicleRefId'] =  response.json()['vehicleRefId']
                logger.info(f"Message : Account RefID. Status as created with vehicleRefId : {response.json()['vehicleRefId']}")
            else:
                logger.info(f"Account RefID is not invalid or available {self.temp_account_ref_ids[account_type]}")

        except Exception as e:
            logger.error(f"Error testing account type {account_type}", exc_info=e)
            raise


    @pytest.mark.smoke
    @pytest.mark.parametrize("account_type,expected_status", [
        pytest.param("PA1", HTTPStatus.CREATED,
                     id="POST Personal_Revenue_Prepaid_Non_visitor"),
        pytest.param("PA2", HTTPStatus.CREATED,
                     id="POST Personal Revenue Prepaid Visitor"),
        pytest.param("PA3", HTTPStatus.CREATED,
                     id="POST Personal Non Revenue Postpaid Non visitor"),
        pytest.param("BA1", HTTPStatus.CREATED,
                     id="POST Business Revenue Prepaid Non Visitor"),
        pytest.param("BA2", HTTPStatus.CREATED,
                     id="POST Business Non Revenue Postpaid Non Visitor"),
        pytest.param("FB1", HTTPStatus.CREATED,
                     id="POST Fleet Business Revenue Postpaid As Non Visitor SubFleet Rental Any RentalType"),
        pytest.param("FB2", HTTPStatus.CREATED,
                     id="POST Fleet Business Revenue Postpaid As Non Visitor SubFleet Rental Any RentalType")
    ])
    def test_account_vehicle_tag_submit_for_doa(self,api_client, account_type, expected_status):
        """Validating API - demographics get with different DOA account types
        args:
            api_client :  API fixtures with scope to session
            account_type : DOA account type
            expected_status : HTTPStatus constants
        """
        logger.info(f"Testing account creation with type: {self.temp_account_ref_ids[account_type]}")
        base_account_payload = self.temp_account_ref_ids[account_type]
        try:
            response = api_client.post("/api/accounts/VehicleTag/submit", data=base_account_payload)
            assert response.status_code == expected_status
            if expected_status == HTTPStatus.CREATED:
                assert response.json()["status"] == "Success"
                self.temp_account_ref_ids[account_type]['accountId'] = response.json()['accountId']
                logger.info(f"Message : Account is created Successfully and ID is : {response.json()['accountId']}")
            else:
                logger.info(f"Account RefID is not invalid or available {self.temp_account_ref_ids[account_type]}")

        except Exception as e:
            logger.error(f"Error testing account type {account_type}", exc_info=e)
            raise

    @pytest.mark.smoke
    @pytest.mark.parametrize("account_type,expected_status", [
        pytest.param("PA1", HTTPStatus.OK,
                     id="PUT Personal_Revenue_Prepaid_Non_visitor"),
        pytest.param("PA2", HTTPStatus.OK,
                     id="PUT Personal Revenue Prepaid Visitor"),
        pytest.param("PA3", HTTPStatus.OK,
                     id="PUT Personal Non Revenue Postpaid Non visitor"),
        pytest.param("BA1", HTTPStatus.OK,
                     id="PUT Business Non Revenue Postpaid Non Visitor"),
        pytest.param("FB1", HTTPStatus.OK,
                     id="PUT Fleet Business Revenue Postpaid As Non Visitor SubFleet Rental Any RentalType"),
           ])
    def test_account_vehicle_tag_update_for_doa(self,api_client, account_type, expected_status):
        """Validating API - demographics get with different DOA account types
        args:
            api_client :  API fixtures with scope to session
            account_type : DOA account type
            expected_status : HTTPStatus constants
        """
        logger.info(f"Testing account creation with type: {self.temp_account_ref_ids[account_type]}")
        base_account_payload = {'vehicleRefId': self.temp_account_ref_ids[account_type]['vehicleRefId'],
                                'vehicleColor': 'RED'}
        try:
            response = api_client.put("/api/accounts/VehicleTag/update", data=base_account_payload)
            assert response.status_code == expected_status
            if expected_status == HTTPStatus.OK:
                assert response.json()["vehicleRefId"] == self.temp_account_ref_ids[account_type]['vehicleRefId']
                assert response.json()["vehicleColor"] == "RED"
            else:
                logger.info(f"Account RefID is not invalid or available {self.temp_account_ref_ids[account_type]}")
        except Exception as e:
            logger.error(f"Error testing account type {account_type}", exc_info=e)
            raise

    @pytest.mark.e2e
    @pytest.mark.parametrize("account_type,expected_status", [
        pytest.param("PA1", HTTPStatus.CREATED,
                     id="POST Personal_Revenue_Prepaid_Non_visitor"),
        pytest.param("PA2", HTTPStatus.CREATED,
                     id="POSTe Personal Revenue Prepaid Visitor"),
        pytest.param("PA3", HTTPStatus.CREATED,
                     id="POST Personal Non Revenue Postpaid Non visitor"),
        pytest.param("BA1", HTTPStatus.CREATED,
                     id="POST Business Revenue Prepaid Non Visitor"),
        pytest.param("BA2", HTTPStatus.CREATED,
                     id="POST Business Non Revenue Postpaid Non Visitor"),
        pytest.param("FB1", HTTPStatus.CREATED,
                     id="POST Fleet Business Revenue Postpaid As Non Visitor SubFleet Rental Any RentalType"),
        pytest.param("FB2", HTTPStatus.CREATED,
                     id="POST Fleet_Business_Revenue_Postpaid_As_Non_Visitor_SubFleet_Rental_Any_RentalType")
    ])
    def test_open_account_for_doa(self, api_client, account_type, expected_status):
        """Validating API - create or draft with different DOA account types
        args:
            api_client :  API fixtures with scope to session
            account_type : DOA account type
            expected_status : HTTPStatus constants
        """
        logger.info(f"Validate create_or_draft API for the account type: {account_type}")
        open_account_ref_ids = {}
        base_account_payload = self.__get_payload(testdata_set={"create_or_draft": account_type})
        try:
            response = api_client.post("/api/accounts/demographics/createOrDraft", data=base_account_payload)

            assert response.status_code == expected_status
            if expected_status == HTTPStatus.CREATED:
                open_account_ref_ids[account_type] = {'accountRefId': response.json()['accountRefId']}
                logger.info(
                    f"Account Reference ID {response.json()['accountRefId']} is created for the account type: {account_type}")
                logger.info(f"Successfully created account with type: {account_type}")
                assert response.json()["status"] == "Created"
                logger.info(f"status : Created")
                assert response.json()["message"] == "Temporary Account successfully created"
                logger.info(f"Message : Temporary Account successfully created")
            else:
                logger.info(f"Successfully validated rejection of invalid account type: {account_type}")
                logger.info(f"Here the payload for the same: {base_account_payload}")

        except Exception as e:
            logger.error(f"Error testing account type {account_type}", exc_info=e)
            raise

        logger.info(f"Validating demographics_get API for the account type: {open_account_ref_ids[account_type]}")
        expected_status = HTTPStatus.OK
        base_account_payload = open_account_ref_ids[account_type]

        try:
            response = api_client.post("/api/accounts/demographics/get", data=base_account_payload)
            assert response.status_code == expected_status

            if expected_status == HTTPStatus.OK:
                assert response.json()["accountStatus"] == "SAVED"
                logger.info(f"Message : Account RefID. Status as SAVED")
            else:
                logger.info(f"Account RefID is not invalid or available", open_account_ref_ids[account_type])

        except Exception as e:
            logger.error(f"Error testing account type {account_type}", exc_info=e)
            raise

        logger.info(f"Validate vehicle_tag_add API for the account type: {open_account_ref_ids[account_type]}")
        base_account_payload = self.__get_payload(testdata_set={"vehicle_tag_add": open_account_ref_ids[account_type]},
                                                  country="United States")
        expected_status = HTTPStatus.CREATED
        try:
            response = api_client.post("/api/accounts/VehicleTag/add", data=base_account_payload)
            assert response.status_code == expected_status
            if expected_status == HTTPStatus.CREATED:
                open_account_ref_ids[account_type]['vehicleRefId'] = response.json()['vehicleRefId']
                logger.info(
                    f"Message : Account RefID. Status as created with vehicleRefId : {response.json()['vehicleRefId']}")
            else:
                logger.info(f"Account RefID is not invalid or available {open_account_ref_ids[account_type]}")

        except Exception as e:
            logger.error(f"Error testing account type {account_type}", exc_info=e)
            raise

        logger.info(f"Validate VehicleTag_submit API for action type: {open_account_ref_ids[account_type]}")
        expected_status = HTTPStatus.CREATED
        base_account_payload = open_account_ref_ids[account_type]
        try:
            response = api_client.post("/api/accounts/VehicleTag/submit", data=base_account_payload)
            assert response.status_code == expected_status
            if expected_status == HTTPStatus.CREATED:
                assert response.json()["status"] == "Success"
                open_account_ref_ids[account_type]['accountId'] = response.json()['accountId']
                logger.info(f"Message : Account is created Successfully and ID is : {response.json()['accountId']}")
            else:
                logger.info(f"Account RefID is not invalid or available {open_account_ref_ids[account_type]}")

        except Exception as e:
            logger.error(f"Error testing account type {account_type}", exc_info=e)
            raise

        logger.info(f"Validate VehicleTag_update API for type: {open_account_ref_ids[account_type]}")
        base_account_payload = {'vehicleRefId': open_account_ref_ids[account_type]['vehicleRefId'],
                                'vehicleColor': 'RED'}
        expected_status = HTTPStatus.OK
        try:
            response = api_client.put("/api/accounts/VehicleTag/update", data=base_account_payload)
            assert response.status_code == expected_status
            if expected_status == HTTPStatus.OK:
                assert response.json()["vehicleRefId"] == open_account_ref_ids[account_type]['vehicleRefId']
                assert response.json()["vehicleColor"] == "RED"
            else:
                logger.info(f"Account RefID is not invalid or available {base_account_payload[account_type]}")
        except Exception as e:
            logger.error(f"Error testing account type {account_type}", exc_info=e)
            raise