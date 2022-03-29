# Intelligent Placer
## Project description
Intelligent placer is a software for placing objects in polygon. 
Programm gets input picture like this:
![test 10](/test/img/10.jpg "test 10")
And if exist disposition like this:
![test 10 proof](/item_set/a.jpg "test 10 proof")
where all objects placed in polygon, programm answer true, otherwise - false.

Now this is just educational task, so programm can receive only photos of objects, which were in training dataset.

## Formal statement of the problem
### General
- programm gets input with path to photo of objects and polygon(all objects and polygon on one photo)
- programm must answer and stop working in no more than *5 minutes*
- answer must be *"true"* or *"false"*
- answer output to standart output stream (in console)

### Task terms
- polygon must be closed
- polygon must be convex
- objects are unique (no instances of same object)
- programm answer *"false"* if input incorrect
- programm may output warning, that input was incorrect, but its optional
- if object is not solid, calculations anyway treat them like it is solid in position that was on photo. For examle:
    - plush toy
    - rope
    - chain
    - scissors
- all objects treat as continuous, with no holes
    - if object has holes, they treated as interior of objects, not as available place
    - if in input photo was object *A* into hole of object *B*, *A* will not be consider as independent object

### Content of photo
- objects and polygon must be placed on white (or light) surface
- objects are from training dataset
- objects must not collide with each other
    - at least 4 pixels between objects must contain only pixels of surface, no objects pixels
- objects must not collide with polygon
    - at least 4 pixels between objects and polygon must contain only pixels of surface, no objects or polygon pixels
- objects and polygon must be entirely contained in a photo
    - at least 4 pixels on boards of photo must contain only pixels of surface, no objects or polygon pixels
- objects must be placed outside of the polygon
- polygon must have black (or dark) borders and transparent interior (common case is drowen on paper with marker)

### Photometric
- photo must be in *\*.jpg* format
- camera direction can be rotated no more then *15&deg;* from surface macronormal (vertical in common case)
- illumination and color of objects should be such that they contrast with surface
    - object border at least 10 units darker than surface (if lightness is sum of components in R8G8B8 colorspace)
- other photometric parameters are not specified, but photo still should meet other types of requirements


## Chosen set of items
Chosen set of items and white surface can be viewed [here](https://github.com/kirillova-ak5/intelligent_placer/blob/develop/item_set/item_set_document.md)


## Training dataset
Training dataset with correct answers, comments and corner cases can be viewed [here](https://github.com/kirillova-ak5/intelligent_placer/blob/develop/test/test_document.md)


## Development plan

This plan is created accordong to some principles
- we believe that we build algorithm, which can find solution for more generalized problem
  it means: program can work with another set of items with minimal changes(no changes in souce code, only additional training or changes in some external files)
  how treat this: we wont using any item specific information in algorithm
- we work with only 2d progections of real-world
  it means: we get all input information from one picture, so we dont need to take care about real-world sizes in santimeters or etc.
  how treat this: all computation will be in relative sizes or pixel sizes


### Algorithm
With current results

0. Convert image to low-res (256 pixels at y axis, x size saves aspect ratio)

![input](/pics/2.jpg "input image")
1. Binarize image

  1.1 Canny

  1.2 binary_closing from skimage

  1.3 binary_fill_holes from skimage

![binarise](/pics/binarisation.png "binarisation")

2. Detect objects and polygon

  2.1 cv.findContours on binarized image

  2.2 Filter and classify finded contours

    2.2.1 Delete contours, which inner area is lower then constant

    2.2.2 Delete nested contours

    2.2.3 Contour with max inner area threats as polygon

    2.2.4 Remaining contours is objects

3. Find minimal bounding rectangle(OBB) of objects and polygon

![contours_and_obb](/pics/contours_and_obb.png "contours and obb")

4. Create set of OBB sized objects' textures, which contains correspondong parts of binarized image

5. Create polygon texture like objects' textures, but invert binarisation

*With this we can just transform(rotate or translate) object texture and add it to polygon texture*

*If we have value >1 in some pixel, here object collides with exterior of polygon*

*Each next object we also can transform and add to image from prev iteration*

*If we have value >1 in some pixel, here object collides with exterior of polygon or previously placed objects*

6. Placement

  6.1 Try to place object on image

    6.1.1 Itarate for all possible transforms(translation x, y with 2px step, rotation angle with 2 deg step)

      6.1.1.1 Add tramsformed object on image, got a new image

      6.1.1.2 Compute error as num of pixels, where value greater then one.

      6.1.1.3 If error is greater than 0.02% of pixels amount, continue iterating

      6.1.1.4 Else and if it was last object - we placed successfully

      6.1.1.5 Else try to place next object on new image

      6.1.1.6 If next object placed successfully - we placed successfully

      6.1.1.7 Else continue iterating

    6.1.2 If we try all transforms - we cant place

7. Output result

![placement](/pics/placement.png "placement")


### Future works:

Now the algorithm is brute force and works terribly long, so firstly we need to improve performance
#### Ideas:
- Improve time limit in problem statement if it possible
- Adaptive iterations (start with a big step, where the error is minimal search with less step)
- Modificate error function and error and error limit
- Reorder objects by area or OBB max edges(larger and longer object is more difficult to place)

#### Another improvments:
- Infractructure to run all tests and view rezults
- Noise filtering on binarisation results
- Change polygon detecton (maw area is not the best way to find out, what region is polygon)
  - use Hough transform to check that border is set of straight lines
  - inner color of region is close to white plane color
