# Data Analysis Workflow & Event Research

## 1. End-to-End Workflow
This project follows a structured pipeline designed to ensure statistical rigor and reproducibility.

### Phase 1: Data Engineering
*   **Ingestion:** Load raw CSV data (`src/data_loader.py`).
*   **Validation:** Check for missing columns and malformed dates using `logging`.
*   **Preprocessing:** 
    *   Standardize mixed date formats.
    *   Linear interpolation for missing values.
    *   Filter for the "Modern Era" (2010+).

### Phase 2: Exploratory Data Analysis (EDA)
*   **Visual Inspection:** Plot raw time series to identify trends.
*   **Statistical Testing:** Perform Augmented Dickey-Fuller (ADF) test to confirm non-stationarity.
*   **Volatility Analysis:** Calculate log returns and rolling standard deviation to identify periods of high variance.

### Phase 3: Bayesian Modeling
*   **Specification:** Define PyMC model with priors ($\mu \sim N(80, 20)$).
*   **Inference:** Run NUTS sampler (2000 draws, 2 chains).
*   **Diagnostics:** Check trace plots and $\hat{R}$ for convergence.

### Phase 4: Insight Generation
*   **Extraction:** Identify posterior mean of $\tau$ (change point).
*   **Attribution:** Map $\tau$ to historical events (see below).
*   **Communication:** Visualize results with credible intervals.

---

## 2. Key Events Dataset (2010–2022)
We have identified 10 key events that influence the regimes detected by our model.

| Date       | Category       | Event                                      | Impact Mechanism |
|------------|----------------|--------------------------------------------|------------------|
| Dec 2010   | Geopolitical   | **Arab Spring Begins**                     | Supply Risk      |
| Feb 2011   | Geopolitical   | **Libyan Civil War**                       | Supply Disruption|
| Jul 2012   | Sanctions      | **Iran Oil Sanctions (EU/US)**             | Supply Cut       |
| Nov 2014   | Policy         | **OPEC Maintains Output**                  | Supply Glut      |
| Jul 2015   | Policy         | **Iran Nuclear Deal Agreed**               | Supply Expectation|
| Jan 2016   | Policy         | **Iran Sanctions Lifted**                  | Supply Glut      |
| Nov 2016   | Policy         | **OPEC+ Production Cuts**                  | Supply Control   |
| Sep 2019   | Geopolitical   | **Abqaiq Attack (Saudi Arabia)**           | Supply Shock     |
| Mar 2020   | Market/Pandemic| **COVID-19 / Saudi-Russia Price War**      | Demand Shock     |
| Feb 2022   | Geopolitical   | **Russia Invades Ukraine**                 | Supply Risk      |

---

## 3. Assumptions and Limitations
*   **Correlation vs. Causation:** The model detects *when* prices changed. It does not prove *what* caused it. The table above provides context, not causal proof.
*   **Stationarity:** We assume regimes are locally stationary (constant mean within a regime), though volatility often spikes during transitions.
*   **Model Sensitivity:** Results are sensitive to Prior selection. We used informed priors based on historical averages ($80/bbl).

## 4. Stakeholder Communication Plan
*   **Investors:** Present "Risk Regimes." Highlights periods where volatility exceeds thresholds.
*   **Policymakers:** Focus on "Shock Magnitude." How much did prices jump during the 2014 vs 2022 shocks?
*   **Energy Companies:** Focus on "Hedging Windows." Identifying the start of a new regime is the trigger point for buying/selling futures.
