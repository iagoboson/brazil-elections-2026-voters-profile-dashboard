import pandas as pd
from pathlib import Path
import plotly.express as px
import streamlit as st


# PAGE CONFIGURATION

st.set_page_config(
    page_title="Brazil Elections 2026",
    page_icon="🗳️",
    layout="wide",
)


# LANGUAGE

language = st.sidebar.selectbox(
    "Language / Idioma",
    options=["English", "Português"],
    index=0,
)

lang = "en" if language == "English" else "pt"


TEXT = {
    "en": {
        "title": "Brazil Elections 2026",
        "subtitle": "Electorate Profile",
        "filters": "Filters",
        "state": "State",
        "all": "All",
        "no_data": "No data matches the selected filters.",
        "voters": "Registered voters",
        "biometry": "Biometric coverage",
        "disability": "Voters with disabilities",
        "social_name": "Social name registrations",
        "quilombola": "Quilombola voters",
        "libras": "Libras interpreters",
        "zone": "Electoral zone",
        "gender": "Gender",
        "marital_status": "Marital status",
        "age": "Age group",
        "education": "Education",
        "race": "Race/Color",
        "gender_identity": "Gender identity",
        "gender_chart": "Electorate by Gender",
        "age_chart": "Age Distribution",
        "education_chart": "Education Distribution",
        "race_chart": "Electorate by Race/Color",
        "marital_chart": "Electorate by Marital Status",
        "identity_chart": "Electorate by Gender Identity",
        "voter_axis": "Voters",
    },
    "pt": {
        "title": "Eleições Brasil 2026",
        "subtitle": "Perfil do Eleitorado",
        "filters": "Filtros",
        "state": "Estado",
        "all": "Todos",
        "no_data": "Nenhum dado corresponde aos filtros selecionados.",
        "voters": "Eleitores registrados",
        "biometry": "Cobertura biométrica",
        "disability": "Eleitores com deficiência",
        "social_name": "Cadastros com nome social",
        "quilombola": "Eleitores quilombolas",
        "libras": "Intérpretes de Libras",
        "zone": "Zona eleitoral",
        "gender": "Gênero",
        "marital_status": "Estado civil",
        "age": "Faixa etária",
        "education": "Escolaridade",
        "race": "Raça/Cor",
        "gender_identity": "Identidade de gênero",
        "gender_chart": "Eleitorado por gênero",
        "age_chart": "Distribuição por idade",
        "education_chart": "Distribuição por escolaridade",
        "race_chart": "Eleitorado por raça/cor",
        "marital_chart": "Eleitorado por estado civil",
        "identity_chart": "Eleitorado por identidade de gênero",
        "voter_axis": "Eleitores",
    },
}


def t(key):
    return TEXT[lang][key]

def add_percentage(data):
    data = data.copy()

    data["Percentage"] = (
        data["QT_ELEITORES"]
        / data["QT_ELEITORES"].sum()
        * 100
    )

    return data

VALUE_TRANSLATIONS_EN = {
    "FEMININO": "Female",
    "MASCULINO": "Male",
    "NÃO INFORMADO": "Not informed",
    "SOLTEIRO": "Single",
    "CASADO": "Married",
    "DIVORCIADO": "Divorced",
    "VIÚVO": "Widowed",
    "SEPARADO JUDICIALMENTE": "Legally separated",
    "ANALFABETO": "Illiterate",
    "LÊ E ESCREVE": "Literate without formal education",
    "ENSINO FUNDAMENTAL INCOMPLETO": "Incomplete elementary education",
    "ENSINO FUNDAMENTAL COMPLETO": "Elementary education",
    "ENSINO MÉDIO INCOMPLETO": "Incomplete high school",
    "ENSINO MÉDIO COMPLETO": "High school",
    "SUPERIOR INCOMPLETO": "Incomplete higher education",
    "SUPERIOR COMPLETO": "Higher education",
    "Branca": "White",
    "Preta": "Black",
    "Parda": "Brown (Parda)",
    "Amarela": "Asian",
    "Indígena": "Indigenous",
    "Cisgênero": "Cisgender",
    "Transgênero": "Transgender",
    "Prefere não informar": "Prefers not to answer",
    "SIM": "Yes",
    "NÃO": "No",
    "Inválida": "Invalid",
}


def display_value(value):
    if lang == "pt":
        return str(value)

    value = str(value)

    if value in VALUE_TRANSLATIONS_EN:
        return VALUE_TRANSLATIONS_EN[value]

    if value == "100 anos ou mais":
        return "100 years or older"

    if value.endswith(" anos"):
        return (
            value.replace(" a ", "–")
            .replace(" anos", " years")
        )

    return value


def format_integer(value):
    formatted = f"{int(value):,}"

    if lang == "pt":
        return formatted.replace(",", ".")

    return formatted


# STATE SELECTION

