// ==UserScript==
// @name         comicbook
// @namespace    http://comicbook.moeoverflow.com/
// @version      0.1
// @description  download epub with comicbook
// @author       everpcpc
// @match        https://nhentai.net/*
// @require      https://cdnjs.cloudflare.com/ajax/libs/socket.io/2.3.0/socket.io.js
// @grant        GM_addStyle
// ==/UserScript==

GM_addStyle(`
    .progressBar {
        position: absolute;
        display: block;
        z-index: 100;
        left: 0;
        right: 0;
        top: 0;
        width: 100%;
        text-align: center;
        background-color: grey;
    }
    .download {
        width: 100%;
        height: 100%;
        cursor: pointer;
    }
    .progress {
        width: 0;
        height: 100%;
        background-color: green;
        color: white;
        position: absolute;
        z-index: -10;
    }
` );

(function () {
    'use strict';

    var COMICBOOK_DOMAIN = 'h.comicbook.party';
    var socket = io(COMICBOOK_DOMAIN + ':443');
    var intervals = Object();

    var iconDownload = `<i class="fa fa-download"></i>`;
    var iconProgress = `<i class="fa fa-tachometer"></i>`;


    function checkStatus(element, url) {
        socket.emit('check-status', {
            url: url,
            start: false
        }, function (response) {
            checkResponse(element, url, response);
        });
    }


    function updateProgress(element, percent) {
        element.querySelectorAll('.progress')[0].style.width = percent;
        element.querySelectorAll('span')[0].innerHTML = iconProgress + percent;
    }


    function checkResponse(element, url, response) {
        let interval = intervals[url];
        if (response.status == 'ready') {
            if (interval != null) {
                clearInterval(interval);
            }
            element.onclick = function () { window.location = 'https://' + COMICBOOK_DOMAIN + response.url };
            element.innerHTML = `<div class="download">` + iconDownload + `</div><span></span>`;
            element.style.background = 'green';
        } else if (response.status == 'generating') {
            if (interval == null) {
                intervals[url] = setInterval(function () { checkStatus(element, url) }, 3000);
            }
            element.onclick = null;
            updateProgress(element, (response.progress * 100).toFixed(2) + '%');
        } else if (response.status == 'started') {
            if (interval == null) {
                intervals[url] = setInterval(function () { checkStatus(element, url) }, 3000);
            }
            element.onclick = null;
            updateProgress(element, '1%');
        } else if (response.status == 'absent') {
            if (interval != null) {
                clearInterval(interval);
            }
            element.onclick = function () { startDownload(element, url) };
            element.innerHTML = `<div class="download">` + iconDownload + `</div><span></span>`;
        }
    }


    function startDownload(element, url) {
        let progress = element.querySelectorAll('.download')[0];
        progress.innerHTML = "";
        progress.classList.add('progress');
        progress.classList.remove('download');
        element.querySelectorAll('span')[0].innerHTML = iconProgress + 'starting...';

        socket.emit('check-status', {
            url: url,
            start: true
        }, function (response) {
            checkResponse(element, url, response);
        });
    }


    var galleries = document.querySelectorAll('#content .index-container .gallery');
    Array.prototype.forEach.call(galleries, function (element, idx) {
        let progressBar = document.createElement('div');
        let url = element.querySelectorAll('.cover')[0].href;
        progressBar.classList.add('progressBar');
        element.appendChild(progressBar);
        checkStatus(progressBar, url);
    });

})();
