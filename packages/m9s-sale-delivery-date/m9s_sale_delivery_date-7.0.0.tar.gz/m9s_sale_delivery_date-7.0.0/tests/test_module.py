# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.tests.test_tryton import ModuleTestCase


class SaleDeliveryDateTestCase(ModuleTestCase):
    "Test Sale Delivery Date module"
    module = 'sale_delivery_date'


del ModuleTestCase
