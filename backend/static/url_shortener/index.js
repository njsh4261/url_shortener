// send POST request to server
function postURLEnc() {
    $.ajax({
        method: 'POST',
        url:'http://localhost:8088/url-enc',
        type: 'json',
        data: {
            'url': document.getElementById("input-textbox").value,
        },
        success: function(res) {
            printResult(res, true);
        },
        error: function(err) {
            printResult(err, false);
        },
    });
}

// print output
function printResult(res, is_success) {
    let result_msg = document.getElementById("result-msg");
    console.log(res)
    if(is_success) {
        document.getElementById("output-textbox").value = res.shorten_url;
        result_msg.style.color = "green";
        result_msg.innerHTML = res.message;
    }
    else {
        result_msg.style.color = "red";
        result_msg.innerHTML = res.message;
    }
}

function copyToClipboard() {
    navigator.clipboard.writeText(
        document.getElementById("output-textbox").value
    );
}
