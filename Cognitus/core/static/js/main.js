function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();

            if (cookie.substring(0, name.length + 1) === name + "=") {
                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );
                break;
            }
        }
    }
    return cookieValue;
}

function getAllDatas(url) {
    $.ajax({
        url: url,
        type: "GET",
        dataType: "json",
        success: (data) => {
            const dataList = $("#dataList");
            dataList.empty();
            // console.log(data)
            data.forEach((post) => {
                const postHTMLElement = `
                <li>
                    <p>id: ${post.id}</p>
                    <p>Label: ${post.label}</p>
                    <p>Text: ${post.text}</p>
                </li>
                `;
                dataList.append(postHTMLElement);
            });
        },
        error: (error) => {
            console.log("error");
        },
    });
}

function addData(url, payload) {
    $.ajax({
        url: url,
        type: "POST",
        dataType: "json",
        data: JSON.stringify({ payload: payload }),
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        success: (data) => {
            console.log(data);
        },
        error: (error) => {
            console.log(error);
        },
    });
}

function updateData(url, payload) {
    $.ajax({
        url: url,
        type: "PUT",
        dataType: "json",
        data: JSON.stringify({ payload: payload }),
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        success: (data) => {
            console.log(data);
        },
        error: (error) => {
            console.log(error);
        },
    });
}

function deleteData(url) {
    $.ajax({
        url: url,
        type: "DELETE",
        dataType: "json",
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        success: (data) => {
            console.log(data);
            console.log("aaaaaaaaaa");
        },
        error: (error) => {
            console.log("bbbbbbbbbb");
            console.log(error);
        },
    });
}

function uploadFile(url, file) {
    var formData = new FormData();
    formData.append("myFile", file, file.name);

    $.ajax({
        url: url,
        type: "POST",
        data: formData,
        processData: false,
        contentType: false,
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        success: function (data) {
            console.log(data);
        },
        error: function (error) {
            console.log(error);
        },
    });
}

function trainData(url) {
    $.ajax({
        url: url,
        type: "GET",
        dataType: "json",
        success: (data) => {
            console.log(data);
            $('#status').html("Successfully Trained");
        },
        error: (error) => {
            console.log(error);
            $('#status').html("Failed");
        },
    });
}

function prediction(url, payload) {
    $.ajax({
        url: url,
        type: "POST",
        dataType: "json",
        data: JSON.stringify({ payload: payload }),
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        success: (data) => {
            console.log(data);
            $("#result").text("Predict Result: " + data.predict_result);
        },
        error: (error) => {
            console.log(error);
            $("#result").text("Predict Result: " + error.text);
        },
    });
}
