$(document).ready(function() {

    $('.btn').on('click', function() {

        var button_value = this.id;

        req = $.ajax({
            url : '/update',
            type : 'POST',
            data : { button_value: button_value }
        });

        req.done(function(data) {
            var btvlcontent = document.getElementById('update_inner');
            btvlcontent.innerHTML = '<p class="text-info-cont info-pad">Pressed '+button_value+' button</p>';
        });

    });

});