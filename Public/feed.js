function toggleDropdown() {
    var dropdown = document.getElementById("user-dropdown");
    dropdown.style.display = dropdown.style.display === "none" ? "block" : "none";
}

function clearPostPrompt() {
    document.getElementById('user-post').value = "";
    document.getElementById('anime-name').value = "";
}

function sendPostToDb() {
    const reviewBox = document.getElementById("user-post");
    const review = reviewBox.value;
    const animeBox = document.getElementById("anime-name");
    const anime = animeBox.value;

    if (review === "" || anime === "") { 
        return;
    }

    const iD = generateId();
    const postData = {"anime": anime, "review": review, "id": iD};

    const request = new XMLHttpRequest();
    request.onreadystatechange = function() {
        if (this.readyState === 4 && this.status === 200) {
            console.log(this.response);
            clearPostPrompt();
            updateFeed();
        }
    };
    request.open("POST", "/submit-post", true);
    request.setRequestHeader("Content-Type", "application/json");
    request.send(JSON.stringify(postData));
}

function generateId() {
    const alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890';
    let token = '';
    for (let i = 0; i < 30; i++) {
        token += alphabet[Math.floor(Math.random() * alphabet.length)];
    }   
    return token;
}

function updateFeed() {
    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            //clearPostPrompt()
            const posts = JSON.parse(this.response);
            for (const post of posts) {
                addPostToFeed(post);
            }
        }
    }
    request.open("GET", "/feed");
    request.send();
}

function addPostToFeed(postJSON) {
    const feed = document.getElementById("posted-content");
    feed.innerHTML += postToHTML(postJSON);
    feed.scrollIntoView(false);
    feed.scrollTop = feed.scrollHeight - feed.clientHeight;
}

function postToHTML(postJSON) {
    const username = postJSON.username;
    const anime = postJSON.anime;
    const review = postJSON.review;
    const id = postJSON.id;

    let messageHTML = "<form action='/like' method='POST'>";
    messageHTML += "<input type='hidden' name='postId' value='" + id + "'>"; 
    messageHTML += "<button type='submit' class='button-style' id='like-button-" + id + "'>&#128077; " + "{{likes}}" + "</button>";
    messageHTML += "</form>";

    messageHTML += "<span id='post_" + id + "'><b>" + username + "- " + anime + "</b>: " + review + "<br/></span>";
    return messageHTML;
}
function onLoadFunction() {
    //document.addEventListener("keypress", function (event) {
        //if (event.code === "Enter") {
          //  sendPostToDb();
        //}
    //});

    setInterval(updateFeed, 5000);
}

function like(id) {
    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            const responseData = JSON.parse(this.responseText);
            const likeButtonText = getElementById("like-button-" + responseData.id)         
            likeButtonText.innerHTML = "&#128077 " + responseData.like
            console.log(this.response);
        }
    }
    const ids = {"username": username, "id": id};
    request.open("POST", "/like");
    request.send(JSON.stringify(ids));
    //request sent has username and id: response should have the id and the number of likes
    //you can do whatever you want to handle if the perosn already has liked it
}