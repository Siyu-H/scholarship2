# streamlit_app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px


# 设置网页样式
st.set_page_config(
    page_title="Aid Worker Security Dashboard", layout="wide", page_icon="🛡️"
)


# 加载数据（自动缓存）
@st.cache_data
def load_data():
    return pd.read_csv("security_incidents.csv")


df = load_data()

# 侧边导航栏
st.sidebar.title("📌 Navigation")
section = st.sidebar.radio(
    "Go to Section",
    [
        "🏁 Introduction",
        "📅 Yearly Trends",
        "🌍 Geographic Patterns",
        "⚔️ Attack Types",
        "🧍‍♂️ Victim Profiles",
        "🧨 Perpetrator Analysis",
        "📅 Time & Cross Analysis",
        "✅ Conclusion & Recommendations"
    ],
)

# ---------------------------
# 🏁 SECTION: INTRODUCTION
# ---------------------------
if section == "🏁 Introduction":
    st.title("🛡️ Aid Worker Security Incidents Dashboard")
    st.markdown(
        """
    ### 👋 Welcome

    Welcome to the **Aid Worker Security Dashboard** — an interactive platform designed to explore **4,337 documented security incidents** involving humanitarian aid workers across the globe from **1997 to 2025**.

    Through the power of **data visualization** and **interactive storytelling**, this dashboard uncovers patterns in **when**, **where**, and **how** these attacks occur, and **who** they affect the most.

    Our goal is to empower **policymakers**, **NGOs**, **field organizations**, and **researchers** with **data-driven insights** to improve security planning and reduce future harm.

    ---

    ### 🔍 What This Dashboard Covers

    - 📅 **Yearly Trends** – How have incidents and their severity changed over time?
    - 🌍 **Geographic Hotspots** – Which countries and regions are most dangerous?
    - ⚔️ **Attack Characteristics** – What types of attacks are most common, and where do they occur?
    - 🧍‍♀️ **Victim Profiles** – Who are the victims: national vs. international staff?
    - 🧨 **Perpetrator Analysis** – Who are the perpetrators and how does their behavior vary?
    - 📅 **Time & Cross Patterns** – Explore monthly/quarterly trends and country × method × severity patterns.
    - 📌 **Conclusion & Recommendations** – Actionable strategies based on data insights.

    ---

    ### 📁 Dataset Summary

    - **Total Records:** 4,337 incidents  
    - **Time Span:** 1997 – 2025  
    - **Columns Include:** Country, Region, Actor Type, Victim Info, Gender, Attack Method, Location, Severity  
    - **Source:** [Aid Worker Security Database](https://aidworkersecurity.org)[^1]

    This rare and comprehensive dataset offers a critical lens into the challenges faced by aid workers worldwide.

    ---

    👉 Use the **sidebar navigation** to begin exploring each part of the dashboard.
    """
    )


