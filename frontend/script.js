
let editor = CodeMirror.fromTextArea(document.getElementById("code"), {
    lineNumbers: true,
    mode: "text/x-python",
    theme: "default",
    readOnly: false,
    viewportMargin: Infinity
});

const btn = document.getElementById("generateBtn");
const loader = document.getElementById("loader");

btn.addEventListener("click", generateCode);

function generateCode() {
    let description = document.getElementById("description").value.trim();
    let language = document.getElementById("language").value;

    if (!description) {
        alert("Please enter a description!");
        return;
    }


    loader.style.display = "block";

    fetch("http://127.0.0.1:5000/generate", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({description, language})
    })
    .then(res => res.json())
    .then(data => {
        loader.style.display = "none"; 
        editor.setValue(data.code);


        let mode = "text/x-python";
        if(language === "Java") mode = "text/x-java";
        else if(language === "C++") mode = "text/x-c++src";
        else if(language === "JavaScript") mode = "text/javascript";
        else if(language === "HTML") mode = "text/html";

        editor.setOption("mode", mode);
    })
    .catch(err => {
        loader.style.display = "none";
        alert("Error generating code: " + err);
    });
}
