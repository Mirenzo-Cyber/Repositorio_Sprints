# Relatório: Erros Numéricos e Representação Computacional

**Exercício 1: Por que 0.1 + 0.2 != 0.3**
Os computadores utilizam a base binária (base 2) com um limite de memória de 64 bits (padrão IEEE 754). Números como 0.1 e 0.2 geram dízimas periódicas infinitas em binário. Ao arredondar para caber na memória, acumula-se um resíduo na 17ª casa decimal, fazendo com que a soma seja `0.30000000000000004` e falhe no teste de igualdade direta (`== 0.3`).

**Exercício 2: Erro Absoluto e Relativo**
- O **Erro Absoluto** mede a distância direta entre o valor matemático real e a aproximação computacional (|x - x_aprox|).
- O **Erro Relativo** mede a proporção dessa falha em relação à grandeza do número (|x - x_aprox| / |x|). Num sistema de risco, o erro relativo é muito mais crítico, pois contextualiza se a falha é aceitável para a escala do problema.

**Exercício 3: Truncamento vs. Arredondamento**
[Espaço reservado para a tua resposta sobre qual método apresentou o menor erro...]

**Exercício 4: Efeitos de Precisão Limitada (Absorção)**
Ao somar números de ordens de grandeza muito distintas (como 1e16 e 1.0), a limitação de bits na mantissa força o computador a ignorar o valor mais pequeno. O número menor é "absorvido", resultando na perda total dessa informação.

**Exercício 5: Propagação de Erros em Cálculos Sucessivos**
Pequenos erros de representação em ponto flutuante acumulam-se em cálculos iterativos. Ao somar 0.1 (que não tem representação exata em binário) 100.000 vezes num laço de repetição, o erro original propaga-se a cada iteração, resultando num desvio evidente face ao valor matemático esperado (10000.0).

**Exercício 6 e 7: NumPy e Comparações Seguras**
O uso de bibliotecas como o NumPy ajuda a mitigar erros de propagação através de operações vetorizadas. Devido à representação em ponto flutuante, a comparação direta com `==` é insegura. A prática correta é utilizar métodos como `math.isclose()` ou `numpy.isclose()`, que consideram uma margem de tolerância para absorver pequenos erros de arredondamento computacional.

**Exercício 8: Determinante vs. Número de Condição**
Numa matriz quase singular, o determinante aproxima-se de zero, mas o seu valor isolado pode ser enganador pois sofre influência direta da escala dos dados. O Número de Condição é a medida mais informativa: quantifica diretamente a sensibilidade do sistema, revelando como pequenos erros nas entradas são amplificados nos resultados.

**Exercício 9: Resolução do Sistema (solve vs inv)**
A função `numpy.linalg.solve` aplica algoritmos diretos otimizados (como a fatoração LU). Calcular explicitamente a matriz inversa com `numpy.linalg.inv` exige mais operações de ponto flutuante, o que acumula erros de arredondamento. Consequentemente, o método `solve` gera um resíduo estrutural ||Ax - b|| menor e mais fiável.