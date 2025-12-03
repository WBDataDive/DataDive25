# HAI Full Database - Data Dictionary

**Dataset**: `hai_full_database.csv`
**Total Columns**: 232
**Source**: Stanford HAI (Human-Centered Artificial Intelligence) Database

This dataset contains comprehensive AI-related metrics across countries and years, including research output, talent, investment, policy, and infrastructure indicators.

---

## Column Categories Overview

| Category | Count | Description |
|----------|-------|-------------|
| **Metadata** | 8 | Country identifiers, year, population |
| **Publications & Citations** | 6 | Research output metrics |
| **Patents & Models** | 3 | Innovation and ML model production |
| **GitHub Activity** | 2 | Open-source contributions |
| **Conference Submissions** | 7 | Academic conference participation |
| **Investment** | 5 | AI startup funding metrics |
| **AI Talent & Skills** | 6 | Workforce and hiring indicators |
| **Policy & Governance** | 4 | Legislative and strategy indicators |
| **Social Media** | 2 | Public discourse metrics |
| **Infrastructure** | 4 | Computing and connectivity |
| **Per Capita Metrics** | 35 | Population-normalized versions |
| **Normalized Metrics** | 148 | Standardized scores for comparison |

---

## Detailed Column Descriptions

### 1. Metadata Columns (8 columns)

| Column | Description | Type | Example Values |
|--------|-------------|------|----------------|
| `PublishYear` | Year of data publication | Integer | 2017, 2018, 2019 |
| `CountryName` | Full country name | String | "Australia", "Brazil" |
| `CountryGroup` | Country classification | String | "core", "emerging" |
| `Code` | ISO 3-letter country code | String | "AUS", "BRA", "CHN" |
| `Country` | ISO 2-letter country code | String | "AU", "BR", "CN" |
| `Region` | World Bank region | String | "East Asia & Pacific", "Europe & Central Asia" |
| `IncomeGroup` | World Bank income classification | String | "High income", "Upper middle income" |
| `Population` | Total population | Integer | 24592588, 204703445 |

---

### 2. Publications & Citations (6 columns)

**Key for Job Demand Analysis**: These metrics indicate AI research capacity and knowledge production, which correlates with demand for AI researchers and data scientists.

| Column | Description | Relevance to Challenge 8 |
|--------|-------------|--------------------------|
| `number_of_total_journal_publications` | Total AI-related journal publications | Indicates research-intensive markets with demand for AI PhDs and researchers |
| `number_of_total_conference_publications` | Total AI conference publications | Shows active AI research communities |
| `number_of_total_publications` | Combined journal + conference publications | Overall AI research output |
| `number_of_total_journal_citations` | Citations to journal publications | Research impact and influence |
| `number_of_total_conference_citations` | Citations to conference publications | Academic network strength |
| `number_of_total_citations` | Total citations received | Knowledge influence metric |

---

### 3. Patents & ML Models (3 columns)

**Key for Job Demand Analysis**: Patent activity indicates commercial AI development and demand for applied AI engineers.

| Column | Description | Relevance to Challenge 8 |
|--------|-------------|--------------------------|
| `number_of_total_patent_grants` | AI-related patents granted | Indicates commercial AI innovation and demand for AI engineers in industry |
| `number_of_notable_ml_models` | Notable ML models developed | Cutting-edge AI capability; demand for ML engineers and researchers |
| `academia_industry_model_production_concentration` | Ratio of academia vs industry model production | Shows whether demand is academic or commercial |

---

### 4. GitHub Activity (2 columns)

**Key for Job Demand Analysis**: Open-source activity indicates practical AI development skills in the workforce.

| Column | Description | Relevance to Challenge 8 |
|--------|-------------|--------------------------|
| `number_of_github_repos` | AI-related GitHub repositories | Indicates developer community size and practical AI skills (supply side) |
| `number_of_github_stars` | Stars on AI repos | Quality and impact of open-source AI work |

---

### 5. Conference Submissions (7 columns)

**Key for Job Demand Analysis**: Conference participation shows active AI research community and demand for specialized researchers.

Top AI/ML conferences tracked:
- **AAAI**: Association for the Advancement of Artificial Intelligence
- **AIES**: AI, Ethics, and Society
- **FAccT**: Fairness, Accountability, and Transparency
- **ICLR**: International Conference on Learning Representations
- **ICML**: International Conference on Machine Learning
- **NeurIPS**: Neural Information Processing Systems

