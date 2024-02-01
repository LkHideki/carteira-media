# Calculadora da rentabilidade

Faz o parse de planilhas csv e monta um objeto Carteira com os ativos lidos.

A classe `Carteira` tem um método `.calcule_rentabilidade_media_em_percentual(•)` que calcula a rentabilidade média considerando o polinômio em (1+i):

$$
\sum_{k=0}^{n} a_k (1+i) ^k = m
$$

onde $m$ é o montante no final de um período considerado e $a_k$ é o aporte no tempo $k$.

## Uso
1. Crie e ative um *ambiente virtual*.
2. Instale as dependências com `pip install -r requirements.txt`.
3. Coloque suas planilhas .csv na pasta dados/ no formato dos exemplos. Dê os nomes que quiser.
4. Edite o `main.py`.
5. Execute, no terminal, `python3 src/main.py`.