UF_OPTIONS = [
    "BR", "AC", "AL", "AM", "AP", "BA", "CE", "DF", "ES",
    "GO", "MA", "MG", "MS", "MT", "PA", "PB", "PE",
    "PI", "PR", "RJ", "RN", "RO", "RR", "RS", "SC",
    "SE", "SP", "TO", "ZZ",
]

st.sidebar.header(t("filters"))

selected_uf = st.sidebar.selectbox(
    t("state"),
    options=UF_OPTIONS,
    index=UF_OPTIONS.index("DF"),
)


# DATA LOADING

@st.cache_data
def load_data(uf):
    data_dir = Path("processed")

    if uf == "BR":
        files = sorted(data_dir.glob("electorate_??_2026.parquet"))
        return pd.concat(
            [pd.read_parquet(file) for file in files],
            ignore_index=True,
        )

    return pd.read_parquet(
        data_dir / f"electorate_{uf}_2026.parquet"
    )


df = load_data(selected_uf)


# FILTERS

filter_columns = {
    t("zone"): "NR_ZONA",
    t("gender"): "DS_GENERO",
    t("marital_status"): "DS_ESTADO_CIVIL",
    t("age"): "DS_FAIXA_ETARIA",
    t("education"): "DS_GRAU_ESCOLARIDADE",
    t("race"): "DS_RACA_COR",
    t("gender_identity"): "DS_IDENTIDADE_GENERO",
    t("quilombola"): "DS_QUILOMBOLA",
    t("libras"): "DS_INTERPRETE_LIBRAS",
}

filtered_df = df.copy()

for label, column in filter_columns.items():
    if column not in df.columns:
        continue

    options = sorted(df[column].dropna().unique())

    selected = st.sidebar.multiselect(
        label,
        options=options,
        default=[],
        placeholder=t("all"),
        format_func=display_value,
    )

    if selected:
        filtered_df = filtered_df[
            filtered_df[column].isin(selected)
        ]


if filtered_df.empty:
    st.warning(t("no_data"))
    st.stop()

df = filtered_df


# TITLE

region = selected_uf

if selected_uf == "BR":
    region = "Brazil" if lang == "en" else "Brasil"
elif selected_uf == "ZZ":
    region = "Abroad" if lang == "en" else "Exterior"

st.title(t("title"))
st.subheader(f"{t('subtitle')} — {region}")


# KPIs

total = df["QT_ELEITORES"].sum()

biometric_rate = (
    df["QT_ELEITORES_BIOMETRIA"].sum() / total
)

disability_rate = (
    df["QT_ELEITORES_DEFICIENCIA"].sum() / total
)

social_name = df["QT_ELEITORES_NOME_SOCIAL"].sum()

quilombola = df.loc[
    df["DS_QUILOMBOLA"] == "SIM",
    "QT_ELEITORES",
].sum()

libras_interpreters = df.loc[
    df["DS_INTERPRETE_LIBRAS"] == "SIM",
    "QT_ELEITORES",
].sum()


kpi1, kpi2, kpi3, kpi4 = st.columns(4)

kpi1.metric(t("voters"), format_integer(total))
kpi2.metric(t("biometry"), f"{biometric_rate:.1%}")
kpi3.metric(t("disability"), f"{disability_rate:.1%}")
kpi4.metric(t("social_name"), format_integer(social_name))

kpi5, kpi6 = st.columns(2)

kpi5.metric(t("quilombola"), format_integer(quilombola))
kpi6.metric(t("libras"), format_integer(libras_interpreters))


# GENDER

gender = (
    df.groupby("DS_GENERO", as_index=False)["QT_ELEITORES"]
    .sum()
)

gender = add_percentage(gender)
gender["Category"] = gender["DS_GENERO"].map(display_value)

gender_colors = {
    display_value("FEMININO"): "#EC4899",
    display_value("MASCULINO"): "#2563EB",
    display_value("NÃO INFORMADO"): "#94A3B8",
}

gender_fig = px.pie(
    gender,
    names="Category",
    values="QT_ELEITORES",
    color="Category",
    color_discrete_map=gender_colors,
    hole=0.55,
    title=t("gender_chart"),
)

gender_fig.update_traces(
    textposition="inside",
    textinfo="label+percent",
    hovertemplate=(
        "<b>%{label}</b><br>"
        + t("voter_axis")
        + ": %{value:,.0f}<br>"
        + "Share: %{percent:.1%}"
        + "<extra></extra>"
    ),
)

gender_fig.update_layout(
    legend_title_text="",
    margin=dict(t=60, b=20, l=20, r=20),
)

st.plotly_chart(gender_fig, use_container_width=True)


# AGE

