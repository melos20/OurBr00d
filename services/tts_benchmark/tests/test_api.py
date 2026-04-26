def test_list_evaluations(client):
    response = client.get("/api/v1/evaluations")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_generate_audio(client):
    payload = {
        "text": "Hello world",
        "model_id": "kokoro-82m"
    }
    response = client.post("/api/v1/generate", json=payload)
    assert response.status_code == 200
    assert response.headers["content-type"] == "audio/wav"

def test_generate_invalid_model(client):
    payload = {
        "text": "Hello",
        "model_id": "invalid-model"
    }
    response = client.post("/api/v1/generate", json=payload)
    assert response.status_code == 400

def test_create_evaluation(client):
    payload = {
        "text_input": "Testing submission",
        "model_id": "kokoro-82m",
        "score_speed": 4,
        "score_human_like": 4,
        "score_warmth": 3,
        "score_no_hiccups": 5,
        "persist_audio": False
    }
    response = client.post("/api/v1/evaluations", json=payload)
    assert response.status_code == 201
    assert "id" in response.json()