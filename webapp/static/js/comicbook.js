$('.ui.accordion').accordion();
$('.ui.dropdown').dropdown();
$('.message .close').on('click', function() {
    $(this).closest('.message').transition('fade')
    ;
});
var comicForm = $('#comic-form');
var dlButton = $('#dl-button');
var link = $('#comiclink');

var downloadUrl = '';
var canDownload = false;
var data = undefined;

var regex = 'regExp[/\
((https\:\/\/)?nhentai\.net\/g\/[0-9]+(\/)?$)\
|\
((http\:\/\/)?e-hentai.org\/g\/[0-9]+\/[0-9a-z]+(\/)?$)\
|\
((http\:\/\/)?(www.)?wnacg.com\/photos-index-aid-[0-9]+.html$)\
/]'


comicForm.form({
    on: 'blur',
    fields: {
      	comiclink: {
	        identifier  : 'comiclink',
	        rules: [{
	        	type   : regex,
	            prompt : 'Please input correct link.'
	        }]
      	}
    },
    onValid: function() {
        if (link.val() == '') {
            console.log("kong");
            dlButton.addClass('disabled');
            $('#progress').hide();
            canDownload = false
            return;
        }



        if (link.val().match(/nhentai\.net/)) {
            data = {
                type: 'nhentai',
                id: link.val().match(/[0-9]+/)[0]
            }
        } else if (link.val().match(/e-hentai\.org/)) {
            var value = link.val().match(/[0-9]+\/[0-9a-z]+/)[0].split('/');
            data = {
                type: 'ehentai',
                id: value[0],
                token: value[1]
            }
        } else if (link.val().match(/wnacg\.com/)) {
            data = {
                type: 'wnacg',
                id: link.val().match(/[0-9]+/)[0]
            }
        } else {
            data = undefined;
        }
        canDownload = true
        $('#progress').show()
        getStatus();
    },
    onInvalid: function() {
        console.log("on invalid")
        dlButton.addClass('disabled')

        if (link.val() == '') {
            $('#input-field').removeClass('error');
        }
        $('#progress').hide()
    }
});
comicForm.submit = function() {
    return false;
};

dlButton.prop('disabled', true);
dlButton.click(function() {
    if (comicForm.form('is valid') && canDownload) {
        $('#social-share').show();
        window.location = downloadUrl;
    }
});

$('#social-share').hide();

$('#progress').progress({
    percent: 0
});
$('#progress').hide();


var socket = io('ws://127.0.0.1:5000');

setInterval(getStatus, 3000);

function getStatus() {
    if (data == undefined) {
        return
    }
    socket.emit('check-status', data, function (response) {
        if (response.status == 'ready') {
            dlButton.removeClass('disabled')
            $('#progress').progress({
                percent: 100,
                text: {
                    success : 'You can download it.'
                }
            });
            downloadUrl = response.url;
        } else if (response.status == 'generating') {
            dlButton.addClass('disabled')
            $('#progress').progress({
                percent: parseInt(response.progress * 100),
                text: {
                  active  : 'Generating...{percent}%'
                }
            });
        } else if (response.status == 'started') {
            dlButton.addClass('disabled')
            $('#progress').progress({
                percent: 0,
                text: {
                  active  : 'Started.'
                }
            });
        }
    });
}

var socialShareTitle = '我通过 Comicbook 下载了 epub 漫画本子，你也试一下吧 o(*////▽////*)q';
socialShare('#social-share', {
    title               : 'Just downloaded a Dōjinshi epub comic from Comicbook.',
    sites               : ['twitter', 'facebook', 'weibo','qzone'],
    origin              : 'moeoverflow',
    weiboTitle          : socialShareTitle + ' @moeoverflow',
    qzoneTitle          : 'Moeoverflow | Comicbook',
    qzoneDescription    : socialShareTitle,
    qqTitle             : socialShareTitle
 });