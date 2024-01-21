# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.tests.test_tryton import ModuleTestCase


class PurchaseSupplierLeadTimeTestCase(ModuleTestCase):
    "Test Purchase Supplier Lead Time module"
    module = 'purchase_supplier_lead_time'


del ModuleTestCase
