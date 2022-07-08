from odoo.addons.l10n_us_hr_payroll.tests.test_us_payslip import TestUsPayslip, process_payslip
from odoo.addons.l10n_us_hr_payroll.models.l10n_us_hr_payroll import USHrContract


class TestUsFlPayslip(TestUsPayslip):
    ###
    #   2018 Taxes and Rates
    ###
    FL_UNEMP_MAX_WAGE = 7000.0
    FL_UNEMP = -2.7 / 100.0

    def test_2018_taxes(self):
        salary = 5000.0

        employee = self._createEmployee()
        contract = self._createContract(employee, salary, struct_id=self.ref('l10n_us_fl_hr_payroll.hr_payroll_salary_structure_us_fl_employee'))

        self._log('2018 Florida tax first payslip:')
        payslip = self._createPayslip(employee, '2018-01-01', '2018-01-31')

        payslip.compute_sheet()

        cats = self._getCategories(payslip)

        self.assertPayrollEqual(cats['WAGE_US_FL_UNEMP'], salary)
        self.assertPayrollEqual(cats['ER_US_FL_UNEMP'], cats['WAGE_US_FL_UNEMP'] * self.FL_UNEMP)

        process_payslip(payslip)

        # Make a new payslip, this one will have maximums

        remaining_fl_unemp_wages = self.FL_UNEMP_MAX_WAGE - salary if (self.FL_UNEMP_MAX_WAGE - 2*salary < salary) \
            else salary

        self._log('2018 Florida tax second payslip:')
        payslip = self._createPayslip(employee, '2018-02-01', '2018-02-28')

        payslip.compute_sheet()

        cats = self._getCategories(payslip)

        self.assertPayrollEqual(cats['WAGE_US_FL_UNEMP'], remaining_fl_unemp_wages)
        self.assertPayrollEqual(cats['ER_US_FL_UNEMP'], remaining_fl_unemp_wages * self.FL_UNEMP)

    def test_2018_taxes_with_external(self):
        salary = 5000.0
        external_wages = 6000.0

        employee = self._createEmployee()
        contract = self._createContract(employee, salary, external_wages=external_wages,
                                        struct_id=self.ref('l10n_us_fl_hr_payroll.hr_payroll_salary_structure_us_fl_employee'))

        self._log('2018 Forida_external tax first payslip:')
        payslip = self._createPayslip(employee, '2018-01-01', '2018-01-31')

        payslip.compute_sheet()

        cats = self._getCategories(payslip)

        self.assertPayrollEqual(cats['WAGE_US_FL_UNEMP'], self.FL_UNEMP_MAX_WAGE - external_wages)
        self.assertPayrollEqual(cats['ER_US_FL_UNEMP'], cats['WAGE_US_FL_UNEMP'] * self.FL_UNEMP)

    def test_2018_taxes_with_state_exempt(self):
        salary = 5000.0
        external_wages = 6000.0

        employee = self._createEmployee()
        contract = self._createContract(employee, salary, external_wages=external_wages, struct_id=self.ref(
            'l10n_us_fl_hr_payroll.hr_payroll_salary_structure_us_fl_employee'), futa_type=USHrContract.FUTA_TYPE_BASIC)

        self._log('2018 Forida_external tax first payslip:')
        payslip = self._createPayslip(employee, '2018-01-01', '2018-01-31')

        payslip.compute_sheet()

        cats = self._getCategories(payslip)

        self.assertPayrollEqual(cats.get('WAGE_US_FL_UNEMP', 0.0), 0.0)
        self.assertPayrollEqual(cats.get('ER_US_FL_UNEMP', 0.0), 0.0)
