$('.ui.accordion').accordion();
$('.ui.dropdown').dropdown();
$('.message .close').on('click', function() {
    $(this).closest('.message').transition('fade')
    ;
});
var comicForm = $('#comic-form');
var dlButton = $('#dl-button');
var link = $('#comiclink');

comicForm.form({
    on: 'blur',
    fields: {
      	comiclink: {
	        identifier  : 'comiclink',
	        rules: [{
	        	type   : 'regExp[/((https\:\/\/)?nhentai\.net\/g\/[0-9]+(\/)?$)|((http\:\/\/)?g.e-hentai.org\/g\/[0-9]+\/[0-9a-z]+(\/)?$)|((http\:\/\/)?(www.)?wnacg.org\/photos-index-aid-[0-9]+.html$)/]',
	            prompt : 'Please input correct link.'
	        }]
      	}
    },
    onValid: function() {

    },
    onInvalid: function() {
        if (link.val() == '') {
            $('#input-field').removeClass('error');
        }
    }
});
comicForm.submit = function() {
    return false;
};

$('#dl-button').click(function() {
    if (comicForm.form('is valid')) {
        var source = ''
        var downloadUrl = ''
        if (link.val().match(/nhentai\.net/)) {
            source = 'nhentai'
            var id = link.val().match(/[0-9]+/)[0];
            downloadUrl = '/comic/nhentai/download/' + id;
            dlButton.addClass('loading');
            $.get('/comic/nhentai/check/' + id, response);
        } else if (link.val().match(/e-hentai\.org/)) {
            source = 'ehentai'
            var data = link.val().match(/[0-9]+\/[0-9a-z]+/)[0].split('/');
            var gid = data[0];
            var token = data[1];
            downloadUrl = '/comic/ehentai/download/' + gid + '/' + token;
            dlButton.addClass('loading');
            $.get('/comic/ehentai/check/' + gid + '/' + token, response);
        } else if (link.val().match(/wnacg\.org/)) {
            source = 'wnacg'
            var aid = link.val().match(/[0-9]+/)[0];
            downloadUrl = '/comic/wnacg/download/' + aid;
            console.log(downloadUrl)
            dlButton.addClass('loading');
            $.get('/comic/wnacg/check/' + aid, response);
        }
    }
    function response(result) {
        dlButton.removeClass('loading');
        if (result.status == 'success') {
            $('i', dlButton).removeClass('download');
            $('i', dlButton).addClass('checkmark green');
            window.location = downloadUrl;
            setTimeout(function() {
                $('i', dlButton).addClass('download');
                $('i', dlButton).removeClass('checkmark green');
            }, 2)
        } else {
            $('#message').removeClass('hidden');
        }
    }

})
