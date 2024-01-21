# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.tests.test_tryton import ModuleTestCase


class StockPackageShippingGlsTestCase(ModuleTestCase):
    "Test Stock Package Shipping Gls module"
    module = 'stock_package_shipping_gls'


del ModuleTestCase
