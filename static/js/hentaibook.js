var comicForm = $('#comic-form')
var dlButton = $('#dl-button')
comicForm.form({
    on: 'change',
    fields: {
      	comiclink: {
	        identifier  : 'comiclink',
	        rules: [{
	        	type   : 'empty',
	            prompt : 'Please input link.'
	        },{
	        	type   : 'regExp[/(https://)?nhentai.net\/g\/[0-9]+(\/)?$/]',
	            prompt : 'Please input correct link.'
	        }]
      	}
    },
    onValid: function() {
        dlButton.removeClass('disabled')
    },
    onInvalid: function() {
        dlButton.addClass('disabled')
    }
});
comicForm.submit = function() {
    return false;
};

$('#dl-button').click(function() {
    if (comicForm.form('is valid')) {
        var link = $('#comiclink').val();
        var id = link.match(/[0-9]+/)[0];
        dlButton.addClass('loading');
        $.get('/comic/download/' + id, function(result) {
            dlButton.removeClass('loading');
            console.log(result);
            console.log(result.status);
            if (result.status == 'success') {
                $('i', dlButton).removeClass('download');
                $('i', dlButton).addClass('checkmark green');
                window.location.href = '/comic/' + id;
                setTimeout(function() {
                    $('i', dlButton).addClass('download');
                    $('i', dlButton).removeClass('checkmark green');
                }, 2)
            } else {
                $('i', dlButton).removeClass('download');
                $('i', dlButton).addClass('checkmark');
                window.location.href = '/comic/' + id;
                setTimeout(function() {
                    $('i', dlButton).addClass('download');
                    $('i', dlButton).removeClass('checkmark');
            }
        });
    }

})
