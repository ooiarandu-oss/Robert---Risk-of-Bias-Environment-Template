ROB2 = {
    "language": "pt",
    "items_language": "pt",
    "translation_note": None,
    "reference": "Sterne JAC, Savović J, Page MJ, Elbers RG, Blencowe NS, Boutron I, et al. RoB 2: A revised tool for assessing risk of bias in randomized trials.",
    "id": "rob2",
    "family": "RoB 2",
    "name": "RoB 2.0",
    "meta": "Ensaios clínicos randomizados",
    "type": "rob",
    "domains": [
        {"num": "1", "name": "Viés decorrente do processo de randomização", "signaling_questions": [
            {"num": "1.1", "text": "A sequência de alocação dos participantes foi aleatória?"},
            {"num": "1.2", "text": "Foi mantido o sigilo de alocação dos participantes até eles serem recrutados e alocados para as intervenções?"},
            {"num": "1.3", "text": "As diferenças na linha de base entre os grupos de intervenção sugeriram problema com o processo de randomização?"}
        ]},
        {"num": "2", "name": "Viés devido a desvios das intervenções pretendidas", "signaling_questions": []},
        {"num": "3", "name": "Viés devido a dados ausentes dos desfechos", "signaling_questions": []},
        {"num": "4", "name": "Viés na mensuração do desfecho", "signaling_questions": []},
        {"num": "5", "name": "Viés na seleção do resultado relatado", "signaling_questions": []},
        {"num": "6", "name": "Julgamento geral", "signaling_questions": []}
    ],
    "options": ["Sim", "Parcialmente sim", "Parcialmente não", "Não", "Nenhuma informação", "Não aplicável"],
    "judgements": ["Baixo risco", "Algumas preocupações", "Alto risco"]
}
