$(function(){
    var networks = undefined;

    function showHideFormFields() {
        var security = $(this).find(':selected').attr('data-security');
        // start off with all fields hidden
        $('#identity-group').addClass('hidden');
        $('#passphrase-group').addClass('hidden');
        $('#hidden-ssid-group').addClass('hidden');
        if(security === 'NONE') {
            return; // nothing to do
        }
        if(security === 'ENTERPRISE') {
            $('#identity-group').removeClass('hidden');
            $('#passphrase-group').removeClass('hidden');
            return;
        } 
        if(security === 'HIDDEN') {
            $('#hidden-ssid-group').removeClass('hidden');
            // fall through
        } 
        // otherwise security is HIDDEN, WEP, WPA, or WPA2 which need password
        $('#passphrase-group').removeClass('hidden');
    }

    $('#ssid-select').change(showHideFormFields);

    $.get("/regcode", function(data){
        console.log('regcode=',data);
        if(data.length !== 0){
            regcode = JSON.parse(data);
            $('#reg.code').val(regcode);
        }
    });

    $.get("/networks", function(data){
        console.log('data=',data);
        if(data.length === 0){
            $('.before-submit').hide();
            $('#no-networks-message').removeClass('hidden');
        } else {
            networks = JSON.parse(data);
            $.each(networks, function(i, val){
                console.log('val=',val);
                $('#ssid-select').append(
                    $('<option>')
                        .text(val.ssid)
                        .attr('val', val.ssid)
                        .attr('data-security', val.security.toUpperCase())
                );
            });

            jQuery.proxy(showHideFormFields, $('#ssid-select'))();
        }
    });

    $('#connect-form').submit(function(ev){
        $.post('/connect', $('#connect-form').serialize(), function(data){
            $('.before-submit').hide();
            $('#submit-message').removeClass('hidden');
        });
        ev.preventDefault();
    });
});
