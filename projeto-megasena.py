import streamlit as st
import pandas as pd
import io
import matplotlib.pyplot as plt
import seaborn as sns
from data_sources import DataCentralEngine
from analytics import AnalyticsStatisticalEngine
from generator import CombinationsGeneratorEngine
from ui_blocks import UIPremiumComponents

# Inicialização e Configuração do Ciclo de Vida do Streamlit
st.set_page_config(page_title="Mega-Sena AI Pro 2.0", layout="wide", page_icon="🔮")
UIPremiumComponents.injetar_design_system_css()
UIPremiumComponents.renderizar_cabecalho()

# Inicialização das Instâncias de Negócio em Memória (Singleton Pattern)
if 'data_engine' not in st.session_state:
    st.session_state['data_engine'] = DataCentralEngine()
    st.session_state['app_data'] = st.session_state['data_engine'].obter_dados_caixa_realtime()

app_data = st.session_state['app_data']
df_historico = app_data["historico"]
df_frequencias = AnalyticsStatisticalEngine.calcular_frequencias(df_historico)

# --------------------------------------------------------------------------
# SEÇÃO 1: CENTRAL DE DADOS & STATUS DA APLICAÇÃO (CONEXÃO)
# --------------------------------------------------------------------------
with st.expander("🌐 Central de Status dos Dados e Monitor de Sincronização", expanded=False):
    c_status1, c_status2, c_status3 = st.columns(3)
    with c_status1:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>Mapeamento de Fonte</div><div class='metric-value' style='font-size:16px; color:#145DA0;'>{app_data['fonte']}</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-card'><div class='metric-label'>Status de Conexão</div><div class='metric-value' style='font-size:16px; color:#2ECC71;'>{app_data['status']}</div></div>", unsafe_allow_html=True)
    with c_status2:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>Último Concurso Sincronizado</div><div class='metric-value'>#{app_data['concurso']}</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-card'><div class='metric-label'>Data do Sorteio</div><div class='metric-value' style='font-size:16px;'>{app_data['data']}</div></div>", unsafe_allow_html=True)
    with c_status3:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>Massa Crítica Armazenada</div><div class='metric-value'>{len(df_historico)} concursos</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-card'><div class='metric-label'>Última Verificação Geral</div><div class='metric-value' style='font-size:14px;'>{app_data['timestamp_tentativa']}</div></div>", unsafe_allow_html=True)
    if "Offline" in app_data['status']:
        st.caption(f"ℹ️ Motivo do isolamento: {app_data['msg']}")

# Roteador Principal de Abas SaaS
abas_saas = [
    "🎲 Simulador de Volante Pro", 
    "🔍 Detetive de Jogos Históricos", 
    "📊 Inteligência Estatística Industrial", 
    "🧪 Backtesting & Auditoria de IA", 
    "💎 Recursos Premium SaaS", 
    "🎬 IA Avatar Video Generator"
]
aba_ativa = st.sidebar.radio("Navegação do Ecossistema:", abas_saas)

# --------------------------------------------------------------------------
# ABA 1: SIMULADOR DE VOLANTE PRO & GERADOR
# --------------------------------------------------------------------------
if aba_ativa == "🎲 Simulador de Volante Pro":
    st.subheader("🎲 Simulador de Volante Pro")
    
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.markdown("### Configurações do Motor")
        qtd_jogos = st.number_input("Quantidade de combinações a gerar:", min_value=1, max_value=15, value=3, step=1)
        modo_geracao = st.radio("Lógica de Seleção:", ["Aleatória Pura (Equiprovável)", "Filtros Estatísticos Ponderados"])
        
        paridade = "Equilibrado (3P / 3Í)"
        if modo_geracao == "Filtros Estatísticos Ponderados":
            paridade = st.selectbox("Filtro Condicional de Paridade:", ["Equilibrado (3P / 3Í)", "Predominante Par (4P / 2Í)", "Predominante Ímpar (2P / 4Í)"])
            st.caption("ℹ️ Nota Científica: Os filtros apenas restringem o subconjunto amostral às zonas de maior densidade histórica. Eles alteram as combinações selecionadas, mas não possuem vantagem preditiva sobre sorteios futuros singulares.")
            
        usar_semente = st.checkbox("Fixar semente numérica (Reprodutibilidade Científica)")
        semente_val = None
        if usar_semente:
            semente_val = st.number_input("Valor da Semente:", min_value=1, max_value=99999, value=42)

        if st.button("Gerar Lote de Combinações", type="primary"):
            generator = CombinationsGeneratorEngine(df_frequencias)
            is_ponderado = (modo_geracao == "Filtros Estatísticos Ponderados")
            st.session_state['jogos_lote'] = generator.gerar_cartoes_inteligentes(int(qtd_jogos), is_ponderado, paridade, semente_val)

    with col_g2:
        st.markdown("### Visualização Espacial")
        if 'jogos_lote' in st.session_state and len(st.session_state['jogos_lote']) > 0:
            jogos = st.session_state['jogos_lote']
            
            idx_selecionado = st.selectbox(
                "Escolha o cartão para projetar no Volante Virtual:",
                range(len(jogos)),
                format_func=lambda x: f"Cartão #{x+1} -> {jogos[x]}"
            )
            
            UIPremiumComponents.renderizar_volante_html(jogos[idx_selecionado])
            
            csv_dados = []
            for i, j in enumerate(jogos, 1):
                p_p, p_i = AnalyticsStatisticalEngine.analisar_paridade(j)
                csv_dados.append({"Jogo": f"Cartão {i}", "Dezenas": "-".join(f"{x:02d}" for x in j), "Pares": p_p, "Impares": p_i})
            df_csv = pd.DataFrame(csv_dados)
            
            st.markdown("#### Exportar Dados")
            st.download_button(
                label="📥 Exportar Combinações para CSV",
                data=df_csv.to_csv(index=False).encode('utf-8'),
                file_name="combinacoes_megasena_ai.csv",
                mime="text/csv"
            )
        else:
            st.info("Aguardando ativação do motor de simulação para desenhar a matriz espacial.")

