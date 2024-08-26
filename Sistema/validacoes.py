import re
import uuid

def validarId(uuid_str: str) -> bool:
    try:
        uuid.UUID(uuid_str, version=4)
        return True
    except ValueError: return False

def validarCpf(cpf: str) -> bool:
    if not cpf.isnumeric() or len(cpf) != 11: return False

    def calcularDigito(cpf: str, posicoes: int) -> str:
        soma = sum(int(digito) * (posicoes + 1 - i) for i, digito in enumerate(cpf[:posicoes]))
        resto = soma % 11
        return '0' if resto < 2 else str(11 - resto)

    return cpf[-2] == calcularDigito(cpf, 9) and cpf[-1] == calcularDigito(cpf, 10)

def validarCnpj(cnpj: str) -> bool:
    if not cnpj.isnumeric() or len(cnpj) != 14: return False

    def calcularDigito(cnpj: str, multiplicadores: list) -> str:
        soma = sum(int(cnpj[i]) * multiplicador for i, multiplicador in enumerate(multiplicadores))
        resto = soma % 11
        return '0' if resto < 2 else str(11 - resto)

    multiplicadores1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    multiplicadores2 = [6] + multiplicadores1

    return cnpj[-2] == calcularDigito(cnpj, multiplicadores1) and cnpj[-1] == calcularDigito(cnpj, multiplicadores2)

def validarEmail(email: str) -> bool:
    EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(EMAIL_REGEX, email) is not None

def validarTelefone(telefone: str) -> bool:
    TELEFONE_REGEX = r'^\d{8,}$'
    return re.match(TELEFONE_REGEX, telefone) is not None

def validarCep(cep: str) -> bool: return cep.isnumeric() and len(cep) == 8

def validarNaoVazio(valor: str) -> bool: return bool(valor.strip())

def validarNumero(numero: str) -> bool: return numero.isnumeric()

def validarFloat(numero: str) -> bool:
    try:
        float(numero)
        return True
    except ValueError: return False

def obterEntrada(mensagem: str, validacao: str, erroMensagem: str) -> str:
    while True:
        entrada = input(mensagem)
        if not globals()[validacao](entrada): print(erroMensagem)
        else: return entrada