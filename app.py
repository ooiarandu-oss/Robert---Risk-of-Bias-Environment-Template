"""
ROBERT — Risk of Bias and Evidence Review Template
Corrected single-file Streamlit app.

Main fixes included:
- English-first interface with flag-based language switch.
- Instrument items remain in English; Portuguese/Spanish translations are shown below items.
- Sidebar uses direct page buttons instead of a second Navigation dropdown.
- Risk of Bias and GRADE pages open their own layouts directly.
- Adds Risk of Bias traffic-light plot, Risk of Bias summary bar chart, and GRADE/CINeMA certainty heatmap.
- ROBINS-I and ROBINS-E now use a manual assessment workflow with preliminary considerations, domain judgments, direction of bias, suggested overall judgment, and manual override.
- Removes hard dependency on fpdf; PDF export uses matplotlib PdfPages, reducing Streamlit Cloud dependency errors.
"""

from __future__ import annotations

from io import BytesIO
from textwrap import wrap
from typing import Dict, List, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from matplotlib.backends.backend_pdf import PdfPages


st.set_page_config(
    page_title="ROBERT — Risk of Bias and Evidence Review Template",
    layout="wide",
    page_icon="🧾",
)


# -----------------------------------------------------------------------------
# Translation dictionaries: app interface changes by flag. Instrument items stay
# in English; item translations appear below the English wording.
# -----------------------------------------------------------------------------

LANGUAGES = {
    "en": {"flag": "🇬🇧", "label": "English"},
    "pt": {"flag": "🇧🇷", "label": "Português"},
    "es": {"flag": "🇪🇸", "label": "Español"},
}

T = {
    "en": {
        "subtitle": "Risk of Bias and Evidence Review Template",
        "home": "Home",
        "risk": "Risk of Bias",
        "grade": "GRADE",
        "agreement": "Reviewer agreement",
        "viz": "Data visualization",
        "builder": "Manual Table Builder",
        "about": "About",
        "welcome": "Welcome to ROBERT",
        "select_template": "Select a template below to begin a structured assessment.",
        "metadata": "Study metadata",
        "study_title": "Study title",
        "author_year": "Author/year",
        "reviewer": "Reviewer",
        "doi": "DOI",
        "record": "Record number",
        "assessment": "Assessment",
        "exports": "Exports",
        "download_pdf": "Download PDF report",
        "download_excel": "Download Excel",
        "download_csv": "Download CSV",
        "traffic": "Risk of Bias traffic-light plot",
        "summary": "Risk of Bias summary bar chart",
        "grade_heatmap": "GRADE/CINeMA certainty-of-evidence heatmap",
        "add_row": "Add row",
        "remove_row": "Remove row",
        "reset": "Reset",
        "translation_note": "Scale items are kept in the original language because verified translation and cultural adaptation studies were not identified.",
        "robins_manual_notice": "This ROBINS template supports manual risk-of-bias assessment. ROBERT does not replace the official ROBINS algorithm. Reviewers should use the official guidance documents when assigning final judgments.",
        "preliminary_considerations": "Preliminary considerations",
        "manual_domain_assessment": "Manual domain-level assessment",
        "suggested_overall": "Suggested overall judgment",
        "manual_override": "Manual override of overall judgment",
        "override_justification": "Justification for override",
        "direction_bias": "Predicted direction of bias",
        "notes": "Notes",
    },
    "pt": {
        "subtitle": "Template de Risco de Viés e Revisão de Evidências",
        "home": "Home",
        "risk": "Risco de Viés",
        "grade": "GRADE",
        "agreement": "Concordância entre avaliadores",
        "viz": "Visualização de dados",
        "builder": "Construtor manual de tabela",
        "about": "Sobre",
        "welcome": "Bem-vindo ao ROBERT",
        "select_template": "Selecione um modelo abaixo para iniciar uma avaliação estruturada.",
        "metadata": "Metadados do estudo",
        "study_title": "Título do estudo",
        "author_year": "Autor/ano",
        "reviewer": "Avaliador",
        "doi": "DOI",
        "record": "Número do registro",
        "assessment": "Avaliação",
        "exports": "Exportações",
        "download_pdf": "Baixar relatório PDF",
        "download_excel": "Baixar Excel",
        "download_csv": "Baixar CSV",
        "traffic": "Gráfico traffic-light de risco de viés",
        "summary": "Gráfico de barras resumido de risco de viés",
        "grade_heatmap": "Mapa de calor GRADE/CINeMA da certeza da evidência",
        "add_row": "Adicionar linha",
        "remove_row": "Remover linha",
        "reset": "Reiniciar",
        "translation_note": "Os itens das escalas foram mantidos no idioma original pela falta de trabalhos de tradução e adaptação cultural.",
        "robins_manual_notice": "Este modelo ROBINS apoia a avaliação manual do risco de viés. O ROBERT não substitui o algoritmo oficial do ROBINS. Os revisores devem consultar os documentos oficiais de orientação ao atribuir os julgamentos finais.",
        "preliminary_considerations": "Considerações preliminares",
        "manual_domain_assessment": "Avaliação manual por domínio",
        "suggested_overall": "Julgamento geral sugerido",
        "manual_override": "Sobrescrever manualmente o julgamento geral",
        "override_justification": "Justificativa para sobrescrita",
        "direction_bias": "Direção prevista do viés",
        "notes": "Notas",
    },
    "es": {
        "subtitle": "Plantilla de Riesgo de Sesgo y Revisión de Evidencia",
        "home": "Inicio",
        "risk": "Riesgo de sesgo",
        "grade": "GRADE",
        "agreement": "Acuerdo entre revisores",
        "viz": "Visualización de datos",
        "builder": "Constructor manual de tablas",
        "about": "Acerca de",
        "welcome": "Bienvenido a ROBERT",
        "select_template": "Seleccione una plantilla para iniciar una evaluación estructurada.",
        "metadata": "Metadatos del estudio",
        "study_title": "Título del estudio",
        "author_year": "Autor/año",
        "reviewer": "Revisor",
        "doi": "DOI",
        "record": "Número de registro",
        "assessment": "Evaluación",
        "exports": "Exportaciones",
        "download_pdf": "Descargar informe PDF",
        "download_excel": "Descargar Excel",
        "download_csv": "Descargar CSV",
        "traffic": "Gráfico traffic-light de riesgo de sesgo",
        "summary": "Gráfico de barras resumido de riesgo de sesgo",
        "grade_heatmap": "Mapa de calor GRADE/CINeMA de certeza de la evidencia",
        "add_row": "Añadir fila",
        "remove_row": "Eliminar fila",
        "reset": "Reiniciar",
        "translation_note": "Los ítems de las escalas se mantienen en el idioma original por falta de estudios verificados de traducción y adaptación cultural.",
        "robins_manual_notice": "Esta plantilla ROBINS apoya la evaluación manual del riesgo de sesgo. ROBERT no reemplaza el algoritmo oficial de ROBINS. Los revisores deben consultar los documentos oficiales de orientación al asignar los juicios finales.",
        "preliminary_considerations": "Consideraciones preliminares",
        "manual_domain_assessment": "Evaluación manual por dominio",
        "suggested_overall": "Juicio general sugerido",
        "manual_override": "Sobrescribir manualmente el juicio general",
        "override_justification": "Justificación de la sobrescritura",
        "direction_bias": "Dirección prevista del sesgo",
        "notes": "Notas",
    },
}

JUDGMENT_OPTIONS = ["Low", "Some concerns", "Moderate", "Serious", "Critical", "High", "No information", "Not applicable"]
CERTAINTY_OPTIONS = ["High", "Moderate", "Low", "Very low"]
DOMAIN_OPTIONS = [
    "D1 — Randomization process",
    "D2 — Deviations from intended interventions",
    "D3 — Missing outcome data",
    "D4 — Measurement of the outcome",
    "D5 — Selection of the reported result",
    "Overall",
]

