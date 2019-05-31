# i2e
Convert image to set of equations through edge detection and optimize curve fiting.
View this file in raw format to see the line breaks.
Usage:
python i2e.py IMAGE
or
python i2e.py IMAGE LOW HIGH
or
python i2e.py IMAGE LOW HIGH MIN
or
python i2e.py IMAGE LOW HIGH MINX MINY
IMAGE can be png or jpg or whatever format supported by opencv2.
LOW and HIGH are thresholds used by Canny edge detection.
MINX is the minimum number of continuos pixels going horizontaly needed to be captured using an equation. The same goes for MINY. if only MIN is given, both MINX and MINY will be set to MIN.
Output:
The program will show you the edges it detected, expect the output graph to look like that. It will also dump all the equation to output.txt, you can just copy the whole file into desmos calculator to see the result.
Tips:
If there are too many edges, try increasing the thresholds.
If the image is not as detailed, try deceasing the thresholds.
Increasing MINX and MINY will also help with reducing small edges, most notably small parterns on ties, flags, ... that can't be reduced by thresholds, but higher MINX and MINY also mean more lost of data.
It is recommended to set MINX and MINY to atleast 2, to reduce the number of equation needed, but still keep the image some what the same. Also setting one of MINX or MINY much higher compared to the other can reduce number of equation needed while keeping the same look because you don't often find image with a lots of edge going both ways, minus when it contain partern of some kind.

How it work:
Canny edge dectection is used on the image to detect edges, then the program decompose the edges into multiple "curves", these curves are then appoximated using curve fitting, upto polynomial of degree 4 in the form of y=F(x)=ax^3+bx^2+cx+d. Since curve fitting can't appoximate vertical line well, the algorithm is ran again with the image "rotated" to produce equation in the form of x=ay^3+by^2+cy+d, which is more than enough to draw the image. Also since the curves are defined from -inf to inf, we have to block the unwanted part. Desmos calculator have a way to define function between [low, high] but one way to do it without directly binding the value is to use roots of negative number. For example, if we don't want funtion F(x) to show up for x>x0, we can use F(x)+sqrt(x0-x)-sqrt(x0-x). Since x0-x<0 for x>x0, F(x)+sqrt(x0-x)-sqrt(x0-x) can't be graph in (x0, inf). The same goes for x<x0. Generally speaking, it is possible to block F(x) on some segment (x0, x1) using roots of some function G(x) that is alway negative for x in (x0, x1), and alway possitive elsewhere. The most simple G(x) function is in the form of G(x)=ax^2+bx+c=(x-x0)(x-x1), if x0 = -inf or x1 = inf we can used G(x) as mentioned above.
Also it should be noted that curve fit is good enough but using other method like UnivariateSpline can produce much better result, albeit not being in polynomial form to be used by desmos.
