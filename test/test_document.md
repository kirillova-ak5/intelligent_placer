# Test data
## Set of most important tests
This cases were chosen as minimal set for iteratively check, that program works correctly.
### First test, most simple. 
Checks that program can work with one object and such polygon, where its clearly seen, can we plase, or not. 
![test 0](/test/img/0.jpg "test 0")
Answer: true

![test 1](/test/img/1.jpg "test 1")
Answer: false


### Precision test
There are two two similar polygons(triangles) and their size is is close to the corner case of bounding triangle of object.
![test 2](/test/img/2.jpg "test 2")
Answer: true

![test 3](/test/img/3.jpg "test 3")
Answer: false


### Two convex objects
Checks that program can work with two convex object.
For first "two convex" test i choose polygon, for which there is only one correct placement.
![test 4](/test/img/4.jpg "test 4")
Answer: true

For second "two convex" test i choose polygon, in which we can place both of objects one at time. And by area this polygon is larger than in first "two convex" test, but both of objects at the same time can't be placed here.
![test 5](/test/img/5.jpg "test 5")
Answer: false


### Convex and non-convex objects
Convex and non-convex objects can be plased only with usage of recess of non convex.
![test 6](/test/img/6.jpg "test 6")
Answer: true


### Handdraw
Checks that polygon drowen by hand can be scanned and handled correctly.
![test 7](/test/img/7.jpg "test 7")
Answer: true


### Two non-convex objects
Two non-convex objects can be plased only with usage of recesses both of non convex.
![test 8](/test/img/8.jpg "test 8")
Answer: true

Two non-convex objects can't be plased, but both of them can be placed one at time.
![test 9](/test/img/9.jpg "test 9")
Answer: false


### Stress test
Stress test with a lot of objects(all) and wery carefully placement. For true answer i attach picture-proof, because its hard to believe that all objeckts really can be placed on A4.
![test 10](/test/img/10.jpg "test 10")
![test 10 proof](/item_set/a.jpg "test 10 proof")
Answer: true

![test 11](/test/img/11.jpg "test 11")
Answer: false


### Corner cases
Zero objects can be successully plased in correct polygon.
![test 12](/test/img/12.jpg "test 12")
Answer: true

Incorrect polygon because there is nothing.
![test 13](/test/img/13.jpg "test 13")
Answer: false

Incorrect polygon because there is point.
![test 14](/test/img/14.jpg "test 14")
Answer: false

Incorrect polygon because it is not closed.
![test 15](/test/img/15.jpg "test 15")
Answer: false

Incorrect polygon because it is not convex.
![test 16](/test/img/16.jpg "test 16")
Answer: false


## Regular cases
![test 17](/test/img/17.jpg "test 17")
Answer: false

![test 18](/test/img/18.jpg "test 18")
Answer: true

![test 19](/test/img/19.jpg "test 19")
Answer: false

![test 20](/test/img/20.jpg "test 20")
Answer: true

![test 21](/test/img/21.jpg "test 21")
Answer: false

![test 22](/test/img/22.jpg "test 22")
Answer: true

![test 23](/test/img/23.jpg "test 23")
Answer: false

![test 24](/test/img/24.jpg "test 24")
Answer: true

![test 25](/test/img/25.jpg "test 25")
Answer: false

![test 26](/test/img/26.jpg "test 26")
Answer: true

![test 27](/test/img/27.jpg "test 27")
Answer: false

![test 28](/test/img/28.jpg "test 28")
Answer: true

![test 29](/test/img/29.jpg "test 29")
Answer: false
