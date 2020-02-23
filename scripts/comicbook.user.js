// ==UserScript==
// @name         comicbook
// @namespace    https://moeoverflow.com/
// @version      0.2
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
` );

(function () {
    'use strict';

    var COMICBOOK_DOMAIN = 'h.comicbook.party';
    var socket = io(COMICBOOK_DOMAIN + ':443');
    var intervals = Object();


    function checkStatus(element, url, start = false) {
        socket.emit('check-status', {
            url: url,
            start: start
        }, function (response) {
            checkResponse(element, url, response);
        });
    }


    function updateProgress(element, url, text = '', percent = '0%') {
        let interval = intervals[url];
        let progressInner = element.querySelectorAll('.progress')[0];
        let progressIcon = element.querySelectorAll('i')[0]
        element.querySelectorAll('span')[0].innerHTML = ' ' + text;
        if (text) {
            element.onclick = null;
            element.style.cursor = 'default';
            if (interval == null) {
                intervals[url] = setInterval(function () { checkStatus(element, url) }, 3000);
            }
            progressIcon.classList = 'fa fa-tachometer';
            progressInner.style.width = percent;
        } else {
            element.style.cursor = 'pointer';
            if (interval != null) {
                clearInterval(interval);
            }
            progressIcon.classList = 'fa fa-download';
        }
    }


    function checkResponse(element, url, response) {
        if (response.status == 'ready') {
            element.onclick = function () { window.location = 'https://' + COMICBOOK_DOMAIN + response.url };
            updateProgress(element, url);
            element.style.background = 'green';
        } else if (response.status == 'generating') {
            let percent = (response.progress * 100).toFixed(2) + '%';
            updateProgress(element, url, percent, percent);
        } else if (response.status == 'started') {
            updateProgress(element, url, 'started', '1%');
        } else if (response.status == 'absent') {
            element.onclick = function () {
                updateProgress(element, url, 'starting...', '0%');
                checkStatus(element, url, true);
            };
            updateProgress(element, url);
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
        progressBar.innerHTML = `<div class="progress"></div><i></i><span></span>`;
        checkStatus(progressBar, url);
    });

})();
