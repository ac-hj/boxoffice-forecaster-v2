# Boxoffice Forecaster (Attempt #2)

IMPORTANT NOTE: the jupyter notebook in this repo is an *annotated* notebook. Please refer to the notebook for more background details, such as data preprocessing, EDA, and modeling!

-----------

As I was working on this project earlier, I wondered why the model was *not* performing well. Across different models, there were slight variations in the accuracy, precision, and recall scores, but they were all within the range of 0.5. This was actually a really bad news for as it meant that the model could only predict as well as just randomly guesssing whether or not a movie will be successful. 

There are two speculations that I made for this poor performance:

1. Our data for successful movies was *too* small compared to the unsuccessful movie data that by oversampling, successful movies were becoming misrepresented. 
2. PCA is known to be suitable for categorical features, and our data, which also has numerical features, may not have been the best to apply PCA on.

With these speculations, I wanted to see if I could improve the model by changing the sampling methods and not applying PCA. 

## Experiment

### Resampling methods
1. Undersampling
2. Oversampling
3. No sampling

** These resampling method experiments do *not* use scaling or PCA.

### Scaling and dimensionality reduction 
1. Scaling only
2. Scaling only the numerical columns + PCA
3. Scaling all + PCA

** I added additional experiments for scaling as I wanted to see if scaling the numerical columns separately would change anything.

## Conclusion

Surprisingly, both resampling and dimesionality reduction *decreased* the performance of the model. Scaling did not produce a signficant change and decreased the accuracy very slightly. Given these, I decided to not do any sampling, scaling, or dimensionality reduction for my final model. Undersampling and no sampling performed similarly, but no sampling had much less false positive cases, which is better in our context. This is because false positive means predicting a movie to be successful when it won't, which could result in an economic loss (like investment). This is more significant than false negatives because false negative means predicting a movie to be not successful when it would be, which would likely result in more regrets than economic loss.

Following is the result from the improved model, which is all the same as the original model but without sampling, scaling, and dimensionality reduction. 


|   | precision | recall | f1-score | support |
| ------------- | ------------- | ------------ | ------------- | ------------ |
| 0  | 0.94  |  0.99 | 0.97 | 2876|
| 1 | 0.76  | 0.40 | 0.53 | 285|
| accuracy | | | 0.93 | 3161 |
| macro avg | 0.85| 0.70| 0.75| 3161 |
| weighted avg | 0.93 | 0.93 | 0.93 | 3161 |

Precision-recall curve:

<img width="500" alt="Screen Shot 2021-05-26 at 6 17 07 PM" src="https://user-images.githubusercontent.com/58259611/119750626-961ad700-be4e-11eb-905e-3837456b03b1.png">

As we can see above, the sweet spot for the tradeoff between precision and recall scores is not the best. However, this is a *significant* improvement from the previous model, where the best possible trade off was about 0.1 for precision and 0.8 for recall. This insight is valuable for our data given how imbalanced our data is with the positive class data. This precision-recall curve allows us to focus on the positive class and see how our model performs with this class despite the data imbalance. 

ROC Curve:

<img width="500" alt="Screen Shot 2021-05-26 at 6 16 47 PM" src="https://user-images.githubusercontent.com/58259611/119750600-8ac7ab80-be4e-11eb-9639-3a08b23da320.png">

Compared to our original model before, we can now see a small bump in this graph! This is a good sign since it shows that we can achieve higher True Positive Rate with lower False Positive Rate, and as we have noted, false positive cases are not very good for the purpose of our model. This also shows a significant improvement from our previous model, where our ROC was a straight diagonal line, where the FPR was increasing at the same rate as the TPR. 

## Flask App

With this best model, I created a very simple flask web app to accompany the model.
Just fill in the required features, and the model will predict the success of the provided movie and give a confidence level for the prediction!

<img width="1440" alt="Screen Shot 2021-05-31 at 4 02 32 PM" src="https://user-images.githubusercontent.com/58259611/120247828-b4574d00-c229-11eb-802f-b8cb5f5a4075.png">

<img width="1440" alt="Screen Shot 2021-05-31 at 4 04 23 PM" src="https://user-images.githubusercontent.com/58259611/120247898-f5e7f800-c229-11eb-8e00-a1cf321c2965.png">



