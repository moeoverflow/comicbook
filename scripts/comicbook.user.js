// ==UserScript==
// @name         comicbook
// @namespace    https://moeoverflow.com/
// @version      0.3.2
// @description  download epub with comicbook
// @author       everpcpc
// @match        https://nhentai.net/*
// @require      https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.1.3/socket.io.js
// @grant        GM_addStyle
// ==/UserScript==

GM_addStyle(`
    .progressBar {
        position: absolute;
        display: block;
        z-index: 5;
        left: 0;
        right: 0;
        top: 0;
        width: 100%;
        text-align: center;
        background-color: grey;
    }
    .progress {
        width: 0;
        height: 100%;
        background-color: green;
        color: white;
        position: absolute;
        z-index: -10;
    }

    @keyframes spinner-border {
        to { transform: rotate(360deg); }
    }
    .spinner-border {
        display: inline-block;
        width: 2rem;
        height: 2rem;
        vertical-align: inherit;
        border: .25em solid currentColor;
        border-right-color: transparent;
        border-radius: 50%;
        -webkit-animation: spinner-border .75s linear infinite;
        animation: spinner-border .75s linear infinite;
    }
    .spinner-border-sm {
        width: 1.5rem;
        height: 1.5rem;
        border-width: .2em;
    }
` );

