# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.tests.test_tryton import ModuleTestCase


class PurchaseSupplierDiscountTestCase(ModuleTestCase):
    "Test Purchase Supplier Discount module"
    module = 'purchase_supplier_discount'


del ModuleTestCase
