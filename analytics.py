import numpy as np
import pandas as pd
from typing import List, Tuple, Dict, Any

class AnalyticsStatisticalEngine:
    @staticmethod
    def calcular_frequencias(df_historico: pd.DataFrame) -> pd.DataFrame:
        """Calcula frequências absolutas e relativas das dezenas no histórico."""
        dezenas_cols = [f'Dezena_{i+1}' for i in range(6)]
        todos_numeros = df_historico[dezenas_cols].values.flatten()
        contagem = pd.Series(todos_numeros).value_counts().reindex(range(1, 61), fill_value=0)
        
        return pd.DataFrame({
            'Dezena': contagem.index,
            'Frequencia_Absoluta': contagem.values,
            'Frequencia_Relativa': contagem.values / len(df_historico)
        }).sort_values('Dezena').reset_index(drop=True)

    @staticmethod
    def analisar_paridade(combinacao: List[int]) -> Tuple[int, int]:
        """Retorna a contagem exata de números (Pares, Ímpares)."""
        pares = sum(1 for n in combinacao if n % 2 == 0)
        return pares, 6 - pares

    @staticmethod
    def analisar_quadrantes(combinacao: List[int]) -> List[int]:
        """Mapeia a distribuição espacial dos números dentro dos 4 quadrantes."""
        q1 = q2 = q3 = q4 = 0
        for n in combinacao:
            linha = (n - 1) // 10
            coluna = (n - 1) % 10
            if linha < 3 and coluna < 5: q1 += 1
            elif linha < 3 and coluna >= 5: q2 += 1
            elif linha >= 3 and coluna < 5: q3 += 1
            else: q4 += 1
        return [q1, q2, q3, q4]

    @staticmethod
    def calcular_somas_historicas(df_historico: pd.DataFrame) -> List[int]:
        """Calcula a soma das seis dezenas sorteadas por concurso."""
        dezenas_cols = [f'Dezena_{i+1}' for i in range(6)]
        return df_historico[dezenas_cols].sum(axis=1).tolist()

    @staticmethod
    def executar_backtesting_temporal(df_historico: pd.DataFrame) -> Dict[str, Any]:
        """Realiza backtesting dividindo treino/teste sem vazamento de dados."""
        ponto_corte = int(len(df_historico) * 0.8)
        dados_treino = df_historico.iloc[:ponto_corte]
        dados_teste = df_historico.iloc[ponto_corte:]
        
        freq_treino = AnalyticsStatisticalEngine.calcular_frequencias(dados_treino)
        pesos = np.array(freq_treino['Frequencia_Relativa'].values, copy=True)
        pesos /= pesos.sum()
        
        acertos_algoritmo = []
        acertos_aleatorios = []
        dezenas_teste = dados_teste[[f'Dezena_{i+1}' for i in range(6)]].values
        
        for teste_sorteio in dezenas_teste:
            set_teste = set(teste_sorteio)
            # Simulação Ponderada Histórica
            jogo_algo = np.random.choice(range(1, 61), 6, replace=False, p=pesos)
            acertos_algo = len(set_teste.intersection(jogo_algo))
            acertos_algoritmo.append(acertos_algo)
            
            # Simulação Aleatória Pura
            jogo_aleat = np.random.choice(range(1, 61), 6, replace=False)
            acertos_aleat = len(set_teste.intersection(jogo_aleat))
            acertos_aleatorios.append(acertos_aleat)
            
        return {
            "media_algoritmo": float(np.mean(acertos_algoritmo)),
            "media_aleatorio": float(np.mean(acertos_aleatorios)),
            "max_acertos_algoritmo": int(np.max(acertos_algoritmo)),
            "max_acertos_aleatorio": int(np.max(acertos_aleatorios)),
            "tamanho_amostra_teste": len(dados_teste)
        }