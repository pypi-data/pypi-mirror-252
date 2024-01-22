# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.tests.test_tryton import ModuleTestCase


class ProjectInvoiceOperationTestCase(ModuleTestCase):
    "Test Project Invoice Operation module"
    module = 'project_invoice_operation'


del ModuleTestCase
