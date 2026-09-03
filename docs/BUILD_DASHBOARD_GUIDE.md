# Build Dashboard in Power BI Desktop

**Prerequisites:** Power BI Desktop connected to PostgreSQL `recruitment_dw`

## Step 1: Import Data

1. **Home** → **Get Data** → **More...** → **PostgreSQL database**
2. Server: `localhost:5432`, Database: `recruitment_dw`
3. Authentication: Database → Username: `recruitment`, Password: `recruitment123`
4. Select **Import** mode
5. In Navigator, select ALL 5 tables:
   - `fact_applications`
   - `dim_date`
   - `dim_technology`
   - `dim_candidate`
   - `dim_assessment`
6. Click **Transform Data** → verify tables load → click **Close & Apply**

## Step 2: Verify Relationships (Model View)

1. Click **Model view** icon (left sidebar)
2. Verify these relationships exist (auto-detected):
   - `fact_applications[date_key]` → `dim_date[date_key]`
   - `fact_applications[technology_key]` → `dim_technology[technology_key]`
   - `fact_applications[candidate_key]` → `dim_candidate[candidate_key]`
   - `fact_applications[assessment_key]` → `dim_assessment[assessment_key]`
3. If missing: drag FK from fact to PK in dimension

## Step 3: Create Measures

Go to **Report view**. Right-click any table in the **Data** pane → **New measure**.

Create these measures (paste in the formula bar):

```dax
Total Applications = COUNT(fact_applications[application_id])
```

```dax
Total Hired = SUM(fact_applications[is_hired])
```

```dax
Hiring Rate = DIVIDE([Total Hired], [Total Applications]) * 100
```

```dax
Avg Code Challenge = AVERAGE(fact_applications[code_challenge_score])
```

```dax
Avg Interview Score = AVERAGE(fact_applications[technical_interview_score])
```

## Step 4: Build Pages

### Page 1: Overview

Rename the page to "Overview" (right-click page tab → Rename).

**KPI Cards:**
1. Insert → **Card**
   - Drag `Total Applications` measure → Card
   - Repeat for `Total Hired` and `Hiring Rate`

**Bar Chart - Applications by Technology:**
1. Insert → **Stacked bar chart**
   - Axis: `dim_technology[technology_name]`
   - Values: `Total Applications`
   - Sort by `Total Applications` descending

**Column Chart - Applications by Year:**
1. Insert → **Stacked column chart**
   - Axis: `dim_date[year]`
   - Values: `Total Applications`

---

### Page 2: R1 - Hiring Trends

1. Click **+** to add new page → rename to "R1 - Hiring Trends"

**Line Chart - Monthly Trend:**
1. Insert → **Line chart**
   - X-axis: `dim_date[year]`, then add `dim_date[month_name]`
   - Y-axis: `Hiring Rate`

**Table:**
1. Insert → **Table**
   - Columns: `dim_date[year]`, `dim_date[month_name]`, `Total Applications`, `Total Hired`, `Hiring Rate`

---

### Page 3: R2 - Technology Analysis

New page → "R2 - Technology Analysis"

**Bar Chart:**
1. Insert → **Stacked bar chart**
   - Axis: `dim_technology[technology_name]`
   - Values: `Total Hired`
   - Sort descending

**Table:**
1. Insert → **Table**
   - Columns: `dim_technology[technology_name]`, `Total Applications`, `Total Hired`, `Hiring Rate`

---

### Page 4: R3 - Candidate Profile

New page → "R3 - Candidate Profile"

**Bar Chart by Seniority:**
1. Insert → **Stacked bar chart**
   - Axis: `dim_candidate[seniority]`
   - Values: `Hiring Rate`

**Column Chart by Experience:**
1. Insert → **Stacked column chart**
   - Axis: Create a **Calculated Column** first:
     - Right-click `dim_candidate` → **New column**
     - Formula: `experience_range = SWITCH(TRUE(), dim_candidate[yoe] < 5, "0-4 years", dim_candidate[yoe] < 10, "5-9 years", dim_candidate[yoe] < 20, "10-19 years", "20+ years")`
   - Axis: `dim_candidate[experience_range]`
   - Values: `Total Hired`

**Table:**
1. Insert → **Table**
   - Columns: `dim_candidate[seniority]`, `dim_candidate[experience_range]`, `Total Applications`, `Total Hired`, `Hiring Rate`

---

### Page 5: R4 - Geographic Analysis

New page → "R4 - Geographic Analysis"

**Bar Chart:**
1. Insert → **Stacked bar chart**
   - Axis: `dim_candidate[country]`
   - Values: `Total Applications`
   - Add filter: Top N = 20 by `Total Applications`

**Table:**
1. Insert → **Table**
   - Columns: `dim_candidate[country]`, `Total Applications`, `Total Hired`, `Hiring Rate`

---

### Page 6: R5 - Assessment Analysis

New page → "R5 - Assessment Analysis"

**Matrix:**
1. Insert → **Matrix**
   - Rows: `dim_assessment[code_challenge_score]`
   - Columns: `dim_assessment[technical_interview_score]`
   - Values: `Total Applications`

**Column Chart:**
1. Insert → **Stacked column chart**
   - X-axis: `dim_assessment[code_challenge_score]`
   - Y-axis: `Total Applications`

---

## Step 5: Save

**File → Save As** → `dashboard_recruitment.pbix`