REFERENCE_LIBRARY = {
    "rob2": "Sterne, J. A. C., Savović, J., Page, M. J., Elbers, R. G., Blencowe, N. S., Boutron, I., Cates, C. J., Cheng, H.-Y., Corbett, M. S., Eldridge, S. M., Emberson, J. R., Hernán, M. A., Hopewell, S., Hróbjartsson, A., Junqueira, D. R., Jüni, P., Kirkham, J. J., Lasserson, T., Li, T., ... Higgins, J. P. T. (2019). RoB 2: A revised tool for assessing risk of bias in randomised trials. BMJ, 366, l4898. https://doi.org/10.1136/bmj.l4898",
    "robins_i": "Sterne, J. A., Hernán, M. A., Reeves, B. C., Savović, J., Berkman, N. D., Viswanathan, M., Henry, D., Altman, D. G., Ansari, M. T., Boutron, I., Carpenter, J. R., Chan, A.-W., Churchill, R., Deeks, J. J., Hróbjartsson, A., Kirkham, J., Jüni, P., Loke, Y. K., Pigott, T. D., ... Higgins, J. P. T. (2016). ROBINS-I: A tool for assessing risk of bias in non-randomised studies of interventions. BMJ, 355, i4919. https://doi.org/10.1136/bmj.i4919",
    "robins_e": "Higgins, J. P. T., Morgan, R. L., Rooney, A. A., Taylor, K. W., Thayer, K. A., Silva, R. A., Lemeris, C., Akl, E. A., Bateson, T. F., Berkman, N. D., Glenn, B. S., Hróbjartsson, A., LaKind, J. S., McAleenan, A., Meerpohl, J. J., Nachman, R. M., Obbagy, J. E., O’Connor, A., Radke, E. G., ... Sterne, J. A. C. (2024). A tool to assess risk of bias in non-randomized follow-up studies of exposure effects (ROBINS-E). Environment International, 186, 108602. https://doi.org/10.1016/j.envint.2024.108602",
    "jbi_manual": "Aromataris, E., Lockwood, C., Porritt, K., Pilla, B., & Jordan, Z. (Eds.). (2024). JBI manual for evidence synthesis. JBI. https://synthesismanual.jbi.global",
    "jbi_cross": "Barker, T., Hasanoff, S., Aromataris, E., Stone, J. C., Leonardi-Bee, J., Sears, K., Klugar, M., Tufanaru, C., Moola, S., Liu, X.-L., & Munn, Z. (2026). The revised JBI critical appraisal tool for the assessment of risk of bias for analytical cross-sectional studies. JBI Evidence Synthesis, 24(3), 401–408. https://doi.org/10.11124/JBIES-24-00523",
    "nos": "Wells, G. A., Shea, B., O’Connell, D., Peterson, J., Welch, V., Losos, M., & Tugwell, P. (2000). The Newcastle-Ottawa Scale (NOS) for assessing the quality of nonrandomized studies in meta-analyses. Ottawa Hospital Research Institute. https://www.ohri.ca/programs/clinical_epidemiology/oxford.asp",
    "nos_cross": "Carra, M. C., Romandini, P., & Romandini, M. (2025). Risk of bias evaluation of cross-sectional studies: Adaptation of the Newcastle-Ottawa Scale. Journal of Periodontal Research. https://doi.org/10.1111/jre.13405",
    "downs_black": "Downs, S. H., & Black, N. (1998). The feasibility of creating a checklist for the assessment of the methodological quality both of randomised and non-randomised studies of health care interventions. Journal of Epidemiology and Community Health, 52(6), 377–384. https://doi.org/10.1136/jech.52.6.377",
}

