import streamlit as st

ENGLISH_LABELS = {
    'study_info': 'Study information',
    'study_title': 'Study title',
    'study_author_year': 'Author, year',
    'study_reviewer': 'Reviewer',
    'study_doi': 'DOI',
    'study_record': 'Registration number',
    'study_date': 'Assessment date',
    'assessment_items': '📋 Assessment Items',
    'response': 'Response',
    'domain_judgement': 'Domain judgement',
    'direction_of_bias': 'Expected direction of bias',
    'justification': 'Justification',
    'overall_decision': 'Overall Decision:',
    'overall_comments': 'General comments',
    'include': 'Include',
    'exclude': 'Exclude',
    'seek_further_info': 'Seek further information',
    'not_applicable': 'Not applicable'
}

PORTUGUESE_LABELS = {
    'study_info': 'ℹ️ Informações do Estudo',
    'study_title': 'Título do estudo',
    'study_author_year': 'Autor, ano',
    'study_reviewer': 'Avaliador',
    'study_doi': 'DOI',
    'study_record': 'Número do registro',
    'study_date': 'Data da avaliação',
    'assessment_items': '📋 Itens de Avaliação',
    'response': 'Resposta',
    'domain_judgement': 'Julgamento do domínio',
    'direction_of_bias': 'Direção prevista do viés',
    'justification': 'Justificativa',
    'overall_decision': 'Decisão Global:',
    'overall_comments': 'Comentários Gerais',
    'include': 'Include',
    'exclude': 'Exclude',
    'seek_further_info': 'Seek further information',
    'not_applicable': 'Not applicable'
}


def render_instrument_form(instrument, locale='en'):
    labels = ENGLISH_LABELS if locale == 'en' else PORTUGUESE_LABELS

    st.markdown(f"### {instrument['name']}")
    st.caption(instrument.get('meta', ''))

    with st.expander(labels['study_info'], expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.text_input(labels['study_title'], key='study_title')
            st.text_input(labels['study_author_year'], key='study_author_year')
            st.text_input(labels['study_reviewer'], key='study_reviewer')
        with col2:
            st.text_input(labels['study_doi'], key='study_doi')
            st.text_input(labels['study_record'], key='study_record')
            st.date_input(labels['study_date'], key='study_date')

    st.divider()
    st.markdown(f"### {labels['assessment_items']}")

    responses = {}

    if instrument['type'] in ['robins', 'rob']:
        for dom in instrument['domains']:
            st.markdown(f"#### Domínio {dom['num']}: {dom['name']}")
            if 'signaling_questions' in dom and dom['signaling_questions']:
                for sq in dom['signaling_questions']:
                    key = f"q_{dom['num']}_{sq['num']}"
                    st.write(f"**{sq['num']}** {sq['text']}")
                    responses[key] = st.radio(labels['response'], instrument['options'], key=key, horizontal=True, label_visibility='collapsed')

            if 'judgements' in instrument:
                j_key = f"judgement_{dom['num']}"
                st.write(f"**{labels['domain_judgement']}**")
                responses[j_key] = st.radio(labels['domain_judgement'], instrument['judgements'], key=j_key, horizontal=True, label_visibility='collapsed')

            if 'directions' in instrument:
                d_key = f"direction_{dom['num']}"
                st.write(f"**{labels['direction_of_bias']}**")
                responses[d_key] = st.radio(labels['direction_of_bias'], instrument['directions'], key=d_key, horizontal=True, label_visibility='collapsed')

            just_key = f"justification_{dom['num']}"
            responses[just_key] = st.text_area(f"{labels['justification']} (Domínio {dom['num']})", key=just_key, height=68)
            st.divider()
    else:
        for idx, item in enumerate(instrument['items']):
            st.markdown(f"**[{item.get('domain', '')}] {item['num']} - {item['text']}**")

            col_a, col_b = st.columns([1, 1])
            with col_a:
                resp_key = f"item_{idx}"
                responses[resp_key] = st.radio(labels['response'], instrument['options'], key=resp_key, horizontal=True, label_visibility='collapsed')
            with col_b:
                just_key = f"just_{idx}"
                responses[just_key] = st.text_input(labels['justification'] + "/Comment", key=just_key, label_visibility='collapsed', placeholder='Your justification...')
            st.write("")
        st.divider()

        st.markdown(f"### {labels['overall_decision']}")
        col_app1, col_app2 = st.columns(2)
        with col_app1:
            if instrument['type'] == 'jbi':
                st.radio(labels['overall_decision'], [labels['include'], labels['exclude'], labels['seek_further_info'], labels['not_applicable']], key='overall_decision', horizontal=True)
            else:
                st.radio(labels['overall_decision'], [labels['include'], labels['exclude'], labels['seek_further_info']], key='overall_decision', horizontal=True)
        with col_app2:
            st.text_area(labels['overall_comments'], key='overall_comments')

    return responses
