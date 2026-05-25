import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(
    page_title="ROBERT — Risk of Bias Environment Template",
    layout="wide",
    page_icon="📝",
)


def inject_custom_css():
    st.markdown(
        """
        <style>
        :root {
            --color-text-primary: #1F2937;
            --color-text-secondary: #4B5563;
            --color-text-tertiary: #9CA3AF;
            --color-background-primary: #ffffff;
            --color-background-secondary: #F3F4F6;
            --color-border-tertiary: #E5E7EB;
            --color-border-secondary: #D1D5DB;
            --border-radius-lg: 14px;
            --border-radius-md: 10px;
        }
        .main-header {
            color: #1D9E75;
            text-align: center;
            margin-bottom: 0.2rem;
            font-weight: bold;
        }
        .sub-header {
            text-align: center;
            color: #4B5563;
            margin-top: 0px;
            margin-bottom: 18px;
            font-size: 1rem;
        }
        .instr-card {
            border: 1px solid var(--color-border-tertiary);
            border-radius: var(--border-radius-lg);
            padding: 18px;
            background: var(--color-background-primary);
            transition: all 0.2s;
            min-height: 170px;
        }
        .instr-card:hover {
            border-color: #1D9E75;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
        }
        .instr-card-family {
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--color-text-tertiary);
            margin-bottom: 6px;
        }
        .instr-card-name {
            font-size: 16px;
            font-weight: 700;
            color: var(--color-text-primary);
            line-height: 1.3;
        }
        .instr-card-meta {
            font-size: 12px;
            color: var(--color-text-secondary);
            margin-top: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def main():
    inject_custom_css()

    st.markdown("<h1 class='main-header'>ROBERT</h1>", unsafe_allow_html=True)
    st.markdown("<h4 class='sub-header'>Risk of Bias Environment Template</h4>", unsafe_allow_html=True)

    page = st.sidebar.selectbox(
        "Navigation",
        [
            "Home",
            "Risk of Bias Templates",
            "GRADE Assessment",
            "Reviewer Agreement",
            "Data Visualization",
            "Manual Table Builder",
            "Portuguese Templates",
            "About",
        ],
        index=0,
    )

    if page == "Home":
        render_home_page()
    elif page == "Risk of Bias Templates":
        render_risk_of_bias_page(locale="en")
    elif page == "GRADE Assessment":
        render_grade_assessment_page()
    elif page == "Reviewer Agreement":
        render_reviewer_agreement_page()
    elif page == "Data Visualization":
        render_data_visualization_page()
    elif page == "Manual Table Builder":
        render_manual_table_builder_page()
    elif page == "Portuguese Templates":
        render_portuguese_templates_page()
    elif page == "About":
        render_about_page()


def render_home_page():
    st.subheader("Welcome to ROBERT")
    st.markdown(
        "ROBERT (Risk Of Bias Environment Template) is a project that aims to facilitate the application of risk of bias assessments using templates in a web interface."
    )
    st.markdown(
        "Here, researchers can use known tools for assessing risk of bias. Among them, ROBERT provides templates for:"
    )
    st.markdown(
        "- RoB 2.0: for randomized studies;"
        "\n- ROBINS series: for non-randomized intervention and exposure studies;"
        "\n- Newcastle-Ottawa series: for cohort, case-control, and cross-sectional studies;"
        "\n- JBI series: for case reports, case series, and cross-sectional studies;"
        "\n- Downs and Black: for randomized and non-randomized studies of healthcare interventions."
    )
    st.markdown(
        "ROBERT's goal is to facilitate the application of these instruments in research by providing structured reports based on the analysis performed."
    )
    st.markdown("\nThe ROBERT application also offers:")
    st.markdown(
        "- a GRADE assessment template for evaluating the certainty/quality of evidence;"
        "\n- calculation and reporting of Cohen's Kappa and the Intraclass Correlation Coefficient (ICC) for evaluating inter-reviewer agreement."
    )

    st.markdown("### How to use ROBERT:")
    st.markdown(
        "1. Select a risk-of-bias or methodological appraisal template."
        "\n2. Enter the study metadata."
        "\n3. Complete the item-level or domain-level assessment."
        "\n4. Add reviewer justifications when needed."
        "\n5. Export the PDF report and Excel/CSV files."
        "\n6. Use the Reviewer Agreement page to calculate Cohen's Kappa and ICC."
        "\n7. Use the visualization tools to create summary tables and plots."
    )

    st.markdown("### Data privacy note:")
    st.markdown("ROBERT does not use a database. Data are processed during the active session and downloaded locally by the user.")


def render_risk_of_bias_page(locale="en"):
    from templates_config import INSTRUMENTS
    from utils.render_template import render_instrument_form

    st.subheader("Risk of Bias Templates")
    st.markdown("Select a template below to begin a structured risk-of-bias assessment.")

    cols = st.columns(3)
    for idx, (inst_id, inst) in enumerate(INSTRUMENTS.items()):
        col = cols[idx % 3]
        with col:
            is_selected = st.session_state.get("selected_instrument_en") == inst_id
            border_color = "#1D9E75" if is_selected else "#E5E7EB"
            bg_color = "#E1F5EE" if is_selected else "#ffffff"
            st.markdown(
                f"""
                <div class='instr-card' style='border-color: {border_color}; background: {bg_color};'>
                    <div class='instr-card-family'>{inst['family']}</div>
                    <div class='instr-card-name'>{inst['name']}</div>
                    <div class='instr-card-meta'>{inst['meta']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(f"Select {inst['name']}", key=f"select_en_{inst_id}", use_container_width=True):
                st.session_state.selected_instrument_en = inst_id
                st.rerun()

    st.divider()
    if "selected_instrument_en" in st.session_state:
        selected_inst = INSTRUMENTS[st.session_state.selected_instrument_en]
        responses = render_instrument_form(selected_inst, locale="en")
        study_info = {
            "study_title": st.session_state.get("study_title", ""),
            "study_author_year": st.session_state.get("study_author_year", ""),
            "study_reviewer": st.session_state.get("study_reviewer", ""),
            "study_doi": st.session_state.get("study_doi", ""),
            "study_record": st.session_state.get("study_record", ""),
            "study_date": str(st.session_state.get("study_date", "")),
        }
        st.divider()
        st.markdown("### Export Reports")
        from utils.export_pdf import generate_pdf_report
        from utils.export_excel import generate_excel_report
        from utils.export_robvis_generic import generate_robvis_csv
        from utils.export_critiplot import generate_critiplot_csv

        e1, e2, e3, e4 = st.columns(4)
        with e1:
            pdf_data = generate_pdf_report(selected_inst, responses, study_info)
            st.download_button(
                "📄 Download PDF",
                pdf_data,
                file_name=f"{selected_inst['id']}_report.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
        with e2:
            excel_data = generate_excel_report(selected_inst, responses, study_info)
            st.download_button(
                "📊 Download Excel",
                excel_data,
                file_name=f"{selected_inst['id']}_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )
        with e3:
            robvis_data = generate_robvis_csv(selected_inst, responses, study_info["study_title"])
            st.download_button(
                "📈 Download robvis CSV",
                robvis_data,
                file_name=f"{selected_inst['id']}_robvis.csv",
                mime="text/csv",
                use_container_width=True,
            )
        if selected_inst["type"] in ["nos", "jbi"]:
            with e4:
                critiplot_data = generate_critiplot_csv(selected_inst, responses, study_info["study_title"])
                st.download_button(
                    "📉 Download critiplot CSV",
                    critiplot_data,
                    file_name=f"{selected_inst['id']}_critiplot.csv",
                    mime="text/csv",
                    use_container_width=True,
                )

        render_instrument_reference(selected_inst, locale="en")


def render_portuguese_templates_page():
    from templates_config import INSTRUMENTS
    from utils.render_template import render_instrument_form

    st.subheader("Portuguese Templates")
    st.markdown(
        "O ROBERT disponibiliza modelos em português quando há versões traduzidas ou adaptadas confiáveis."
    )
    st.markdown(
        "Para instrumentos sem tradução verificada, os itens permanecem no idioma original e uma nota metodológica é exibida."
    )

    cols = st.columns(3)
    for idx, (inst_id, inst) in enumerate(INSTRUMENTS.items()):
        col = cols[idx % 3]
        with col:
            is_selected = st.session_state.get("selected_instrument_pt") == inst_id
            border_color = "#1D9E75" if is_selected else "#E5E7EB"
            bg_color = "#E1F5EE" if is_selected else "#ffffff"
            st.markdown(
                f"""
                <div class='instr-card' style='border-color: {border_color}; background: {bg_color};'>
                    <div class='instr-card-family'>{inst['family']}</div>
                    <div class='instr-card-name'>{inst['name']}</div>
                    <div class='instr-card-meta'>{inst['meta']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(f"Selecionar {inst['name']}", key=f"select_pt_{inst_id}", use_container_width=True):
                st.session_state.selected_instrument_pt = inst_id
                st.rerun()

    st.divider()
    if "selected_instrument_pt" in st.session_state:
        selected_inst = INSTRUMENTS[st.session_state.selected_instrument_pt]
        if selected_inst.get("translation_note"):
            st.warning(selected_inst["translation_note"])

        responses = render_instrument_form(selected_inst, locale="pt")
        study_info = {
            "study_title": st.session_state.get("study_title", ""),
            "study_author_year": st.session_state.get("study_author_year", ""),
            "study_reviewer": st.session_state.get("study_reviewer", ""),
            "study_doi": st.session_state.get("study_doi", ""),
            "study_record": st.session_state.get("study_record", ""),
            "study_date": str(st.session_state.get("study_date", "")),
        }
        st.divider()
        st.markdown("### Exportar Relatórios")
        from utils.export_pdf import generate_pdf_report
        from utils.export_excel import generate_excel_report
        from utils.export_robvis_generic import generate_robvis_csv
        from utils.export_critiplot import generate_critiplot_csv

        e1, e2, e3, e4 = st.columns(4)
        with e1:
            pdf_data = generate_pdf_report(selected_inst, responses, study_info)
            st.download_button(
                "📄 Baixar PDF",
                pdf_data,
                file_name=f"{selected_inst['id']}_report.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
        with e2:
            excel_data = generate_excel_report(selected_inst, responses, study_info)
            st.download_button(
                "📊 Baixar Excel",
                excel_data,
                file_name=f"{selected_inst['id']}_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )
        with e3:
            robvis_data = generate_robvis_csv(selected_inst, responses, study_info["study_title"])
            st.download_button(
                "📈 Baixar robvis CSV",
                robvis_data,
                file_name=f"{selected_inst['id']}_robvis.csv",
                mime="text/csv",
                use_container_width=True,
            )
        if selected_inst["type"] in ["nos", "jbi"]:
            with e4:
                critiplot_data = generate_critiplot_csv(selected_inst, responses, study_info["study_title"])
                st.download_button(
                    "📉 Baixar critiplot CSV",
                    critiplot_data,
                    file_name=f"{selected_inst['id']}_critiplot.csv",
                    mime="text/csv",
                    use_container_width=True,
                )

        render_instrument_reference(selected_inst, locale="pt")


def render_grade_assessment_page():
    st.subheader("GRADE Assessment")
    st.markdown("Use the table below to summarize certainty of evidence across outcomes.")

    base_columns = [
        "Outcome",
        "Number of studies",
        "Design",
        "Risk of bias",
        "Inconsistency",
        "Indirectness",
        "Imprecision",
        "Publication bias",
        "Participants — intervention",
        "Participants — comparator",
        "Relative effect (95% CI)",
        "Absolute effect",
        "Certainty of evidence",
        "Justification",
    ]

    if "grade_df" not in st.session_state:
        st.session_state.grade_df = pd.DataFrame(columns=base_columns)
        st.session_state.grade_df.loc[0] = {col: "" for col in base_columns}

    t1, t2, t3, t4, t5, t6, t7 = st.columns([1.5, 1.5, 1.5, 1.5, 1, 1, 1])
    with t1:
        if st.button("➕ Add outcome", use_container_width=True):
            new_row = {col: "" for col in st.session_state.grade_df.columns}
            st.session_state.grade_df.loc[len(st.session_state.grade_df)] = new_row
            st.rerun()
    with t2:
        if st.button("➖ Remove outcome", use_container_width=True) and len(st.session_state.grade_df) > 1:
            st.session_state.grade_df = st.session_state.grade_df.iloc[:-1]
            st.rerun()
    with t3:
        if st.button("➕ Add study", use_container_width=True):
            col_name = f"Study {len([c for c in st.session_state.grade_df.columns if 'Study' in c]) + 1}"
            st.session_state.grade_df.insert(2, col_name, "")
            st.rerun()
    with t4:
        if st.button("➖ Remove study", use_container_width=True):
            study_cols = [c for c in st.session_state.grade_df.columns if c.startswith("Study")]
            if study_cols:
                st.session_state.grade_df.drop(columns=[study_cols[-1]], inplace=True)
                st.rerun()

    from utils.export_pdf import generate_grade_pdf
    from utils.export_excel import generate_grade_excel

    with t5:
        pdf_data = generate_grade_pdf(st.session_state.grade_df)
        st.download_button("📄 Download PDF", pdf_data, file_name="GRADE_assessment.pdf", mime="application/pdf", use_container_width=True)
    with t6:
        excel_data = generate_grade_excel(st.session_state.grade_df)
        st.download_button("📊 Download Excel", excel_data, file_name="GRADE_assessment.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
    with t7:
        csv_data = st.session_state.grade_df.to_csv(index=False).encode("utf-8")
        st.download_button("📈 Download CSV", csv_data, file_name="GRADE_assessment.csv", mime="text/csv", use_container_width=True)

    column_config = {
        "Design": st.column_config.SelectboxColumn(
            "Design",
            options=[
                "Randomized controlled trial",
                "Observational study",
                "Cohort",
                "Case-control",
                "Cross-sectional",
                "Case series",
                "Case report",
                "Systematic review",
            ],
        ),
        "Risk of bias": st.column_config.SelectboxColumn(
            "Risk of bias",
            options=["No serious limitations", "Serious", "Very serious", "Not assessed", "Unclear"],
        ),
        "Inconsistency": st.column_config.SelectboxColumn(
            "Inconsistency",
            options=["No serious limitations", "Serious", "Very serious", "Not assessed", "Unclear"],
        ),
        "Indirectness": st.column_config.SelectboxColumn(
            "Indirectness",
            options=["No serious limitations", "Serious", "Very serious", "Not assessed", "Unclear"],
        ),
        "Imprecision": st.column_config.SelectboxColumn(
            "Imprecision",
            options=["No serious limitations", "Serious", "Very serious", "Not assessed", "Unclear"],
        ),
        "Publication bias": st.column_config.SelectboxColumn(
            "Publication bias",
            options=["No serious limitations", "Serious", "Very serious", "Not assessed", "Unclear"],
        ),
        "Certainty of evidence": st.column_config.SelectboxColumn(
            "Certainty of evidence",
            options=["High", "Moderate", "Low", "Very low"],
        ),
    }

    st.session_state.grade_df = st.data_editor(
        st.session_state.grade_df,
        column_config=column_config,
        num_rows="fixed",
        use_container_width=True,
        hide_index=True,
        height=360,
    )


def render_reviewer_agreement_page():
    st.subheader("Reviewer Agreement")
    st.markdown("Use the tables below to capture reviewer decisions and calculate agreement metrics without relying on uploads.")

    if "kappa_df" not in st.session_state:
        st.session_state.kappa_df = pd.DataFrame([{"Item": "", "Reviewer A": "", "Reviewer B": ""}])
    if "icc_df" not in st.session_state:
        st.session_state.icc_df = pd.DataFrame([{"Scale or domain": "", "Reviewer A Total": "", "Reviewer B Total": ""}])

    c1, c2, c3, c4 = st.columns([1.5, 1.5, 1.5, 1])
    with c1:
        if st.button("➕ Add item row", use_container_width=True):
            st.session_state.kappa_df.loc[len(st.session_state.kappa_df)] = {col: "" for col in st.session_state.kappa_df.columns}
            st.rerun()
    with c2:
        if st.button("➖ Remove item row", use_container_width=True) and len(st.session_state.kappa_df) > 1:
            st.session_state.kappa_df = st.session_state.kappa_df.iloc[:-1]
            st.rerun()
    with c3:
        if st.button("➕ Add ICC row", use_container_width=True):
            st.session_state.icc_df.loc[len(st.session_state.icc_df)] = {col: "" for col in st.session_state.icc_df.columns}
            st.rerun()
    with c4:
        if st.button("Reset tables", use_container_width=True):
            st.session_state.kappa_df = pd.DataFrame([{"Item": "", "Reviewer A": "", "Reviewer B": ""}])
            st.session_state.icc_df = pd.DataFrame([{"Scale or domain": "", "Reviewer A Total": "", "Reviewer B Total": ""}])
            st.session_state.pop("kappa_result", None)
            st.session_state.pop("icc_result", None)
            st.rerun()

    st.markdown("#### Cohen’s Kappa — item-level agreement")
    st.session_state.kappa_df = st.data_editor(
        st.session_state.kappa_df,
        num_rows="fixed",
        use_container_width=True,
        hide_index=True,
        height=280,
    )

    st.markdown("#### ICC — total score agreement")
    st.session_state.icc_df = st.data_editor(
        st.session_state.icc_df,
        num_rows="fixed",
        use_container_width=True,
        hide_index=True,
        height=220,
    )

    if st.button("Calculate agreement", use_container_width=True):
        st.session_state.kappa_result = calculate_kappa(st.session_state.kappa_df)
        st.session_state.icc_result = calculate_icc(st.session_state.icc_df)

    result_cols = st.columns(2)
    with result_cols[0]:
        kappa_value = st.session_state.get("kappa_result")
        if kappa_value is not None:
            st.metric("Cohen’s Kappa", f"{kappa_value:.3f}")
        else:
            st.info("Enter matching categories for Reviewer A and Reviewer B to compute Kappa.")
    with result_cols[1]:
        icc_value = st.session_state.get("icc_result")
        if icc_value is not None:
            st.metric("ICC", f"{icc_value:.3f}")
        else:
            st.info("Enter at least two total score pairs to compute ICC.")

    download_data = pd.concat(
        [
            st.session_state.kappa_df.assign(Table="Kappa"),
            st.session_state.icc_df.assign(Table="ICC"),
        ],
        ignore_index=True,
    )
    csv_output = download_data.to_csv(index=False).encode("utf-8")
    st.download_button("Download Reviewer Agreement CSV", csv_output, file_name="reviewer_agreement.csv", mime="text/csv", use_container_width=True)


def calculate_kappa(df):
    pairs = []
    for _, row in df.iterrows():
        a = str(row.get("Reviewer A", "")).strip()
        b = str(row.get("Reviewer B", "")).strip()
        if a and b:
            pairs.append((a, b))
    if not pairs:
        return None
    total = len(pairs)
    a_counts = {}
    b_counts = {}
    agreement = 0
    labels = set()
    for a, b in pairs:
        a_counts[a] = a_counts.get(a, 0) + 1
        b_counts[b] = b_counts.get(b, 0) + 1
        labels.add(a)
        labels.add(b)
        if a == b:
            agreement += 1
    p0 = agreement / total
    pe = sum((a_counts.get(label, 0) / total) * (b_counts.get(label, 0) / total) for label in labels)
    if pe == 1:
        return None
    return (p0 - pe) / (1 - pe)


def calculate_icc(df):
    pairs = []
    for _, row in df.iterrows():
        a = row.get("Reviewer A Total", "")
        b = row.get("Reviewer B Total", "")
        try:
            a_val = float(a)
            b_val = float(b)
            pairs.append((a_val, b_val))
        except Exception:
            continue
    if len(pairs) < 2:
        return None
    n = len(pairs)
    mean_targets = [(a + b) / 2 for a, b in pairs]
    grand_mean = sum(a + b for a, b in pairs) / (2 * n)
    ss_between = 2 * sum((mt - grand_mean) ** 2 for mt in mean_targets)
    ss_within = sum((a - mt) ** 2 + (b - mt) ** 2 for (a, b), mt in zip(pairs, mean_targets))
    ms_between = ss_between / (n - 1)
    ms_within = ss_within / (n * (2 - 1))
    denom = ms_between + ms_within
    if denom == 0:
        return None
    return (ms_between - ms_within) / denom


def render_data_visualization_page():
    st.subheader("Data Visualization")
    st.markdown("Use the table below to create summary charts from your review categories.")

    if "viz_df" not in st.session_state:
        st.session_state.viz_df = pd.DataFrame(
            [{"Template / Domain": "", "Category": "", "Count": ""}]
        )

    c1, c2, c3 = st.columns([1.5, 1.5, 1])
    with c1:
        if st.button("➕ Add row", use_container_width=True):
            st.session_state.viz_df.loc[len(st.session_state.viz_df)] = {col: "" for col in st.session_state.viz_df.columns}
            st.rerun()
    with c2:
        if st.button("➖ Remove row", use_container_width=True) and len(st.session_state.viz_df) > 1:
            st.session_state.viz_df = st.session_state.viz_df.iloc[:-1]
            st.rerun()
    with c3:
        if st.button("Reset table", use_container_width=True):
            st.session_state.viz_df = pd.DataFrame(
                [{"Template / Domain": "", "Category": "", "Count": ""}]
            )
            st.rerun()

    st.session_state.viz_df = st.data_editor(
        st.session_state.viz_df,
        num_rows="fixed",
        use_container_width=True,
        hide_index=True,
        height=320,
    )

    summary = (
        st.session_state.viz_df.assign(Count=pd.to_numeric(st.session_state.viz_df["Count"], errors="coerce").fillna(0))
        .groupby("Category", dropna=False)["Count"]
        .sum()
        .reset_index()
    )

    if not summary.empty:
        st.markdown("### Summary chart")
        st.bar_chart(summary.set_index("Category"))

    st.download_button(
        "Download visualization CSV",
        st.session_state.viz_df.to_csv(index=False).encode("utf-8"),
        file_name="visualization_data.csv",
        mime="text/csv",
        use_container_width=True,
    )


def render_manual_table_builder_page():
    st.subheader("Manual Table Builder")
    st.markdown("Build and export a custom summary table for your review work.")

    if "builder_df" not in st.session_state:
        st.session_state.builder_df = pd.DataFrame(
            [{"Column 1": "", "Column 2": "", "Column 3": ""}]
        )

    c1, c2, c3 = st.columns([1.5, 1.5, 1])
    with c1:
        if st.button("➕ Add row", use_container_width=True):
            st.session_state.builder_df.loc[len(st.session_state.builder_df)] = {col: "" for col in st.session_state.builder_df.columns}
            st.rerun()
    with c2:
        if st.button("➖ Remove row", use_container_width=True) and len(st.session_state.builder_df) > 1:
            st.session_state.builder_df = st.session_state.builder_df.iloc[:-1]
            st.rerun()
    with c3:
        if st.button("Reset table", use_container_width=True):
            st.session_state.builder_df = pd.DataFrame(
                [{"Column 1": "", "Column 2": "", "Column 3": ""}]
            )
            st.rerun()

    st.session_state.builder_df = st.data_editor(
        st.session_state.builder_df,
        num_rows="fixed",
        use_container_width=True,
        hide_index=True,
        height=320,
    )

    st.download_button(
        "Download table CSV",
        st.session_state.builder_df.to_csv(index=False).encode("utf-8"),
        file_name="manual_table.csv",
        mime="text/csv",
        use_container_width=True,
    )
    with BytesIO() as buffer:
        st.session_state.builder_df.to_excel(buffer, index=False)
        st.download_button(
            "Download table Excel",
            buffer.getvalue(),
            file_name="manual_table.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )


def render_instrument_reference(instrument, locale="en"):
    title = "Reference" if locale == "en" else "Referência"
    with st.expander(title, expanded=False):
        st.write(instrument.get("reference", "Reference unavailable."))
        if locale == "pt" and instrument.get("translation_note"):
            st.markdown(f"**Nota metodológica:** {instrument['translation_note']}")


def render_about_page():
    st.subheader("About ROBERT")
    st.markdown("ROBERT is a risk of bias environment template designed to support researchers in systematic assessments with structured reports and exports.")
    st.markdown("The English version is the application’s main interface, with complete Risk of Bias Templates and GRADE Assessment modules.")
    st.markdown("### Data privacy")
    st.markdown("ROBERT does not use a database. Data remain inside the active session and downloads are handled locally by the user.")
    st.markdown("### References")
    st.markdown("The application includes references for each instrument on its template page. Portuguese templates show translation notes when original item wording is kept due to lack of verified cultural adaptation.")


if __name__ == "__main__":
    main()
