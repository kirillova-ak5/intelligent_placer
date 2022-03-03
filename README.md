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
