from datetime import datetime
from enum import Enum, auto
from uuid import uuid4

IDADE_MINIMA_ESPECIAL = 45

class TipoTransacao(Enum):
    CREDITO = auto()
    DEBITO = auto()


class Transacao:
    def __init__(
        self,
        id_cliente: str,
        valor: float,
        saldo_anterior: float,
        tipo: TipoTransacao,
        data: datetime,
    ):
        self.id_transacao = f"TX-{uuid4()}"
        self.id_cliente = id_cliente
        self.valor = valor
        self.saldo_anterior = saldo_anterior
        self.tipo = tipo
        self.data = data


class Cliente:
    def __init__(
        self,
        idc: str,
        nome: str,
        sobrenome: str,
        idade: int,
        profissao: str,
        saldo_inicial: float = 0.0,
    ):
        self.id_cliente = idc
        self.nome = nome
        self.sobrenome = sobrenome
        self.idade = idade
        self.profissao = profissao
        self.saldo = saldo_inicial
        self.transacoes: list[Transacao] = []

    def eh_especial(self) -> bool:
        return self.idade > IDADE_MINIMA_ESPECIAL

    def nome_completo(self) -> str:
        return f"{self.nome} {self.sobrenome}"

    def registra_transacao(
        self,
        valor: float,
        tipo: TipoTransacao,
        data: datetime | None = None,
    ) -> Transacao:

        transacao = Transacao(
            id_cliente=self.id_cliente,
            valor=valor,
            saldo_anterior=self.saldo,
            tipo=tipo,
            data=data if data is not None else datetime.now(),
        )

        match tipo:
            case TipoTransacao.CREDITO:
                self.saldo += valor
            case TipoTransacao.DEBITO:
                self.saldo -= valor

        self.transacoes.append(transacao)

        return transacao
