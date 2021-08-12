let ip_ = $("input#ip")
let machine_name_ = $("input#machine_name")
let passowrd_ = $("input#password_")
let relaod = $("a#reload__top")

relaod.click(() => {
    window.location.replace("/");
})

let runcmd_btn = $("button.run_cmd").click(() => {

    var url = "/getoutput"
    fetch(url, {
        method: 'POST',
        body: JSON.stringify({
            'ip': ip_.val(),
            'machine_name': machine_name_.val(),
            'passowrd': passowrd_.val(),
        })
    })
    window.location.replace("/getoutput");
})

$("button.get_res").click(() => {

    var url = "/getstatus"
    fetch(url, {
        method: 'POST',
        body: JSON.stringify({
            'ip': ip_.val(),
            'machine_name': machine_name_.val(),
            'passowrd': passowrd_.val(),
        })
    }).then(() => {
        window.location.replace(url);
    } )

})




$("button#getoutput").click(() => {

    var inputcmd = $("input#getinput")

    var url = "/getoutput"
    fetch(url, {
        method: 'POST',
        body: JSON.stringify({
            'inputcmd' : inputcmd.val()
        })
    }).then((res) => {
        return res.json()
    }).then((data) => {
        document.getElementById('fill__output').value = data.values.text;
    })
    
})










/*

    var url = "/getoutput"
    fetch(url, {
        method: 'POST',
        body: JSON.stringify({
            'ip': ip_.val(),
            'machine_name': machine_name_.val(),
            'passowrd' : passowrd_.val()
        })
    }).then((res) => {
        return res.json()
    }).then((data) => {
        console.log(data)
    })

*/