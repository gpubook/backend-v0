import requests
from decimal import Decimal
from .base import CloudProvider
from gpu_instances import (
    GPUInstance,
    GPUInstancePricing,
    GPUInstanceStorageLocal,
    GPUInstanceStoragePricing,
    GPUInstanceSpecs,
    GPUInstanceNetwork,
    GPUInstanceDatacenter,
)


class VoltagePark(CloudProvider):
    def __init__(self):
        super().__init__()
        self.api_instances_url = "https://cloud-api.voltagepark.com/api/v0/client/deploy/instantvms"
        self.api_cluster_url = "https://cloud-api.voltagepark.com/api/v1/bare-metal/locations"
        self.update_pricing()

    def get_pricing(self):
        return [instance.to_dict() for instance in self.pricing_data]

    def update_pricing(self):
        response = requests.get(self.api_instances_url)

        preconfigs = response.json()['preconfig_options']

        for preconfig in preconfigs:
            preconfig['count'] = 0

        for instance in response.json()['virtual_machines'].values():
            for preconfig in preconfigs:
                print(preconfig)
                if instance['preconfig_id'] == preconfig['uuid']:
                    preconfig['count'] += 1

        preconfig_list = []
        for preconfig in preconfigs:
            preconfig_list.append(
                GPUInstance(
                    specs=GPUInstanceSpecs(
                        gpu_count=preconfig['gpu_count'][0],
                        gpu_model=preconfig['gpu_model'][0],
                        ram=preconfig['ram'],
                        cpu_model='intel-xeon-platinum-8470',
                        cpu_count=preconfig['cpu_count'],
                    ),
                    operating_systems='ubuntu-24.04-lts',
                    network=GPUInstanceNetwork(
                        speed=100000,
                        ipv4=False,
                        ipv6=False,
                        nat=True,
                    ),
                    datacenter=GPUInstanceDatacenter(
                        city="Dallas",
                        country="US",
                        continent="NA",
                        tier=3,
                    ),
                    pricing=[
                        GPUInstancePricing(
                            hourly_price=(Decimal(preconfig['compute_rate_hourly']) +
                                          Decimal(preconfig['storage_rate_hourly'])),
                            count=preconfig['count']
                        )
                    ],
                    storage_local=GPUInstanceStorageLocal(
                        adjust=True,
                        storage_only_billing=True,
                        amount=preconfig['storage'],
                        price=Decimal(preconfig['storage_rate_hourly']),
                        price_incremental=GPUInstanceStoragePricing(
                            amount=1,
                            max_multiple=30000,
                            price_hourly=Decimal("0.0000684931507"),
                            price_month=Decimal("0.05")
                        )
                    ),
                    storage_network=None,
                )
            )

        self.pricing_data = preconfig_list

