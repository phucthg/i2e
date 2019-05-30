# i2e
Convert image to set of equations through edge detection and optimize curve fiting.
Usage:
python i2e.py IMAGE
or
python i2e.py IMAGE LOW HIGH

IMAGE can be png or jpg or whatever format supported by opencv2.
LOW and HIGH are thresholds used by Canny edge detection.
Output:
The program will show you the edges it detected, expect the output graph to look like that. It will also dump all the equation to output.txt, you can just copy the whole file into desmos calculator to see the result.
Tips:
If there are too many edges, try increasing the thresholds.
If the image is not as detailed, try deceasing the thresholds.


How it work:
Canny edge dectection is used on the image to detect edges, then the program decompose the edges into multiple "curves", these curves are then appoximated using curve fitting, upto polynomial of degree 4 in the form of y=F(x)=ax^3+bx^2+cx+d. Since curve fitting can't appoximate vertical line well, the algorithm is ran again with the image rotated to produce equaltion in the form of x=ay^3+by^2+cy+d, witch is more than enough to draw the image. Also the since curves are defined from -inf to inf, we have to block the unwanted part. Desmos calculator have a way to define function between [low, high] but to one way to do it without directly binding the value is to or roots of negative number. For example, if we don't want funtion F(x) to show up for x>x0, we can use F(x)+sqrt(x0-x)-sqrt(x0-x). Since x0-x<0 for x>x0, F(x)+sqrt(x0-x)-sqrt(x0-x) can't be graph in (x0, inf). The same goes for x<x0. Generally speaking, it is possible to block F(x) on some segment (x0, x1) using roots of some function G(x) that is alway negative for x in (x0, x1), and alway possitive elsewhere. The most simple G(x) function is in the form of G(x)=ax^2+bx+c=(x-x0)(x-x1), if x0 = -inf or x1 = inf we can used G(x) as mentioned above.