# ---------------------------
# 📅 SECTION: YEARLY TRENDS (增强 & 丰富版)
# ---------------------------
elif section == "📅 Yearly Trends":
    import plotly.graph_objects as go
    import plotly.express as px

    st.header("📅 How Have Security Incidents Evolved Over Time?")
    st.markdown(
        """
        How have threats to humanitarian workers changed across the past three decades?  
        This section analyzes both the **frequency** of security incidents and their **severity** over time, providing a high-level view of how risks have evolved.

        By examining trends in incident count, victim outcomes, and total human impact, we can better understand how global instability, armed conflict, and reporting practices have shaped the threat landscape for aid workers.
        """
    )

    # ① 事件数量趋势图（交互折线图）
    st.subheader("🧮 Total Incidents per Year")
    yearly_counts = df["Year"].value_counts().sort_index()

    fig1 = go.Figure()
    fig1.add_trace(
        go.Scatter(
            x=yearly_counts.index,
            y=yearly_counts.values,
            mode="lines+markers",
            line=dict(color="#2a9d8f"),
            marker=dict(size=6),
            hovertemplate="Year: %{x}<br>Incidents: %{y}<extra></extra>",
        )
    )
    fig1.update_layout(
        title="Number of Incidents per Year (1997–2025)",
        xaxis_title="Year",
        yaxis_title="Number of Incidents",
        height=400,
        template="simple_white",
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown(
        """
        - From **2000 to 2014**, the number of recorded attacks rose steadily, highlighting a growing threat to aid workers.
        - The period between **2013 and 2020** is marked by high volatility, with dramatic spikes and dips in incident numbers—potentially linked to escalating regional conflicts (e.g., Syria, South Sudan) or fluctuations in global humanitarian presence.
        - The sharp decline in **2025** is likely not meaningful and may simply reflect **incomplete data** for the ongoing year.
        """
    )

    # ② 严重性：死亡 / 受伤 / 绑架趋势
    st.subheader("☠️ Deaths, Wounds, and Kidnappings per Year")
    severity_year = (
        df.groupby("Year")[["Total killed", "Total wounded", "Total kidnapped"]]
        .sum()
        .reset_index()
    )

    fig2 = px.bar(
        severity_year,
        x="Year",
        y=["Total killed", "Total wounded", "Total kidnapped"],
        title="Severity of Incidents by Year",
        labels={"value": "People", "variable": "Outcome"},
        color_discrete_sequence=["#e63946", "#f4a261", "#457b9d"],
    )
    fig2.update_layout(
        barmode="stack", height=450, xaxis_title="Year", yaxis_title="Total Victims"
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown(
        """
        - The number of individuals **killed and wounded** has varied significantly year to year.
        - Sudden spikes in casualties may point to **large-scale attacks**, **targeted violence**, or **improved data collection and verification**.
        - While **kidnapping incidents** are generally more stable, some peaks still emerge—likely linked to specific regional crises.
        """
    )

    # ③ 每年总受害人趋势（合计线图）
    st.subheader("📊 Total Victims per Year (Killed + Wounded + Kidnapped)")
    severity_year["Total victims"] = (
        severity_year["Total killed"]
        + severity_year["Total wounded"]
        + severity_year["Total kidnapped"]
    )

    fig3 = go.Figure()
    fig3.add_trace(
        go.Scatter(
            x=severity_year["Year"],
            y=severity_year["Total victims"],
            mode="lines+markers",
            line=dict(color="#1d3557"),
            hovertemplate="Year: %{x}<br>Total Victims: %{y}<extra></extra>",
        )
    )
    fig3.update_layout(
        title="Combined Human Impact per Year",
        xaxis_title="Year",
        yaxis_title="Total Victims",
        height=400,
        template="simple_white",
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown(
        """
        - This chart reveals the **total human cost** of each year, aggregating deaths, injuries, and kidnappings into a single measure of impact.
        - It shows that some years—such as **2013** and **2023**—not only had many incidents, but also exceptionally high **casualties per attack**.
        - These insights are crucial for identifying years of **extraordinary violence**, which may warrant deeper qualitative investigation.
        """
    )


# ---------------------------
# # 🌍 SECTION: GEOGRAPHIC PATTERNS
# # ---------------------------
# elif section == "🌍 Geographic Patterns (coming)":
#     import plotly.express as px

#     st.header("🌍 Which Countries Are Most Affected?")
#     st.markdown(
#         """
#     Security incidents are not evenly distributed across the globe.
#     This section explores **where** attacks on aid workers are most frequent, using both a ranked chart and an interactive map.

#     Understanding geographic patterns helps organizations prioritize **risk mitigation**, **training**, and **resource allocation**.
#     """
#     )

#     # ======================
#     # 📊 静态 Top 10 柱状图
#     # ======================
#     st.subheader("📊 Top 10 Countries by Number of Incidents")

#     top10 = df['Country'].value_counts().dropna().head(10).reset_index()
#     top10.columns = ['Country', 'Incidents']

#     fig_bar = px.bar(
#         top10.sort_values("Incidents"),
#         x="Incidents",
#         y="Country",
#         orientation="h",
#         color="Incidents",
#         color_continuous_scale="Reds",
#         title="Top 10 Countries by Incident Count"
#     )

#     fig_bar.update_layout(
#         height=450,
#         xaxis_title="Number of Incidents",
#         yaxis_title="Country",
#         margin=dict(l=40, r=40, t=50, b=40)
#     )
#     st.plotly_chart(fig_bar, use_container_width=True)

#     st.markdown(
#         """
#     - The countries listed above represent the **most dangerous environments** for aid workers.
#     - These include prolonged conflict zones such as **Afghanistan**, **Syria**, and **South Sudan**.
#     """
#     )

#     # ======================
#     # 🌍 交互式世界地图（Plotly）
#     # ======================
#     st.subheader("🗺️ Interactive World Map of Incidents")

#     # 国家事件统计表（用于地图）
#     country_counts = df["Country"].dropna().value_counts().reset_index()
#     country_counts.columns = ["Country", "Incident Count"]

#     fig_map = px.choropleth(
#         country_counts,
#         locations="Country",
#         locationmode="country names",
#         color="Incident Count",
#         hover_name="Country",
#         color_continuous_scale="Reds",
#         title="Total Incidents by Country (1997–2025)",
#     )

#     fig_map.update_layout(
#         margin=dict(l=40, r=40, t=50, b=40),
#         geo=dict(showframe=False, showcoastlines=True),
#         height=500,
#     )

#     st.plotly_chart(fig_map, use_container_width=True)

#     st.markdown(
#         """
#     - Darker countries on the map have recorded more incidents.
#     - You can **hover**, **zoom**, or **pan** the map to explore regions of interest.
#     - The map shows high-risk clusters in **Central Africa**, **Middle East**, and **South Asia**.
#     """
#     )
# ---------------------------
# ---------------------------
# 🌍 SECTION: GEOGRAPHIC PATTERNS (最终整合 + Data Storytelling)
# ---------------------------
elif section == "🌍 Geographic Patterns":
    import plotly.express as px
    import matplotlib.pyplot as plt

    st.header("🌍 Which Countries and Regions Are Most Affected?")
    st.markdown(
        """
        While humanitarian work spans the globe, **not all regions are equally dangerous**.  
        This section uncovers the **geographic patterns of attacks** on aid workers — where these incidents are most concentrated, how they vary across countries and regions, and how these patterns have shifted over time.

        By identifying **hotspots of violence**, we can help aid organizations and policymakers better prepare and allocate resources.
        """
    )

    # ======================
    # 📊 Top 10 Static Bar Chart
    # ======================
    st.subheader("📊 Top 10 Countries by Incident Count")
    top10_countries = df["Country"].dropna().value_counts().head(10)

    left, center, right = st.columns([1, 4, 1])
    with center:
        fig_static, ax = plt.subplots(figsize=(8, 4.5))
        top10_countries.sort_values().plot(kind="barh", ax=ax, color="#e76f51")
        ax.set_title(
            "Top 10 Most Affected Countries", fontsize=14, fontweight="bold", pad=10
        )
        ax.set_xlabel("Number of Incidents")
        ax.set_ylabel("Country")
        ax.grid(True, linestyle="--", alpha=0.4)
        fig_static.patch.set_facecolor("white")
        ax.set_facecolor("#f9f9f9")
        for i, v in enumerate(top10_countries.sort_values()):
            ax.text(v + 1, i, str(v), va="center", fontsize=9)
        st.pyplot(fig_static)

    st.markdown(
        """
        These top 10 countries account for a **disproportionate share** of attacks on aid workers.

        - **Afghanistan** leads with over 600 incidents, followed closely by **South Sudan**, **Sudan**, and **Syria** — all countries with histories of prolonged conflict.
        - **Somalia** and the **Democratic Republic of the Congo** also appear, reinforcing the dangers aid workers face in regions with political instability and armed groups.
        - This data shows how **fragile states** and **active conflict zones** consistently emerge as high-risk environments for humanitarian operations.
        """
    )

    # ======================
    # 📈 Incident Trends by Country Over Time
    # ======================
    st.subheader("📈 Incident Trends in Top Countries Over Time")
    top_countries = df["Country"].value_counts().head(6).index.tolist()
    df_top = df[df["Country"].isin(top_countries)]
    country_year = (
        df_top.groupby(["Year", "Country"]).size().reset_index(name="Incidents")
    )

    fig_trend = px.line(
        country_year,
        x="Year",
        y="Incidents",
        color="Country",
        markers=True,
        title="Incident Trends Over Time in Most Affected Countries",
    )
    fig_trend.update_layout(height=450, template="simple_white")
    st.plotly_chart(fig_trend, use_container_width=True)

    st.markdown(
        """
        When we zoom into trends over time, we see **distinct country profiles**:

        - **Afghanistan** experienced a steady rise until the early 2010s, likely tied to military operations and insurgent activity.
        - **South Sudan** saw a sharp increase after 2013, aligning with the outbreak of civil war.
        - **Syria** spiked around 2014–2016, reflecting the intensity of that conflict’s humanitarian crisis.

        This time-series view underscores how **political developments** and **conflict escalation** directly translate into risks for humanitarian workers.
        """
    )

    # ======================
    # 🌐 Regional Distribution
    # ======================
    st.subheader("🌐 Regional Distribution of Incidents")
    if "Region" in df.columns:
        region_counts = df["Region"].dropna().value_counts().reset_index()
        region_counts.columns = ["Region", "Incidents"]

        fig_region = px.bar(
            region_counts.sort_values("Incidents", ascending=True),
            x="Incidents",
            y="Region",
            orientation="h",
            color="Incidents",
            color_continuous_scale="Blues",
            title="Total Incidents by Region",
        )
        fig_region.update_layout(height=450)
        st.plotly_chart(fig_region, use_container_width=True)

        st.markdown(
            """
            Looking beyond countries, a regional lens offers **finer-grained insight** into where threats concentrate:

            - Areas like the **Gaza Strip**, **Herat**, and **Kunduz** emerge as regional hotspots, even within already high-risk nations.
            - These regions often contain **urban centers, border zones, or contested territories**, making them flashpoints for violence.
            - For organizations planning field missions, this view is critical for **micro-level security planning**.
            """
        )
    else:
        st.warning(
            "🧭 'Region' column not found in your dataset. Regional view skipped."
        )

    # ======================
    # 🗺️ Interactive World Map
    # ======================
    st.subheader("🗺️ Interactive World Map of Incidents")

    country_counts = df["Country"].dropna().value_counts().reset_index()
    country_counts.columns = ["Country", "Incident Count"]

    fig_map = px.choropleth(
        country_counts,
        locations="Country",
        locationmode="country names",
        color="Incident Count",
        hover_name="Country",
        color_continuous_scale="Reds",
        title="Total Incidents by Country (1997–2025)",
    )

    fig_map.update_layout(
        margin=dict(l=40, r=40, t=50, b=40),
        geo=dict(showframe=False, showcoastlines=True),
        height=500,
    )
    st.plotly_chart(fig_map, use_container_width=True)

    st.markdown(
        """
        This **global heatmap** reinforces earlier insights, while offering an intuitive overview:

        - Countries in **dark red**, such as **Afghanistan** and **South Sudan**, clearly stand out.
        - Less intense zones — like parts of Latin America and Southeast Asia — still show moderate risk levels, often linked to local criminal violence or instability.
        - Users can **hover, zoom, and pan** to explore patterns interactively, making it a powerful tool for both research and field planning.

        Together, these visuals provide a compelling geographic story of where humanitarian work is most at risk — and why that matters.
        """
    )
elif section == "⚔️ Attack Types":
    import pandas as pd
    import plotly.express as px
    import plotly.graph_objects as go

    st.header("\u2694\ufe0f What Types of Attacks Are Most Common?")
    st.markdown(
        """
    Understanding **how aid workers are attacked** helps organizations prepare appropriate protocols.

    This section explores the **most common attack methods**, **where** they occur, and **how** they have evolved over time.
    """
    )

    # ======================
    # 📊 Top 10 Attack Methods
    # ======================
    st.subheader("📊 Most Common Means of Attack")

    means_counts = df["Means of attack"].dropna().value_counts().head(10).reset_index()
    means_counts.columns = ["Means of Attack", "Count"]

    fig1 = px.bar(
        means_counts.sort_values("Count", ascending=True),
        x="Count",
        y="Means of Attack",
        orientation="h",
        color="Count",
        color_continuous_scale="Oranges",
        title="Top 10 Attack Methods",
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown(
        """
We begin by asking a fundamental question: **How are aid workers most often attacked?**

The chart above paints a stark picture. **Shooting**, **Kidnapping**, and **Bodily Assault** dominate the landscape of violence, together accounting for the majority of all recorded incidents.

- **Shooting** is by far the most common tactic — a direct, often deadly form of violence that reflects armed group presence in unstable regions.
- **Kidnapping**, while slightly less frequent, poses prolonged risks for victims and can involve ransom, political messaging, or forced labor.
- **Bodily Assault** suggests close-range attacks and may represent chaotic environments or breakdowns in local law enforcement.

Interestingly, while less frequent, tactics like **Aerial Bombardment** and **IEDs** may carry a higher lethality per incident. These methods underscore the militarized nature of some conflict zones.

Understanding these patterns helps humanitarian groups **tailor protection training** and **anticipate the most probable threats** in the field.
        """
    )

    # ======================
    # 📌 Grouped Bar: Attack × Location
    # ======================
    st.subheader("📌 Attack Methods by Location Type")

    top_means = df["Means of attack"].value_counts().head(6).index.tolist()
    df_filtered = df[df["Means of attack"].isin(top_means)]
    grouped = (
        df_filtered.groupby(["Means of attack", "Location"])
        .size()
        .reset_index(name="Count")
    )

    fig2 = px.bar(
        grouped,
        x="Means of attack",
        y="Count",
        color="Location",
        barmode="group",
        title="Top Attack Methods Across Locations",
        height=450,
        color_discrete_sequence=px.colors.qualitative.Set2,
    )

    fig2.update_layout(
        xaxis_title="Means of Attack",
        yaxis_title="Number of Incidents",
        legend_title="Location Type",
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown(
        """
Violence doesn’t happen in a vacuum — **where** attacks occur is just as important as how.

This grouped bar chart reveals distinct patterns between attack methods and location types:

- **Kidnappings** overwhelmingly occur on **roads**, highlighting the danger of travel between project sites or during field visits.
- **Shootings** also peak in public or road settings, suggesting opportunistic or targeted violence in transit zones.
- **Aerial Bombardments** cluster around **compounds and project sites**, pointing to militarized campaigns against organizational infrastructure.

These patterns are more than statistics — they reflect **operational vulnerabilities**. For example, missions may need armored vehicles for road travel, or reinforced compounds in known aerial strike zones.

By pairing methods with location types, we uncover **attack profiles** that aid organizations can directly respond to in security planning.
        """
    )

    # ======================
    # 🧱 Treemap View: Attack Method × Location
    # ======================
    st.subheader("🧱 Treemap: Attack Methods and Locations")

    df_tree = df[df["Means of attack"].isin(top_means)][
        ["Means of attack", "Location"]
    ].dropna()
    tree_data = (
        df_tree.groupby(["Means of attack", "Location"])
        .size()
        .reset_index(name="Count")
    )

    fig_tree = px.treemap(
        tree_data,
        path=["Means of attack", "Location"],
        values="Count",
        color="Means of attack",
        color_discrete_sequence=px.colors.qualitative.Set2,
        title="Attack Methods and Locations (Treemap)",
    )

    fig_tree.update_layout(height=500, margin=dict(t=40, l=0, r=0, b=10))
    st.plotly_chart(fig_tree, use_container_width=True)

    st.markdown(
        """
This **treemap** acts like a strategic map, revealing the **relative footprint** of each attack type and its associated locations.

Each colored block represents a combination of method and setting. The larger the block, the more frequent the pairing:

- **Shooting on Roads** and **Kidnapping on Roads** dominate the treemap, echoing the threats of ambush during travel.
- **Bodily Assault** shows a more **diverse footprint**, appearing across project sites, public spaces, and even homes — pointing to unpredictable flashpoints.
- **Unknown categories** (in both method and location) are also substantial, reminding us of reporting limitations and the fog of conflict.

Unlike a single bar or pie chart, this layout allows us to compare **both prevalence and diversity**. For field staff, this dual-view helps in **resource allocation** — prioritizing not just common threats, but complex ones across multiple settings.
        """
    )

    # ======================
    # 📈 Attack Methods Over Time
    # ======================
    st.subheader("📈 How Have Attack Methods Changed Over Time?")

    year_attack = (
        df.groupby(["Year", "Means of attack"]).size().reset_index(name="Count")
    )
    year_attack_filtered = year_attack[year_attack["Means of attack"].isin(top_means)]

    fig4 = px.area(
        year_attack_filtered,
        x="Year",
        y="Count",
        color="Means of attack",
        title="Trends of Attack Methods Over Time",
        groupnorm="fraction",
        height=450,
    )
    st.plotly_chart(fig4, use_container_width=True)

    st.markdown(
        """
Violence is dynamic — and so are the tactics used against aid workers.

This timeline shows how **attack methods have shifted** from 1997 to 2025. Early years are dominated by **Unknown** categories, likely due to inconsistent reporting. But as data improves, clear trends emerge:

- **Kidnapping** saw a sharp rise in the late 2000s and early 2010s, aligning with conflicts in Somalia, Syria, and South Sudan.
- **Shooting** remains consistently high, reflecting its continued use across regions and periods.
- **Bodily Assault** and **Shelling** fluctuate more, often tied to regional flare-ups or localized unrest.

These trends offer more than historical insight — they support **predictive awareness**. Field teams can monitor which methods are rising in frequency and **adjust field protocols accordingly**, ensuring both preparation and adaptability.
        """
    )
elif section == "🧍‍♂️ Victim Profiles":
    import plotly.express as px
    import pandas as pd

    st.header("🧍 Who Are the Victims?")
    st.markdown(
        """
        Understanding who is most vulnerable in humanitarian settings is critical for building effective protection strategies.  
        This section explores **which aid workers are most at risk**, and how **different types of harm** have affected them **over time and across regions**.
        """
    )

    # 统计汇总
    national = df["Total nationals"].fillna(0).astype(int).sum()
    international = df["Total internationals"].fillna(0).astype(int).sum()
    killed = df["Total killed"].fillna(0).astype(int).sum()
    wounded = df["Total wounded"].fillna(0).astype(int).sum()
    kidnapped = df["Total kidnapped"].fillna(0).astype(int).sum()

    yearly = (
        df.groupby("Year")[["Total killed", "Total wounded", "Total kidnapped"]]
        .sum()
        .reset_index()
    )

    # Top 5 countries
    country_victims = df.groupby("Country")[
        ["Total killed", "Total wounded", "Total kidnapped"]
    ].sum()
    country_victims["Total"] = country_victims.sum(axis=1)
    top_countries = (
        country_victims.sort_values("Total", ascending=False).head(5).reset_index()
    )
    top_countries_melted = top_countries.melt(
        id_vars="Country",
        value_vars=["Total killed", "Total wounded", "Total kidnapped"],
        var_name="Type",
        value_name="Count",
    )

    # 1️⃣ National vs International
    st.subheader("👥 National vs International Staff")
    staff_df = pd.DataFrame(
        {
            "Type": ["National Staff", "International Staff"],
            "Count": [national, international],
        }
    )

    fig_donut = px.pie(
        staff_df,
        names="Type",
        values="Count",
        hole=0.4,
        color_discrete_sequence=["#66c2a5", "#fc8d62"],
    )
    fig_donut.update_traces(
        textinfo="percent+label",
        pull=[0.03, 0],
        marker=dict(line=dict(color="white", width=2)),
    )
    fig_donut.update_layout(
        title=dict(text="Victim Composition by Staff Type", x=0.5, font=dict(size=18)),
        showlegend=False,
        height=400,
    )
    st.plotly_chart(fig_donut, use_container_width=True)

    st.markdown(
        f"""
        - Among the **{national + international} recorded aid worker victims**, a staggering **{round(national / (national + international) * 100, 1)}%** are **national staff**.
        - This stark imbalance reflects the reality that national staff—who often operate in frontline or remote areas—face **disproportionately higher risks** than their international counterparts.
        """
    )

    # 2️⃣ Victim Type Breakdown
    st.subheader("💥 Victim Type Breakdown: Total vs Proportional")
    view_option = st.radio(
        "Choose view type:",
        ["📊 Total Count View", "📉 Proportional View"],
        horizontal=True,
    )

    if view_option == "📊 Total Count View":
        fig_bar = px.bar(
            x=["Killed", "Wounded", "Kidnapped"],
            y=[killed, wounded, kidnapped],
            color=["Killed", "Wounded", "Kidnapped"],
            text=[killed, wounded, kidnapped],
            color_discrete_sequence=["#d62728", "#1f77b4", "#2ca02c"],
        )
        fig_bar.update_traces(textposition="outside", marker_line_color="white")
        fig_bar.update_layout(
            title=dict(
                text="Total Number of Victims by Type", x=0.5, font=dict(size=20)
            ),
            yaxis_title="Number of Victims",
            xaxis_title="Victim Type",
            showlegend=False,
            height=450,
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        st.markdown(
            """
            - Overall, **killings and injuries** account for the majority of victimization, with **over 3,000 aid workers killed** and another **3,000 wounded** in the last two decades.
            - **Kidnappings**, while less frequent, still affect over **2,000 individuals**, indicating a persistent and targeted threat.
            """
        )

    else:
        # 构造比例图数据
        harm_fields = {
            "Killed": ["Nationals killed", "Internationals killed"],
            "Wounded": ["Nationals wounded", "Internationals wounded"],
            "Kidnapped": ["Nationals kidnapped", "Internationals kidnapped"],
        }

        data = {"Harm Type": [], "Staff Type": [], "Count": []}
        for harm, (nat_col, int_col) in harm_fields.items():
            nat_count = df[nat_col].fillna(0).astype(int).sum()
            int_count = df[int_col].fillna(0).astype(int).sum()
            data["Harm Type"] += [harm, harm]
            data["Staff Type"] += ["National", "International"]
            data["Count"] += [nat_count, int_count]

        df_stacked = pd.DataFrame(data)
        df_stacked["Percentage"] = df_stacked.groupby("Harm Type")["Count"].transform(
            lambda x: x / x.sum() * 100
        )

        fig_pct = px.bar(
            df_stacked,
            x="Harm Type",
            y="Percentage",
            color="Staff Type",
            barmode="stack",
            text=df_stacked["Percentage"].round(1).astype(str) + "%",
            color_discrete_sequence=["#66c2a5", "#fc8d62"],
        )
        fig_pct.update_layout(
            title=dict(
                text="Relative Victim Composition by Staff Type",
                x=0.5,
                font=dict(size=20),
            ),
            yaxis_title="Percentage (%)",
            xaxis_title="Harm Type",
            legend=dict(orientation="h", x=0.5, xanchor="center", y=1.05),
            height=450,
        )
        fig_pct.update_traces(textposition="inside")
        st.plotly_chart(fig_pct, use_container_width=True)

        st.markdown(
            """
            - In every harm category, **national staff are disproportionately affected**—they account for over **90% of killings and injuries**.
            - Interestingly, **international staff are slightly more likely to be kidnapped** compared to other forms of harm, but still remain a minority.
            - This highlights the **unique vulnerabilities** faced by national staff who often lack the same security resources as their international peers. This aligns with findings by Humanitarian Outcomes[^2], where national staff face significantly greater exposure in volatile settings.
            """
        )

    # 3️⃣ Trends Over Time
    st.subheader("📈 Trends Over Time (by Harm Type)")

    fig_line = px.line(
        yearly,
        x="Year",
        y=["Total killed", "Total wounded", "Total kidnapped"],
        markers=True,
        line_shape="spline",
        color_discrete_map={
            "Total killed": "#d62728",
            "Total wounded": "#1f77b4",
            "Total kidnapped": "#2ca02c",
        },
        title="Victim Harm Types Over Time",
    )
    fig_line.update_layout(
        yaxis_title="Number of Victims", legend_title="Harm Type", height=450
    )
    st.plotly_chart(fig_line, use_container_width=True)

    st.markdown(
        """
        - Over time, we observe a **notable rise in injuries**, especially after 2015, reflecting either intensified conflict zones or improved reporting.
        - Meanwhile, **kidnappings show cyclical surges**, often correlating with political instability or militant activity in specific regions.
        - Tracking these trends allows organizations to **anticipate emerging threats** and adjust risk mitigation strategies accordingly.
        """
    )

    # 4️⃣ 国家分布
    st.subheader("🌍 Top 5 Countries by Harm Type")

    fig_country = px.bar(
        top_countries_melted,
        x="Count",
        y="Country",
        color="Type",
        orientation="h",
        barmode="group",
        title="Top 5 Countries: Victim Breakdown by Harm Type",
        color_discrete_sequence=px.colors.qualitative.Pastel,
    )
    fig_country.update_layout(
        height=500,
        xaxis_title="Number of Victims",
        yaxis_title="Country",
        legend_title="Type of Harm",
    )
    st.plotly_chart(fig_country, use_container_width=True)

    st.markdown(
        """
        - Countries like **Afghanistan**, **South Sudan**, and **Syria** consistently top the charts, but each shows **distinct harm profiles**.
        - For instance, **South Sudan** reports a higher number of **injuries**, while **Afghanistan** has more **fatalities**.
        - Such patterns emphasize the need for **region-specific response plans** rather than one-size-fits-all policies.
        """
    )

elif section == "🧨 Perpetrator Analysis":
    st.header("🧨 Who Are the Perpetrators?")
    st.markdown(
        """
        Understanding the nature of violence against aid workers also requires identifying **who is behind these attacks**.  
        In this section, we explore the **types of perpetrators**, the **kinds of harm they cause**, and how their **geographic footprint** varies across conflict zones.
        """
    )

    # ======================
    # 📊 Top Perpetrator Types
    # ======================
    st.subheader("📊 Perpetrator Types")
    actor_type_counts = df["Actor type"].dropna().value_counts().head(10).reset_index()
    actor_type_counts.columns = ["Actor Type", "Count"]

    fig1 = px.bar(
        actor_type_counts,
        x="Count",
        y="Actor Type",
        orientation="h",
        color="Count",
        color_continuous_scale="Inferno",
        title="Top Perpetrator Types",
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown(
        """
        - The majority of attacks are carried out by **non-state armed groups**, with **national and unknown affiliations** dominating the list.  
        - Notably, more than **2,000 incidents** are attributed to **"Unknown" actors**, raising concerns about the **difficulty of attribution** and potential **gaps in field reporting**. According to Geneva Call[^3], these groups often disregard humanitarian neutrality, posing a growing threat to frontline operations.
        - This uncertainty poses a challenge for humanitarian agencies when designing targeted mitigation strategies.
        """
    )

    # ======================
    # 📌 Harm Caused by Actor Type
    # ======================
    st.subheader("📌 Harm Caused by Top Perpetrator Types")
    top_actors = df["Actor type"].value_counts().head(5).index.tolist()
    df_top_actors = df[df["Actor type"].isin(top_actors)]
    harm_grouped = (
        df_top_actors.groupby("Actor type")[
            ["Total killed", "Total wounded", "Total kidnapped"]
        ]
        .sum()
        .reset_index()
    )
    harm_melted = harm_grouped.melt(
        id_vars="Actor type", var_name="Harm Type", value_name="Count"
    )

    fig2 = px.bar(
        harm_melted,
        x="Count",
        y="Actor type",
        color="Harm Type",
        barmode="stack",
        orientation="h",
        title="Top Perpetrators: Harm Type Distribution",
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown(
        """
        - **Unknown actors** consistently lead in causing all three types of harm: **deaths, injuries, and kidnappings**.
        - **Non-state armed groups (national or unspecified)** rank high in **lethality**, especially through ambush-style operations.
        - Interestingly, **unaffiliated individuals** still pose a significant threat, often operating in unpredictable or opportunistic contexts.
        - These insights highlight the need for **differentiated protection measures** tailored to the specific risks posed by each perpetrator group.
        """
    )

    # ======================
    # 🌍 Perpetrator Geography Bubble Chart
    # ======================
    st.subheader("🌍 Perpetrator Spread by Country")
    df_geo = df.dropna(subset=["Country", "Actor type"])
    country_actor = (
        df_geo.groupby(["Country", "Actor type"]).size().reset_index(name="Incidents")
    )

    fig3 = px.scatter(
        country_actor,
        x="Country",
        y="Actor type",
        size="Incidents",
        color="Actor type",
        title="Perpetrator Incidents by Country",
        height=500,
    )
    fig3.update_layout(
        xaxis_title="Country",
        yaxis_title="Actor Type",
        legend_title="Actor Type",
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown(
        """
        - **Spatial patterns** reveal that some actors are **highly localized**: for example, **non-state groups** are prominent in countries like **Afghanistan** and **South Sudan**.
        - In contrast, **foreign forces** and **host-state actors** tend to appear in **more politically charged environments**.
        - While some groups appear frequently with lower levels of harm, others—though less frequent—may be associated with **high-severity attacks**.
        - Recognizing these spatial and behavioral differences is key for humanitarian planners to implement **context-specific safety protocols** and **effective advocacy efforts**.
        """
    )

elif section == "📅 Time & Cross Analysis":
    st.header("📅 Time Trends & 🔁 Cross-Dimensional Insights")
    st.markdown(
        """
        This section uncovers **temporal patterns** and **cross-dimensional insights** that help us understand the evolving landscape of aid worker incidents. Specifically, we explore:

        - **How incident frequency changes over time** (monthly and quarterly trends)
        - **How countries, attack methods, and harm severity interact**, revealing critical hotspots
        """
    )

    # ======================
    # 📅 Monthly and Quarterly Trends
    # ======================
    st.subheader("📆 Monthly and Quarterly Incident Trends")

    df_time = df.copy()
    df_time = df_time.dropna(subset=["Year", "Month"])
    df_time["Year"] = df_time["Year"].astype(int)
    df_time["Month"] = df_time["Month"].astype(int)
    df_time["Date"] = pd.to_datetime(df_time[["Year", "Month"]].assign(DAY=1))
    df_time["Quarter"] = df_time["Date"].dt.to_period("Q").astype(str)

    # Monthly Trend
    monthly_counts = df_time.groupby("Date").size().reset_index(name="Incidents")
    fig_month = px.line(
        monthly_counts,
        x="Date",
        y="Incidents",
        title="Monthly Incident Trends",
        markers=True,
        line_shape="spline",
        height=400,
    )
    st.plotly_chart(fig_month, use_container_width=True)

    # Quarterly Trend
    quarterly_counts = df_time.groupby("Quarter").size().reset_index(name="Incidents")
    fig_quarter = px.bar(
        quarterly_counts,
        x="Quarter",
        y="Incidents",
        title="Quarterly Incident Distribution",
        color="Incidents",
        color_continuous_scale="Blues",
        height=400,
    )
    st.plotly_chart(fig_quarter, use_container_width=True)

    st.markdown(
        """
        - Over the past two decades, **monthly and quarterly incidents have increased**, with notable spikes in recent years.
        - The **post-2015 surge** may reflect both rising conflict intensity and improvements in data reporting. A similar trend has been observed in independent reports[^4], pointing to both increased conflict intensity and improved incident reporting.
        - Understanding these temporal shifts helps stakeholders anticipate **surge periods** and **optimize deployment timing**.
        """
    )

    # ======================
    # 🔁 Country × Attack × Severity
    # ======================
    st.subheader("🔁 Country × Attack Method × Severity")

    df_cross = df.dropna(subset=["Country", "Means of attack"])
    df_cross = (
        df_cross.groupby(["Country", "Means of attack"])
        .agg(
            {
                "Total killed": "sum",
                "Total wounded": "sum",
                "Total kidnapped": "sum",
            }
        )
        .reset_index()
    )

    df_cross_melted = df_cross.melt(
        id_vars=["Country", "Means of attack"],
        value_vars=["Total killed", "Total wounded", "Total kidnapped"],
        var_name="Severity",
        value_name="Count",
    )

    fig_heatmap = px.density_heatmap(
        df_cross_melted,
        x="Means of attack",
        y="Country",
        z="Count",
        facet_col="Severity",
        color_continuous_scale="OrRd",
        title="Heatmap: Country × Attack Type × Severity",
        height=600,
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)

    st.markdown(
        """
        - This heatmap reveals **how attack methods differ by country**, and the **severity of resulting harm**.
        - Countries like **Occupied Palestinian Territories** and **South Sudan** show **concentrated patterns of deadly ambushes or kidnappings**.
        - The intersection of high-lethality tactics (e.g., **ambushes**, **IEDs**) with specific countries highlights **targeted risks** that require customized responses.
        - These insights can inform **mission planning**, **resource allocation**, and **staff training** by identifying where and how the most severe threats are likely to occur.
        """
    )


elif section == "✅ Conclusion & Recommendations":
    st.header("✅ Conclusions & Recommendations")
    st.markdown(
        """
        Over the course of this dashboard, we have traced the complex and evolving landscape of security threats faced by humanitarian aid workers. From year-by-year trends to specific attack methods, from regional hotspots to individual victim profiles, the data reveals a sobering yet critical story—one that must inform how humanitarian work is protected and supported going forward.

        ### 🧭 Key Conclusions

        - **National staff shoulder the heaviest burden**: Nearly 90% of all recorded victims are national employees. These individuals are often the frontline lifeline of humanitarian missions, yet they face the greatest risks with the fewest protections.

        - **Lethal violence is the norm, not the exception**: Across more than 4,300 incidents, we observed that killings and injuries far outweigh kidnappings. This reinforces the urgency of improving field-level safety protocols and crisis response systems.

        - **Different types of staff face different threats**: While national staff are disproportionately affected by fatal incidents, international staff tend to be more targeted in kidnappings—possibly due to perceived political leverage or ransom value.

        - **Perpetrators remain shadowy, but deadly**: A significant number of attacks come from unknown actors, while non-state armed groups consistently appear among the most dangerous and lethal sources of harm. Lack of attribution impedes accountability and risk forecasting.

        - **Violence is intensifying, not stabilizing**: Trends over time show a consistent rise in monthly and quarterly incident counts since 2015, suggesting escalating insecurity in the field rather than progress toward safety.

        - **Some countries carry a disproportionate share of risk**: Nations such as Afghanistan, South Sudan, Syria, and the Occupied Palestinian Territories consistently emerge as epicenters of high-severity attacks. Within these countries, certain regions—like Herat, Gaza, and Kunduz—are particularly deadly.

        ### 📌 Strategic Recommendations

        - **🔒 Prioritize national staff safety** through tailored training, access to mental health support, risk-adjusted benefits, and stronger legal protections. These individuals often lack the resources and evacuation options available to their international counterparts.

        - **📍 Localize security strategies** by developing country- and region-specific risk frameworks. What works in one conflict zone may fail in another; adaptive planning is key.

        - **📆 Monitor and forecast with time trends**: Use monthly and quarterly incident data to anticipate peak risk periods—especially in regions with seasonal surges or historical conflict anniversaries.

        - **🕵️‍♂️ Improve documentation and attribution** of incidents. Strengthening data partnerships with local actors and investing in incident forensics can help reduce the number of attacks labeled as perpetrated by “unknown actors.” This echoes recommendations by the ICRC[^5], who advocate for improved field-level safety systems and staff preparedness in volatile areas.

        - **🚨 Identify high-risk intersections**: Pay close attention to scenarios where deadly attack methods (like ambushes or IEDs) intersect with vulnerable staff types or regions. These hotspots should receive additional resources and rapid-response capability.

        ---

        ### 💡 Final Reflection

        Each data point in this dashboard reflects a human life disrupted—or ended—while trying to make the world a more humane place. Data alone cannot stop bullets or threats. But it can inform action. It can drive smarter policy. It can strengthen systems. And most importantly, it can help ensure that aid workers return home safely.

        Our hope is that this analysis becomes more than numbers on a dashboard—it becomes a tool for advocacy, planning, and protection.


        ### 📚 References

        - [^1]Aid Worker Security Database (2024). *Global record of major attacks on humanitarian workers*. Retrieved from [https://aidworkersecurity.org](https://aidworkersecurity.org)
        - [^2]Humanitarian Outcomes (2023). *Aid Worker Security Report 2023: Figures at a Glance*. Retrieved from [https://www.humanitarianoutcomes.org](https://www.humanitarianoutcomes.org)
        - [^3]Stoddard, A., Harmer, A., & Czwarno, M. (2022). *Spotlight on Local Aid Workers: Rising Risks and Needs for Protection*. Humanitarian Outcomes. [https://www.humanitarianoutcomes.org](https://www.humanitarianoutcomes.org)
        - [^4]Geneva Call (2021). *Protecting Humanitarian Action in Armed Conflict*. Retrieved from [https://genevacall.org](https://genevacall.org)
        - [^5]ICRC (2020). *Security of Humanitarian Personnel: Principles and Best Practices*. [https://www.icrc.org](https://www.icrc.org)
        """
    )
