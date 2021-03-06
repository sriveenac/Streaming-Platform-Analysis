# Streaming-Platform-Analysis
This is the final project for ECE 143 at UCSD
## Context
There are so many online streaming platforms that each offer their own collection of movies and TV Shows. With these increasing options, it can be difficult to evalute which ones to subscribe to. In this analysis, we evaluate the 4 most popular platforms: Netflix, Amazon Prime, Hulu, and Disney Plus. We present the best platform to subscribe depending on the type of content that you enjoy. We also present an easy-to-use tool that recommends movies and tv shows based on a content of your choice, or by filtering on your preferences. 

## Data
Our dataset comes from ShivamB on Kaggle (https://www.kaggle.com/shivamb/netflix-shows) who regularly scrapes the 4 platforms for their content. Please re-download the data instead of using the ones in this repo to get the most up to date content 

## Requirements and Dependencies:
```
pip install requirements.txt

```
## Repo File Structure 
```bash
├── Data
│   ├── Instructions.txt                        <- Instructions for how to download the most recent scrape of the data from Kaggle
│   ├── all_data_processed.csv                  <- combined and pre-processed dataset for all 4 platforms after running pre_processing.py
│   ├── amazon_prime_titles.csv                 <- raw Amazon Prime dataset from kaggle after following instruction in instructions.txt
│   ├── country_analyis_processed.csv           <- combined and pre-processed dataset for country level analysis after running pre_processing.py
│   ├── disney_plus_titles.csv                  <- raw Disney+ dataset from kaggle after following instruction in instructions.txt
│   ├── hulu_titles.csv                         <- raw Hulu dataset from kaggle after following instruction in instructions.txt
│   ├── master_processed.csv                    <- combined and pre-processed dataset for visualizations (removing null rows + director/cast data)
│   ├── netflix_titles.csv                      <- raw Netflix dataset from kaggle after following instruction in instructions.txt
│   ├── pre_processing.py                       <- File to pre-process and create sub_tables for analysis
│   └── release_year_analysis_processed.csv     <- combined and pre-processed dataset for release year analysis after running pre_processing.py
├── recommender_gui
│   ├── Instructions.md                         <- Instructions on how to run the recommender GUI
│   ├── rs_header.png
│   ├── quiz_header.png
│   ├── heading.png
│   └── recommender_gui.py                      
├── ECE143 Final Presentation.pdf
├── Visualizations_Notebook.ipynb               <- Visualization Notebook
├── README.md
└── requirements.txt
```

## Running the Code
  1) Clone or download the repo into your local or virtual environment 
  2) Download the most recent datatsets as explained in Data/instructions.txt or use the datasets in the Data directory that have been downloaded on December 1,2021

### Recommender GUI
  1) Open a terminal window and go into the recommender_gui directory in this project 
  2) run the following on your terminal or simply run the recommender.py file 
      ```
      python3 recommender_gui.py
      ```
### Data analysis and Visualization
  1) Simply run the code in the jupyter notebook 

## Third Party Modules Used: 
  1) Numpy
  2) Pandas 
  3) Tkinter 
  4) tkinter.ttk
  5) sklearn.feature_extraction.text
  6) sklearn.metrics.pairwise
  7) Pillow (PIL) 
  8) matplotlib.pyplot 
  9) seaborn 
  10) Pylab
 ## Citations 
 Netflix Dataset: https://www.kaggle.com/shivamb/netflix-shows
 Amazon Prime Dataset: https://www.kaggle.com/shivamb/amazon-prime-movies-and-tv-shows
 Disney+ Dataset: https://www.kaggle.com/shivamb/disney-movies-and-tv-shows
 Hulu Dataset: https://www.kaggle.com/shivamb/hulu-movies-and-tv-shows
 Recommender System Idea: 
  Our Idea extend the below code to factor in all the platforms and consider the highest similarity across platforms 
  https://www.kaggle.com/pranesh3/content-based-filtering
  
