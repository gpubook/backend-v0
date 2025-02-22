import requests
import os
from decimal import Decimal
from dotenv import load_dotenv
from .base import CloudProvider
from datetime import datetime, timedelta
from gpu_instances import (
    GPUInstance,
    GPUInstancePricing,
    GPUInstanceStorageLocal,
    GPUInstanceSpecs,
    GPUInstanceNetwork
)

load_dotenv()


class SFCompute(CloudProvider):
    def __init__(self):
        super().__init__()
        current_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z")
        max_time = (datetime.utcnow() + timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M:%S.000Z")
        self.api_instances_url = f"https://api.sfcompute.com/v0/orders?include_public=true&min_start_date={current_time}&max_start_date={max_time}"
        self.api_bearer_token = os.getenv("SFCOMPUTE_API_BEARER_TOKEN")
        self.update_pricing()

    def get_pricing(self):
        return [instance.to_dict() for instance in self.pricing_data]

    def update_pricing(self):
        response = requests.get(
            self.api_instances_url,
            headers={
                "Authorization": f"Bearer {self.api_bearer_token}",
                "Content-Type": "application/json",
            }
        )

        configurations = {}

        orders = response.json()['data']

        for order in orders:
            # Check if the configuration starts at the top of the hour
            start_date = datetime.strptime(order["start_at"], "%Y-%m-%dT%H:%M:%S.000Z")
            config_key = f'{order["quantity"]}-{order["instance_type"]}'
            if start_date.minute == 0:
                if config_key not in configurations:
                    configurations[config_key] = {}
                if order["price"] not in configurations[config_key]:
                    configurations[config_key][order["price"]] = {
                        "quantity": 1,
                    }
                else:
                    configurations[config_key][order["price"]]["quantity"] += 1

        configurations_list = []

        for configuration_item in configurations:
            gpu_count = str(configuration_item).split('-')[0]
            gpu_model = str(configuration_item).split('-')[1].replace('i', '')

            for price in configurations[configuration_item]:
                quantity = configurations[configuration_item][price]["quantity"]
                price = price

                configurations_list.append(
                    GPUInstance(
                        specs=GPUInstanceSpecs(
                            gpu_count=int(gpu_count)*8,
                            gpu_model=gpu_model,
                            ram=1024
                        ),
                        operating_systems=None,
                        network=GPUInstanceNetwork(
                            speed=1000,
                            ipv4=False,
                            ipv6=False,
                            nat=True,
                        ),
                        pricing=[
                            GPUInstancePricing(
                                hourly_price=(price)/100/(int(gpu_count)*8),
                                count=quantity
                            )
                        ],
                        storage_local=GPUInstanceStorageLocal(
                            adjust=False,
                            storage_only_billing=False,
                            amount=200
                        ),
                        storage_network=None,
                    )
                )

            self.pricing_data = configurations_list