age_order = [
    "16 anos", "17 anos", "18 anos", "19 anos", "20 anos",
    "21 a 24 anos", "25 a 29 anos", "30 a 34 anos",
    "35 a 39 anos", "40 a 44 anos", "45 a 49 anos",
    "50 a 54 anos", "55 a 59 anos", "60 a 64 anos",
    "65 a 69 anos", "70 a 74 anos", "75 a 79 anos",
    "80 a 84 anos", "85 a 89 anos", "90 a 94 anos",
    "95 a 99 anos", "100 anos ou mais",
]


age = (
    df.groupby("DS_FAIXA_ETARIA", as_index=False)["QT_ELEITORES"]
    .sum()
)

age = add_percentage(age)

age = age[
    age["DS_FAIXA_ETARIA"].isin(age_order)
].copy()

age["DS_FAIXA_ETARIA"] = pd.Categorical(
    age["DS_FAIXA_ETARIA"],
    categories=age_order,
    ordered=True,
)

age = age.sort_values("DS_FAIXA_ETARIA")
age["Category"] = age["DS_FAIXA_ETARIA"].map(display_value)

age_fig = px.bar(
    age,
    x="Category",
    y="QT_ELEITORES",
    text="Percentage",
    custom_data=["Percentage"],
    title=t("age_chart"),
    labels={
        "Category": t("age"),
        "QT_ELEITORES": t("voter_axis"),
    },
)

age_fig.update_traces(
    texttemplate="%{text:.1f}%",
    textposition="outside",
    hovertemplate=(
        "<b>%{x}</b><br>"
        + t("voter_axis")
        + ": %{y:,.0f}<br>"
        + "Share: %{customdata[0]:.1f}%"
        + "<extra></extra>"
    ),
)

st.plotly_chart(age_fig, use_container_width=True)


# EDUCATION

education_order = [
    "ANALFABETO",
    "LÊ E ESCREVE",
    "ENSINO FUNDAMENTAL INCOMPLETO",
    "ENSINO FUNDAMENTAL COMPLETO",
    "ENSINO MÉDIO INCOMPLETO",
    "ENSINO MÉDIO COMPLETO",
    "SUPERIOR INCOMPLETO",
    "SUPERIOR COMPLETO",
]

education = (
    df.groupby(
        "DS_GRAU_ESCOLARIDADE",
        as_index=False,
    )["QT_ELEITORES"]
    .sum()
)

education = education[
    education["DS_GRAU_ESCOLARIDADE"].isin(education_order)
].copy()

education["DS_GRAU_ESCOLARIDADE"] = pd.Categorical(
    education["DS_GRAU_ESCOLARIDADE"],
    categories=education_order,
    ordered=True,
)

education = education.sort_values("DS_GRAU_ESCOLARIDADE")
education["Category"] = education[
    "DS_GRAU_ESCOLARIDADE"
].map(display_value)

education_fig = px.bar(
    education,
    x="Category",
    y="QT_ELEITORES",
    title=t("education_chart"),
    labels={
        "Category": t("education"),
        "QT_ELEITORES": t("voter_axis"),
    },
)

education_fig.update_layout(xaxis_tickangle=-35)

st.plotly_chart(education_fig, use_container_width=True)


# RACE, MARITAL STATUS AND GENDER IDENTITY

race = (
    df.groupby("DS_RACA_COR", as_index=False)["QT_ELEITORES"]
    .sum()
    .sort_values("QT_ELEITORES")
)

race["Category"] = race["DS_RACA_COR"].map(display_value)

marital_status = (
    df.groupby("DS_ESTADO_CIVIL", as_index=False)["QT_ELEITORES"]
    .sum()
    .sort_values("QT_ELEITORES")
)

marital_status["Category"] = marital_status[
    "DS_ESTADO_CIVIL"
].map(display_value)

gender_identity = (
    df.groupby(
        "DS_IDENTIDADE_GENERO",
        as_index=False,
    )["QT_ELEITORES"]
    .sum()
    .sort_values("QT_ELEITORES")
)

gender_identity["Category"] = gender_identity[
    "DS_IDENTIDADE_GENERO"
].map(display_value)


race_fig = px.bar(
    race,
    x="QT_ELEITORES",
    y="Category",
    orientation="h",
    title=t("race_chart"),
    labels={
        "QT_ELEITORES": t("voter_axis"),
        "Category": "",
    },
)

marital_fig = px.bar(
    marital_status,
    x="QT_ELEITORES",
    y="Category",
    orientation="h",
    title=t("marital_chart"),
    labels={
        "QT_ELEITORES": t("voter_axis"),
        "Category": "",
    },
)

identity_fig = px.bar(
    gender_identity,
    x="QT_ELEITORES",
    y="Category",
    orientation="h",
    title=t("identity_chart"),
    labels={
        "QT_ELEITORES": t("voter_axis"),
        "Category": "",
    },
)


chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.plotly_chart(race_fig, use_container_width=True)

with chart_col2:
    st.plotly_chart(marital_fig, use_container_width=True)

st.plotly_chart(identity_fig, use_container_width=True)