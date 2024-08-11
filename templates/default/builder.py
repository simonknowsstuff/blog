import os
import shutil
from bs4 import BeautifulSoup as bsoup
import markdown
import datetime as dt
from pathlib import Path

def generate_post_html_content(post):
    data = None
    with open(Path(__file__).with_name('post.html')) as f:
        data = f.read()
    md = markdown.Markdown(extensions = ['meta'])
    html = md.convert(post['html']) # Read html content.
    soup = bsoup(data, 'html.parser') # Template soup.
    post_container = soup.find('div', {'id': 'post-container'})
    # Replace post container tags with content:
    post_heading_tag = soup.find('h1', {'id': 'post-heading'})
    post_date_tag = soup.find('p', {'id': 'post-date'})
    post_title_tag = soup.find('title')
    post_heading_tag.append(post['title'])
    post_date_tag.append('Published on: ' + post['date'])
    if post['edited'] is not None:
        post_date_tag.append(' | Edited on: ' + post['edited'])
    post_title_tag.append(post['title'])
    # Change css reference to parent directory:
    soup.find('link', {'rel': 'stylesheet', 'href': 'style.css'})['href'] = '../style.css'
    psoup = bsoup(html, 'html.parser')

    # Note:
    # For now, this function only expects image tags and files in their respective files / folders.
    # But I may update it in the future to check for other files like audio or video.
    # The code below just redirects the sources of the tags to the static directory.
         
    img_sources = []
    for img in psoup.find_all('img'):
        if img['src'] not in img_sources and img['src'].startswith('static/'):
            img_sources.append(img['src'])
    for link in img_sources:
        count = 0
        for img in psoup.find_all('img', {'src': link}):
            img_path = img['src']
            img['id'] = img_path[len('static/'):] + str(count)
            img['src'] = '../' + img_path
            if img.parent.name != 'div': # Change parent to an image container
                img.parent.name = 'div'
                img.parent['class'] = 'img-container'
            count += 1
    # Open all links in new tab:
    for anchor in psoup.find_all('a'):
        if not anchor['href'].startswith('../'): # Avoid links to the website itself.
            anchor['target'] = '_blank'
    
    post_container.append(psoup)
    return str(soup)

def generate_index_html_content(index_dict):
    print('Generating index file...')
    data = None
    with open(Path(__file__).with_name('index.html')) as f:
        data = f.read()
    soup = bsoup(data, 'html.parser')
    posts_tag = soup.find('div', {'id': 'posts'})
    for post in index_dict['posts']:
        post_title = post['title']
        post_summary = post['summary']
        post_date = post['date']
        new_div = soup.new_tag("div", **{'class':'post'})
        new_div_str = "<h3><a href=\"posts/{name}.html\">{title}</a></h3><p class=\"post_date\">{date}</p><p>{summ}</p>"
        new_div_str = new_div_str.format(
            name=post['filename'], 
            title=post_title, 
            date=post_date, 
            summ=post_summary)
        new_div.append(bsoup(new_div_str, 'html.parser'))
        posts_tag.append(new_div)
    # Refiltering all the posts based on their latest dates:
    posts_date: list = soup.findAll('div', {'class': 'post'})
    posts_date.sort(key=lambda a: dt.datetime.strptime(a.p.string, '%d-%m-%Y'), reverse=True)
    posts_tag.clear()
    for post in posts_date:
        posts_tag.append(post)
    return str(soup.prettify())

def generate_static_content():
    print('Generating static content...')
    if not os.path.isdir('output/static'):
        os.mkdir('output/static')
    for file in os.scandir('static'):
        shutil.copy2(file.path, 'output/static')
    return

def generate_template_files():
    for file in os.scandir(Path(__file__).resolve().parent):
        if file.is_file() and file.name not in ['index.html','post.html','builder.py']:
            shutil.copy2(file.path, 'output')
    return

def build(index_dict): # The mandatory funciton required by the generator.py script.
    print('Building template...')
    generate_static_content()
    generate_template_files()
    with open('output/index.html', 'w') as f:
        f.write(generate_index_html_content(index_dict))
    print('Generating post files...')
    for item in index_dict['posts']:
        with open(f'output/posts/{item['filename']}.html', 'w') as f:
            f.write(generate_post_html_content(item))
    return