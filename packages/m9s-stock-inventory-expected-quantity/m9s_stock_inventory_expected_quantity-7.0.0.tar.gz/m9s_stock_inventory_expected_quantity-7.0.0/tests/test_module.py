# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.tests.test_tryton import ModuleTestCase


class StockInventoryExpectedQuantityTestCase(ModuleTestCase):
    "Test Stock Inventory Expected Quantity module"
    module = 'stock_inventory_expected_quantity'


del ModuleTestCase
