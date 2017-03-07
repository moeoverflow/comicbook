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
var statusUrl = '';
var canDownload = false;

var regex = 'regExp[/\
((https\:\/\/)?nhentai\.net\/g\/[0-9]+(\/)?$)\
|\
((http\:\/\/)?e-hentai.org\/g\/[0-9]+\/[0-9a-z]+(\/)?$)\
|\
((http\:\/\/)?(www.)?wnacg.org\/photos-index-aid-[0-9]+.html$)\
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
            $('#dl-button').addClass('disabled');
            $('#progress').hide();
            canDownload = false
            return;
        }



        if (link.val().match(/nhentai\.net/)) {
            var id = link.val().match(/[0-9]+/)[0];

            statusUrl = '/comic/nhentai/' + id;
            downloadUrl = '/comic/download/nhentai-' + id + '.epub';
        } else if (link.val().match(/e-hentai\.org/)) {
            source = 'ehentai'
            var data = link.val().match(/[0-9]+\/[0-9a-z]+/)[0].split('/');
            var gid = data[0];
            var token = data[1];

            statusUrl = '/comic/ehentai/' + gid + '/' + token;
            downloadUrl = '/comic/download/ehentai-' + gid + '.epub';
        } else if (link.val().match(/wnacg\.com/)) {
            source = 'wnacg'
            var aid = link.val().match(/[0-9]+/)[0];

            statusUrl = '/comic/wnacg/' + aid;
            downloadUrl = '/comic/download/wnacg-' + aid + '.epub';
        }
        canDownload = true
        $('#progress').show()
        getStatus();
    },
    onInvalid: function() {
        console.log("on invalid")
        $('#dl-button').addClass('disabled')

        if (link.val() == '') {
            $('#input-field').removeClass('error');
        }
        $('#progress').hide()
    }
});
comicForm.submit = function() {
    return false;
};

$('#dl-button').prop('disabled', true);
$('#dl-button').click(function() {
    if (comicForm.form('is valid') && canDownload) {
        window.location = downloadUrl;
    }
});

$('#progress').progress({
    percent: 0
});
$('#progress').hide();

setInterval(getStatus, 5000);

function getStatus() {
    if (statusUrl == '') {
        return
    }

    $.get(statusUrl, function (response) {
        canDownload = false;
        if (response.status == 'ready') {
            $('#dl-button').removeClass('disabled')
            $('#progress').progress({
                percent: 100,
                text: {
                    success : 'You can download it.'
                }
            });
            canDownload = true;
        } else if (response.status == 'generating') {
            $('#dl-button').addClass('disabled')
            $('#progress').progress({
                percent: parseInt(response.progress * 100),
                text: {
                  active  : 'Generating...{percent}%'
                }
            });
        } else if (response.status == 'started') {
            $('#dl-button').addClass('disabled')
            $('#progress').progress({
                percent: 0,
                text: {
                  active  : 'Started.'
                }
            });
        }
    });
}
