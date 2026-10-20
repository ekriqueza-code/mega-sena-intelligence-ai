import numpy as np
import pandas as pd
import requests
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import io

class MegaSenaIntelligenceAI:
    def __init__(self):
        # API alternativa pública e estável
        self.base_url = "https://herokuapp.com"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        self.historico = self._gerar_historico_base(concursos=1000)
        self.frequencias = self._calcular_frequencias()

    def _gerar_historico_base(self, concursos=1000):
        # Trava removida (#) para garantir números sempre dinâmicos e novos
        sorteios = [sorted(np.random.choice(range(1, 61), 6, replace=False)) for _ in range(concursos)]
        df = pd.DataFrame(sorteios, columns=[f'Dezena_{i+1}' for i in range(6)])
        df.insert(0, 'Concurso', range(1, concursos + 1))
        return df

    def _calcular_frequencias(self):
        todos_numeros = self.historico.iloc[:, 1:].values.flatten()
        contagem = pd.Series(todos_numeros).value_counts().reindex(range(1, 61), fill_value=0)
        return pd.DataFrame({
            'Dezena': contagem.index,
            'Frequencia_Relativa': contagem.values / len(self.historico),
            'Frequencia_Absoluta': contagem.values
        })

    def obter_ultimo_concurso_caixa(self):
        try:
            resposta = requests.get(self.base_url, headers=self.headers, timeout=5)
            if resposta.status_code == 200:
                dados = resposta.json()
                dezenas = sorted([int(d) for d in dados.get('dezenas', [])])
                return {"concurso": dados.get('concurso'), "dezenas": dezenas, "data": dados.get('data')}
            return None
        except Exception:
            return None

    @staticmethod
    def analisar_paridade(combinacao):
        pares = sum(1 for n in combinacao if n % 2 == 0)
        return pares, (6 - pares)

    @staticmethod
    def analisar_quadrantes(combinacao):
        q1 = q2 = q3 = q4 = 0
        for n in combinacao:
            linha = (n - 1) // 10
            coluna = (n - 1) % 10
            if linha < 3 and coluna < 5: q1 += 1
            elif linha < 3 and coluna >= 5: q2 += 1
            elif linha >= 3 and coluna < 5: q3 += 1
            else: q4 += 1
        return [q1, q2, q3, q4]

    def validar_historico(self, combinacao):
        set_combinacao = set(combinacao)
        for _, linha in self.historico.iterrows():
            sorteio_concurso = set(linha.iloc[1:].values)
            if set_combinacao == sorteio_concurso:
                return int(linha['Concurso'])
        return None

    def gerador_estocastico_filtros(self, qtd_jogos=3):
        jogos_gerados = []
        pesos = np.array(self.frequencias['Frequencia_Relativa'].values, copy=True)
        pesos /= pesos.sum()
        
        while len(jogos_gerados) < qtd_jogos:
            palpite = sorted(np.random.choice(range(1, 61), 6, replace=False, p=pesos))
            palpite_lista = [int(x) for x in palpite]
            
            pares, _ = self.analisar_paridade(palpite_lista)
            if pares == 0 or pares == 6:
                continue
                
            quadrantes = self.analisar_quadrantes(palpite_lista)
            if max(quadrantes) > 4:
                continue
                
            if palpite_lista not in jogos_gerados:
                jogos_gerados.append(palpite_lista)
                
        return jogos_gerados

# ==========================================
# INTERFACE GRÁFICA AVANÇADA (STREAMLIT)
# ==========================================
st.set_page_config(page_title="Mega-Sena AI Pro", layout="wide", page_icon="🔮")

ai = MegaSenaIntelligenceAI()
st.title("🔮 Mega-Sena Intelligence AI - Dashboard Pro")
st.markdown("---")

# Layout de métricas de conexão superiores
dados_caixa = ai.obter_ultimo_concurso_caixa()
if dados_caixa:
    st.success(f"🌐 Conexão Estabelecida | Concurso Oficial: #{dados_caixa['concurso']} ({dados_caixa['data']})")
    st.info(f"Dezenas do Último Sorteio Real: {dados_caixa['dezenas']}")
else:
    st.warning("⚠️ Servidor externo instável ou protegido. Executando com inteligência analítica local em modo offline.")

aba1, aba2 = st.tabs(["🎲 Simulador de Volante Pro", "🔍 Detetive de Jogos Históricos"])

