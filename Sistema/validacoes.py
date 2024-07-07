import re
import uuid

def validarId(uuid_str):
    try:
        uuid.UUID(uuid_str, version=4)
        return True
    except ValueError: return False

def validarCPF(cpf):
    if not cpf.isnumeric() or len(cpf) != 11: return False

    def calcular_digito(cpf, posicoes):
        soma = sum(int(digito) * (posicoes + 1 - i) for i, digito in enumerate(cpf[:posicoes]))
        resto = soma % 11
        return '0' if resto < 2 else str(11 - resto)
    return cpf[-2] == calcular_digito(cpf, 9) and cpf[-1] == calcular_digito(cpf, 10)

def validarCNPJ(cnpj):
    if not cnpj.isnumeric() or len(cnpj) != 14: return False

    def calcular_digito(cnpj, multiplicadores):
        soma = sum(int(cnpj[i]) * multiplicador for i, multiplicador in enumerate(multiplicadores))
        resto = soma % 11
        return '0' if resto < 2 else str(11 - resto)

    multiplicadores_1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    multiplicadores_2 = [6] + multiplicadores_1

    return cnpj[-2] == calcular_digito(cnpj, multiplicadores_1) and cnpj[-1] == calcular_digito(cnpj, multiplicadores_2)

def validarEmail(email):
    EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(EMAIL_REGEX, email) is not None

def validarTelefone(telefone):
    TELEFONE_REGEX = r'^\d{8,}$'
    return re.match(TELEFONE_REGEX, telefone) is not None

def validarCEP(cep): return cep.isnumeric() and len(cep) == 8

def validarNaoVazio(valor): return bool(valor.strip())

def validarNumero(numero): return numero.isnumeric()

def validarFloat(numero):
    try:
        float(numero)
        return True
    except ValueError: return False

def obterEntrada(mensagem, validacao, erroMensagem):
    while True:
        entrada = input(mensagem)
        if not globals()[validacao](entrada): print(erroMensagem)
        else: return entrada