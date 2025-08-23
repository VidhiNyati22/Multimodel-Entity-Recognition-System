# import json
# import pytest
# from app import app


# @pytest.fixture
# def client():
#     app.config['TESTING'] = True
#     with app.test_client() as client:
#         yield client

# def test_process_text(client):
#     response = client.post('/model1', json={
#         'text': 'This is a test input'
#     })
#     assert response.status_code == 200
#     data = json.loads(response.data)
#     assert 'entities' in data

# def test_rate_limiting(client):
#     for _ in range(11):  # Exceeding the rate limit
#         response = client.post('/model1', json={
#             'text': 'This is a test input'
#         })
#     assert response.status_code == 429  # Too Many Requests

# # Add more tests as needed