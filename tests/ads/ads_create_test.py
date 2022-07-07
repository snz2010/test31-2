import pytest


@pytest.mark.django_db
def test_ads_create(client, user, category):

    response = client.post(
        "/ad/create/",
        {
            "name": "name_12345",
            "author": user.id,
            "price": 10,
            "description": "new_ad_description",
            "is_published": False,
            "category": category.id
        },
        content_type="application/json"
    )


    assert response.status_code == 201
    assert response.data == {
            "id": 1,
            "name": "name_12345",
            "author": user.id,
            "price": 10,
            "image": None,
            "description": "new_ad_description",
            "is_published": False,
            "category": category.id,
    }

