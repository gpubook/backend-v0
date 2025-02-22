class GPUInstance:
    def __init__(self, specs, operating_systems, network, storage_local,
                 pricing, storage_network, datacenter=None):
        self.pricing = pricing
        self.specs = specs
        self.network = network
        self.datacenter = datacenter
        self.storage_network = storage_network
        self.operating_systems = operating_systems
        self.storage_local = storage_local

    def get_pricing(self):
        return {
            'hourly_price': self.hourly_price,
            'spot_price': self.spot_price,
            'monthly_price': self.monthly_price,
            'biannual_price': self.biannual_price,
            'annual_price': self.annual_price,
            'biennial_price': self.biennial_price
        }

    def to_dict(self):
        return {
            'pricing': [pricing.to_dict() for pricing in self.pricing],
            'specs': self.specs.to_dict(),
            'operating_systems': (self.operating_systems.to_dict()
                                  if self.operating_systems else None),
            'network': self.network.to_dict(),
            'datacenter': (self.datacenter.to_dict()
                           if self.datacenter else None),
            'storage_local': self.storage_local.to_dict(),
            'storage_network': (self.storage_network.to_dict()
                                if self.storage_network else None)
        }

class GPUInstanceOperatingSystems:
    def __init__(self, operating_systems):
        self.operating_systems = operating_systems

    def to_dict(self):
        return {
            'operating_systems': self.operating_systems
        }

class GPUInstancePricing:
    def __init__(self, hourly_price=None, spot_price=None, monthly_price=None,
                 biannual_price=None, annual_price=None, biennial_price=None,
                 count=None):
        self.hourly_price = hourly_price
        self.spot_price = spot_price
        self.monthly_price = monthly_price
        self.biannual_price = biannual_price
        self.annual_price = annual_price
        self.biennial_price = biennial_price
        self.count = count

    def to_dict(self):
        return {
            'hourly_price': self.hourly_price,
            'spot_price': self.spot_price,
            'monthly_price': self.monthly_price,
            'biannual_price': self.biannual_price,
            'annual_price': self.annual_price,
            'biennial_price': self.biennial_price,
            'count': self.count
        }


class GPUInstanceNetwork:
    def __init__(self, speed, ipv4, ipv6, nat):
        self.speed = speed
        self.ipv4 = ipv4
        self.ipv6 = ipv6
        self.nat = nat

    def to_dict(self):
        return {
            'speed': self.speed,
            'ipv4': self.ipv4,
            'ipv6': self.ipv6,
            'nat': self.nat
        }

class GPUInstanceDatacenter:
    def __init__(self, city, country, continent, tier):
        self.city = city
        self.country = country
        self.continent = continent
        self.tier = tier

    def to_dict(self):
        return {
            'city': self.city,
            'country': self.country,
            'continent': self.continent,
            'tier': self.tier
        }


class GPUInstanceSpecs:
    def __init__(self, gpu_count, gpu_model, ram, cpu_model='generic', cpu_count=None):
        self.gpu_count = gpu_count
        self.gpu_model = gpu_model
        self.ram = ram
        self.cpu_model = cpu_model
        self.cpu_count = cpu_count

    def to_dict(self):
        return {
            'gpu_count': self.gpu_count,
            'gpu_model': self.gpu_model,
            'ram': self.ram,
            'cpu_model': self.cpu_model,
            'cpu_count': self.cpu_count
        }


class GPUInstanceStorageLocal:
    def __init__(self, amount, adjust, storage_only_billing, 
                 price=None, price_incremental=None):
        self.adjust = adjust
        self.storage_only_billing = storage_only_billing
        self.amount = amount
        self.price = price
        self.price_incremental = price_incremental

    def to_dict(self):
        return {
            'amount': self.amount,
            'price': self.price,
            'price_incremental': (self.price_incremental.to_dict()
                                  if self.price_incremental else None),
            'adjust': self.adjust,
            'storage_only_billing': self.storage_only_billing
        }


class GPUInstanceStoragePricing:
    def __init__(self, amount, max_multiple, price_hourly, price_month):
        self.amount = amount
        self.max_multiple = max_multiple
        self.price_hourly = price_hourly
        self.price_month = price_month

    def to_dict(self):
        return {
            'amount': self.amount,
            'max_multiple': self.max_multiple,
            'price_hourly': self.price_hourly,
            'price_month': self.price_month
        }
