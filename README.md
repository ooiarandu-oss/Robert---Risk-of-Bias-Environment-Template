# Robert — Risk of Bias and Evidence Template

**Robert** is a free and modular Streamlit application designed to support risk-of-bias assessment, methodological appraisal, GRADE assessment, and structured reporting in evidence synthesis.

The app was developed to help researchers, reviewers, students, and health technology assessment teams document methodological judgments in a transparent, reproducible, and exportable format.

---

## Overview

Systematic reviews and health technology assessments require structured and transparent assessment of methodological quality, risk of bias, and certainty of evidence. However, this process is often performed manually using spreadsheets or text documents, which may increase the risk of transcription errors, inconsistent judgments, and loss of methodological justifications.

Robert was created as an open, no-database workflow for completing appraisal templates, documenting reviewer decisions, and exporting structured reports.

The application currently focuses on:

- Risk-of-bias and methodological appraisal templates;
- GRADE assessment tables;
- PDF report generation;
- Excel export;
- robvis Generic export;
- structured reviewer documentation;
- future reviewer agreement workflows.

---

## Features

### Risk of Bias Templates

Robert includes structured templates for:

- **RoB 2.0** — randomized controlled trials;
- **ROBINS-I** — non-randomized studies of interventions;
- **ROBINS-E** — non-randomized studies of exposures;
- **Newcastle-Ottawa Scale — Cohort studies**;
- **Newcastle-Ottawa Scale — Case-control studies**;
- **Newcastle-Ottawa Scale — Cross-sectional studies**;
- **Downs and Black Checklist**;
- **JBI Critical Appraisal Checklist for Case Reports**;
- **JBI Critical Appraisal Checklist for Case Series**;
- **JBI Critical Appraisal Checklist for Analytical Cross-Sectional Studies**.

Each template allows users to enter:

- study title;
- author and year;
- DOI;
- record number;
- reviewer name;
- item-level judgments;
- domain-level judgments, when applicable;
- notes and methodological justifications.

---

## GRADE Assessment

Robert includes a dynamic GRADE assessment table inspired by methodological guidance for evidence synthesis and health technology assessment.

The table supports the documentation of:

- outcome;
- number of studies;
- study design;
- methodological limitations / risk of bias;
- inconsistency;
- indirectness;
- imprecision;
- publication bias;
- participants in intervention and comparator groups;
- relative effect;
- absolute effect;
- final certainty of evidence;
- justification.

Rows can be added or removed dynamically.

---

## Export Options

Robert currently supports:

- **PDF reports**;
- **Excel files**;
- **CSV files**;
- **robvis Generic CSV export**;
- **instrument-specific structured reports**.

### Downs and Black PDF Report

The Downs and Black report includes:

- article metadata;
- evaluator information;
- total score;
- percentage score;
- methodological quality classification;
- risk-of-bias summary;
- section-level summary;
- tables separated by checklist domains;
- item-level notes and justifications;
- full reference to the original Downs and Black checklist.

### JBI PDF Report

The JBI reports include:

- checklist type;
- article metadata;
- reviewer and date;
- author, year, record number and DOI;
- item-level summary table;
- answers for each item;
- overall decision;
- reviewer comments;
- references.

---

## No Database Design

Robert does **not** store user data permanently.

All information is processed during the active Streamlit session and exported locally by the user. This design was chosen to:

- keep the app free;
- avoid the need for login or user authentication;
- reduce data privacy risks;
- simplify deployment;
- make the application suitable for Streamlit Community Cloud.

---

## Project Structure

A suggested structure is:

```text
Robert/
│
├── app.py
├── requirements.txt
│
├── templates_config/
│   ├── rob2_pt.py
│   ├── robins_i_pt.py
│   ├── robins_e_pt.py
│   ├── nos_case_control_pt.py
│   ├── nos_cohort_pt.py
│   ├── nos_cross_sectional_pt.py
│   ├── downs_black_pt.py
│   ├── jbi_case_report_pt.py
│   ├── jbi_case_series_pt.py
│   ├── jbi_cross_sectional_pt.py
│   └── grade_pt.py
│
├── utils/
│   ├── render_template.py
│   ├── scoring.py
│   ├── export_pdf.py
│   ├── export_excel.py
│   ├── export_robvis_generic.py
│   ├── export_critiplot.py
│   └── helpers.py
│
└── assets/
    └── references.json
