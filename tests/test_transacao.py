from datetime import datetime

from dominio import Cliente, TipoTransacao


def test_credito_aumenta_o_saldo() -> None:
    cliente = Cliente("CUST005", "Bruno", "Lima", 30, "Analyst", saldo_inicial=100.0)

    cliente.registra_transacao(50.0, TipoTransacao.CREDITO)

    assert cliente.saldo == 150.0


def test_debito_reduz_o_saldo() -> None:
    cliente = Cliente("CUST006", "Clara", "Souza", 40, "Lawyer", saldo_inicial=200.0)

    cliente.registra_transacao(80.0, TipoTransacao.DEBITO)

    assert cliente.saldo == 120.0


def test_debito_do_saldo_total_zera_a_conta() -> None:
    cliente = Cliente("CUST007", "Diego", "Farias", 33, "Teacher", saldo_inicial=75.0)

    cliente.registra_transacao(75.0, TipoTransacao.DEBITO)

    assert cliente.saldo == 0.0


def test_cliente_novo_comeca_com_saldo_zero() -> None:
    cliente = Cliente("CUST008", "Elisa", "Ramos", 22, "Student")

    assert cliente.saldo == 0.0
    assert cliente.transacoes == []


def test_transacao_guarda_o_saldo_anterior() -> None:
    cliente = Cliente("CUST009", "Felipe", "Nunes", 50, "Doctor", saldo_inicial=300.0)

    transacao = cliente.registra_transacao(100.0, TipoTransacao.CREDITO)

    assert transacao is not None
    assert transacao.saldo_anterior == 300.0
    assert cliente.saldo == 400.0


def test_transacao_registra_valor_e_tipo() -> None:
    cliente = Cliente("CUST012", "Helena", "Braga", 28, "Designer", saldo_inicial=10.0)

    transacao = cliente.registra_transacao(25.5, TipoTransacao.CREDITO)

    assert transacao is not None
    assert transacao.valor == 25.5
    assert transacao.tipo == TipoTransacao.CREDITO
    assert cliente.saldo == 35.5


def test_transacao_referencia_o_cliente() -> None:
    cliente = Cliente("CUST013", "Igor", "Melo", 37, "Engineer", saldo_inicial=500.0)

    transacao = cliente.registra_transacao(20.0, TipoTransacao.DEBITO)

    assert transacao is not None
    assert transacao.id_cliente == "CUST013"
    assert cliente.saldo == 480.0


def test_transacao_eh_adicionada_ao_historico() -> None:
    cliente = Cliente("CUST014", "Julia", "Antunes", 45, "Nurse", saldo_inicial=90.0)

    transacao = cliente.registra_transacao(40.0, TipoTransacao.DEBITO)

    assert transacao is not None
    assert cliente.transacoes == [transacao]
    assert cliente.saldo == 50.0


def test_historico_preserva_a_ordem_das_transacoes() -> None:
    cliente = Cliente("CUST015", "Lucas", "Prado", 41, "Analyst", saldo_inicial=100.0)

    primeira = cliente.registra_transacao(50.0, TipoTransacao.CREDITO)
    segunda = cliente.registra_transacao(30.0, TipoTransacao.DEBITO)

    assert primeira is not None
    assert segunda is not None
    assert cliente.transacoes == [primeira, segunda]
    assert cliente.saldo == 120.0


def test_saldo_apos_sequencia_de_transacoes() -> None:
    cliente = Cliente("CUST016", "Mariana", "Rocha", 52, "Doctor", saldo_inicial=1000.0)

    cliente.registra_transacao(200.0, TipoTransacao.CREDITO)
    cliente.registra_transacao(500.0, TipoTransacao.DEBITO)
    cliente.registra_transacao(50.0, TipoTransacao.CREDITO)

    assert cliente.saldo == 750.0


def test_saldo_anterior_da_segunda_transacao_eh_o_saldo_apos_a_primeira() -> None:
    cliente = Cliente("CUST017", "Nelson", "Vieira", 60, "Retired", saldo_inicial=100.0)

    cliente.registra_transacao(40.0, TipoTransacao.CREDITO)
    segunda = cliente.registra_transacao(60.0, TipoTransacao.DEBITO)

    assert segunda is not None
    assert segunda.saldo_anterior == 140.0
    assert cliente.saldo == 80.0


def test_transacao_com_valor_zero_nao_altera_o_saldo() -> None:
    cliente = Cliente(
        "CUST018", "Olivia", "Cardoso", 35, "Architect", saldo_inicial=250.0
    )

    cliente.registra_transacao(0.0, TipoTransacao.DEBITO)

    assert cliente.saldo == 250.0


def test_transacao_usa_a_data_informada() -> None:
    cliente = Cliente(
        "CUST019", "Paulo", "Teixeira", 47, "Engineer", saldo_inicial=100.0
    )
    data = datetime(2025, 3, 14, 10, 30)

    transacao = cliente.registra_transacao(10.0, TipoTransacao.CREDITO, data)

    assert transacao is not None
    assert transacao.data == data
    assert cliente.saldo == 110.0


def test_transacao_sem_data_usa_o_momento_atual() -> None:
    cliente = Cliente(
        "CUST020", "Renata", "Dias", 29, "Journalist", saldo_inicial=100.0
    )

    antes = datetime.now()
    transacao = cliente.registra_transacao(10.0, TipoTransacao.CREDITO)
    depois = datetime.now()

    assert transacao is not None
    assert antes <= transacao.data <= depois
    assert cliente.saldo == 110.0


def test_cada_transacao_recebe_um_identificador_unico() -> None:
    cliente = Cliente("CUST021", "Sergio", "Bastos", 55, "Manager", saldo_inicial=500.0)

    primeira = cliente.registra_transacao(10.0, TipoTransacao.CREDITO)
    segunda = cliente.registra_transacao(10.0, TipoTransacao.CREDITO)

    assert primeira is not None
    assert segunda is not None
    assert primeira.id_transacao.startswith("TX-")
    assert segunda.id_transacao.startswith("TX-")
    assert primeira.id_transacao != segunda.id_transacao
    assert cliente.saldo == 520.0


def test_transacoes_de_clientes_diferentes_sao_independentes() -> None:
    cliente_a = Cliente(
        "CUST022", "Tatiana", "Lopes", 31, "Analyst", saldo_inicial=100.0
    )
    cliente_b = Cliente(
        "CUST023", "Vitor", "Amaral", 44, "Analyst", saldo_inicial=100.0
    )

    cliente_a.registra_transacao(50.0, TipoTransacao.CREDITO)

    assert cliente_a.saldo == 150.0
    assert cliente_b.saldo == 100.0
    assert cliente_b.transacoes == []


def test_debito_com_saldo_insuficiente_nao_altera_o_saldo() -> None:
    cliente = Cliente("CUST024", "Bruno", "Lima", 30, "Analyst", saldo_inicial=100.0)

    transacao = cliente.registra_transacao(150.0, TipoTransacao.DEBITO)

    assert transacao is None
    assert cliente.saldo == 100.0
    assert cliente.transacoes == []