INSTRUMENTS = {'rob2': {'family': 'RoB 2',
          'name': 'Cochrane RoB 2',
          'meta': 'Randomized trials · domain-level judgments',
          'type': 'rob',
          'reference': REFERENCE_LIBRARY["rob2"],
          'items': [{'domain': 'D1 — Randomization process',
                     'item_en': 'Bias arising from the randomization process.',
                     'pt': 'Viés decorrente do processo de randomização.',
                     'es': 'Sesgo derivado del proceso de aleatorización.'},
                    {'domain': 'D2 — Deviations from intended interventions',
                     'item_en': 'Bias due to deviations from intended interventions.',
                     'pt': 'Viés devido a desvios das intervenções pretendidas.',
                     'es': 'Sesgo debido a desviaciones de las intervenciones previstas.'},
                    {'domain': 'D3 — Missing outcome data',
                     'item_en': 'Bias due to missing outcome data.',
                     'pt': 'Viés devido a dados ausentes do desfecho.',
                     'es': 'Sesgo debido a datos faltantes del desenlace.'},
                    {'domain': 'D4 — Measurement of the outcome',
                     'item_en': 'Bias in measurement of the outcome.',
                     'pt': 'Viés na mensuração do desfecho.',
                     'es': 'Sesgo en la medición del desenlace.'},
                    {'domain': 'D5 — Selection of the reported result',
                     'item_en': 'Bias in selection of the reported result.',
                     'pt': 'Viés na seleção do resultado relatado.',
                     'es': 'Sesgo en la selección del resultado reportado.'}]},
 'robins_i': {'family': 'ROBINS',
              'name': 'ROBINS-I',
              'meta': 'Non-randomized studies of interventions · domain-level judgments',
              'type': 'robins',
              'translation_note': True,
              'reference': REFERENCE_LIBRARY["robins_i"],
              'items': [{'domain': 'Planning',
                         'item_en': 'List the important confounding factors relevant to all or most studies on this topic.',
                         'pt': 'Liste os fatores de confusão importantes relevantes para todos ou para a maioria dos estudos sobre este tema.',
                         'es': 'Enumere los factores de confusión importantes relevantes para todos o la mayoría de los estudios sobre este tema.'},
                        {'domain': 'Preliminary considerations',
                         'item_en': 'Specify the numerical result, outcome, intervention strategy, comparator strategy, and target trial being assessed.',
                         'pt': 'Especifique o resultado numérico, o desfecho, a estratégia de intervenção, a estratégia comparadora e o ensaio-alvo avaliado.',
                         'es': 'Especifique el resultado numérico, el desenlace, la estrategia de intervención, la estrategia comparadora y el ensayo objetivo '
                               'evaluado.'},
                        {'domain': 'D1 — Confounding',
                         'item_en': 'Bias due to confounding.',
                         'pt': 'Viés devido ao confundimento.',
                         'es': 'Sesgo debido a confusión.'},
                        {'domain': 'D2 — Selection of participants',
                         'item_en': 'Bias in selection of participants into the study or into the analysis.',
                         'pt': 'Viés na seleção de participantes para o estudo ou para a análise.',
                         'es': 'Sesgo en la selección de participantes para el estudio o el análisis.'},
                        {'domain': 'D3 — Classification of interventions',
                         'item_en': 'Bias in classification of interventions.',
                         'pt': 'Viés na classificação das intervenções.',
                         'es': 'Sesgo en la clasificación de las intervenciones.'},
                        {'domain': 'D4 — Deviations from intended interventions',
                         'item_en': 'Bias due to deviations from intended interventions.',
                         'pt': 'Viés devido a desvios das intervenções pretendidas.',
                         'es': 'Sesgo debido a desviaciones de las intervenciones previstas.'},
                        {'domain': 'D5 — Missing data',
                         'item_en': 'Bias due to missing data.',
                         'pt': 'Viés devido a dados ausentes.',
                         'es': 'Sesgo debido a datos faltantes.'},
                        {'domain': 'D6 — Measurement of outcomes',
                         'item_en': 'Bias in measurement of outcomes.',
                         'pt': 'Viés na mensuração dos desfechos.',
                         'es': 'Sesgo en la medición de los desenlaces.'},
                        {'domain': 'D7 — Selection of reported result',
                         'item_en': 'Bias in selection of the reported result.',
                         'pt': 'Viés na seleção do resultado relatado.',
                         'es': 'Sesgo en la selección del resultado reportado.'},
                        {'domain': 'Overall', 'item_en': 'Overall risk of bias.', 'pt': 'Risco geral de viés.', 'es': 'Riesgo general de sesgo.'}]},
 'robins_e': {'family': 'ROBINS',
              'name': 'ROBINS-E',
              'meta': 'Non-randomized studies of exposures · domain-level judgments',
              'type': 'robins',
              'translation_note': True,
              'reference': REFERENCE_LIBRARY["robins_e"],
              'items': [{'domain': 'Planning',
                         'item_en': 'List the important confounding factors and co-exposures relevant to the exposure-outcome relationship.',
                         'pt': 'Liste os fatores de confusão e coexposições importantes relevantes para a relação exposição-desfecho.',
                         'es': 'Enumere los factores de confusión y coexposiciones importantes para la relación exposición-desenlace.'},
                        {'domain': 'Preliminary considerations',
                         'item_en': 'Specify the exposure effect estimate, outcome, exposure definition, comparator, and eligible population.',
                         'pt': 'Especifique a estimativa de efeito da exposição, o desfecho, a definição da exposição, o comparador e a população elegível.',
                         'es': 'Especifique la estimación del efecto de la exposición, el desenlace, la definición de exposición, el comparador y la población '
                               'elegible.'},
                        {'domain': 'D1 — Confounding',
                         'item_en': 'Bias due to confounding.',
                         'pt': 'Viés devido ao confundimento.',
                         'es': 'Sesgo debido a confusión.'},
                        {'domain': 'D2 — Exposure measurement',
                         'item_en': 'Bias arising from measurement of the exposure.',
                         'pt': 'Viés decorrente da mensuração da exposição.',
                         'es': 'Sesgo derivado de la medición de la exposición.'},
                        {'domain': 'D3 — Selection of participants',
                         'item_en': 'Bias in selection of participants into the study or into the analysis.',
                         'pt': 'Viés na seleção de participantes para o estudo ou para a análise.',
                         'es': 'Sesgo en la selección de participantes para el estudio o el análisis.'},
                        {'domain': 'D4 — Post-exposure interventions',
                         'item_en': 'Bias due to post-exposure interventions.',
                         'pt': 'Viés devido a intervenções pós-exposição.',
                         'es': 'Sesgo debido a intervenciones posteriores a la exposición.'},
                        {'domain': 'D5 — Missing data',
                         'item_en': 'Bias due to missing data.',
                         'pt': 'Viés devido a dados ausentes.',
                         'es': 'Sesgo debido a datos faltantes.'},
                        {'domain': 'D6 — Outcome measurement',
                         'item_en': 'Bias in measurement of the outcome.',
                         'pt': 'Viés na mensuração do desfecho.',
                         'es': 'Sesgo en la medición del desenlace.'},
                        {'domain': 'D7 — Selection of reported result',
                         'item_en': 'Bias in selection of the reported result.',
                         'pt': 'Viés na seleção do resultado relatado.',
                         'es': 'Sesgo en la selección del resultado reportado.'},
                        {'domain': 'Overall', 'item_en': 'Overall risk of bias.', 'pt': 'Risco geral de viés.', 'es': 'Riesgo general de sesgo.'}]},
 'nos_case_control': {'family': 'Newcastle-Ottawa Scale',
                      'name': 'NOS Case-Control',
                      'meta': 'Case-control studies · star-based quality assessment',
                      'type': 'nos',
                      'translation_note': True,
                      'reference': REFERENCE_LIBRARY["nos"],
                      'items': [{'domain': 'Selection',
                                 'item_en': 'Is the case definition adequate? Options: independent validation; record linkage/self-report; no description.',
                                 'pt': 'A definição dos casos é adequada? Opções: validação independente; ligação de registros/autorrelato; sem descrição.',
                                 'es': '¿La definición de caso es adecuada? Opciones: validación independiente; enlace de registros/autoinforme; sin '
                                       'descripción.'},
                                {'domain': 'Selection',
                                 'item_en': 'Representativeness of the cases. Options: consecutive or representative series; potential selection bias or not '
                                            'stated.',
                                 'pt': 'Representatividade dos casos. Opções: série consecutiva ou representativa; potencial viés de seleção ou não informado.',
                                 'es': 'Representatividad de los casos. Opciones: serie consecutiva o representativa; potencial sesgo de selección o no '
                                       'informado.'},
                                {'domain': 'Selection',
                                 'item_en': 'Selection of controls. Options: community controls; hospital controls; no description.',
                                 'pt': 'Seleção dos controles. Opções: controles comunitários; controles hospitalares; sem descrição.',
                                 'es': 'Selección de controles. Opciones: controles comunitarios; controles hospitalarios; sin descripción.'},
                                {'domain': 'Selection',
                                 'item_en': 'Definition of controls. Options: no history of disease/endpoint; no description of source.',
                                 'pt': 'Definição dos controles. Opções: sem histórico da doença/desfecho; sem descrição da fonte.',
                                 'es': 'Definición de controles. Opciones: sin historia de enfermedad/desenlace; sin descripción de la fuente.'},
                                {'domain': 'Comparability',
                                 'item_en': 'Comparability of cases and controls on the basis of design or analysis; control for the most important factor and '
                                            'additional factors.',
                                 'pt': 'Comparabilidade de casos e controles com base no delineamento ou análise; controle do fator mais importante e de '
                                       'fatores adicionais.',
                                 'es': 'Comparabilidad de casos y controles según diseño o análisis; control del factor más importante y factores '
                                       'adicionales.'},
                                {'domain': 'Exposure',
                                 'item_en': 'Ascertainment of exposure. Options: secure record; blinded structured interview; non-blinded interview; '
                                            'self-report/medical record only; no description.',
                                 'pt': 'Verificação da exposição. Opções: registro seguro; entrevista estruturada cegada; entrevista não cegada; '
                                       'autorrelato/prontuário apenas; sem descrição.',
                                 'es': 'Determinación de la exposición. Opciones: registro seguro; entrevista estructurada cegada; entrevista no cegada; '
                                       'autoinforme/registro médico solamente; sin descripción.'},
                                {'domain': 'Exposure',
                                 'item_en': 'Same method of ascertainment for cases and controls.',
                                 'pt': 'Mesmo método de verificação para casos e controles.',
                                 'es': 'Mismo método de determinación para casos y controles.'},
                                {'domain': 'Exposure',
                                 'item_en': 'Non-response rate. Options: same rate for both groups; non-respondents described; different rate with no '
                                            'designation.',
                                 'pt': 'Taxa de não resposta. Opções: mesma taxa em ambos os grupos; não respondentes descritos; taxa diferente sem '
                                       'designação.',
                                 'es': 'Tasa de no respuesta. Opciones: misma tasa en ambos grupos; no respondientes descritos; tasa diferente sin '
                                       'designación.'}]},
 'nos_cohort': {'family': 'Newcastle-Ottawa Scale',
                'name': 'NOS Cohort',
                'meta': 'Cohort studies · star-based quality assessment',
                'type': 'nos',
                'translation_note': True,
                'reference': REFERENCE_LIBRARY["nos"],
                'items': [{'domain': 'Selection',
                           'item_en': 'Representativeness of the exposed cohort. Options: truly representative; somewhat representative; selected group; no '
                                      'description.',
                           'pt': 'Representatividade da coorte exposta. Opções: verdadeiramente representativa; parcialmente representativa; grupo '
                                 'selecionado; sem descrição.',
                           'es': 'Representatividad de la cohorte expuesta. Opciones: verdaderamente representativa; algo representativa; grupo seleccionado; '
                                 'sin descripción.'},
                          {'domain': 'Selection',
                           'item_en': 'Selection of the non-exposed cohort. Options: drawn from the same community; drawn from a different source; no '
                                      'description.',
                           'pt': 'Seleção da coorte não exposta. Opções: mesma comunidade; fonte diferente; sem descrição.',
                           'es': 'Selección de la cohorte no expuesta. Opciones: misma comunidad; fuente diferente; sin descripción.'},
                          {'domain': 'Selection',
                           'item_en': 'Ascertainment of exposure. Options: secure record; structured interview; written self-report; no description.',
                           'pt': 'Verificação da exposição. Opções: registro seguro; entrevista estruturada; autorrelato escrito; sem descrição.',
                           'es': 'Determinación de la exposición. Opciones: registro seguro; entrevista estructurada; autoinforme escrito; sin descripción.'},
                          {'domain': 'Selection',
                           'item_en': 'Demonstration that outcome of interest was not present at start of study.',
                           'pt': 'Demonstração de que o desfecho de interesse não estava presente no início do estudo.',
                           'es': 'Demostración de que el desenlace de interés no estaba presente al inicio del estudio.'},
                          {'domain': 'Comparability',
                           'item_en': 'Comparability of cohorts on the basis of design or analysis; control for the most important factor and additional '
                                      'factors.',
                           'pt': 'Comparabilidade das coortes com base no delineamento ou análise; controle do fator mais importante e de fatores adicionais.',
                           'es': 'Comparabilidad de cohortes según diseño o análisis; control del factor más importante y factores adicionales.'},
                          {'domain': 'Outcome',
                           'item_en': 'Assessment of outcome. Options: independent blind assessment; record linkage; self-report; no description.',
                           'pt': 'Avaliação do desfecho. Opções: avaliação independente cegada; ligação de registros; autorrelato; sem descrição.',
                           'es': 'Evaluación del desenlace. Opciones: evaluación independiente cegada; enlace de registros; autoinforme; sin descripción.'},
                          {'domain': 'Outcome',
                           'item_en': 'Was follow-up long enough for outcomes to occur?',
                           'pt': 'O seguimento foi longo o suficiente para que os desfechos ocorressem?',
                           'es': '¿El seguimiento fue suficientemente largo para que ocurrieran los desenlaces?'},
                          {'domain': 'Outcome',
                           'item_en': 'Adequacy of follow-up of cohorts. Options: complete follow-up; low risk from losses; inadequate follow-up; no '
                                      'statement.',
                           'pt': 'Adequação do seguimento das coortes. Opções: seguimento completo; baixo risco por perdas; seguimento inadequado; sem '
                                 'declaração.',
                           'es': 'Adecuación del seguimiento de cohortes. Opciones: seguimiento completo; bajo riesgo por pérdidas; seguimiento inadecuado; '
                                 'sin declaración.'}]},
 'nos_cross_sectional': {'family': 'Newcastle-Ottawa Scale',
                         'name': 'NOS Cross-sectional',
                         'meta': 'Cross-sectional studies · adapted NOS',
                         'type': 'nos',
                         'translation_note': True,
                         'reference': REFERENCE_LIBRARY["nos_cross"],
                         'items': [{'domain': 'Selection',
                                    'item_en': 'Representativeness of the sample. Options: truly representative; somewhat representative; selected/convenience '
                                               'sample; no description.',
                                    'pt': 'Representatividade da amostra. Opções: verdadeiramente representativa; parcialmente representativa; amostra '
                                          'selecionada/conveniência; sem descrição.',
                                    'es': 'Representatividad de la muestra. Opciones: verdaderamente representativa; algo representativa; muestra '
                                          'seleccionada/conveniencia; sin descripción.'},
                                   {'domain': 'Selection',
                                    'item_en': 'Sample size. Options: justified and satisfactory; not justified; no information.',
                                    'pt': 'Tamanho da amostra. Opções: justificado e satisfatório; não justificado; sem informação.',
                                    'es': 'Tamaño muestral. Opciones: justificado y satisfactorio; no justificado; sin información.'},
                                   {'domain': 'Selection',
                                    'item_en': 'Non-respondents or missing data. Options: acceptable recruitment/description; unsatisfactory rate; no '
                                               'information; appropriate missing-data methods.',
                                    'pt': 'Não respondentes ou dados ausentes. Opções: recrutamento/descrição aceitável; taxa insatisfatória; sem informação; '
                                          'métodos apropriados para dados ausentes.',
                                    'es': 'No respondientes o datos faltantes. Opciones: reclutamiento/descripción aceptable; tasa insatisfactoria; sin '
                                          'información; métodos apropiados para datos faltantes.'},
                                   {'domain': 'Selection',
                                    'item_en': 'Ascertainment of the exposure or risk factor.',
                                    'pt': 'Verificação da exposição ou fator de risco.',
                                    'es': 'Determinación de la exposición o factor de riesgo.'},
                                   {'domain': 'Comparability',
                                    'item_en': 'Comparability of subjects in different outcome groups on the basis of design or analysis; control for '
                                               'confounding factors.',
                                    'pt': 'Comparabilidade dos sujeitos em diferentes grupos de desfecho com base no delineamento ou análise; controle de '
                                          'fatores de confusão.',
                                    'es': 'Comparabilidad de sujetos en diferentes grupos de desenlace según diseño o análisis; control de factores de '
                                          'confusión.'},
                                   {'domain': 'Outcome',
                                    'item_en': 'Assessment of outcome.',
                                    'pt': 'Avaliação do desfecho.',
                                    'es': 'Evaluación del desenlace.'},
                                   {'domain': 'Outcome',
                                    'item_en': 'Statistical test. Options: clearly described, appropriate, and includes measures of association/precision; '
                                               'inappropriate or not described.',
                                    'pt': 'Teste estatístico. Opções: claramente descrito, apropriado e inclui medidas de associação/precisão; inadequado ou '
                                          'não descrito.',
                                    'es': 'Prueba estadística. Opciones: claramente descrita, apropiada e incluye medidas de asociación/precisión; inapropiada '
                                          'o no descrita.'}]},
 'jbi_cross': {'family': 'JBI',
               'name': 'JBI Cross-sectional',
               'meta': 'Analytical cross-sectional studies · 8 items',
               'type': 'jbi',
               'translation_note': True,
               'reference': REFERENCE_LIBRARY["jbi_cross"],
               'items': [{'domain': 'Sampling',
                          'item_en': 'Were the criteria for inclusion in the sample clearly defined?',
                          'pt': 'Os critérios de inclusão na amostra foram claramente definidos?',
                          'es': '¿Se definieron claramente los criterios de inclusión en la muestra?'},
                         {'domain': 'Participants and setting',
                          'item_en': 'Were the study subjects and the setting described in detail?',
                          'pt': 'Os participantes e o contexto do estudo foram descritos em detalhe?',
                          'es': '¿Se describieron con detalle los sujetos y el contexto del estudio?'},
                         {'domain': 'Exposure measurement',
                          'item_en': 'Was the exposure measured in a valid and reliable way?',
                          'pt': 'A exposição foi medida de forma válida e confiável?',
                          'es': '¿La exposición se midió de forma válida y fiable?'},
                         {'domain': 'Objective criteria',
                          'item_en': 'Were objective, standard criteria used for measurement of the condition?',
                          'pt': 'Foram usados critérios objetivos e padronizados para mensurar a condição?',
                          'es': '¿Se usaron criterios objetivos y estandarizados para medir la condición?'},
                         {'domain': 'Confounding',
                          'item_en': 'Were confounding factors identified?',
                          'pt': 'Os fatores de confusão foram identificados?',
                          'es': '¿Se identificaron los factores de confusión?'},
                         {'domain': 'Confounding strategies',
                          'item_en': 'Were strategies to deal with confounding factors stated?',
                          'pt': 'Foram declaradas estratégias para lidar com fatores de confusão?',
                          'es': '¿Se declararon estrategias para abordar factores de confusión?'},
                         {'domain': 'Outcome measurement',
                          'item_en': 'Were the outcomes measured in a valid and reliable way?',
                          'pt': 'Os desfechos foram medidos de forma válida e confiável?',
                          'es': '¿Los desenlaces se midieron de forma válida y fiable?'},
                         {'domain': 'Statistical analysis',
                          'item_en': 'Was appropriate statistical analysis used?',
                          'pt': 'Foi utilizada análise estatística apropriada?',
                          'es': '¿Se utilizó un análisis estadístico apropiado?'}]},
 'downs_black': {'family': 'Downs and Black',
                 'name': 'Downs and Black Checklist',
                 'meta': 'Healthcare interventions · randomized and non-randomized studies',
                 'type': 'score',
                 'translation_note': True,
                 'reference': REFERENCE_LIBRARY["downs_black"],
                 'items': [{'domain': 'Reporting',
                            'item_en': 'Is the hypothesis/aim/objective of the study clearly described?',
                            'pt': 'A hipótese/objetivo do estudo está claramente descrito?',
                            'es': '¿La hipótesis/objetivo del estudio está claramente descrito?'},
                           {'domain': 'Reporting',
                            'item_en': 'Are the main outcomes to be measured clearly described in the Introduction or Methods section?',
                            'pt': 'Os principais desfechos a serem medidos estão claramente descritos na Introdução ou Métodos?',
                            'es': '¿Los principales desenlaces que se medirán están claramente descritos en la Introducción o Métodos?'},
                           {'domain': 'Reporting',
                            'item_en': 'Are the characteristics of the patients included in the study clearly described?',
                            'pt': 'As características dos pacientes incluídos estão claramente descritas?',
                            'es': '¿Las características de los pacientes incluidos están claramente descritas?'},
                           {'domain': 'External validity',
                            'item_en': 'Were the subjects asked to participate in the study representative of the entire population from which they were '
                                       'recruited?',
                            'pt': 'Os participantes convidados eram representativos da população da qual foram recrutados?',
                            'es': '¿Los sujetos invitados eran representativos de la población de origen?'},
                           {'domain': 'External validity',
                            'item_en': 'Were those subjects who were prepared to participate representative of the entire population from which they were '
                                       'recruited?',
                            'pt': 'Os sujeitos que aceitaram participar eram representativos da população da qual foram recrutados?',
                            'es': '¿Los sujetos que aceptaron participar eran representativos de la población de origen?'},
                           {'domain': 'Internal validity — bias',
                            'item_en': 'Were the statistical tests used to assess the main outcomes appropriate?',
                            'pt': 'Os testes estatísticos usados para avaliar os principais desfechos foram apropriados?',
                            'es': '¿Las pruebas estadísticas utilizadas fueron apropiadas?'},
                           {'domain': 'Internal validity — confounding',
                            'item_en': 'Were the patients in different intervention groups recruited from the same population?',
                            'pt': 'Os pacientes dos diferentes grupos de intervenção foram recrutados da mesma população?',
                            'es': '¿Los pacientes de los diferentes grupos de intervención procedían de la misma población?'},
                           {'domain': 'Power',
                            'item_en': 'Did the study have sufficient power to detect a clinically important effect?',
                            'pt': 'O estudo teve poder suficiente para detectar um efeito clinicamente importante?',
                            'es': '¿El estudio tuvo potencia suficiente para detectar un efecto clínicamente importante?'}]}}


