import json

import pytest
from http import HTTPStatus

from zmq.utils.jsonapi import dumps

from src.utils.logger import logger
from testdata.testdata_engine import TestDataDriver

@pytest.mark.smoke
@pytest.mark.imc
class TestInventoryManagementController:
    # Class properties
    # To store account reference ids
    temp_imc_fields = {}

    def __get_payload(self, testdata_set, country="United States"):
        payload = dict()
        logger.info(f"Testing account creation with type: {testdata_set}")
        testdata = TestDataDriver()
        for api_name in testdata_set.keys():
            match api_name:
                case "add_vendor":
                    payload = testdata.get_vendor_details(country=testdata_set['add_vendor'])
                case "add_inventory_type":
                    payload = testdata.get_add_inventory_type(testdata_set["add_inventory_type"])
        return payload

    def is_key_value_present(self, data, **kwargs):
        """Check if a specific key-value pair exists in the JSON response."""

        def search(data):
            if isinstance(data, dict):
                # Check if all key-value pairs match in the current dictionary
                if all(data.get(k) == v for k, v in kwargs.items()):
                    return True
                # Recursively search in the values of the dictionary
                for value in data.values():
                    if search(value):
                        return True
            elif isinstance(data, list):
                # Recursively search each item in the list
                for item in data:
                    if search(item):
                        return True
            return False

        return search(data)

    @pytest.mark.smoke
    @pytest.mark.parametrize("country_name,expected_status", [
        pytest.param("United States", HTTPStatus.CREATED,
                     id="TC Validate Add Vendor API")])
    def test_add_vendor(self, api_client, country_name, expected_status):
        """Validating API - add a vendor
        args:
            api_client :  API fixtures with scope to session
            country : provide country name
            expected_status : HTTPStatus constants
        """
        logger.info(f"Testing add vendor API for the country: {country_name}")
        base_account_payload = self.__get_payload(testdata_set = {"add_vendor":country_name})
        try:
            response = api_client.post("/api/imc/addVendor", data=base_account_payload)

            assert response.status_code == expected_status
            if expected_status == HTTPStatus.CREATED:
                #self.temp_imc_fields['vendor'] = {'vendorId': response.json()['vendor']['vendorId']}
                logger.info(
                    f"Vendor created successfully with ID : {response.json()['vendor']['vendorId']}")
                assert response.json()["status"]== "Success"
                logger.info(f"status : Success")
                assert response.json()["message"]== "Vendor created successfully"
                logger.info(f"Message : Vendor created successfully")
            else:
                logger.info(f"Vendor creation is unsuccessful")
                logger.info(f"Here the payload for the same: {base_account_payload}")

        except Exception as e:
            logger.error(f"Here the payload for the same: {base_account_payload}", exc_info=e)
            raise

    @pytest.mark.smoke
    @pytest.mark.e2e
    @pytest.mark.parametrize("country_name,expected_status", [
        pytest.param("United States", HTTPStatus.CREATED,
                     id="TC Validate Add Vendor API")])
    def test_vendor_management_add_get_update_delete(self, api_client, country_name, expected_status):
        """Validating API - add a vendor
        args:
            api_client :  API fixtures with scope to session
            country : provide country name
            expected_status : HTTPStatus constants
        """
        logger.info(f"Testing add vendor API for the country: {country_name}")
        base_account_payload = self.__get_payload(testdata_set = {"add_vendor":country_name})
        try:
            response = api_client.post("/api/imc/addVendor", data=base_account_payload)

            assert response.status_code == expected_status
            if expected_status == HTTPStatus.CREATED:
                self.temp_imc_fields['vendor'] = {'vendorId': response.json()['vendor']['vendorId']}
                logger.info(
                    f"Vendor created successfully with ID : {response.json()['vendor']['vendorId']}")
                assert response.json()["status"]== "Success"
                logger.info(f"status : Success")
                assert response.json()["message"]== "Vendor created successfully"
                logger.info(f"Message : Vendor created successfully")
            else:
                logger.info(f"Vendor creation is unsuccessful")
                logger.info(f"Here the payload for the same: {base_account_payload}")

        except Exception as e:
            logger.error(f"Here the payload for the same: {base_account_payload}", exc_info=e)
            raise

        logger.info(f"Testing get All Vendor API")
        expected_status = HTTPStatus.OK
        try:
            response = api_client.get("/api/imc/getAllVendor")
            assert response.status_code == expected_status
            if expected_status == HTTPStatus.OK:
                assert response.json()["status"] == "Success"
                logger.info(f"status : Success")
                assert response.json()["message"] == "All vendors retrieved successfully"
                logger.info(f"Message : All vendors retrieved successfully")

                # Find Vendor ID where value contains the search value
                key_value_to_check = {"vendorId": self.temp_imc_fields['vendor']['vendorId']}
                is_present = self.is_key_value_present(response.json(), **key_value_to_check)
                logger.info(f"Vendor ID {key_value_to_check} is present: {is_present}")
            else:
                logger.info(f"Fetching AllVendor is unsuccessful")

        except Exception as e:
            logger.error(f"Fetching AllVendor is unsuccessful", exc_info=e)
            raise

        logger.info(f"Testing get AllVendorId And Name API")
        expected_status = HTTPStatus.OK
        try:
            response = api_client.get("/api/imc/getAllVendorIdAndName")
            #response = api_client.get("/api/imc/getAllVenodrIdAndName")

            assert response.status_code == expected_status
            if expected_status == HTTPStatus.OK:
                assert response.json()["status"] == "Success"
                logger.info(f"status : Success")
                assert response.json()["message"] == "All vendor IDs and names retrieved successfully"
                logger.info(f"Message : All vendor IDs and names retrieved successfully")

                # Find Vendor ID where value contains the search value
                key_value_to_check = {"vendorId": self.temp_imc_fields['vendor']['vendorId']}
                is_present = self.is_key_value_present(response.json(), **key_value_to_check)
                logger.info(f"Vendor ID {key_value_to_check} is present: {is_present}")

                # Find Vendor company name where value contains the search value
                key_value_to_check = {"vendorCompanyName": base_account_payload['vendorCompanyName']}
                is_present = self.is_key_value_present(response.json(), **key_value_to_check)
                logger.info(f"Vendor Name {key_value_to_check} is present: {is_present}")
            else:
                logger.info(f"Fetching get All Vendor Id And Name is unsuccessful")

        except Exception as e:
            logger.error(f"Fetching AllVendor is unsuccessful", exc_info=e)
            raise

        logger.info(f"Testing updateVendor API")
        base_account_payload = {"vendorCompanyOwnerName": "New owner"}
        vendor_id = self.temp_imc_fields['vendor']['vendorId']
        try:
            response = api_client.put(r"/api/imc/updateVendor/"+str(vendor_id), data=base_account_payload)
            assert response.status_code == expected_status
            if expected_status == HTTPStatus.CREATED:
                assert response.json()["status"] == "Success"
                logger.info(f"status : Success")
                assert response.json()["message"] == "Vendor updated successfully"
                logger.info(f"Message : Vendor updated successfully")

                # Find Vendor company name where value contains the search value
                key_value_to_check = base_account_payload
                is_present = self.is_key_value_present(response.json(), **key_value_to_check)
                logger.info(f"Vendor Name {key_value_to_check} is present: {is_present}")
            else:
                logger.info(f"Vendor update is unsuccessful")
                logger.info(f"Here the payload for the same: {base_account_payload}")

        except Exception as e:
            logger.error(f"Here the payload for the same: {base_account_payload}", exc_info=e)
            raise

        logger.info(f"Testing Delete a vendor API")
        vendor_id = self.temp_imc_fields['vendor']['vendorId']
        expected_status = HTTPStatus.NO_CONTENT

        try:
            response = api_client.delete(r"/api/imc/deleteVendor/" + str(vendor_id))
            assert response.status_code == expected_status
            logger.info(f"Message : Vendor id deleted successfully")

        except Exception as e:
            logger.error(f"Here the payload for the same: {base_account_payload}", exc_info=e)
            raise

    @pytest.mark.smoke
    @pytest.mark.e2e
    @pytest.mark.parametrize("inventory_type,expected_status", [
        pytest.param("TAG", HTTPStatus.CREATED)])
    def test_inventory_type_management_api(self, api_client, inventory_type, expected_status):
        """Validating API - add inventory type
        args:
            api_client :  API fixtures with scope to session
            inventory_type : TAG  or NON-TAG
            expected_status : HTTPStatus constants
        """
        logger.info(f"Testing Add Inventory Type API for the inventory type : {inventory_type}")
        base_account_payload = self.__get_payload(testdata_set = {"add_inventory_type": inventory_type})
        try:
            response = api_client.post("/api/imc/addInventoryType", data=base_account_payload)

            assert response.status_code == expected_status
            if expected_status == HTTPStatus.CREATED:
                self.temp_imc_fields['inventoryId'] = response.json()['inventoryType']['id']
                logger.info(
                    f"Vendor created successfully with ID : {response.json()['inventoryType']['id']}")
                assert response.json()["status"]== "Success"
                logger.info(f"status : Success")
                assert response.json()["message"]== "Inventory type created successfully"
                logger.info(f"Message : Inventory type created successfully")
            else:
                logger.info(f"Inventory Type creation is unsuccessful")
                logger.info(f"Here the payload for the same: {base_account_payload}")

        except Exception as e:
            logger.error(f"Here the payload for the same: {base_account_payload}", exc_info=e)
            raise

        logger.info(f"Testing get all inventory type")
        expected_status = HTTPStatus.OK
        try:
            response = api_client.get("/api/imc/getAllInventoryType")
            assert response.status_code == expected_status
            if expected_status == HTTPStatus.OK:
                assert response.json()["status"] == "Success"
                logger.info(f"status : Success")
                assert response.json()["message"] == "All inventory types retrieved successfully"
                logger.info(f"Message : Inventory type created successfully")
            else:
                logger.info(f"Inventory Type creation is unsuccessful")
                logger.info(f"Here the payload for the same: {base_account_payload}")

        except Exception as e:
            logger.error(f"Here the payload for the same: {base_account_payload}", exc_info=e)
            raise

        logger.info(f"Testing get all inventory type")
        expected_status = HTTPStatus.OK
        inventory_id = self.temp_imc_fields['inventoryId']
        try:
            response = api_client.get(r"/api/imc/getInventoryTypeById/"+str(inventory_id))
            assert response.status_code == expected_status
            if expected_status == HTTPStatus.OK:
                assert response.json()["status"] == "Success"
                logger.info(f"status : Success")
                assert response.json()["message"] == "Inventory type retrieved successfully"
                logger.info(f"Message : Inventory type created successfully")
                assert response.json()['inventoryType']['id'] == self.temp_imc_fields['inventoryId']
            else:
                logger.info(f"Inventory Type creation is unsuccessful")
                logger.info(f"Here the payload for the same: {base_account_payload}")

        except Exception as e:
            logger.error(f"Here the payload for the same: {base_account_payload}", exc_info=e)
            raise

        logger.info(f"Testing get all inventory type")
        expected_status = HTTPStatus.OK
        inventory_id = self.temp_imc_fields['inventoryId']
        try:
            response = api_client.get(r"/api/imc/getInventoryTypeById/" + str(inventory_id))
            assert response.status_code == expected_status
            if expected_status == HTTPStatus.OK:
                assert response.json()["status"] == "Success"
                logger.info(f"status : Success")
                assert response.json()["message"] == "Inventory type retrieved successfully"
                logger.info(f"Message : Inventory type created successfully")
                assert response.json()['inventoryType']['id'] == self.temp_imc_fields['inventoryId']
            else:
                logger.info(f"Inventory Type creation is unsuccessful")
                logger.info(f"Here the payload for the same: {base_account_payload}")

        except Exception as e:
            logger.error(f"Here the payload for the same: {base_account_payload}", exc_info=e)
            raise

