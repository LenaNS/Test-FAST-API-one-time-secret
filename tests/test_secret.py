from httpx import AsyncClient
from tests.test_data import secret_dataset, secret_keys
from tests.coftest import ac

async def test_create_secret(ac: AsyncClient):
    """Сохранение секрета"""

    response = await ac.post(
        "/generate",
        params=secret_dataset,
    )
    resp_data = response.json()
    assert response.status_code == 200
    assert sorted(list(resp_data.keys())) == secret_keys


async def test_get_secret(ac: AsyncClient):
    """Получение секрета"""

    response = await ac.post(
        "/generate",
        params=secret_dataset,
    )
    resp_data = response.json()

    print("AAAAAAAAAAAAAAAAAAAAAA", resp_data["secret_key"])

    secret_key = resp_data["secret_key"]
    response = await ac.get(
        f"/secret/{secret_key}",
        params = secret_dataset["secret"]
    )
    
    # print(response)
    assert response.status_code == 200
