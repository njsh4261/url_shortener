// send POST request to server
function postURLEnc() {
    $.ajax({
        type: 'POST',
        url:'http://localhost:8088/url-enc',
        data: {
            'url': document.getElementById("input-textbox").value,
        },
    }).done(function(res) {
        printResult(res, true);
    }).fail(function(err) {
        printResult(err.responseJSON, false);
    });
}

// print output
function printResult(res, is_success) {
    let result_msg = document.getElementById("result-msg");
    if(is_success) {
        document.getElementById("output-textbox").value = res.shorten_url;
        result_msg.style.color = "green";
        result_msg.innerHTML = res.message;
    }
    else {
        document.getElementById("output-textbox").value = "";
        result_msg.style.color = "red";
        result_msg.innerHTML = res.message;
    }
}

function copyToClipboard() {
    navigator.clipboard.writeText(
        document.getElementById("output-textbox").value
    );
}
