const siteUrl = '//127.0.0.1:8000/';
const styleUrl = siteUrl + 'static/css/bookmarklet.css';
const minWidth = 150;
const minHeight = 150;

// load css
var head = document.getElementsByTagName('head')[0];
var link = document.createElement('link');
link.rel = 'stylesheet';
link.type = 'text/css';
link.href = styleUrl + '?r=' + Math.floor(Math.random() * 999999999);
head.appendChild(link)


// laad html
var body = document.getElementsByTagName('body')[0];
boxHtml = `
    <div id="bookmarklet">
        <a href="#" id="close">&times;</a>
        <h1>Select an image to scrap</h1>
        <div class="images"></div>
    </div>
`;
body.innerHTML += boxHtml;


function bookmarkletLaunch() {
    var bookmarklet = document.getElementById('bookmarklet');
    var imagesFound = bookmarklet.querySelector('.images');
    imagesFound.innerHTML = '';
    bookmarklet.style.display = 'block';
    bookmarklet.querySelector('#close').addEventListener('click', function () {
        bookmarklet.style.display = 'none';
    })

    var images = document.querySelectorAll('img[src$=".jpg"], img[src$=".jpeg"], img[src$=".png"]');
    console.log('images', images)
    images.forEach(image => {
        const { naturalHeight, naturalWidth } = image;
        console.log('image', Object.keys(image))

        if (naturalWidth >= minWidth && naturalHeight >= minHeight) {
            var imageFound = document.createElement('img');
            imageFound.src = image.src;
            imagesFound.append(imageFound)
        }
    })

    // select image event
    imagesFound.querySelectorAll('img').forEach(image => {
        image.addEventListener('click', function (event) {

            const imageSelected = event.target;
            bookmarklet.style.display = 'none';
            const title = imageSelected.alt || document.title;
            const url = `${siteUrl}images/create/?url=${encodeURIComponent(imageSelected.src)}&title=${encodeURIComponent(title)}`;
            window.open(url, '_blank')
        })
    })
}

bookmarkletLaunch();