| Column | Description |
|--------|-------------|
| `number_of_ra_submissions_aaai` | Submissions to AAAI conference |
| `number_of_ra_submissions_aies` | Submissions to AIES conference |
| `number_of_ra_submissions_facct` | Submissions to FAccT conference |
| `number_of_ra_submissions_iclr` | Submissions to ICLR conference |
| `number_of_ra_submissions_icml` | Submissions to ICML conference |
| `number_of_ra_submissions_neurips` | Submissions to NeurIPS conference |
| `total_number_of_ra_submissions` | Total submissions across all tracked conferences |

---

### 6. Investment Metrics (5 columns)

**Key for Job Demand Analysis**: Investment directly correlates with job creation in AI startups and companies.

| Column | Description | Relevance to Challenge 8 |
|--------|-------------|--------------------------|
| `private_investment` | Private investment in AI companies (USD) | **CRITICAL**: Direct indicator of AI job demand through startup funding |
| `merger_acquisition_investment` | M&A investment in AI | Consolidation and growth in AI sector |
| `minority_stake_investment` | Minority stake investments | Growth-stage AI companies expanding |
| `public_offering_investment` | IPO investment in AI companies | Mature AI companies going public |
| `number_of_newly_funded_companies` | New AI startups receiving funding | **CRITICAL**: Number of new AI employers entering market |

---

### 7. AI Talent & Skills (6 columns) ⭐ **MOST RELEVANT FOR CHALLENGE 8**

**These are your PRIMARY indicators for supply and demand analysis!**

| Column | Description | Supply/Demand | Relevance |
|--------|-------------|---------------|-----------|
| `relative_ai_skills_penetration` | % of workforce with AI skills | **SUPPLY** | Direct measure of AI talent availability |
| `relative_ai_hiring_rate_yoy_ratio` | Year-over-year AI hiring rate change | **DEMAND** | Growth in AI job demand |
| `ai_talent_concentration` | Concentration of AI talent in country | **SUPPLY** | Geographic distribution of AI workforce |
| `ai_job_postings_perc_of_all_job_postings` | AI jobs as % of all job postings | **DEMAND** | **PRIMARY DEMAND METRIC** |
| `net_migration_flow_ai_skills_per_10k` | Net migration of AI talent (per 10k) | **SUPPLY FLOW** | Brain drain/gain indicator |
| `ai_talent_concentration_gender_equality_index` | Gender balance in AI workforce | **SUPPLY QUALITY** | Diversity and inclusion metric |

---

### 8. Policy & Governance (4 columns)

**Key for Job Demand Analysis**: Government AI strategy indicates future demand through public sector investment and initiatives.

| Column | Description | Relevance to Challenge 8 |
|--------|-------------|--------------------------|
| `num_ai_related_bills_passed` | Number of AI-related laws passed | Policy support for AI sector growth |
| `num_ai_related_bills_passed_3y_moving_average` | 3-year moving average of AI bills | Sustained policy attention |
| `ai_mentions_in_legislative_proceedings` | AI mentions in government proceedings | Policy discourse and priorities |
| `national_ai_strategy_is_released` | Whether country has national AI strategy | Strategic commitment to AI development |

---

### 9. Social Media Metrics (2 columns)

| Column | Description | Relevance |
|--------|-------------|-----------|
| `ai_social_media_posts` | Volume of AI-related social media posts | Public interest and awareness |
| `ai_social_media_conversations_net_sentiment` | Net sentiment of AI discussions | Public perception of AI |

---

### 10. Infrastructure (4 columns)

**Key for Job Demand Analysis**: Infrastructure capacity enables AI development and job creation.

| Column | Description | Relevance to Challenge 8 |
|--------|-------------|--------------------------|
| `parts_semiconductor_devices_export_value` | Export value of semiconductors (USD) | Hardware manufacturing capability |
| `number_of_supercomputers` | Number of supercomputers | Computational infrastructure for AI training |
| `compute_capacity_rmax_gflops` | Total computing capacity (GFLOPS) | AI training capability |
| `internet_speed_median_download_mbps` | Median internet speed (Mbps) | Digital infrastructure for remote AI work |

---

### 11. Per Capita Metrics (35 columns)

All metrics prefixed with `pc_` are **population-normalized** versions of the raw metrics.

**Purpose**: Enable fair comparison between countries of different sizes.

**Format**: `pc_<metric_name>` = `<metric_name>` / `Population`

**Examples**:
- `pc_number_of_total_publications` = Publications per capita
- `pc_private_investment` = AI investment per capita
- `pc_ai_talent_concentration` = AI talent per capita
- `pc_ai_job_postings_perc_of_all_job_postings` = AI job postings per capita

---

### 12. Normalized Metrics (148 columns)

Metrics prefixed with `norm_` are **standardized scores** for cross-country comparison.

