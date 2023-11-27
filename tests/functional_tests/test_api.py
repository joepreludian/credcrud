import uuid

import pytest
from fastapi.testclient import TestClient

from credcrud.auth.handler import SECRET_TOKEN
from credcrud.card.routes import router as card_router
from credcrud.main import app
from tests.builders import db_session

card_router.db_session = db_session

client = TestClient(app)

class TestCardEndpoints:

    base_endpoint = "/v1/credit-card"
    auth_headers = {
        "Content-Type": "application/json",
        "Authorization": f"bearer {SECRET_TOKEN}"
    }

    def test_keep_alive(self):
        return_data = client.get("/healthcheck")
        assert return_data.status_code == 200

    @pytest.mark.parametrize(('route', 'client_method',), (
        ("/", client.get),
        ("/some_id", client.get),
        ("/", client.post),
        ("/some_id", client.delete)
    ))
    @pytest.mark.parametrize(('extra_headers', ), (
        ({"Authorization": "not_begin_with_bearer a_fake_token"},),
        ({},)
    ))
    def test_protected_routes_without_credentials(self, route, client_method, extra_headers):
        return_data = client_method(
            url=f"{self.base_endpoint}{route}",
            headers={"Content-Type": "application/json", **extra_headers},
        )

        payload = return_data.json()

        assert return_data.status_code == 401
        assert payload == {"detail": "Unauthorized"}

    def test_create_card(self):
        return_data = client.post(
            url=self.base_endpoint,
            headers=self.auth_headers,
            json={
                "exp_date": "02/2024",
                "holder": "Jon Trigueiro",
                "number": "5526172242727676",
                "cvv": "123"
            }
        )

        payload = return_data.json()

        assert return_data.status_code == 201

        payload_keys = payload.keys()
        for expected_key in ["id", "brand", "exp_date", "holder", "number", "cvv"]:
            assert expected_key in payload_keys

        assert "*" in payload['number']
        assert payload["id"] is not None
        assert payload["brand"] == "master"

    @pytest.mark.parametrize(('override', 'expected_message'), (
        ({'exp_date': '02/1990'}, "The Card has expired"),
        ({'number': '0000000000000001'}, "Card number provided is invalid")
    ))
    def test_create_card_invalid_payload(self, override, expected_message):
        return_data = client.post(
            url=self.base_endpoint,
            headers=self.auth_headers,
            json={
                "exp_date": "02/2056",
                "holder": "Jon Trigueiro",
                "number": "5526172242727676",
                "cvv": "123",
                **override
            }
        )

        assert return_data.status_code == 422
        assert expected_message in return_data.text

    def test_fetch_card_that_has_been_created(self):
        card_payload = {
            "exp_date": "02/2056",
            "holder": "Jon Trigueiro",
            "number": "4024007185766093",
            "cvv": "123"
        }

        new_client_return = client.post(
            url=self.base_endpoint,
            headers=self.auth_headers,
            json=card_payload
        )

        new_client_return_payload = new_client_return.json()

        fetch_return = client.get(
            url=f"{self.base_endpoint}/{new_client_return_payload['id']}",
            headers=self.auth_headers
        )

        fetch_payload = fetch_return.json()

        assert fetch_return.status_code == 200
        assert new_client_return_payload == fetch_payload

    def test_fetch_card_with_invalid_uuid(self):
        fetch_return = client.get(
            url=f"{self.base_endpoint}/id_that_i_know_that_dont_exists",
            headers=self.auth_headers
        )

        assert fetch_return.status_code == 400
        assert fetch_return.json() == {"error": "The ID 'id_that_i_know_that_dont_exists' is not an invalid UUID"}

    def test_fetch_card_that_dont_exists(self):
        search_id = str(uuid.uuid4())

        fetch_return = client.get(
            url=f"{self.base_endpoint}/{search_id}",
            headers=self.auth_headers
        )

        assert fetch_return.status_code == 404
        assert fetch_return.json() == {'error': f'The Card {search_id} could not be found'}

    def test_fetch_all_cards(self):

        fetch_return = client.get(
            url=self.base_endpoint,
            headers=self.auth_headers
        )

        return_payload = fetch_return.json()

        assert fetch_return.status_code == 200
        assert type(return_payload) is list
        assert len(return_payload) == 2  # Cards created on the example above

    def test_delete_card_invalid_id(self):
        fetch_return = client.delete(
            url=f"{self.base_endpoint}/id_that_i_know_that_dont_exists",
            headers=self.auth_headers
        )

        assert fetch_return.status_code == 400
        assert fetch_return.json() == {"error": "The ID 'id_that_i_know_that_dont_exists' is not an invalid UUID"}

    def test_delete_card_that_doesnt_exist(self):
        search_id = str(uuid.uuid4())

        fetch_return = client.delete(
            url=f"{self.base_endpoint}/{search_id}",
            headers=self.auth_headers
        )

        assert fetch_return.status_code == 404
        assert fetch_return.json() == {'error': f'The Card {search_id} could not be found'}

    def test_delete_card_that_already_exists(self):

        fetch_return = client.get(
            url=self.base_endpoint,
            headers=self.auth_headers
        )

        valid_card_id = fetch_return.json()[0]['id']

        fetch_return = client.delete(
            url=f"{self.base_endpoint}/{valid_card_id}",
            headers=self.auth_headers
        )

        assert fetch_return.status_code == 204
        assert fetch_return.text == ''  # No content
