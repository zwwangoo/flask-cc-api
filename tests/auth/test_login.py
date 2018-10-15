import pytest


class TestUserLogin(object):

    @pytest.fixture(autouse=True)
    def transact(self, client):
        self.user_name = '2'
        self.user_password = '123456'
        self.client = client
        self.data = {
            'user_name': self.user_name,
            'user_password': self.user_password
        }

    def test_login_error_when_name_erroe(self):
        response = self.client.post('/auth/login', json=self.data)
        assert response.status_code == 200
        result = response.get_json()
        assert 'error_code' in result
        assert result.get('error_code') == 200001