**Format**: Each metric has TWO normalized versions:
- `norm_<metric>_display`: Score for visualization (0-100 scale)
- `norm_<metric>_calc`: Score for calculations (normalized to mean=0, std=1)

**Purpose**:
- Compare countries on a common scale
- Create composite indices
- Build dashboards with consistent scales

**Methodology**: Likely min-max normalization or z-score standardization

---

## Key Metrics for Challenge 8: Digital/AI Job Demand & Supply

### PRIMARY DEMAND INDICATORS
1. **`ai_job_postings_perc_of_all_job_postings`** - Direct measure of job demand
2. **`relative_ai_hiring_rate_yoy_ratio`** - Growth in hiring demand
3. **`private_investment`** - Funding driving job creation
4. **`number_of_newly_funded_companies`** - New AI employers

### PRIMARY SUPPLY INDICATORS
1. **`relative_ai_skills_penetration`** - Available workforce with AI skills
2. **`ai_talent_concentration`** - Geographic talent availability
3. **`number_of_github_repos`** - Practical AI developer skills
4. **`number_of_total_publications`** - Research talent pool

### SUPPLY-DEMAND MATCHING METRICS
1. **`net_migration_flow_ai_skills_per_10k`** - Talent flows (indicates mismatches)
2. Compare `ai_job_postings_perc_of_all_job_postings` vs `relative_ai_skills_penetration`
3. Industry concentration: `academia_industry_model_production_concentration`

### ENABLING FACTORS
1. **`internet_speed_median_download_mbps`** - Digital infrastructure
2. **`national_ai_strategy_is_released`** - Policy support
3. **`compute_capacity_rmax_gflops`** - Technical infrastructure

---

## Data Quality Notes

### Missing Values
- Not all countries have data for all metrics
- Some metrics only available for recent years
- Conference submissions may have gaps for smaller countries

### Time Coverage
- Check `PublishYear` range in your dataset
- Likely spans 2017-2023 or similar

### Geographic Coverage
- Focus on countries with `CountryGroup` = "core" for complete data
- Emerging markets may have partial coverage

---

## Recommended Analysis Approaches

### 1. **Supply-Demand Ratio**
```
Supply-Demand Ratio =
  relative_ai_skills_penetration / ai_job_postings_perc_of_all_job_postings
```
- **Ratio > 1**: Oversupply (more talent than jobs)
- **Ratio < 1**: Shortage (more jobs than talent)

### 2. **Skills Gap Index**
Combine multiple metrics:
- High job postings + Low skills penetration = **Skills Gap**
- High investment + Low talent concentration = **Opportunity + Gap**

### 3. **Geographic Imbalance**
- Map `ai_talent_concentration` vs `ai_job_postings_perc_of_all_job_postings`
- Identify `net_migration_flow_ai_skills_per_10k` patterns

### 4. **Trend Analysis**
- Use `PublishYear` to track changes over time
- Calculate year-over-year growth rates
- Forecast future supply-demand dynamics

---

## Citation Metrics Note

Columns 12-14 are citations metrics (not initially visible):
- `number_of_total_journal_citations`
- `number_of_total_conference_citations`
- `number_of_total_citations`

These measure research impact and should be analyzed alongside publication counts.

---

## Questions for Analysis

1. **Which countries have the highest AI job demand growth?**
   - Use: `relative_ai_hiring_rate_yoy_ratio`

2. **Where are skills gaps most severe?**
   - Compare: `ai_job_postings_perc_of_all_job_postings` vs `relative_ai_skills_penetration`

3. **Which regions are experiencing brain drain vs brain gain?**
   - Use: `net_migration_flow_ai_skills_per_10k`

4. **How does investment correlate with job creation?**
   - Correlate: `private_investment` with `number_of_newly_funded_companies` and `ai_job_postings_perc_of_all_job_postings`

5. **What role does infrastructure play?**
   - Analyze: `internet_speed_median_download_mbps` and `compute_capacity_rmax_gflops` vs demand/supply metrics

---

## Dashboard Visualization Recommendations

### Geographic Visualizations
- **Choropleth maps** showing supply-demand ratios by country
- **Flow maps** showing talent migration patterns

### Time Series
- **Line charts** tracking demand vs supply over time
- **Area charts** showing investment trends

### Comparisons
- **Scatter plots**: Supply vs Demand with country bubbles sized by population
- **Bar charts**: Top 10 countries by skills gap
- **Heatmaps**: Skills availability across industries and regions

### Composite Indices
- Create **radar charts** showing multidimensional AI readiness
- **Rankings tables** with sortable columns

---

**Last Updated**: 2025-12-03
**Dataset Version**: HAI Full Database
