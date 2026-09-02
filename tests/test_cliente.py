from dominio import Cliente


def test_cliente_jovem_nao_eh_especial() -> None:
    cliente = Cliente("CUST003", "Otavio", "Pereira", 19, "Student")

    assert cliente.eh_especial() is False


def test_cliente_com_45_anos_nao_eh_especial() -> None:
    cliente = Cliente("CUST010", "Marina", "Costa", 45, "Engineer")

    assert cliente.eh_especial() is False


def test_cliente_com_46_anos_eh_especial() -> None:
    cliente = Cliente("CUST011", "Marina", "Costa", 46, "Engineer")

    assert cliente.eh_especial() is True


def test_cliente_idoso_eh_especial() -> None:
    cliente = Cliente("CUST001", "Henrique", "Silva", 70, "Doctor")

    assert cliente.eh_especial() is True


def test_nome_completo_junta_nome_e_sobrenome() -> None:
    cliente = Cliente("CUST002", "Sofia", "Almeida", 68, "Doctor")

    assert cliente.nome_completo() == "Sofia Almeida"


def test_nome_completo_de_outro_cliente() -> None:
    cliente = Cliente("CUST004", "Gabriela", "Monteiro", 26, "Student")

    assert cliente.nome_completo() == "Gabriela Monteiro"
