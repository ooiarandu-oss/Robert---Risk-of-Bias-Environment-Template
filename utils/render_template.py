import streamlit as st

def render_instrument_form(instrument):
    st.markdown(f"### {instrument['name']}")
    st.caption(instrument['meta'])
    
    with st.expander("ℹ️ Informações do Estudo", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Título do estudo", key="study_title")
            st.text_input("Autor, ano", key="study_author_year")
            st.text_input("Avaliador", key="study_reviewer")
        with col2:
            st.text_input("DOI", key="study_doi")
            st.text_input("Número do registro", key="study_record")
            st.date_input("Data da avaliação", key="study_date")
            
    st.divider()
    st.markdown("### 📋 Itens de Avaliação")
    
    responses = {}
    
    if instrument['type'] == 'robins' or instrument['type'] == 'rob':
        # For ROBINS and RoB 2, they use Domains with signaling questions
        for dom in instrument['domains']:
            st.markdown(f"#### Domínio {dom['num']}: {dom['name']}")
            if 'signaling_questions' in dom and dom['signaling_questions']:
                for sq in dom['signaling_questions']:
                    key = f"q_{dom['num']}_{sq['num']}"
                    st.write(f"**{sq['num']}** {sq['text']}")
                    responses[key] = st.radio("Resposta", instrument['options'], key=key, horizontal=True, label_visibility="collapsed")
            
            # Domain Judgement
            if 'judgements' in instrument:
                j_key = f"judgement_{dom['num']}"
                st.write("**Julgamento do domínio**")
                responses[j_key] = st.radio("Julgamento", instrument['judgements'], key=j_key, horizontal=True, label_visibility="collapsed")
            
            # Direction of bias (ROBINS)
            if 'directions' in instrument:
                d_key = f"direction_{dom['num']}"
                st.write("**Direção prevista do viés**")
                responses[d_key] = st.radio("Direção", instrument['directions'], key=d_key, horizontal=True, label_visibility="collapsed")
                
            just_key = f"justification_{dom['num']}"
            responses[just_key] = st.text_area(f"Justificativa (Domínio {dom['num']})", key=just_key, height=68)
            st.divider()
    else:
        # Standard list of items (NOS, JBI, D&B)
        for idx, item in enumerate(instrument['items']):
            st.markdown(f"**[{item.get('domain', '')}] {item['num']} - {item['text']}**")
            
            col_a, col_b = st.columns([1, 1])
            with col_a:
                resp_key = f"item_{idx}"
                responses[resp_key] = st.radio("Resposta", instrument['options'], key=resp_key, horizontal=True, label_visibility="collapsed")
            with col_b:
                just_key = f"just_{idx}"
                responses[just_key] = st.text_input("Justificativa/Comentário", key=just_key, label_visibility="collapsed", placeholder="Sua justificativa...")
            st.write("")
        st.divider()
        
        st.markdown("### 🎯 Decisão Global")
        col_app1, col_app2 = st.columns(2)
        with col_app1:
            if instrument['type'] == 'jbi':
                st.radio("Overall Decision:", ["Include", "Exclude", "Seek further information", "Not applicable"], key="overall_decision", horizontal=True)
            else:
                st.radio("Overall Decision:", ["Include", "Exclude", "Seek further info"], key="overall_decision", horizontal=True)
        with col_app2:
            st.text_area("Comentários Gerais", key="overall_comments")

    return responses
