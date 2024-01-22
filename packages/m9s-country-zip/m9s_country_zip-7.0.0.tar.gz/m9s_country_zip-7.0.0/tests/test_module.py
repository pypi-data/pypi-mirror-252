# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.tests.test_tryton import ModuleTestCase


class CountryZipTestCase(ModuleTestCase):
    "Test Country Zip module"
    module = 'country_zip'


del ModuleTestCase
