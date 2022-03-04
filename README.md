# simonknowsstuff's blog source code!
This blog contains the source code for my blog. All the built files are on the build branch.

## How does this work?
The main file here is a python file named generator.py on the root of the main branch. This program is responsible for generating the output folder from the template folder and github actions copies the output folder content into the build branch.

The template folder must consist of an `index.html` file along with a `post.html` which are responsible for giving the base template for the output html files. The index file must consist of an html division tag with the id `posts` on which the generator inserts the links to the posts created. As for the post file, it must consist of three tags with IDs `post-heading`, `post-date` which can be whatever type of text tag you wish to use and `post-container` which SHOULD be a div tag.

The generator parses the content files from the content folder where all the content is written in markdown files with `title`, `date` and `summary` metadata. 

## Can I use this generator for my projects?
Absolutely, and even without any credit! (Though credit is appreciated) But it is strongly suggested that you read through my existing content posts and the template folder to check how everything is structured and formatted.

This repository will receive updates from time to time, including new posts or added features.
