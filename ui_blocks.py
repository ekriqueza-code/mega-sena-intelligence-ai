import streamlit as st
from typing import List

class UIPremiumComponents:
    @staticmethod
    def injetar_design_system_css() -> None:
        """Injeta a arquitetura CSS Premium baseada nas cores contrastadas do manual SaaS."""
        st.markdown("""
            <style>
                .stApp { background-color: #FFFFFF; color: #0B1F33; }
                h1, h2, h3 { color: #0B1F33 !important; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
                .main-header { background: linear-gradient(135deg, #0B1F33 0%, #145DA0 100%); padding: 25px; border-radius: 10px; color: #FFFFFF !important; margin-bottom: 25px; text-align: center; }
                .main-header h1 { color: #FFFFFF !important; font-size: 26px !important; font-weight: 700; margin-bottom: 5px; }
                .main-header p { color: #E0E6ED !important; font-size: 14px; margin: 0; }
                .metric-card { background-color: #F8FAFC; border: 1px solid #E2E8F0; border-left: 5px solid #145DA0; padding: 15px; border-radius: 6px; margin-bottom: 12px; }
                .metric-value { font-size: 22px; font-weight: bold; color: #0B1F33; }
                .metric-label { font-size: 12px; color: #64748B; text-transform: uppercase; letter-spacing: 0.5px; }
                .game-card { background-color: #F1F5F9; border: 1px solid #CBD5E1; padding: 12px; border-radius: 6px; text-align: center; font-size: 18px; font-weight: bold; color: #145DA0; letter-spacing: 2px; margin-bottom: 10px; }
                .responsible-bar { background-color: #FEF3C7; border: 1px solid #FCD34D; color: #92400E; padding: 12px; border-radius: 6px; font-size: 13px; text-align: center; margin-top: 30px; }
            </style>
        """, unsafe_allow_html=True)

    @staticmethod
    def renderizar_cabecalho() -> None:
        st.markdown("""
            <div class='main-header'>
                <h1>Mega-Sena Intelligence AI</h1>
                <div style='font-size: 16px; font-weight: 300; opacity: 0.9;'>Análise Estatística e Geração de Combinações</div>
                <p style='margin-top: 10px; font-style: italic; opacity: 0.8;'>Explore os resultados históricos, analise frequências e gereDoc combinações para fins informativos.</p>
            </div>
        """, unsafe_allow_html=True)

    @staticmethod
    def renderizar_volante_html(jogo_selecionado: List[int]) -> None:
        """Gera a grade matemática 6x10 responsiva do volante virtual em HTML/CSS."""
        volante_html = "<div style='display: grid; grid-template-columns: repeat(10, 1fr); gap: 6px; width: 100%; max-width: 460px; background: #0B1F33; padding: 15px; border-radius: 8px; margin: 0 auto;'>"
        for numero in range(1, 61):
            if numero in jogo_selecionado:
                # Ativação das dezenas selecionadas em Verde Esmeralda Discreto para alto contraste
                volante_html += f"<div style='background-color: #2ECC71; color: #0B1F33; font-weight: bold; padding: 8px 0; text-align: center; border-radius: 4px; box-shadow: 0 0 5px #2ECC71;'>{numero:02d}</div>"
            else:
                # Fundo neutro contrastado
                volante_html += f"<div style='background-color: #145DA0; color: #FFFFFF; padding: 8px 0; text-align: center; border-radius: 4px; opacity: 0.4;'>{numero:02d}</div>"
        volante_html += "</div>"
        st.markdown(volante_html, unsafe_allow_html=True)