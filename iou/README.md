# IoU

### 1. What is IoU?
IoU - **Intersection over Union**. It is the ratio of the area of the intersection of two areas to the area of their union. IoU measures how much two rectangular areas in an image overlap.

### 2. Mathematical formula

$$ IoU = {\text{{area of intersection of regions A and B}} \over \text{{area of union of regions A and B}}} $$

</br>

![IoU calculating](./images/iou.png)

### 3. IoU with coco images
I wanted to assess the optimal IoU threshold to determine whether to accept or reject the pre-annotations. Based on the IoU value, we can establish the machine learning model's threshold for generating annotations.

This is why I examined the IoU using both perfect COCO annotations and annotations with some errors. I introduced a random percentage error to the X and Y axes in all COCO images containing vehicles.
Here are the results:

![IoU and error chart](./images/iou_chart.png)

As we can see, a larger error means a lower IoU. Some people say that an IoU of 0.7 is considered acceptable. Let's check it:

#### 5% error
![IoU and error chart](./images/000000001532_5.png)
![IoU and error chart](./images/000000044652_5.png)
![IoU and error chart](./images/000000084170_5.png)

#### 10% error
![IoU and error chart](./images/000000001532_10.png)
![IoU and error chart](./images/000000044652_10.png)
![IoU and error chart](./images/000000084170_10.png)

#### 15% error
![IoU and error chart](./images/000000001532_15.png)
![IoU and error chart](./images/000000044652_15.png)
![IoU and error chart](./images/000000084170_15.png)

#### 20% error
![IoU and error chart](./images/000000001532_20.png)
![IoU and error chart](./images/000000044652_20.png)
![IoU and error chart](./images/000000084170_20.png)

Of course, there is a random error, so sometimes it appears acceptable at 15% (as seen in the first image with cars) or 20% (as observed in the image with a plane). However, when we consider the average, the optimal error threshold falls between 10% and 15%, which corresponds to an IoU of 0.7.

For the safety and certainty of accurate pre-annotations, it is advisable to consider an appropriate 10% error threshold.