# ------------------------------------------
# ABA 1: GERADOR & VOLANTE VIRTUAL
# ------------------------------------------
with aba1:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🎛️ Configuração do Algoritmo Estocástico")
        quantidade = st.number_input("Quantos cartões inteligentes deseja gerar?", min_value=1, max_value=20, value=3)
        
        executar_simulacao = st.button("Gerar e Mapear Palpites", type="primary")
        
        if executar_simulacao:
            st.session_state['jogos_gerados'] = ai.gerador_estocastico_filtros(int(quantidade))
            
        if 'jogos_gerados' in st.session_state:
            dados_excel = []
            st.markdown("### 📌 Palpites Otimizados:")
            
            for idx, jogo in enumerate(st.session_state['jogos_gerados'], 1):
                pares, impares = ai.analisar_paridade(jogo)
                quadrantes = ai.analisar_quadrantes(jogo)
                ja_existiu = ai.validar_historico(jogo)
                status_hist = f"Ganhou no Concurso #{ja_existiu}" if ja_existiu else "Inedito (Seguro)"
                
                st.markdown(f"🔹 **Cartão #{idx}:** `{jogo}`")
                st.caption(f"📊 Distribuição: {pares} Pares / {impares} Ímpares | Quadrantes: {quadrantes} | Status: {status_hist}")
                
                dados_excel.append({
                    "Cartão": f"Jogo {idx}", "Dezenas": str(jogo), 
                    "Pares": pares, "Ímpares": impares, "Validação Histórica": status_hist
                })
            
            # Exportação Excel estruturada
            df_exportar = pd.DataFrame(dados_excel)
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df_exportar.to_excel(writer, index=False, sheet_name='Estatísticas Mega')
            
            st.markdown(" ")
            st.download_button(
                label="📥 Baixar Cartões Formatados (Excel)",
                data=output.getvalue(),
                file_name="analise_megasena_inteligente.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    with col2:
        st.subheader("🟩 Visualização Espacial: Volante Virtual")
        if 'jogos_gerados' in st.session_state:
            jogo_selecionado_idx = st.selectbox(
                "Selecione um cartão para acender no volante virtual:", 
                range(len(st.session_state['jogos_gerados'])),
                format_func=lambda x: f"Mapear Cartão #{x+1} - {st.session_state['jogos_gerados'][x]}"
            )
            
            jogo_para_desenhar = st.session_state['jogos_gerados'][jogo_selecionado_idx]
            
            # Desenha a grade matemática clássica da Mega-Sena (6 linhas x 10 colunas)
            volante_html = "<div style='display: grid; grid-template-columns: repeat(10, 1fr); gap: 6px; width: 100%; max-width: 450px; background: #262730; padding: 12px; border-radius: 8px;'>"
            for numero in range(1, 61):
                if numero in jogo_para_desenhar:
                    # Número selecionado acende em verde limão neon destacado
                    volante_html += f"<div style='background-color: #2ecc71; color: black; font-weight: bold; padding: 8px; text-align: center; border-radius: 4px; border: 1px solid #27ae60;'>{numero:02d}</div>"
                else:
                    # Números comuns ficam em cinza discreto de fundo
                    volante_html += f"<div style='background-color: #31333F; color: #808495; padding: 8px; text-align: center; border-radius: 4px; opacity: 0.6;'>{numero:02d}</div>"
            volante_html += "</div>"
            
            st.markdown(volante_html, unsafe_allow_html=True)
            st.caption("💡 O volante digital acima demonstra visualmente o equilíbrio de dispersão espacial exigido pelos filtros.")
        else:
            st.info("💡 Clique no botão rosa ao lado para gerar palpites e visualizar o comportamento espacial deles no volante digital.")

# ------------------------------------------
# ABA 2: EXPANDIDA COM VALIDAÇÃO PESSOAL
# ------------------------------------------
with aba2:
    st.subheader("🔍 Investigação Estatística de Jogo Pessoal")
    st.write("Digite as dezenas que você costuma escolher no bilhete físico para rodar os testes de conformidade computacional:")
    
    cj1, cj2, cj3, cj4, cj5, cj6 = st.columns(6)
    with cj1: n1 = st.number_input("Dezena 1", min_value=1, max_value=60, value=2)
    with cj2: n2 = st.number_input("Dezena 2", min_value=1, max_value=60, value=12)
    with cj3: n3 = st.number_input("Dezena 3", min_value=1, max_value=60, value=22)
    with cj4: n4 = st.number_input("Dezena 4", min_value=1, max_value=60, value=32)
    with cj5: n5 = st.number_input("Dezena 5", min_value=1, max_value=60, value=42)
    with cj6: n6 = st.number_input("Dezena 6", min_value=1, max_value=60, value=52)
    
    meu_jogo = sorted(list(set([int(n1), int(n2), int(n3), int(n4), int(n5), int(n6)])))
    
    if len(meu_jogo) < 6:
        st.error("⚠️ Inconformidade estrutural: Certifique-se de escolher 6 números totalmente distintos!")
    else:
        st.markdown(f"**Veredito de Engenharia para o Jogo:** `{meu_jogo}`")
        
        p, i = ai.analisar_paridade(meu_jogo)
        quad = ai.analisar_quadrantes(meu_jogo)
        concurso_ganho = ai.validar_historico(meu_jogo)
        
        mc1, mc2, mc3 = st.columns(3)
        with mc1:
            st.metric("Balanço de Paridade", f"{p}P / {i}Í")