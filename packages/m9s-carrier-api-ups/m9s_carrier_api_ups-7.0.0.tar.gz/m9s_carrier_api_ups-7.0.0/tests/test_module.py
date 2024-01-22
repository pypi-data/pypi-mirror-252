# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.tests.test_tryton import ModuleTestCase


class CarrierApiUpsTestCase(ModuleTestCase):
    "Test Carrier Api Ups module"
    module = 'carrier_api_ups'
    extras = ['stock_package_shipping_ups', 'stock_package_rate_ups']


del ModuleTestCase
