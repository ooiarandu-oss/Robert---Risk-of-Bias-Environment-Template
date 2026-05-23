import streamlit as st
import pandas as pd

# Must be the first Streamlit command
st.set_page_config(
    page_title="Robert — Risk of Bias Environment Template",
    layout="wide",
    page_icon="📝"
)

# Custom CSS for styling based on the mockup
def inject_custom_css():
    st.markdown("""
        <style>
        :root {
            --color-text-primary: #1F2937;
            --color-text-secondary: #4B5563;
            --color-text-tertiary: #9CA3AF;
            --color-background-primary: #ffffff;
            --color-background-secondary: #F3F4F6;
            --color-border-tertiary: #E5E7EB;
            --color-border-secondary: #D1D5DB;
            --border-radius-lg: 12px;
            --border-radius-md: 8px;
        }
        
        /* Main Header */
        .main-header {
            color: #1D9E75;
            text-align: center;
            margin-bottom: 0.2rem;
            font-weight: bold;
        }
        .sub-header {
            text-align: center;
            color: #7f8c8d;
            margin-top: 0px;
            margin-bottom: 20px;
            font-size: 1.1rem;
        }
        
        /* Instrument Cards */
        .instr-card {
            border: 1px solid var(--color-border-tertiary);
            border-radius: var(--border-radius-lg);
            padding: 16px;
            background: var(--color-background-primary);
            transition: all 0.2s;
            height: 100%;
        }
        .instr-card:hover {
            border-color: #1D9E75;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        .instr-card-family {
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: var(--color-text-tertiary);
            margin-bottom: 4px;
        }
        .instr-card-name {
            font-size: 16px;
            font-weight: 600;
            color: var(--color-text-primary);
            line-height: 1.3;
        }
        .instr-card-meta {
            font-size: 12px;
            color: var(--color-text-secondary);
            margin-top: 8px;
        }
        
        /* Export Buttons - We map these classes in markdown to wrap buttons, but Streamlit buttons are harder to style individually by class. We'll rely on columns and basic button styling where possible, or use HTML links for downloads. */
        
        </style>
    """, unsafe_allow_html=True)


