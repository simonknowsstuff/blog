---
title: Technical details about the blog
date: 04-03-2022
summary: Explanation on how the blog works technically.
draft: False
---

I would like to mention that the source code of the blog is available over [here,](https://github.com/simonknowsstuff/blog) so if you want to check that out and read the README file before reading the post, feel free to!

## So, how does this work?
The blog's design is based off of a template in one of the folders of the root of the repository and the content for the posts are. There are also certain elements created in the index and post HTML files where the content is inserted. The generator is a python file which when run, generates HTML files ready to be hosted automatically with minimal user input.

In the index file mainly, there is only one element's content that is really being changed, and that is the "Posts" box you can see on the front page. Over here, we have a "post container" which lists all the paths of the posts I have written and gives the title, the date and the summary of the post in another neat little box inside the post container.

As for the posts, the post template is taken from the template folder and the actual content, which is written in markdown files inside a folder named "content", is parsed using the [markdown python library](https://pypi.org/project/Markdown/), inserted into the appropriate tags using another [beautiful library](https://pypi.org/project/beautifulsoup4/) in accordance to the template and generated into final post HTML files. There are also special functions I have written in the generator that includes sorting the posts according to dates, and inserting my own classes to make the index file look beautiful but the main takeaway is this.

All these files are generated inside a folder named "output" which is ignored in my github repository. A github actions workflow is set in the repository that runs this python file and copies the content of the output folder to another branch of the repository named "build" which is hosted and ready to display under my github subdomain!

This simple program isn't that great of a project when you look at it as a whole, but I find it interesting to setup everything from scratch completely than rely on a static site generator like HUGO or Jekyll. Don't get me wrong, those are great static site generators, but as stated in my previous post, my goal wasn't solely on creating a blog post - Infact, there was no goal at all, I just wanted to see my idea in action. I will be adding more features to the blog such as the ability to add media locally using a static folder or comment threads under my posts, but that'll do for another time. 