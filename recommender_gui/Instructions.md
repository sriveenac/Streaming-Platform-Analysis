# To run the gui, simply run the following in your terminal while in the recommender_gui directory:
  ```
  python3 recommender_gui.py
  ```
# About the recommender platform
There are 2 ways that you can get the 10 recommended titles: 1) Recommender System 2) Input Based Filtering
## 1) Recommender System 
This method outputs the top 10 similar titles to the title that is chosen in the main page. 
It uses a cosine similarity algorithm which computes the similarity between the title chosen and *all* other titles (TV shows AND movies) on all 4 platforms. The similarity is compared by computing the distance between the "Bag of Words" for each title. The Bag of Words contains the title, the director and cast if data exists, descriptions, and all genres it is listed under.
### To get the best out of the recommendations: 
  1) Both fields *need* to be entered : Name and content of choice 
  2) Press OK after every input to make the selection. If you do not press OK, the input is not registered. 
  3) If there is a specific sequel of the movie or TV show, select the first movie in the drop down so that you can get the most robust recommendations
## Input Based Filtering
This method outputs the top 10 titles that meet all the input criteria. You do not need to answer all the questions to get recommendations.
### To get the best out of the recommendations: 
  1) Press OK to make a selection. If you do not press OK after making a selection, the input is not registered. 
  2) If you do not answer a particular question (i.e press OK after the selection), the data will not filter on this column.
  3) Keep the answers to the questions vague if you want many recommendations 
  4) Make sure you press Yes after "Do you want to lock your choices?" to get the recommendations
  5) If no titles meet your criteria, you will see a pop that will return you to the main page to try new inputs. 
 ### Description of the questions: 
  1) Country of Title: This refers to where the movie was produced. If you want an Indian movie for example, select India here. 
  2) How Old Are You?: This question filters on which movies are appropriate for your age. If you are over 18, you will see all titles. 
  
  