# -----------------------------------------------------------------------------
# CSS and layout helpers
# -----------------------------------------------------------------------------


def inject_custom_css() -> None:
    st.markdown(
        """
        <style>
        :root {
            --robert-primary: #111827;
            --robert-muted: #4B5563;
            --robert-border: #E5E7EB;
            --robert-green: #16A34A;
            --robert-yellow: #F59E0B;
            --robert-red: #DC2626;
            --robert-blue: #0EA5E9;
        }
        .block-container { padding-top: 2rem; padding-bottom: 3rem; }
        .robert-title { text-align:center; font-size:3rem; letter-spacing:0.04em; font-weight:800; color:var(--robert-primary); margin-bottom:0; }
        .robert-subtitle { text-align:center; font-size:1.25rem; font-weight:600; color:var(--robert-primary); margin-top:0.2rem; margin-bottom:2rem; }
        .instr-card { border:1px solid var(--robert-border); border-radius:16px; padding:18px; min-height:160px; background:white; }
        .instr-card-family { font-size:11px; letter-spacing:.08em; text-transform:uppercase; color:#9CA3AF; margin-bottom:8px; }
        .instr-card-name { font-size:17px; font-weight:800; color:#111827; margin-bottom:8px; }
        .instr-card-meta { font-size:13px; color:#4B5563; }
        .item-en { font-weight:700; color:#111827; margin-bottom:2px; }
        .item-translation { font-size:0.88rem; color:#6B7280; font-weight:400; margin-top:0; margin-bottom:0.5rem; }
        .small-note { font-size:0.88rem; color:#6B7280; }
        div[data-testid="stSidebar"] button { width:100%; justify-content:left; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def tr(key: str) -> str:
    lang = st.session_state.get("lang", "en")
    return T[lang].get(key, T["en"].get(key, key))


def header() -> None:
    st.markdown("<div class='robert-title'>ROBERT</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='robert-subtitle'>{tr('subtitle')}</div>", unsafe_allow_html=True)


def language_selector() -> str:
    if "lang" not in st.session_state:
        st.session_state.lang = "en"
    cols = st.sidebar.columns(3)
    for i, code in enumerate(["en", "es", "pt"]):
        with cols[i]:
            if st.button(LANGUAGES[code]["flag"], key=f"lang_{code}", help=LANGUAGES[code]["label"]):
                st.session_state.lang = code
                st.rerun()
    return st.session_state.lang


def sidebar_navigation() -> str:
    if "page" not in st.session_state:
        st.session_state.page = "home"
    pages = [
        ("home", f"🏠 {tr('home')}"),
        ("risk", f"🟥 {tr('risk')}"),
        ("grade", f"🟩 {tr('grade')}"),
        ("agreement", f"🤝 {tr('agreement')}"),
        ("viz", f"📊 {tr('viz')}"),
        ("builder", f"🧱 {tr('builder')}"),
        ("about", f"ℹ️ {tr('about')}"),
    ]
    for key, label in pages:
        button_type = "primary" if st.session_state.page == key else "secondary"
        if st.sidebar.button(label, key=f"nav_{key}", type=button_type):
            st.session_state.page = key
            st.rerun()
    return st.session_state.page


# -----------------------------------------------------------------------------
# Data and export helpers
# -----------------------------------------------------------------------------


def default_rob_df(instrument_id: str) -> pd.DataFrame:
    inst = INSTRUMENTS[instrument_id]
    rows = []
    for idx, item in enumerate(inst["items"], start=1):
        rows.append(
            {
                "Study": "",
                "Domain": item["domain"],
                "Item": f"{idx}. {item['item_en']}",
                "Judgment": "Some concerns",
                "Justification": "",
            }
        )
    return pd.DataFrame(rows)



def default_robins_manual_df(instrument_id: str) -> pd.DataFrame:
    """Manual ROBINS table: domain judgment + justification + direction + notes.

    This deliberately does not implement the full official conditional ROBINS
    algorithm. It documents the reviewer judgment transparently and exportably.
    """
    inst = INSTRUMENTS[instrument_id]
    rows = []
    for idx, item in enumerate(inst["items"], start=1):
        rows.append(
            {
                "Study": "",
                "Domain": item["domain"],
                "Item": f"{idx}. {item['item_en']}",
                "Judgment": "Moderate" if item["domain"] != "Overall" else "Moderate",
                "Support for judgment / Justification": "",
                "Predicted direction of bias": "Unpredictable / unclear",
                "Notes": "",
            }
        )
    return pd.DataFrame(rows)


def robins_preliminary_fields(instrument_id: str) -> pd.DataFrame:
    """Collect preliminary ROBINS fields as a one-row DataFrame."""
    is_exposure = instrument_id == "robins_e"
    left, right = st.columns(2)
    with left:
        result = st.text_area(
            "Numerical result being assessed" if not is_exposure else "Exposure effect estimate being assessed",
            key=f"{instrument_id}_prelim_result",
            height=80,
        )
        outcome = st.text_input("Outcome", key=f"{instrument_id}_prelim_outcome")
        population = st.text_input("Eligible population / participants", key=f"{instrument_id}_prelim_population")
        confounders = st.text_area(
            "Important confounding factors / co-exposures",
            key=f"{instrument_id}_prelim_confounders",
            height=90,
        )
    with right:
        exposure_or_intervention = st.text_input(
            "Intervention strategy" if not is_exposure else "Exposure definition",
            key=f"{instrument_id}_prelim_exposure_intervention",
        )
        comparator = st.text_input("Comparator strategy / comparator exposure level", key=f"{instrument_id}_prelim_comparator")
        target = st.text_area(
            "Target trial / target comparison description",
            key=f"{instrument_id}_prelim_target",
            height=80,
        )
        sources = st.multiselect(
            "Information sources used",
            [
                "Journal article(s)",
                "Study protocol",
                "Statistical analysis plan",
                "Trial/registry record",
                "Grey literature",
                "Conference abstract(s)",
                "Regulatory document",
                "Individual participant data",
                "Personal communication",
                "Other",
            ],
            key=f"{instrument_id}_prelim_sources",
        )
    effect_type = st.radio(
        "Effect being assessed",
        ["Intention-to-treat / assignment effect", "Per-protocol / adherence effect", "Exposure effect", "Not clear / not applicable"],
        horizontal=True,
        key=f"{instrument_id}_prelim_effect_type",
    )
    additional = st.text_area("Additional preliminary notes", key=f"{instrument_id}_prelim_additional", height=80)
    return pd.DataFrame(
        [
            {
                "Numerical result / effect estimate": result,
                "Outcome": outcome,
                "Eligible population / participants": population,
                "Intervention or exposure": exposure_or_intervention,
                "Comparator": comparator,
                "Target trial / target comparison": target,
                "Important confounding factors / co-exposures": confounders,
                "Information sources": "; ".join(sources),
                "Effect being assessed": effect_type,
                "Additional notes": additional,
            }
        ]
    )


def suggest_overall_robins_judgment(df: pd.DataFrame) -> str:
    """Conservative helper for an editable overall judgment.

    It is not the official ROBINS algorithm. It only applies a transparent hierarchy:
    Critical > Serious > Moderate/Some concerns > Low, ignoring Not applicable rows.
    """
    judgments = [normalize_judgment(x) for x in df.get("Judgment", [])]
    judgments = [j for j in judgments if j not in {"Not applicable", "No information"}]
    if any(j == "Critical" for j in judgments):
        return "Critical"
    if any(j == "Serious" for j in judgments):
        return "Serious"
    if any(j in {"Moderate", "Some concerns", "High"} for j in judgments):
        # High is uncommon in ROBINS, but preserve conservative behavior if selected.
        return "Moderate" if "High" not in judgments else "Serious"
    if judgments and all(j == "Low" for j in judgments):
        return "Low"
    return "No information"


def make_study_info(prefix: str) -> Dict[str, str]:
    cols = st.columns(5)
    with cols[0]:
        title = st.text_input(tr("study_title"), key=f"{prefix}_title")
    with cols[1]:
        author_year = st.text_input(tr("author_year"), key=f"{prefix}_author_year")
    with cols[2]:
        reviewer = st.text_input(tr("reviewer"), key=f"{prefix}_reviewer")
    with cols[3]:
        doi = st.text_input(tr("doi"), key=f"{prefix}_doi")
    with cols[4]:
        record = st.text_input(tr("record"), key=f"{prefix}_record")
    return {
        "Study title": title,
        "Author/year": author_year,
        "Reviewer": reviewer,
        "DOI": doi,
        "Record number": record,
    }


def dataframe_to_excel_bytes(sheets: Dict[str, pd.DataFrame]) -> bytes:
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        for sheet_name, df in sheets.items():
            df.to_excel(writer, index=False, sheet_name=sheet_name[:31])
    return output.getvalue()


def df_to_pdf_bytes(title: str, dataframes: List[Tuple[str, pd.DataFrame]], figures: List[Tuple[str, plt.Figure]] | None = None) -> bytes:
    output = BytesIO()
    with PdfPages(output) as pdf:
        for section_title, df in dataframes:
            fig, ax = plt.subplots(figsize=(11.69, 8.27))
            ax.axis("off")
            ax.set_title(section_title, fontsize=16, fontweight="bold", pad=20)
            safe_df = df.copy().astype(str).replace("nan", "")
            max_rows = min(len(safe_df), 18)
            display_df = safe_df.head(max_rows)
            wrapped = display_df.map(lambda x: "\n".join(wrap(str(x), 28)))
            table = ax.table(cellText=wrapped.values, colLabels=wrapped.columns, loc="center", cellLoc="left")
            table.auto_set_font_size(False)
            table.set_fontsize(7)
            table.scale(1, 1.6)
            pdf.savefig(fig, bbox_inches="tight")
            plt.close(fig)
        if figures:
            for fig_title, fig in figures:
                pdf.savefig(fig, bbox_inches="tight")
                plt.close(fig)
    return output.getvalue()


# -----------------------------------------------------------------------------
# Plot functions
# -----------------------------------------------------------------------------


def normalize_judgment(value: str) -> str:
    value = str(value).strip().lower()
    if value in {"low", "low risk", "yes", "y", "baixo", "bajo", "star", "star awarded"}:
        return "Low"
    if value in {"some concerns", "unclear", "u", "maybe", "algumas preocupações", "incierto", "unclear risk"}:
        return "Some concerns"
    if value in {"moderate", "moderate risk", "moderado"}:
        return "Moderate"
    if value in {"serious", "serious risk", "sério", "serio"}:
        return "Serious"
    if value in {"critical", "critical risk", "crítico", "critico"}:
        return "Critical"
    if value in {"high", "high risk", "no", "n", "alto", "no star"}:
        return "High"
    if value in {"not applicable", "na", "n/a"}:
        return "Not applicable"
    return "No information"


def judgment_color(label: str) -> str:
    return {
        "Low": "#2E7D32",
        "Some concerns": "#F9A825",
        "Moderate": "#F9A825",
        "Serious": "#EF6C00",
        "Critical": "#6A1B9A",
        "High": "#C62828",
        "No information": "#BDBDBD",
        "Not applicable": "#757575",
    }.get(label, "#BDBDBD")


def create_traffic_light_plot(df: pd.DataFrame, title: str = "Risk of Bias traffic-light plot") -> plt.Figure:
    plot_df = df.copy()
    plot_df["Judgment"] = plot_df["Judgment"].map(normalize_judgment)
    plot_df["Study"] = plot_df["Study"].replace("", np.nan).fillna("Study")
    pivot = plot_df.pivot_table(index="Study", columns="Domain", values="Judgment", aggfunc="first")
    if pivot.empty:
        pivot = pd.DataFrame({"Overall": ["No information"]}, index=["Study"])
    domains = list(pivot.columns)
    studies = list(pivot.index)

    fig, ax = plt.subplots(figsize=(max(8, len(domains) * 1.7), max(3.5, len(studies) * 0.55)))
    for y, study in enumerate(studies):
        for x, domain in enumerate(domains):
            judgment = pivot.loc[study, domain] if pd.notna(pivot.loc[study, domain]) else "No information"
            ax.scatter(x, y, s=450, color=judgment_color(judgment), edgecolor="black", linewidth=0.4)
            symbol = {"Low": "+", "Some concerns": "?", "Moderate": "M", "Serious": "S", "Critical": "C", "High": "−", "No information": "i", "Not applicable": "NA"}.get(judgment, "i")
            ax.text(x, y, symbol, va="center", ha="center", fontsize=9, fontweight="bold", color="white")
    ax.set_xticks(range(len(domains)))
    ax.set_xticklabels([d.replace(" — ", "\n") for d in domains], rotation=0, ha="center", fontsize=8)
    ax.set_yticks(range(len(studies)))
    ax.set_yticklabels(studies, fontsize=9)
    ax.invert_yaxis()
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.set_xlim(-0.7, len(domains) - 0.3)
    ax.set_ylim(len(studies) - 0.3, -0.7)
    ax.grid(axis="x", alpha=0.2)
    for spine in ax.spines.values():
        spine.set_visible(False)
    return fig


def create_rob_summary_plot(df: pd.DataFrame, title: str = "Risk of Bias summary bar chart") -> plt.Figure:
    plot_df = df.copy()
    plot_df["Judgment"] = plot_df["Judgment"].map(normalize_judgment)
    categories = ["Low", "Some concerns", "Moderate", "Serious", "Critical", "High", "No information", "Not applicable"]
    domains = list(plot_df["Domain"].dropna().unique()) or ["Overall"]
    counts = []
    for domain in domains:
        domain_df = plot_df[plot_df["Domain"] == domain]
        total = max(len(domain_df), 1)
        counts.append([(domain_df["Judgment"] == cat).sum() / total * 100 for cat in categories])
    counts = np.array(counts)

    fig, ax = plt.subplots(figsize=(10, max(3.5, len(domains) * 0.55)))
    left = np.zeros(len(domains))
    for i, cat in enumerate(categories):
        values = counts[:, i]
        ax.barh(domains, values, left=left, label=cat, color=judgment_color(cat))
        left += values
    ax.set_xlim(0, 100)
    ax.set_xlabel("%")
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.28), ncol=3, frameon=False)
    ax.invert_yaxis()
    for spine in ax.spines.values():
        spine.set_visible(False)
    return fig


def create_grade_heatmap(df: pd.DataFrame, title: str = "GRADE/CINeMA certainty-of-evidence heatmap") -> plt.Figure:
    heat_df = df.copy()
    domains = ["Risk of bias", "Inconsistency", "Indirectness", "Imprecision", "Publication bias", "Certainty"]
    for col in domains:
        if col not in heat_df.columns:
            heat_df[col] = "No concerns" if col != "Certainty" else "Moderate"
    rows = heat_df["Outcome"].replace("", np.nan).fillna("Outcome").tolist() or ["Outcome"]

    concern_map = {
        "No concerns": 0,
        "No serious limitations": 0,
        "Not serious": 0,
        "Some concerns": 1,
        "Serious": 1,
        "Major concerns": 2,
        "Very serious": 2,
        "High": 0,
        "Moderate": 1,
        "Low": 2,
        "Very low": 3,
    }
    color_map = {
        0: "#2E7D32",
        1: "#F9A825",
        2: "#EF6C00",
        3: "#C62828",
    }
    values = np.array([[concern_map.get(str(heat_df.loc[i, col]).strip(), 1) for col in domains] for i in heat_df.index])

    fig, ax = plt.subplots(figsize=(10, max(3.5, len(rows) * 0.5)))
    for y in range(values.shape[0]):
        for x in range(values.shape[1]):
            ax.add_patch(plt.Rectangle((x, y), 1, 1, facecolor=color_map[int(values[y, x])], edgecolor="white"))
            label = str(heat_df.iloc[y][domains[x]])
            ax.text(x + 0.5, y + 0.5, "\n".join(wrap(label, 14)), ha="center", va="center", color="white", fontsize=8, fontweight="bold")
    ax.set_xlim(0, len(domains))
    ax.set_ylim(0, len(rows))
    ax.set_xticks(np.arange(len(domains)) + 0.5)
    ax.set_xticklabels(domains, rotation=25, ha="right")
    ax.set_yticks(np.arange(len(rows)) + 0.5)
    ax.set_yticklabels(rows)
    ax.invert_yaxis()
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.axis("off")
    return fig


# -----------------------------------------------------------------------------
# Pages
# -----------------------------------------------------------------------------


def render_home_page() -> None:
    st.subheader(tr("welcome"))
    st.markdown(
        "ROBERT (Risk Of Bias Environment Template) is a project that aims to facilitate the application of risk of bias assessments using templates in a web interface."
    )
    st.markdown(
        "Here, researchers can use known tools for assessing risk of bias and evidence certainty. ROBERT provides templates for RoB 2, ROBINS-I, ROBINS-E, Newcastle-Ottawa Scale (case-control, cohort, and cross-sectional), JBI, Downs and Black, GRADE assessment, reviewer agreement, and evidence visualization."
    )
    st.markdown("### Data privacy note")
    st.markdown("ROBERT does not use a database. Data remain inside the active session and downloads are handled locally by the user.")


def render_instrument_cards() -> str:
    cols = st.columns(3)
    selected = st.session_state.get("selected_instrument", "rob2")
    for idx, (inst_id, inst) in enumerate(INSTRUMENTS.items()):
        with cols[idx % 3]:
            border = "#16A34A" if selected == inst_id else "#E5E7EB"
            st.markdown(
                f"""
                <div class='instr-card' style='border-color:{border};'>
                    <div class='instr-card-family'>{inst['family']}</div>
                    <div class='instr-card-name'>{inst['name']}</div>
                    <div class='instr-card-meta'>{inst['meta']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(f"Select {inst['name']}", key=f"select_{inst_id}", use_container_width=True):
                st.session_state.selected_instrument = inst_id
                st.session_state.rob_df = default_rob_df(inst_id)
                st.rerun()
    return st.session_state.get("selected_instrument", "rob2")




def render_robins_manual_page(inst: Dict, selected_id: str, study_info: Dict[str, str]) -> None:
    """Manual ROBINS-I / ROBINS-E workflow with preliminary considerations and override."""
    st.info(tr("robins_manual_notice"))

    st.markdown(f"### {tr('preliminary_considerations')}")
    preliminary_df = robins_preliminary_fields(selected_id)

    st.markdown(f"### {tr('manual_domain_assessment')}")
    if "robins_manual_df" not in st.session_state or st.session_state.get("robins_manual_instrument") != selected_id:
        st.session_state.robins_manual_df = default_robins_manual_df(selected_id)
        st.session_state.robins_manual_instrument = selected_id

    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button(f"➕ {tr('add_row')}", key=f"{selected_id}_manual_add", use_container_width=True):
            st.session_state.robins_manual_df.loc[len(st.session_state.robins_manual_df)] = {
                "Study": "",
                "Domain": "Overall",
                "Item": "",
                "Judgment": "Moderate",
                "Support for judgment / Justification": "",
                "Predicted direction of bias": "Unpredictable / unclear",
                "Notes": "",
            }
            st.rerun()
    with c2:
        if st.button(f"➖ {tr('remove_row')}", key=f"{selected_id}_manual_remove", use_container_width=True) and len(st.session_state.robins_manual_df) > 1:
            st.session_state.robins_manual_df = st.session_state.robins_manual_df.iloc[:-1]
            st.rerun()
    with c3:
        if st.button(tr("reset"), key=f"{selected_id}_manual_reset", use_container_width=True):
            st.session_state.robins_manual_df = default_robins_manual_df(selected_id)
            st.rerun()

    domain_options = sorted({i["domain"] for i in inst["items"]})
    st.session_state.robins_manual_df = st.data_editor(
        st.session_state.robins_manual_df,
        column_config={
            "Domain": st.column_config.SelectboxColumn("Domain", options=domain_options),
            "Judgment": st.column_config.SelectboxColumn(
                "Judgment",
                options=["Low", "Moderate", "Serious", "Critical", "No information", "Not applicable"],
            ),
            "Predicted direction of bias": st.column_config.SelectboxColumn(
                "Predicted direction of bias",
                options=[
                    "Favours intervention/exposure",
                    "Favours comparator",
                    "Away from the null",
                    "Toward the null",
                    "Unpredictable / unclear",
                    "Not applicable",
                ],
            ),
        },
        hide_index=True,
        use_container_width=True,
        height=420,
    )

    suggested = suggest_overall_robins_judgment(st.session_state.robins_manual_df)
    st.markdown(f"### {tr('suggested_overall')}")
    st.caption("Conservative helper only; this is not the official ROBINS algorithm.")
    st.success(suggested)

    override = st.selectbox(
        tr("manual_override"),
        ["Use suggested judgment", "Low", "Moderate", "Serious", "Critical", "No information"],
        key=f"{selected_id}_overall_override",
    )
    final_overall = suggested if override == "Use suggested judgment" else override
    override_reason = st.text_area(tr("override_justification"), key=f"{selected_id}_overall_override_reason", height=90)
    overall_df = pd.DataFrame(
        [
            {
                "Suggested overall judgment": suggested,
                "Final overall judgment": final_overall,
                "Override justification": override_reason,
            }
        ]
    )

    chart_df = st.session_state.robins_manual_df.rename(columns={"Support for judgment / Justification": "Justification"}).copy()
    st.markdown(f"### {tr('traffic')}")
    traffic_fig = create_traffic_light_plot(chart_df, tr("traffic"))
    st.pyplot(traffic_fig)

    st.markdown(f"### {tr('summary')}")
    summary_fig = create_rob_summary_plot(chart_df, tr("summary"))
    st.pyplot(summary_fig)

    st.markdown(f"### {tr('exports')}")
    c1, c2, c3 = st.columns(3)
    metadata_df = pd.DataFrame([study_info])
    with c1:
        st.download_button(
            tr("download_excel"),
            dataframe_to_excel_bytes(
                {
                    "Metadata": metadata_df,
                    "Preliminary considerations": preliminary_df,
                    "Manual ROBINS assessment": st.session_state.robins_manual_df,
                    "Overall judgment": overall_df,
                }
            ),
            file_name=f"ROBERT_{selected_id}_manual_assessment.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )
    with c2:
        export_csv = pd.concat(
            [
                preliminary_df.assign(Section="Preliminary considerations"),
                st.session_state.robins_manual_df.assign(Section="Manual domain assessment"),
                overall_df.assign(Section="Overall judgment"),
            ],
            ignore_index=True,
            sort=False,
        )
        st.download_button(
            tr("download_csv"),
            export_csv.to_csv(index=False).encode("utf-8"),
            file_name=f"ROBERT_{selected_id}_manual_assessment.csv",
            mime="text/csv",
            use_container_width=True,
        )
    with c3:
        pdf = df_to_pdf_bytes(
            f"ROBERT {inst['name']} Manual Assessment",
            [
                ("Metadata", metadata_df),
                ("Preliminary considerations", preliminary_df),
                ("Manual ROBINS assessment", st.session_state.robins_manual_df),
                ("Overall judgment", overall_df),
            ],
            [(tr("traffic"), traffic_fig), (tr("summary"), summary_fig)],
        )
        st.download_button(
            tr("download_pdf"),
            pdf,
            file_name=f"ROBERT_{selected_id}_manual_report.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

    with st.expander("Reference"):
        st.write(inst.get("reference", "Reference unavailable."))


def render_risk_of_bias_page() -> None:
    lang = st.session_state.get("lang", "en")
    st.subheader(tr("risk"))
    st.markdown(tr("select_template"))
    selected_id = render_instrument_cards()
    inst = INSTRUMENTS[selected_id]

    if lang != "en" and inst.get("translation_note"):
        st.warning(tr("translation_note"))

    st.divider()
    st.markdown(f"### {tr('metadata')}")
    study_info = make_study_info("rob")

    if inst.get("type") == "robins":
        render_robins_manual_page(inst, selected_id, study_info)
        return

    st.markdown(f"### {tr('assessment')}")
    for item in inst["items"]:
        st.markdown(f"<div class='item-en'>{item['item_en']}</div>", unsafe_allow_html=True)
        if lang != "en":
            st.markdown(f"<div class='item-translation'>{item.get(lang, '')}</div>", unsafe_allow_html=True)

    if "rob_df" not in st.session_state:
        st.session_state.rob_df = default_rob_df(selected_id)

    if st.session_state.get("rob_df_instrument") != selected_id:
        st.session_state.rob_df = default_rob_df(selected_id)
        st.session_state.rob_df_instrument = selected_id

    b1, b2, b3 = st.columns(3)
    with b1:
        if st.button(f"➕ {tr('add_row')}", use_container_width=True):
            st.session_state.rob_df.loc[len(st.session_state.rob_df)] = {"Study": "", "Domain": "Overall", "Item": "", "Judgment": "Some concerns", "Justification": ""}
            st.rerun()
    with b2:
        if st.button(f"➖ {tr('remove_row')}", use_container_width=True) and len(st.session_state.rob_df) > 1:
            st.session_state.rob_df = st.session_state.rob_df.iloc[:-1]
            st.rerun()
    with b3:
        if st.button(tr("reset"), use_container_width=True):
            st.session_state.rob_df = default_rob_df(selected_id)
            st.rerun()

    st.session_state.rob_df = st.data_editor(
        st.session_state.rob_df,
        column_config={
            "Domain": st.column_config.SelectboxColumn("Domain", options=DOMAIN_OPTIONS + sorted({i["domain"] for i in inst["items"]})),
            "Judgment": st.column_config.SelectboxColumn("Judgment", options=JUDGMENT_OPTIONS),
        },
        hide_index=True,
        use_container_width=True,
        height=360,
    )

    st.markdown(f"### {tr('traffic')}")
    traffic_fig = create_traffic_light_plot(st.session_state.rob_df, tr("traffic"))
    st.pyplot(traffic_fig)

    st.markdown(f"### {tr('summary')}")
    summary_fig = create_rob_summary_plot(st.session_state.rob_df, tr("summary"))
    st.pyplot(summary_fig)

    st.markdown(f"### {tr('exports')}")
    c1, c2, c3 = st.columns(3)
    report_df = pd.concat([pd.DataFrame([study_info]), st.session_state.rob_df], axis=0, ignore_index=True)
    with c1:
        st.download_button(tr("download_excel"), dataframe_to_excel_bytes({"Assessment": st.session_state.rob_df, "Metadata": pd.DataFrame([study_info])}), file_name="ROBERT_risk_of_bias.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
    with c2:
        st.download_button(tr("download_csv"), st.session_state.rob_df.to_csv(index=False).encode("utf-8"), file_name="ROBERT_risk_of_bias.csv", mime="text/csv", use_container_width=True)
    with c3:
        pdf = df_to_pdf_bytes("ROBERT Risk of Bias", [("Risk of Bias Assessment", report_df)], [(tr("traffic"), create_traffic_light_plot(st.session_state.rob_df, tr("traffic"))), (tr("summary"), create_rob_summary_plot(st.session_state.rob_df, tr("summary")))])
        st.download_button(tr("download_pdf"), pdf, file_name="ROBERT_risk_of_bias_report.pdf", mime="application/pdf", use_container_width=True)

    with st.expander("Reference"):
        st.write(inst.get("reference", "Reference unavailable."))


def default_grade_df() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "Outcome": "",
                "Number of studies": "",
                "Design": "Randomized controlled trial",
                "Risk of bias": "Some concerns",
                "Inconsistency": "Some concerns",
                "Indirectness": "Some concerns",
                "Imprecision": "Some concerns",
                "Publication bias": "Some concerns",
                "Participants — intervention": "",
                "Participants — comparator": "",
                "Relative effect (95% CI)": "",
                "Absolute effect": "",
                "Certainty": "Moderate",
                "Justification": "",
            }
        ]
    )


def render_grade_page() -> None:
    st.subheader(tr("grade"))
    st.markdown("Use the table below to summarize certainty of evidence across outcomes.")
    if "grade_df" not in st.session_state:
        st.session_state.grade_df = default_grade_df()

    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button(f"➕ {tr('add_row')}", key="grade_add", use_container_width=True):
            st.session_state.grade_df.loc[len(st.session_state.grade_df)] = {col: "" for col in st.session_state.grade_df.columns}
            st.rerun()
    with c2:
        if st.button(f"➖ {tr('remove_row')}", key="grade_remove", use_container_width=True) and len(st.session_state.grade_df) > 1:
            st.session_state.grade_df = st.session_state.grade_df.iloc[:-1]
            st.rerun()
    with c3:
        if st.button(tr("reset"), key="grade_reset", use_container_width=True):
            st.session_state.grade_df = default_grade_df()
            st.rerun()

    concern_options = ["No concerns", "Some concerns", "Major concerns", "No serious limitations", "Serious", "Very serious", "Not assessed", "Unclear"]
    st.session_state.grade_df = st.data_editor(
        st.session_state.grade_df,
        column_config={
            "Risk of bias": st.column_config.SelectboxColumn("Risk of bias", options=concern_options),
            "Inconsistency": st.column_config.SelectboxColumn("Inconsistency", options=concern_options),
            "Indirectness": st.column_config.SelectboxColumn("Indirectness", options=concern_options),
            "Imprecision": st.column_config.SelectboxColumn("Imprecision", options=concern_options),
            "Publication bias": st.column_config.SelectboxColumn("Publication bias", options=concern_options),
            "Certainty": st.column_config.SelectboxColumn("Certainty", options=CERTAINTY_OPTIONS),
        },
        hide_index=True,
        use_container_width=True,
        height=360,
    )

    st.markdown(f"### {tr('grade_heatmap')}")
    heatmap_fig = create_grade_heatmap(st.session_state.grade_df, tr("grade_heatmap"))
    st.pyplot(heatmap_fig)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.download_button(tr("download_excel"), dataframe_to_excel_bytes({"GRADE": st.session_state.grade_df}), file_name="ROBERT_GRADE.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
    with c2:
        st.download_button(tr("download_csv"), st.session_state.grade_df.to_csv(index=False).encode("utf-8"), file_name="ROBERT_GRADE.csv", mime="text/csv", use_container_width=True)
    with c3:
        pdf = df_to_pdf_bytes("ROBERT GRADE", [("GRADE Assessment", st.session_state.grade_df)], [(tr("grade_heatmap"), create_grade_heatmap(st.session_state.grade_df, tr("grade_heatmap")))])
        st.download_button(tr("download_pdf"), pdf, file_name="ROBERT_GRADE_report.pdf", mime="application/pdf", use_container_width=True)


def render_agreement_page() -> None:
    st.subheader(tr("agreement"))
    if "kappa_df" not in st.session_state:
        st.session_state.kappa_df = pd.DataFrame([{"Item": "", "Reviewer A": "", "Reviewer B": ""}])
    if "icc_df" not in st.session_state:
        st.session_state.icc_df = pd.DataFrame([{"Domain/scale": "", "Reviewer A total": "", "Reviewer B total": ""}])

    st.markdown("#### Cohen's Kappa")
    st.session_state.kappa_df = st.data_editor(st.session_state.kappa_df, hide_index=True, use_container_width=True, num_rows="dynamic")
    st.markdown("#### Intraclass Correlation Coefficient")
    st.session_state.icc_df = st.data_editor(st.session_state.icc_df, hide_index=True, use_container_width=True, num_rows="dynamic")

    if st.button("Calculate", use_container_width=True):
        kappa = calculate_kappa(st.session_state.kappa_df)
        icc = calculate_icc(st.session_state.icc_df)
        m1, m2 = st.columns(2)
        m1.metric("Cohen's Kappa", "NA" if kappa is None else f"{kappa:.3f}")
        m2.metric("ICC", "NA" if icc is None else f"{icc:.3f}")


def calculate_kappa(df: pd.DataFrame) -> float | None:
    pairs = [(str(r["Reviewer A"]).strip(), str(r["Reviewer B"]).strip()) for _, r in df.iterrows() if str(r.get("Reviewer A", "")).strip() and str(r.get("Reviewer B", "")).strip()]
    if not pairs:
        return None
    labels = sorted(set([x for pair in pairs for x in pair]))
    total = len(pairs)
    observed = sum(a == b for a, b in pairs) / total
    expected = sum((sum(a == lab for a, _ in pairs) / total) * (sum(b == lab for _, b in pairs) / total) for lab in labels)
    if expected == 1:
        return None
    return (observed - expected) / (1 - expected)


def calculate_icc(df: pd.DataFrame) -> float | None:
    pairs = []
    for _, r in df.iterrows():
        try:
            pairs.append((float(r["Reviewer A total"]), float(r["Reviewer B total"])))
        except Exception:
            continue
    if len(pairs) < 2:
        return None
    data = np.array(pairs, dtype=float)
    n, k = data.shape
    mean_targets = data.mean(axis=1)
    mean_raters = data.mean(axis=0)
    grand_mean = data.mean()
    ss_between = k * np.sum((mean_targets - grand_mean) ** 2)
    ss_rater = n * np.sum((mean_raters - grand_mean) ** 2)
    ss_total = np.sum((data - grand_mean) ** 2)
    ss_error = ss_total - ss_between - ss_rater
    ms_between = ss_between / (n - 1)
    ms_error = ss_error / ((n - 1) * (k - 1)) if (n - 1) * (k - 1) else 0
    denom = ms_between + (k - 1) * ms_error
    if denom == 0:
        return None
    return (ms_between - ms_error) / denom


def render_visualization_page() -> None:
    st.subheader(tr("viz"))
    st.markdown("Paste or build risk-of-bias/GRADE data, then use the charts below.")
    if "viz_df" not in st.session_state:
        st.session_state.viz_df = pd.DataFrame([{"Study": "", "Domain": "Overall", "Judgment": "Low", "Outcome": "", "Certainty": "High"}])
    st.session_state.viz_df = st.data_editor(
        st.session_state.viz_df,
        column_config={
            "Domain": st.column_config.SelectboxColumn("Domain", options=DOMAIN_OPTIONS),
            "Judgment": st.column_config.SelectboxColumn("Judgment", options=JUDGMENT_OPTIONS),
            "Certainty": st.column_config.SelectboxColumn("Certainty", options=CERTAINTY_OPTIONS),
        },
        num_rows="dynamic",
        hide_index=True,
        use_container_width=True,
        height=360,
    )
    st.pyplot(create_traffic_light_plot(st.session_state.viz_df, tr("traffic")))
    st.pyplot(create_rob_summary_plot(st.session_state.viz_df, tr("summary")))


def render_table_builder_page() -> None:
    st.subheader(tr("builder"))
    if "builder_df" not in st.session_state:
        st.session_state.builder_df = pd.DataFrame([{"Column 1": "", "Column 2": "", "Column 3": ""}])
    st.session_state.builder_df = st.data_editor(st.session_state.builder_df, num_rows="dynamic", hide_index=True, use_container_width=True)
    c1, c2 = st.columns(2)
    c1.download_button(tr("download_csv"), st.session_state.builder_df.to_csv(index=False).encode("utf-8"), file_name="ROBERT_manual_table.csv", mime="text/csv", use_container_width=True)
    c2.download_button(tr("download_excel"), dataframe_to_excel_bytes({"Table": st.session_state.builder_df}), file_name="ROBERT_manual_table.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)


def render_about_page() -> None:
    st.subheader("About ROBERT")
    st.markdown(
        f"""
ROBERT is a risk of bias and Evidence Review Template designed to support researchers in systematic assessments with structured reports and exports.

The application offers a range of tools for use. Most tools are for risk of bias analysis in reviews, but the application also includes the creation of the GRADE table. Reviewers can perform a statistical analysis of the consensus of their assessment. The data visualization section helps users submit their reports for chart creation.

All tools are authored by various researchers. Each report includes the appropriate reference for each tool. The creators of ROBERT do not hold intellectual property rights to any of these tools.

The ROBERT application is free and open to all users.

### Data privacy
ROBERT does not use a database. Data remain inside the active session and downloads are handled locally by the user.

### References

Guyatt, G. H., Oxman, A. D., Vist, G. E., Kunz, R., Falck-Ytter, Y., Alonso-Coello, P., & Schünemann, H. J. (2008a). GRADE: An emerging consensus on rating quality of evidence and strength of recommendations. *BMJ, 336*, 924–926. https://doi.org/10.1136/bmj.39489.470347.AD.

Guyatt, G. H., Oxman, A. D., Kunz, R., Falck-Ytter, Y., Vist, G. E., Liberati, A., & Schünemann, H. J. (2008b). GRADE: Going from evidence to recommendations. *BMJ, 336*, 1049–1051. https://doi.org/10.1136/bmj.39493.646875.AE.

Lunny, C., Pollock, M., McKenzie, J. E., Brennan, S. E., Pieper, D., & Tugwell, P. (2024). Assessing the methodological quality and risk of bias of systematic reviews: Primer for authors of overviews of systematic reviews. *BMJ Medicine, 3*(1), e000604. https://doi.org/10.1136/bmjmed-2023-000604.

### Instrument references

- RoB 2: {REFERENCE_LIBRARY["rob2"]}
- ROBINS-I: {REFERENCE_LIBRARY["robins_i"]}
- ROBINS-E: {REFERENCE_LIBRARY["robins_e"]}
- JBI Manual: {REFERENCE_LIBRARY["jbi_manual"]}
- JBI Cross-sectional: {REFERENCE_LIBRARY["jbi_cross"]}
- Newcastle-Ottawa Scale — Case-Control and Cohort: {REFERENCE_LIBRARY["nos"]}
- Newcastle-Ottawa Scale — Cross-sectional adaptation: {REFERENCE_LIBRARY["nos_cross"]}
- Downs and Black: {REFERENCE_LIBRARY["downs_black"]}

### Works that helped the development of ROBERT

Escaldelai, F. M. D., Escaldelai, L., & Bergamaschi, D. P. (2022). Sistema “Apoio à Revisão Sistemática”: Solução web para gerenciamento de duplicatas e seleção de artigos elegíveis. *Revista Brasileira de Epidemiologia, 25*, e220030. https://doi.org/10.1590/1980-549720220030.

Haddaway, N. R., Page, M. J., Pritchard, C. C., & McGuinness, L. A. (2022). PRISMA2020: An R package and Shiny app for producing PRISMA 2020-compliant flow diagrams. *Campbell Systematic Reviews, 18*(2), e1230. https://doi.org/10.1002/cl2.1230.

McGuinness, L. A., & Higgins, J. P. T. (2021). Risk-of-bias visualization (robvis): An R package and Shiny web app for visualizing risk-of-bias assessments. *Research Synthesis Methods, 12*(1), 55–61. https://doi.org/10.1002/jrsm.1411.

Motahari Nezhad, H., & CheshmehSohrabi, M. (2025). SPECTRUM SRA: An R Shiny application to automate systematic reviews using artificial intelligence and large language models. *Research Square*. https://doi.org/10.21203/rs.3.rs-7265470/v1.

Sahu, V. (2025). Critiplot: A Python package and web tool for visualizing specialized risk-of-bias assessments (NOS, ROBIS, GRADE, JBI, MMAT) in evidence synthesis. *OSF Preprints*. https://doi.org/10.31222/osf.io/8dtfq_v4.
        """
    )

def main() -> None:
    inject_custom_css()
    language_selector()
    page = sidebar_navigation()
    header()

    if page == "home":
        render_home_page()
    elif page == "risk":
        render_risk_of_bias_page()
    elif page == "grade":
        render_grade_page()
    elif page == "agreement":
        render_agreement_page()
    elif page == "viz":
        render_visualization_page()
    elif page == "builder":
        render_table_builder_page()
    elif page == "about":
        render_about_page()


if __name__ == "__main__":
    main()
