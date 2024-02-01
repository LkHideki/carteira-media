from datetime import datetime
from carteira import Carteira


c1 = Carteira("dados/exemplo-gerado-por-IA.csv")
c2 = Carteira("dados/exemplo-2-gerado-por-IA.csv")

carteira_mista = c1 + c2

print(
    carteira_mista.calcule_rentabilidade_media_em_percentual(datetime(2023, 5, 30), 855)
)
