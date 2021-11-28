# python -m pip install matplotlib
import matplotlib.pyplot as plt
# python -m pip install numpy
import numpy as np
# python -m pip install scipy
from scipy.stats import norm
from scipy import stats


def variavel_aleatoria(nome: str, media: int, desvio_padrao: int, qtd: int):
    va = np.sort(np.random.normal(media, desvio_padrao, qtd))

    arquivo = open(f'Respostas/VA {nome}.txt', 'w')
    np.savetxt(arquivo, va)
    arquivo.close()

    return va


def histograma(dados: list, titulo: str = 'Histograma'):
    plt.hist(dados)
    plt.title(titulo)

    plt.xlabel('Valor')
    plt.ylabel('fa')
    plt.grid(True)

    plt.draw()
    plt.savefig(f'Respostas/{titulo}.png')

    plt.show()

    plt.close()


def fdc(dados: list, titulo: str = 'FDC'):
    valores_proporcionais = 1. * np.arange(len(dados)) / (len(dados) - 1)

    plt.plot(dados, valores_proporcionais, scaley=True)
    plt.title(titulo)

    plt.xlabel('Valor')
    plt.ylabel('Percentual')
    plt.xlim(0, 10)
    plt.ylim(0, 1)
    plt.grid(True)
    plt.xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    plt.yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])

    plt.draw()
    plt.savefig(f'Respostas/{titulo}.png')

    plt.show()

    plt.close()


def pr_maior(dados: list, nome: str, valor: int):
    total = (dados > valor).sum()
    probabilidade = total / len(dados)

    print(f'Pr[{nome}>{valor}] = {probabilidade * 100}%')

    with open(f'Respostas/Pr[{nome} gt {valor}].txt', 'w') as f:
        f.write(f'{probabilidade * 100}%')


def pr_igual(dados: list, nome: str, valor: int):
    total = (dados == valor).sum()
    probabilidade = total / len(dados)

    print(f'Pr[{nome}={valor}] = {probabilidade * 100}%')

    with open(f'Respostas/Pr[{nome} eq {valor}].txt', 'w') as f:
        f.write(f'{probabilidade * 100}%')

# Checando o valor crítico do teste de Kolmogorov-Smirnov
def kolmogorov_smirnov_critico(n):
    # Fonte: https://www.soest.hawaii.edu/GG/FACULTY/ITO/GG413/K_S_Table_one_Sample.pdf
    # Fonte: http://www.real-statistics.com/statistics-tables/kolmogorov-smirnov-table/
    # alpha = 0.05 (nível de confiança de 95%)
    
    if n <= 40:
        # valores entre 1 e 40
        kolmogorov_critico = [0.97500, 0.84189, 0.70760, 0.62394, 0.56328, 0.51926, 0.48342, 0.45427, 0.43001, 0.40925, 
                      0.39122, 0.37543, 0.36143, 0.34890, 0.33760, 0.32733, 0.31796, 0.30936, 0.30143, 0.29408, 
                      0.28724, 0.28087, 0.27490, 0.26931, 0.26404, 0.25907, 0.25438, 0.24993, 0.24571, 0.24170, 
                      0.23788, 0.23424, 0.23076, 0.22743, 0.22425, 0.22119, 0.21826, 0.21544, 0.21273, 0.21012]
        ks_critico = kolmogorov_critico[n - 1]
    elif n > 40:
        # valores acima de 40:
        kolmogorov_critico = 1.36/(np.sqrt(n))
        ks_critico = kolmogorov_critico
    else:
        pass            
            
    return ks_critico

def kolmogorov_smirnov(dados_x: list):
    # media
    media = np.mean(dados_x)

    # desvio padrão
    std = np.std(dados_x, ddof=1)

    ks_critico = kolmogorov_smirnov_critico(len(dados_x))

    # Cálculo do teste de normalidade levando em consideração os parâmetros dos dados de X
    ks_stat, ks_p_valor = stats.kstest(dados_x, cdf='norm', args=(media,std), N =len(dados_x))

    print("\nValor de estatistica")
    print(ks_stat)

    print("\nValor de KS critico")
    print(ks_critico)

    if ks_critico >= ks_stat:
        print(f'\nCom 95% de confianca, aceitamos a hipotese de normalidade dos dados, segundo o teste de Kolmogorov-Smirnov, que indica que o valor da estatistica e menor ou igual ao valor de KS critico')
    else:
        print(f'\nCom 95% de confianca, rejeitamos a hipotese de normalidade dos dados, segundo o teste de Kolmogorov-Smirnov, que indica que o valor da estatistica e maior que o valor de KS critico')


def teste_t(dados_x: list, dados_y:list):
    # Cálculo do Teste T usando os dados de X e Y
    valor_t, p = stats.ttest_ind(dados_x,dados_y)

    print('\nTeste t')
    print(valor_t)


if __name__ == '__main__':
    x = variavel_aleatoria('X', 5, 1, 1000)
    y = variavel_aleatoria('Y', 6, 1, 1000)

    histograma(x, 'Histograma de X')
    histograma(y, 'Histograma de Y')

    fdc(x, 'FDC de X')
    fdc(y, 'FDC de Y')

    pr_maior(x, 'X', 6)
    pr_igual(y, 'Y', 0)

    kolmogorov_smirnov(x)

    teste_t(x,y)
