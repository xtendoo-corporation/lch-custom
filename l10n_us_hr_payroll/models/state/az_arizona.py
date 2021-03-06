# Part of Hibou Suite Professional. See LICENSE_PROFESSIONAL file for full copyright and licensing details.

from .general import _state_applies, sit_wage


def az_arizona_state_income_withholding(payslip, categories, worked_days, inputs):
    """
    Returns SIT eligible wage and rate.
    WAGE = GROSS + DED_FIT_EXEMPT

    :return: result, result_rate (wage, percent)
    """
    state_code = 'AZ'
    if not _state_applies(payslip, state_code):
        return 0.0, 0.0

    # Determine Wage
    wage = sit_wage(payslip, categories)
    if not wage:
        return 0.0, 0.0

    schedule_pay = payslip.dict.contract_id.schedule_pay
    additional = payslip.dict.contract_id.us_payroll_config_value('state_income_tax_additional_withholding')
    withholding_percent = payslip.dict.contract_id.us_payroll_config_value('az_a4_sit_withholding_percentage')

    if withholding_percent <= 0.0:
        return 0.0, 0.0

    wh_percentage = withholding_percent / 100.0
    withholding = wage * wh_percentage

    if withholding < 0.0:
        withholding = 0.0
    withholding += additional
    return wage, -((withholding / wage) * 100.0)
