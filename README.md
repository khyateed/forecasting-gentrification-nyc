# Predicting Green Gentrification in New York City
### CUNY Graduate Center Masters Thesis<br>Kat Desai, advised by Professor Anita Raja<br>May, 2025 
## Abstract
This research presents a machine learning framework for predicting gentrification in New York City, with a focus on the role of green infrastructure in driving urban change. We trained a Random Forest classifier, using historical data on socioeconomic characteristics, housing, and sustainability developments, to identify Census Tracts likely to gentrify over a four-year horizon. Time-series and geospatial feature extraction techniques were used to capture neighborhood dynamics, while missing data was addressed through temporal and spatial interpolation. The final model achieved a balanced accuracy of 85.3% and an F1 score of 86.3%. Model evaluation methods include an ablation study, case studies, error analysis, and Shapley value interpretation. 
<br>Results indicate that in the absence of key drivers, green infrastructure features– particularly the number of trees planted and biking-related infrastructure– were among the strongest predictors of gentrification. This suggests that while sustainable urban investments can enhance environmental quality, they may also facilitate neighborhood change and potential displacement. Our findings contribute to ongoing debates about the intersection of sustainability and equity in urban development, and offer insights for planners and policymakers into the spatial equity implications of green urban planning.

## More Information

To access the full paper or for additional questions, please contact khyatee.d@gmail.com

## Repository Structure

```
├── README.md
│ 
├── Wrangling .......................... Notebooks used for initial raw data collection and cleaning
│
├── Data
│   ├── Cleaned ........................ Cleaned data files generated through data wrangling
│   └-- Outputs ........................ Predictions, labels, intermediate files
│
├── ML-Flow ............................ Notebooks for each step of the ML process
│   ├── 1-kriging.ipynb ................ Joins all cleaned data and interpolates missing values
│   ├── 2-labeling.ipynb ............... Generates target variables
│   ├── 3-feature_engineering.ipynb .... Creates features from cleaned data
│   └-- 4-modeling.ipynb ............... Uses ML model to generate predictions
│
├── Experiments ........................ Notebooks for analysis of predictions
│   ├── case_studies.ipynb ............. Inspects model predictions in specific Census Tracts of interest
│   ├── clustering.ipynb ............... Experimental clustering of raw data
│   └-- error_analysis.ipynb ........... Analysis of incorrect predictions
│
├── EDA
│   ├── mapping.ipynb .................. Creates choropleth maps of features and predictions
│   └-- functions.py ................... Helper functions
│
├── Reporting .......................... Powerpoint slides and research poster
│
└-- Images ............................. Images produced from EDA
```
