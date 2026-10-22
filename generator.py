import numpy as np
import pandas as pd
from typing import List, Optional
from analytics import AnalyticsStatisticalEngine

class CombinationsGeneratorEngine:
    def __init__(self, df_frequencias: pd.DataFrame) -> None:
        self.df_frequencias = df_frequencias

    def gerar_cartoes_inteligentes(
        self, 
        qtd_jogos: int, 
        usar_filtros: bool, 
        paridade_selecionada: Optional[str] = None, 
        semente: Optional[int] = None
    ) -> List[List[int]]:
        """Gera jogos clonando profundamente os arrays de peso para banir erros de Read-Only."""
        if semente is not None:
            np.random.seed(semente)
        else:
            import time
            np.random.seed(int(time.time() * 1000) % 2**32)
            
        jogos_finais: List[List[int]] = []
        
        # RESOLUÇÃO DO ERRO VALUEERROR: Array clonado profundamente para livre manipulação em memória
        pesos = np.array(self.df_frequencias['Frequencia_Relativa'].values, copy=True, dtype=np.float64)
        pesos /= pesos.sum()
        
        tentativas_max = 5000
        tentativas = 0
        
        while len(jogos_finais) < qtd_jogos and tentativas < tentativas_max:
            tentativas += 1
            
            if usar_filtros:
                palpite = np.random.choice(range(1, 61), 6, replace=False, p=pesos)
            else:
                palpite = np.random.choice(range(1, 61), 6, replace=False)
                
            jogo_lista = sorted([int(x) for x in palpite])
            
            if usar_filtros:
                pares, impares = AnalyticsStatisticalEngine.analisar_paridade(jogo_lista)
                if paridade_selecionada == "Equilibrado (3P / 3Í)" and (pares != 3):
                    continue
                if paridade_selecionada == "Predominante Par (4P / 2Í)" and (pares != 4):
                    continue
                if paridade_selecionada == "Predominante Ímpar (2P / 4Í)" and (pares != 2):
                    continue
                
                quadrantes = AnalyticsStatisticalEngine.analisar_quadrantes(jogo_lista)
                if max(quadrantes) > 4:
                    continue
            
            if jogo_lista not in jogos_finais:
                jogos_finais.append(jogo_lista)
                
        if len(jogos_finais) == 0:
            jogos_finais = [sorted([int(x) for x in np.random.choice(range(1, 61), 6, replace=False)]) for _ in range(qtd_jogos)]
            
        return jogos_finais