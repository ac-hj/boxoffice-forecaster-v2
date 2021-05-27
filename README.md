# Boxoffice Forecaster (Improved version)

As I worked through this project earlier, I was extremely curious why the model was *not* performing well. One speculation that I made was that our data for successful movies was *too* small compared to the unsuccessful movie data that by oversampling, successful movies were becoming misrepresented perhaps. Additionally, after researching PCA is more suitable for categorical columns only.

To improve the model, I tried experimenting with the data. I first experimented with sampling, where I tried undersampling and no sampling as well. I also tried experimenting with scaling and dimensionality reduction. As speculated, both undersampling and no sampling improved the performance of the model noticeably. I also saw that not doing dimensionality reduction led to much better performance as well. Given these, I decided to not do any sampling, scaling, or dimensionality reduction. Undersampling and no sampling performed similarly, but no sampling had much less false positive cases, which was better in our context. This is because false positive means predicting a movie to be successful when it won't, which could result in economic loss. This is more significant than false negative because false negative means predicting a movie to be not successful when it would be, which would more likely result in more regrets than economic loss.

Following is the result from the improved model, which is all the same without sampling and dimensionality reduction. 


|   | precision | recall | f1-score | support |
| ------------- | ------------- | ------------ | ------------- | ------------ |
| 0  | 0.94  |  0.99 | 0.97 | 2876|
| 1 | 0.76  | 0.40 | 0.53 | 285|
| accuracy | | | 0.93 | 3161 |
| macro avg | 0.85| 0.70| 0.75| 3161 |
| weighted avg | 0.93 | 0.93 | 0.93 | 3161 |


<img width="444" alt="Screen Shot 2021-05-26 at 6 16 47 PM" src="https://user-images.githubusercontent.com/58259611/119750600-8ac7ab80-be4e-11eb-9639-3a08b23da320.png">
<img width="412" alt="Screen Shot 2021-05-26 at 6 17 07 PM" src="https://user-images.githubusercontent.com/58259611/119750626-961ad700-be4e-11eb-905e-3837456b03b1.png">
