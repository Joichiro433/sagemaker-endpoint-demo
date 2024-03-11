"""
$ locust
"""

import random

from rich import print
from locust import HttpUser, task


class APIClient(HttpUser):
    @task
    def call_pred_method(self):
        instances = [
            {
                "bill_length_mm": random.randint(35, 45),
                "bill_depth_mm": random.randint(15, 25),
                "flipper_length_mm": random.randint(170, 190),
                "body_mass_g": random.randint(3600, 3900),
            }
        ]
        response = self.client.post(
            url="/",
            headers={"Content-Type": "application/json"},
            json=instances,
        )

        # print(response.json())
