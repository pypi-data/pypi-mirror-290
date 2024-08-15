from datetime import date

import pytest
import requests
from fr_date import conv

from seuils.usure import liens

data = liens()
param_list = [(x, data[x]) for x in data]


@pytest.mark.parametrize(
    "a, b",
    param_list,
)
def test_lien_fonctionnel(a, b):
    assert type(conv(a, True)) is date
    response = requests.get(b)
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf;charset=UTF-8"
