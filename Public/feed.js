function toggleDropdown() {
    var dropdown = document.getElementById("user-dropdown");
    dropdown.style.display = dropdown.style.display === "none" ? "block" : "none";
}

function submitPostToHtml(contentJSON) {
    let username = document.getElementById('username').innerText;

    let postContent = document.getElementById('user-post').value;

    //clear user-post
    document.getElementById('user-post').value = '';

    if(postContent === "") {
        return;
    }
    else {
        let newPost = document.createElement('div');
        newPost.innerHTML = '<b>' + username + '</b>: ' + postContent + '<br/><button onclick="like()">👍</button> 0';

        let feed = document.getElementById('posted-content');

        feed.insertBefore(newPost, feed.firstChild);
    }
}