def main():
    inject_custom_css()
    
    st.markdown("<h1 class='main-header'>Robert</h1>", unsafe_allow_html=True)
    st.markdown("<h4 class='sub-header'>Risk of Bias Environment Template</h4>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["🛡️ Risk of Bias templates", "📊 GRADE assessment", "🤝 Reviewer Agreement (Em breve)"])
    
    with tab1:
        render_risk_of_bias_page()
        
    with tab2:
        render_grade_assessment_page()
        
    with tab3:
        render_reviewer_agreement_page()


def render_risk_of_bias_page():
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent))
    
    from templates_config import INSTRUMENTS
    from utils.render_template import render_instrument_form
    
    st.subheader("Escolha o instrumento")
    
    # Create a grid for cards
    cols = st.columns(3)
    for idx, (inst_id, inst) in enumerate(INSTRUMENTS.items()):
        col = cols[idx % 3]
        with col:
            # We use a container that looks like a card
            is_selected = st.session_state.get('selected_instrument') == inst_id
            border_color = "#1D9E75" if is_selected else "#E5E7EB"
            bg_color = "#E1F5EE" if is_selected else "#ffffff"
            
            with st.container():
                st.markdown(f"""
                <div style="border: 1px solid {border_color}; border-radius: 12px; padding: 16px; background: {bg_color}; height: 100%; margin-bottom: 10px;">
                    <div style="font-size: 11px; text-transform: uppercase; letter-spacing: 0.06em; color: {'#0F6E56' if is_selected else '#9CA3AF'}; margin-bottom: 4px;">{inst['family']}</div>
                    <div style="font-size: 16px; font-weight: 600; color: {'#085041' if is_selected else '#1F2937'}; line-height: 1.3;">{inst['name']}</div>
                    <div style="font-size: 12px; color: {'#0F6E56' if is_selected else '#4B5563'}; margin-top: 8px;">{inst['meta']}</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Selecionar {inst['name']}", key=f"btn_{inst_id}", use_container_width=True):
                    st.session_state.selected_instrument = inst_id
                    st.rerun()
                    
    st.divider()
    
    if 'selected_instrument' in st.session_state:
        selected_inst = INSTRUMENTS[st.session_state.selected_instrument]
        
        # We need to render the form first to get the responses, so we put it in a form or just get state
        responses = render_instrument_form(selected_inst)
        
        study_info = {
            "study_title": st.session_state.get("study_title", ""),
            "study_author_year": st.session_state.get("study_author_year", ""),
            "study_reviewer": st.session_state.get("study_reviewer", ""),
            "study_doi": st.session_state.get("study_doi", ""),
            "study_record": st.session_state.get("study_record", ""),
            "study_date": str(st.session_state.get("study_date", ""))
        }
        
        st.divider()
        st.markdown("### Exportar Relatórios")
        
        # We import here to avoid circular imports if any, and make it easier
        from utils.export_pdf import generate_pdf_report
        from utils.export_excel import generate_excel_report
        from utils.export_robvis_generic import generate_robvis_csv
        from utils.export_critiplot import generate_critiplot_csv
        
        e1, e2, e3, e4 = st.columns(4)
        with e1:
            pdf_data = generate_pdf_report(selected_inst, responses, study_info)
            st.download_button("📄 Baixar PDF", pdf_data, file_name=f"{selected_inst['id']}_report.pdf", mime="application/pdf", use_container_width=True)
        with e2:
            excel_data = generate_excel_report(selected_inst, responses, study_info)
            st.download_button("📊 Baixar Excel", excel_data, file_name=f"{selected_inst['id']}_data.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
        with e3:
            robvis_data = generate_robvis_csv(selected_inst, responses, study_info['study_title'])
            st.download_button("📈 Baixar robvis CSV", robvis_data, file_name=f"{selected_inst['id']}_robvis.csv", mime="text/csv", use_container_width=True)
        if selected_inst['type'] in ['nos', 'jbi']:
            with e4:
                critiplot_data = generate_critiplot_csv(selected_inst, responses, study_info['study_title'])
                st.download_button("📉 Baixar critiplot CSV", critiplot_data, file_name=f"{selected_inst['id']}_critiplot.csv", mime="text/csv", use_container_width=True)


def render_grade_assessment_page():
    st.subheader("GRADE Assessment Table")
    
    # Define columns based on Ministry of Health model
    base_columns = [
        "Desfecho",
        "Nº de estudos",
        "Delineamento",
        "Limitações metodológicas",
        "Inconsistência",
        "Evidência indireta",
        "Imprecisão",
        "Viés de publicação",
        "Participantes — tecnologia avaliada",
        "Participantes — comparador",
        "Efeito relativo (IC 95%)",
        "Efeito absoluto",
        "Qualidade da evidência",
        "Justificativa"
    ]
    
    if 'grade_df' not in st.session_state:
        st.session_state.grade_df = pd.DataFrame(columns=base_columns)
        # Add initial row
        st.session_state.grade_df.loc[0] = {col: "" for col in base_columns}
    
    # Toolbar for row/column management
    t1, t2, t3, t4, t5, t6, t7 = st.columns([1.5, 1.5, 1.5, 1.5, 1, 1, 1])
    with t1:
        if st.button("➕ Adicionar desfecho", use_container_width=True):
            new_row = {col: "" for col in st.session_state.grade_df.columns}
            st.session_state.grade_df.loc[len(st.session_state.grade_df)] = new_row
            st.rerun()
    with t2:
        if st.button("➖ Remover desfecho", use_container_width=True) and len(st.session_state.grade_df) > 1:
            st.session_state.grade_df = st.session_state.grade_df.iloc[:-1]
            st.rerun()
    with t3:
        if st.button("➕ Adicionar estudo", use_container_width=True):
            col_name = f"Estudo {len([c for c in st.session_state.grade_df.columns if 'Estudo' in c]) + 1}"
            st.session_state.grade_df.insert(2, col_name, "")
            st.rerun()
    with t4:
        if st.button("➖ Remover estudo", use_container_width=True):
            study_cols = [c for c in st.session_state.grade_df.columns if 'Estudo' in c]
            if study_cols:
                st.session_state.grade_df.drop(columns=[study_cols[-1]], inplace=True)
                st.rerun()
    
    from utils.export_pdf import generate_grade_pdf
    from utils.export_excel import generate_grade_excel
    
    with t5:
        pdf_data = generate_grade_pdf(st.session_state.grade_df)
        st.download_button("📄 PDF", pdf_data, file_name="GRADE_assessment.pdf", mime="application/pdf", use_container_width=True)
    with t6:
        excel_data = generate_grade_excel(st.session_state.grade_df)
        st.download_button("📊 Excel", excel_data, file_name="GRADE_assessment.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
    with t7:
        csv_data = st.session_state.grade_df.to_csv(index=False).encode('utf-8')
        st.download_button("📈 CSV", csv_data, file_name="GRADE_assessment.csv", mime="text/csv", use_container_width=True)

    # Configure columns
    column_config = {
        "Delineamento": st.column_config.SelectboxColumn(
            "Delineamento",
            options=["Ensaio clínico randomizado", "Estudo observacional", "Coorte", "Caso-controle", "Transversal", "Série de casos", "Relato de caso", "Revisão sistemática"],
            help="ECR começa Alta; observacionais Baixa; relatos/séries Muito Baixa"
        ),
        "Limitações metodológicas": st.column_config.SelectboxColumn("Limitações metodológicas", options=["Sem limitações graves", "Grave", "Muito grave", "Não avaliado", "Incerto"], help="Risco de viés: rebaixa 1 nível se grave, 2 se muito grave"),
        "Inconsistência": st.column_config.SelectboxColumn("Inconsistência", options=["Sem limitações graves", "Grave", "Muito grave", "Não avaliado", "Incerto"], help="Heterogeneidade não explicada, I2"),
        "Evidência indireta": st.column_config.SelectboxColumn("Evidência indireta", options=["Sem limitações graves", "Grave", "Muito grave", "Não avaliado", "Incerto"], help="População/Intervenção diferem da PICO"),
        "Imprecisão": st.column_config.SelectboxColumn("Imprecisão", options=["Sem limitações graves", "Grave", "Muito grave", "Não avaliado", "Incerto"], help="Amplitude IC95%, n eventos"),
        "Viés de publicação": st.column_config.SelectboxColumn("Viés de publicação", options=["Sem limitações graves", "Grave", "Muito grave", "Não avaliado", "Incerto"], help="Assimetria funnel plot, estudos pequenos"),
        "Qualidade da evidência": st.column_config.SelectboxColumn(
            "Qualidade da evidência",
            options=["Alta", "Moderada", "Baixa", "Muito baixa"],
            help="Alta, Moderada, Baixa, Muito baixa. Permitido override."
        )
    }

    st.session_state.grade_df = st.data_editor(
        st.session_state.grade_df,
        column_config=column_config,
        num_rows="fixed", # Handled via buttons to avoid issues with dynamic columns
        use_container_width=True,
        hide_index=True,
        height=350
    )


def render_reviewer_agreement_page():
    st.subheader("Reviewer Agreement")
    st.info("Este módulo está planejado para uma etapa futura (Placeholder).")
    st.write("Aqui você poderá:")
    st.markdown("- Fazer upload do Excel do Avaliador 1")
    st.markdown("- Fazer upload do Excel do Avaliador 2")
    st.markdown("- Ver a comparação item a item e identificar divergências")
    st.markdown("- Calcular Kappa de Cohen e ICC")
    st.markdown("- Exportar o consenso")


if __name__ == "__main__":
    main()
