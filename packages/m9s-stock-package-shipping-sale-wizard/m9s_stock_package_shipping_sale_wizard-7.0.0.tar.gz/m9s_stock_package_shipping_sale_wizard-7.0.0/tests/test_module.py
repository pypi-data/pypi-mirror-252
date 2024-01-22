# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.tests.test_tryton import ModuleTestCase


class StockPackageShippingSaleWizardTestCase(ModuleTestCase):
    "Test Stock Package Shipping Sale Wizard module"
    module = 'stock_package_shipping_sale_wizard'


del ModuleTestCase
