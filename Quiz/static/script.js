window.onload = initall;
var saveAnsButton;
function initall(){
    saveAnsButton = document.getElementById('save_ans')
    saveAnsButton.onclick = saveans
}
function saveans(){
    var ans = $("input:radio[name='name']:checked").val()
    // console.log(ans)
    var answ;
    const cor = document.getElementById('correct')
    const c = (cor.textContent)
    if (ans == c){
        answ = 4;
    }
    else{
        answ = 0;
    }   
    var req = new XMLHttpRequest();

    var url = '/saveans?ans=' + answ

    req.open("GET",url,true)
    req.send()
}