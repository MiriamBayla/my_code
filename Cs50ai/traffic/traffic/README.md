Experimentation process:
1. First I tried 2 convolutional layers with after each of them a pooling layer.
    the first convolutional layer had 32 filters with each filter looking at a patch of 3, 3 pixels.
    The second convolutional layer had 64 filters with each filter looking at a patch of 3, 3 pixels.
    The pooling size after both was 2, 2.
    The dropout rate I used was 50%.
    After experimenting with this - the accuracy rate was 96.3%.

2. Next, I tried changing the dropout rate to 25% and that made the accuracy rate 96.7% which is a drop higher.

3. And then, I added a third convolutinal and then pooling layer with 32 filters which lowered the accuracy rate to only 92.1%.

4. After that, I changed the number of filters on the third convolutional layer from 32 to 128 and that made the accuracy rate 96.9%.

5. After adding these third convolutional and pooling layers, I changed the dropout rate back to 50% which upped the accuracy rate to 97.5%