# --------------------------------------------------------------------------
# ABA 2: DETETIVE DE JOGOS HISTÓRICOS
# --------------------------------------------------------------------------
elif aba_ativa == "🔍 Detetive de Jogos Históricos":
    st.subheader("🔍 Detetive de Jogos Históricos")
    op_pesquisa = st.radio("Escolha a modalidade de investigação:", ["Pesquisar Concurso Específico", "Auditar Cartão Customizado contra o Histórico"])
    
    if op_pesquisa == "Pesquisar Concurso Específico":
        num_conc = st.number_input("Digite o número do concurso:", min_value=1, max_value=int(df_historico['Concurso'].max()), value=int(df_historico['Concurso'].max()))
        registro = df_historico[df_historico['Concurso'] == num_conc]
        
        if not registro.empty:
            linha = registro.iloc[0]
            dezenas_sorteadas = [int(linha[f'Dezena_{i+1}']) for i in range(6)]
            st.success(f"📌 Concurso #{num_conc} realizado em {linha['Data']}")
            st.markdown(f"<div class='game-card'>{dezenas_sorteadas}</div>", unsafe_allow_html=True)
            UIPremiumComponents.renderizar_volante_html(dezenas_sorteadas)
        else:
            st.error("Concurso não localizado no banco de dados sincronizado.")
            
    elif op_pesquisa == "Auditar Cartão Customizado contra o Histórico":
        st.markdown("Insira 6 dezenas distintas para rastrear correspondências passadas:")
        c_n1, c_n2, c_n3, c_n4, c_n5, c_n6 = st.columns(6)
        with c_n1: d1 = st.number_input("D1", min_value=1, max_value=60, value=1)
        with c_n2: d2 = st.number_input("D2", min_value=1, max_value=60, value=10)
        with c_n3: d3 = st.number_input("D3", min_value=1, max_value=60, value=20)
        with c_n4: d4 = st.number_input("D4", min_value=1, max_value=60, value=30)
        with c_n5: d5 = st.number_input("D5", min_value=1, max_value=60, value=40)
        with c_n6: d6 = st.number_input("D6", min_value=1, max_value=60, value=50)
        
        cartao_usuario = sorted(list(set([int(d1), int(d2), int(d3), int(d4), int(d5), int(d6)])))
        if len(cartao_usuario) < 6:
            st.error("Erro: Existem números duplicados na entrada. Selecione 6 dezenas distintas.")
        else:
            st.info(f"Analisando Cartão: {cartao_usuario}")
            historico_matches = []
            set_usuario = set(cartao_usuario)
            dezenas_matriz = df_historico[[f'Dezena_{i+1}' for i in range(6)]].values
            concursos_vetor = df_historico['Concurso'].values
            
            for idx, sorteio in enumerate(dezenas_matriz):
                match_count = len(set_usuario.intersection(sorteio))
                if match_count >= 4:
                    historico_matches.append({"Concurso": int(concursos_vetor[idx]), "Acertos": match_count})
                    
            if len(historico_matches) > 0:
                st.warning("⚠️ Rastreamento detectou faixas de acertos históricos importantes para essa combinação:")
                st.dataframe(pd.DataFrame(historico_matches), use_container_width=True)
            else:
                st.success("✅ Este cartão nunca pontuou acima de 3 acertos no histórico analisado (Inédito).")

# --------------------------------------------------------------------------
# ABA 3: INTELIGÊNCIA ESTATÍSTICA INDUSTRIAL (GRÁFICOS)
# --------------------------------------------------------------------------
elif aba_ativa == "📊 Inteligência Estatística Industrial":
    st.subheader("📊 Inteligência Estatística Industrial")
    st.caption("Interpretação Descritiva: Os gráficos mapeiam o comportamento passado do ecossistema físico dos sorteios. Eventos passados não exercem tração ou influência em probabilidades futuras por se tratarem de eventos independentes.")
