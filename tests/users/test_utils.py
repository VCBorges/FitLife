from app.users import utils


def test_clean_cpf_with_mask_with_hifen():
    cpf = '770.911.670-15'
    cleaned_cpf = utils.clean_cpf(cpf)

    assert cleaned_cpf == '77091167015'


def test_clean_cpf_with_mask_with_bar():
    cpf = '770.911.670/15'
    cleaned_cpf = utils.clean_cpf(cpf)

    assert cleaned_cpf == '77091167015'
