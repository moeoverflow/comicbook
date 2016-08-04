var comicForm = $('#comic-form');
var dlButton = $('#dl-button');
var link = $('#comiclink');

comicForm.form({
    on: 'blur',
    fields: {
      	comiclink: {
	        identifier  : 'comiclink',
	        rules: [{
	        	type   : 'regExp[/(https://)?nhentai.net\/g\/[0-9]+(\/)?$/]',
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

        var id = link.val().match(/[0-9]+/)[0];
        console.log(id);
        dlButton.addClass('loading');
        $.get('/comic/download/' + id, function(result) {
            dlButton.removeClass('loading');
            if (result.status == 'success') {
                $('i', dlButton).removeClass('download');
                $('i', dlButton).addClass('checkmark green');
                window.location = '/comic/' + id;
                setTimeout(function() {
                    $('i', dlButton).addClass('download');
                    $('i', dlButton).removeClass('checkmark green');
                }, 2)
            } else {

            }
        });
    }

})
