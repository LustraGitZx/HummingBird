function search(word){
    request_http = new XMLHttpRequest();
        const url= window.location.protocol + "//" + window.location.host + "/search/"+word.replace(' ','');
        request_http.onreadystatechange = (e) => {
            if (request_http.readyState === XMLHttpRequest.DONE) {
                if(request_http.status === 200){
                    const resp = JSON.parse(request_http.response);
                    console.log(resp);
                    document.getElementById('word').value = resp['word'];
                    document.getElementById('trscr').innerText = resp['phonetic'];
                }else{
                    document.getElementById('word').value = "#NOT FOUND";
                    document.getElementById('trscr').innerText = "";
                }
            }
        }

        request_http.open("GET", url);
        request_http.send();
}

document.getElementById('word').addEventListener('keydown', function(event) {
    if(event.keyCode == 13){
        event.preventDefault();
        var word = document.getElementById("word");
        var value = word.value;
        word.value = '';
        word.blur();
        search(value);
    }
  });