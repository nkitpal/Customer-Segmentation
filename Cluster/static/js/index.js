if ( window.history.replaceState ) {
    window.history.replaceState( null, null, window.location.href );
}

function runScript() {
    $.ajax({
        url: 'visualize', 
        success: function(data) {
            $('#images').css("display","block");
            $('#info').css("display","none");
            $('#csv').css("display","none");
        }
    });
}

function runInfo() {
    $.ajax({
        url: 'info', 
        success: function(data) {
            $('#info').css("display","block");
            $('#images').css("display","none");
            $('#csv').css("display","none");
        }
    });
}

function drawCsv() {
    $.ajax({
        url: 'csv', 
        success: function(data) {
            $('#csv').css("display","block");
            $('#info').css("display","none");
            $('#images').css("display","none");
        }
    });
}