(function () {
    'use strict';

    var COMICBOOK_DOMAIN = 'h.comicbook.party';
    var socket = io(COMICBOOK_DOMAIN + ':443');

    var TAGS_BLOCK = [
        'yaoi',
        'futanari',
        'male only',
    ];
    var TAGS_WARNING = [
        'anal',
        'big breasts',
        'big ass',
    ];

    /**
     * API
     * if start == true, Comicbook server will try to generate this comic epub file
     */
    function checkStatus(url, start = false, callback) {
        socket.emit('check-status', {
            url: url,
            start: start
        }, callback);
    }

    /**
     * The main function of this part of the code is to manage the download status of multiple comics,
     * and to decide whether to poll the status.
     * As a universal design, it should work on different websites,which means that most of the time,
     * when we adapt this script to a new website, we should not change this part of the code too much.
     */
    var Manager = function () { };
    Manager.prototype.doCheck = function (url, start = false) {
        let self = this;
        var item = this[url];
        checkStatus(item.url, start, function (response) {
            item.updateDOM(item, response)
            if (
                response.status === 'ready' ||
                response.status === 'absent'
            ) {
                clearInterval(item.interval);
                item.interval = null;
            } else if (
                (response.status === 'started' ||
                    response.status === 'generating') &&
                item.interval == null
            ) {
                item.interval = setInterval(function () { self.doCheck(url); }, 3000);
            }
        })
    }
    /**
     * @param url the url of comic
     * @param updateDOM A callback function to update the DOM when a new status is updated
     */
    Manager.prototype.watchItem = function (url, updateDOM) {
        let self = this;
        this[url] = {
            url: url,
            status: 'none',
            interval: setInterval(function () { self.doCheck(url); }, 3000),
            updateDOM,
        }
        self.doCheck(url);
    }
    var manager = new Manager();


    /**
     * This part of the code is used to add interactive UI components,
     * such as download buttons or progress indicator,
     * to the target website.
     */

    // handle nhentai.net gallery page
    (function () {
        function updateProgress(element, text = '', percent = '0%') {
            let progressInner = element.querySelectorAll('.progress')[0];
            let progressIcon = element.querySelectorAll('i')[0]
            element.querySelectorAll('span')[0].innerHTML = ' ' + text;
            if (text) {
                element.onclick = null;
                element.style.cursor = 'default';
                progressIcon.classList = 'fa fa-tachometer';
                progressInner.style.width = percent;
            } else {
                element.style.cursor = 'pointer';
                progressIcon.classList = 'fa fa-download';
            }
        }

        var galleries = [
            ...document.querySelectorAll('#content .container .gallery'),
            ...document.querySelectorAll('#content .container .gallery-favorite .gallery'),
        ];
        Array.prototype.forEach.call(galleries, function (element) {
            let url = element.querySelectorAll('.cover')[0].href;
            let progressBar = document.createElement('div');
            progressBar.classList.add('progressBar');
            element.appendChild(progressBar);
            progressBar.innerHTML = `
                <div class="progress"></div><i></i><span></span>
            `;
            manager.watchItem(url, function updateDOM(item, response) {
                if (response.status == 'ready') {
                    progressBar.onclick = function () { window.location = 'https://' + COMICBOOK_DOMAIN + response.url };
                    updateProgress(progressBar);
                    progressBar.style.background = 'green';
                } else if (response.status == 'generating') {
                    let percent = (response.progress * 100).toFixed(2) + '%';
                    updateProgress(progressBar, percent, percent);
                } else if (response.status == 'started') {
                    updateProgress(progressBar, 'started', '1%');
                } else if (response.status == 'absent') {
                    progressBar.onclick = function () {
                        updateProgress(progressBar, 'starting...', '0%');
                        manager.doCheck(url, true);
                    };
                    updateProgress(progressBar);
                } else {
                    updateProgress(progressBar);
                }
            })
        });
    })();

    // handle nhentai.net detail page
    (function () {
        var url = window.location.href;
        if (!url.match(/nhentai.net\/g\//)) return;

        let tags = document.querySelectorAll('#tags .tag-container .tags')[2];
        for (let i = 0; i < tags.children.length; i++) {
            let tag = tags.children[i];
            let tagName = tag.querySelector("span .name");
            let tagNameText = tagName.innerText;
            if (TAGS_BLOCK.includes(tagNameText)) {
                tagName.style.background = 'red';
                tagName.style.color = 'white';
            }
            if (TAGS_WARNING.includes(tagNameText)) {
                tagName.style.background = 'orange';
                tagName.style.color = 'white';
            }
        }

        var containers = document.querySelectorAll('#info-block .buttons');
        if (containers.length === 0) return;

        var container = containers[0];
        var epubButton = document.createElement('a');
        epubButton.className = "btn btn-secondary";
        epubButton.innerHTML = `
            <i class="fa fa-download"></i>
            Download EPUB
        `
        epubButton.style.display = 'none';
        container.appendChild(epubButton);

        manager.watchItem(url, function updateDOM(item, response) {
            epubButton.style.display = 'inline-block';
            if (response.status == 'ready') {
                epubButton.onclick = function () { window.location = 'https://' + COMICBOOK_DOMAIN + response.url };
                epubButton.className = "btn"
                epubButton.style.backgroundColor = "green"
                epubButton.innerHTML = `
                    <i class="fa fa-download"></i>
                    Download EPUB
                `
            } else if (response.status == 'generating') {
                let percent = (response.progress * 100).toFixed(2) + '%';
                epubButton.className = "btn btn-info dis"
                epubButton.style.backgroundColor = "#17a2b8"
                epubButton.innerHTML = `
                    <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                    starting... ${percent}
                `
                epubButton.onclick = null;
            } else if (response.status == 'started') {
                epubButton.className = "btn btn-info"
                epubButton.style.backgroundColor = "#17a2b8"
                epubButton.innerHTML = `
                    <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                    starting... 1%
                `
            } else if (response.status == 'absent') {
                epubButton.onclick = function () {
                    epubButton.className = "btn btn-info"
                    epubButton.style.backgroundColor = "#17a2b8"
                    epubButton.innerHTML = `
                        <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                        starting... 1%
                    `
                    manager.doCheck(url, true);
                };
                epubButton.className = "btn btn-secondary";
                epubButton.innerHTML = `
                    <i class="fa fa-download"></i>
                    Download EPUB
                `
            }
            item.status = response.status
        })

    })();
})();
