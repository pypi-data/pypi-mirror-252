# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.tests.test_tryton import ModuleTestCase


class StockPackageRateUpsTestCase(ModuleTestCase):
    "Test Stock Package Rate Ups module"
    module = 'stock_package_rate_ups'


del ModuleTestCase
