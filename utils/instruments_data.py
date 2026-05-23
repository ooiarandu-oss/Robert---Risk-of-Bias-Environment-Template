# utils/instruments_data.py

INSTRUMENTS = {
    'robins-i': {
        'title': 'ROBINS-I',
        'sub': '7 domínios de viés em estudos não-randomizados de intervenções',
        'exports': ['pdf', 'excel', 'robvis'],
        'items': [
            {'num': 'D1', 'domain': 'Pré-intervenção', 'text': 'Viés por confundimento'},
            {'num': 'D2', 'domain': 'Pré-intervenção', 'text': 'Viés na seleção dos participantes'},
            {'num': 'D3', 'domain': 'Na intervenção', 'text': 'Viés na classificação das intervenções'},
            {'num': 'D4', 'domain': 'Pós-intervenção', 'text': 'Viés por desvio das intervenções pretendidas'},
            {'num': 'D5', 'domain': 'Pós-intervenção', 'text': 'Viés por dados ausentes'},
            {'num': 'D6', 'domain': 'Pós-intervenção', 'text': 'Viés na mensuração dos desfechos'},
            {'num': 'D7', 'domain': 'Pós-intervenção', 'text': 'Viés na seleção dos resultados reportados'},
            {'num': 'OV', 'domain': 'Geral', 'text': 'Julgamento geral do risco de viés'},
        ]
    },
    'robins-e': {
        'title': 'ROBINS-E',
        'sub': '7 domínios de viés em estudos não-randomizados de exposições',
        'exports': ['pdf', 'excel', 'robvis'],
        'items': [
            {'num': 'D1', 'domain': 'Pré-exposição', 'text': 'Viés por confundimento'},
            {'num': 'D2', 'domain': 'Pré-exposição', 'text': 'Viés na seleção dos participantes'},
            {'num': 'D3', 'domain': 'Na exposição', 'text': 'Viés na classificação das exposições'},
            {'num': 'D4', 'domain': 'Pós-exposição', 'text': 'Viés por desvio das exposições pretendidas'},
            {'num': 'D5', 'domain': 'Pós-exposição', 'text': 'Viés por dados ausentes'},
            {'num': 'D6', 'domain': 'Pós-exposição', 'text': 'Viés na mensuração dos desfechos'},
            {'num': 'D7', 'domain': 'Pós-exposição', 'text': 'Viés na seleção dos resultados reportados'},
            {'num': 'OV', 'domain': 'Geral', 'text': 'Julgamento geral do risco de viés'},
        ]
    },
    'nos-cohort': {
        'title': 'NOS Cohort',
        'sub': 'Seleção · Comparabilidade · Desfecho — máx. 9 estrelas',
        'exports': ['pdf', 'excel', 'critiplot'],
        'items': [
            {'num': 'S1', 'domain': 'Seleção', 'text': 'Representatividade da coorte exposta'},
            {'num': 'S2', 'domain': 'Seleção', 'text': 'Seleção da coorte não exposta'},
            {'num': 'S3', 'domain': 'Seleção', 'text': 'Ascertamento da exposição'},
            {'num': 'S4', 'domain': 'Seleção', 'text': 'Ausência do desfecho de interesse no início do estudo'},
            {'num': 'C1', 'domain': 'Comparabilidade', 'text': 'Controle do fator de confundimento mais importante'},
            {'num': 'C2', 'domain': 'Comparabilidade', 'text': 'Controle de fator de confundimento adicional'},
            {'num': 'O1', 'domain': 'Desfecho', 'text': 'Avaliação do desfecho'},
            {'num': 'O2', 'domain': 'Desfecho', 'text': 'Duração de seguimento suficiente'},
            {'num': 'O3', 'domain': 'Desfecho', 'text': 'Adequação do seguimento das coortes'},
        ]
    },
    'nos-cc': {
        'title': 'NOS Case-control',
        'sub': 'Seleção · Comparabilidade · Exposição — máx. 9 estrelas',
        'exports': ['pdf', 'excel', 'critiplot'],
        'items': [
            {'num': 'S1', 'domain': 'Seleção', 'text': 'Definição adequada dos casos'},
            {'num': 'S2', 'domain': 'Seleção', 'text': 'Representatividade dos casos'},
            {'num': 'S3', 'domain': 'Seleção', 'text': 'Seleção dos controles'},
            {'num': 'S4', 'domain': 'Seleção', 'text': 'Definição dos controles'},
            {'num': 'C1', 'domain': 'Comparabilidade', 'text': 'Controle do fator de confundimento mais importante'},
            {'num': 'C2', 'domain': 'Comparabilidade', 'text': 'Controle de fator adicional'},
            {'num': 'E1', 'domain': 'Exposição', 'text': 'Ascertamento da exposição'},
            {'num': 'E2', 'domain': 'Exposição', 'text': 'Mesmo método de ascertamento para casos e controles'},
            {'num': 'E3', 'domain': 'Exposição', 'text': 'Taxa de não resposta'},
        ]
    },
    'nos-xs': {
        'title': 'NOS Cross-sectional',
        'sub': 'Seleção · Avaliação de exposição/desfecho · Confundimento — máx. 9 estrelas',
        'exports': ['pdf', 'excel', 'critiplot'],
        'items': [
            {'num': '1', 'domain': 'Seleção', 'text': 'A amostra é representativa da população de interesse?'},
            {'num': '2', 'domain': 'Seleção', 'text': 'Os não respondentes foram descritos adequadamente?'},
            {'num': '3', 'domain': 'Seleção', 'text': 'A exposição foi ascertada por registro seguro ou entrevista estruturada?'},
            {'num': '4', 'domain': 'Seleção', 'text': 'Os participantes foram recrutados em período definido e delimitado?'},
            {'num': '5', 'domain': 'Comparabilidade', 'text': 'O estudo controla o fator mais importante de confundimento?'},
            {'num': '6', 'domain': 'Comparabilidade', 'text': 'O estudo controla qualquer fator adicional de confundimento?'},
            {'num': '7', 'domain': 'Desfecho', 'text': 'O desfecho foi avaliado de forma válida e confiável?'},
            {'num': '8', 'domain': 'Desfecho', 'text': 'Os testes estatísticos utilizados para análise do desfecho foram adequados?'},
            {'num': '9', 'domain': 'Desfecho', 'text': 'A taxa de resposta foi adequada ou os não respondentes foram comparados aos respondentes?'},
        ]
    },
    'db': {
        'title': 'Downs & Black Checklist',
        'sub': 'Completude de relato · Validade interna · Validade externa · Poder — 27 itens, máx. 28 pts',
        'exports': ['pdf', 'excel', 'robvis'],
        'items': [
            {'num': 'R1–9', 'domain': 'Completude de relato', 'text': '9 itens: hipótese, desfechos, características dos participantes, intervenções, distribuição de confundidores, achados principais, medidas de variabilidade, eventos adversos, características de participantes perdidos'},
            {'num': 'VE1–3', 'domain': 'Validade externa', 'text': '3 itens: representatividade, critérios de inclusão/exclusão, período e local do estudo'},
            {'num': 'VI1–7', 'domain': 'Validade interna (viés)', 'text': '7 itens: cegamento de participantes, avaliadores, análise; conformidade com intervenções; desfechos confundidos por comorbidades; dados perdidos; análise por intenção de tratar'},
            {'num': 'VI8–13', 'domain': 'Validade interna (confundimento)', 'text': '6 itens: controle de confundimento, alocação aleatória, ocultação da alocação, características basais'},
            {'num': 'P27', 'domain': 'Poder estatístico', 'text': 'Cálculo amostral fornecido (0–5 pts; frequentemente modificado a 0/1)'},
        ]
    },
    'jbi-cr': {
        'title': 'JBI Case Report',
        'sub': '8 itens — características do paciente, condição clínica, intervenções, eventos adversos',
        'exports': ['pdf', 'excel', 'critiplot'],
        'items': [
            {'num': '1', 'domain': 'Paciente', 'text': 'As características demográficas do paciente foram claramente descritas?'},
            {'num': '2', 'domain': 'Paciente', 'text': 'A história do paciente foi claramente descrita e apresentada como linha do tempo?'},
            {'num': '3', 'domain': 'Clínico', 'text': 'A condição clínica atual do paciente na apresentação foi claramente descrita?'},
            {'num': '4', 'domain': 'Diagnóstico', 'text': 'Os testes diagnósticos ou métodos de avaliação e seus resultados foram claramente descritos?'},
            {'num': '5', 'domain': 'Intervenção', 'text': 'A(s) intervenção(ões) ou procedimento(s) de tratamento foi(ram) claramente descrita(s)?'},
            {'num': '6', 'domain': 'Intervenção', 'text': 'A condição clínica pós-intervenção foi claramente descrita?'},
            {'num': '7', 'domain': 'Segurança', 'text': 'Eventos adversos (danos) ou eventos não antecipados foram identificados e descritos?'},
            {'num': '8', 'domain': 'Aprendizado', 'text': 'O relato de caso fornece informações clínicas relevantes para prática ou pesquisa futuras?'},
        ]
    },
    'jbi-cs': {
        'title': 'JBI Case Series',
        'sub': '10 itens — critérios de inclusão, mensuração, inclusão consecutiva, relato',
        'exports': ['pdf', 'excel', 'critiplot'],
        'items': [
            {'num': '1', 'domain': 'Seleção', 'text': 'Havia critérios claros de inclusão na série de casos?'},
            {'num': '2', 'domain': 'Mensuração', 'text': 'A condição foi mensurada de forma padronizada e confiável em todos os participantes?'},
            {'num': '3', 'domain': 'Mensuração', 'text': 'Métodos válidos foram utilizados para identificação da condição em todos os participantes?'},
            {'num': '4', 'domain': 'Seleção', 'text': 'A série de casos teve inclusão consecutiva dos participantes?'},
            {'num': '5', 'domain': 'Seleção', 'text': 'A série de casos teve inclusão completa dos participantes?'},
            {'num': '6', 'domain': 'Relato', 'text': 'Houve relato claro das características demográficas dos participantes?'},
            {'num': '7', 'domain': 'Relato', 'text': 'Houve relato claro de informações clínicas dos participantes?'},
            {'num': '8', 'domain': 'Desfecho', 'text': 'Os desfechos ou resultados de seguimento dos casos foram claramente relatados?'},
            {'num': '9', 'domain': 'Relato', 'text': 'Houve relato claro de informações sobre o local/clínica do estudo?'},
            {'num': '10', 'domain': 'Análise', 'text': 'As análises estatísticas foram adequadas?'},
        ]
    },
    'jbi-xs': {
        'title': 'JBI Cross-sectional',
        'sub': '8 itens — critérios de inclusão, amostra, exposição, desfecho, confundimento',
        'exports': ['pdf', 'excel', 'critiplot'],
        'items': [
            {'num': '1', 'domain': 'Seleção', 'text': 'Os critérios de inclusão na amostra foram claramente definidos?'},
            {'num': '2', 'domain': 'Seleção', 'text': 'Os sujeitos do estudo e o contexto foram descritos em detalhes suficientes?'},
            {'num': '3', 'domain': 'Exposição', 'text': 'A exposição foi mensurada de forma válida e confiável?'},
            {'num': '4', 'domain': 'Desfecho', 'text': 'Foram utilizados critérios objetivos e padronizados para mensuração da condição?'},
            {'num': '5', 'domain': 'Confundimento', 'text': 'Os fatores de confundimento foram identificados?'},
            {'num': '6', 'domain': 'Confundimento', 'text': 'Estratégias para lidar com fatores de confundimento foram declaradas?'},
            {'num': '7', 'domain': 'Desfecho', 'text': 'Os desfechos foram mensurados de forma válida e confiável?'},
            {'num': '8', 'domain': 'Análise', 'text': 'Foram utilizadas análises estatísticas apropriadas?'},
        ]
    },
}
