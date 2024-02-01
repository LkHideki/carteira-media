from datetime import datetime
import pandas as pd
import numpy as np


class Carteira:
    def __init__(self, csv_path: str = "") -> None:
        if csv_path != "":
            with open(csv_path, "r", encoding="utf-8") as file:
                self.movimentacoes = pd.read_csv(file)
        else:
            self.movimentacoes = pd.DataFrame(
                columns=["data", "operacao", "preco", "quantidade", "ativo"]
            )
        self.movimentacoes["data"] = pd.to_datetime(
            self.movimentacoes["data"], format="%d/%m/%Y"
        )
        self.movimentacoes["operacao"] = self.movimentacoes["operacao"].apply(
            lambda x: 1 if x == "C" else -1
        )
        self.movimentacoes["preco"] = self.movimentacoes["preco"].astype(float)
        self.movimentacoes["quantidade"] = self.movimentacoes["quantidade"].astype(int)

        df = self.movimentacoes
        self.compras = df[df["operacao"] == 1]
        self.vendas = df[df["operacao"] == -1]
        self.c = (self.compras["preco"] * self.compras["quantidade"]).sum()
        self.v = (self.vendas["preco"] * self.vendas["quantidade"]).sum()
        self.delta = self.c - self.v

    def __str__(self) -> str:
        df = self.movimentacoes
        menor_data = df["data"].min().strftime("%d/%m/%Y")
        maior_data = df["data"].max().strftime("%d/%m/%Y")
        final = f"({menor_data} - {maior_data})\n{self.compras.count().iloc[0]} compras e {self.vendas.count().iloc[0]} vendas:"
        return (
            final
            + "\n"
            + f"Entradas =  R$ {self.c :11,.2f}"
            + "\n"
            + f"Saídas   =  R$ {self.v :11,.2f}"
            + "\n"
            + f"Entradas - Saídas = {self.delta : ,.2f}"
        )

    def __add__(self, other):
        """Retorna uma nova carteira com a soma das movimentações de duas carteiras"""
        nova_carteira = Carteira("")
        nova_carteira.movimentacoes = pd.concat(
            [self.movimentacoes, other.movimentacoes], ignore_index=True
        )
        df = nova_carteira.movimentacoes
        nova_carteira.compras = df[df["operacao"] == 1]
        nova_carteira.vendas = df[df["operacao"] == -1]
        nova_carteira.c = (
            nova_carteira.compras["preco"] * nova_carteira.compras["quantidade"]
        ).sum()
        nova_carteira.v = (
            nova_carteira.vendas["preco"] * nova_carteira.vendas["quantidade"]
        ).sum()
        nova_carteira.delta = nova_carteira.c - nova_carteira.v
        return nova_carteira

    def calcule_rentabilidade_media_em_percentual(
        self, data_referencia: datetime, montante_na_data: float
    ):
        """
        Calcula a rentabilidade média em percentual até uma determinada data de referência.

        Args:
            data_referencia (datetime): A data de referência para calcular a rentabilidade média.
            montante_na_data (float): O montante na data de referência.

        Returns:
            list: Uma lista de valores de rentabilidade média em percentual.
        """
        df = self.movimentacoes[self.movimentacoes["data"] <= data_referencia]
        monomios = df["operacao"] * df["preco"] * df["quantidade"]
        _days = (data_referencia - df["data"]).dt.days
        bla: pd.Series = monomios.groupby(_days).sum()
        grau: int = bla.index.max()
        array = np.zeros(grau + 1)
        for i in range(grau, -1, -1):
            if grau - i in bla.index:
                array[i] = bla[grau - i]
        array[-1] -= montante_na_data
        roots = np.roots(array)
        self.i_medio = roots[roots.imag == 0].real  # .tolist()

        sem_valores_absurdos = [
            round(100 * x, 2)
            for x in (np.power(self.i_medio, 30) - 1).tolist()
            if abs(x) < 5e4
        ]

        if self.delta < montante_na_data:
            return [x for x in sem_valores_absurdos if x > 0]
        return [x for x in sem_valores_absurdos if x <= 0]
