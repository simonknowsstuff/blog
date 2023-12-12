function color_index() {
    const posts = document.getElementsByClassName('post');
    let post_index = 0;
    for (post of posts) {
        if (post_index % 2 == 0) {
            post.classList.add('post-1');
        } else {
            post.classList.add('post-2');
        }
        post_index += 1;
    }
}