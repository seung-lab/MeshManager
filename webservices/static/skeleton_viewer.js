let s = null;

let mdata;
/*
function readSwcFile(e) {
    var ff = document.getElementById("swc_input")
    alert(ff)
    const f = e.target.files[0];
    alert(e)
    if (f) {
        const r = new FileReader();
        r.onload = (e2) => {
            const swcTxt = e2.target.result;
            const  swc = sharkViewer.swcParser(swcTxt);
            if (Object.keys(swc).length > 0) {
                s.loadNeuron('swc', '#ff0000', swc);
                s.render();
            } else {
                alert("Please upload a valid swc file.");
            }
        };
        r.readAsText(f);
    } else {
        alert("Failed to load file");
    }
}
*/

function parseSwcTxt(e) {
    alert(e.value)
    const swcTxt = e.value
    const swc = sharkViewer.swcParser(swcTxt);
    if (Object.keys(swc).length > 0) {
        s.loadNeuron('swc', '#ff0000', swc);
        s.render();
    } else {
        alert("No valid swc file found");
    }
}

function readObjFile(e) {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (event) => {
            const objText = event.target.result;
            s.loadCompartment('foo', '#ff0000', objText);
            s.render();
        };
        reader.readAsText(file);
    }
}

window.onload = () => {
    var swc_input = document.getElementById("swc_input")
    //parseSwcTxt(swc_input)
    //document.getElementById("form_body").addEventListener("onload", test, false)
    const swc = sharkViewer.swcParser(document.getElementById("swc_input").value);
    mdata = JSON.parse(document.getElementById("metadata_swc").text);
    s = new sharkViewer.default({
        animated: false,
        mode: 'particle',
        dom_element: document.getElementById('container'),
        metadata: mdata,
        showAxes: 10000,
        cameraChangeCallback: (data) => { console.log(data) }
    });
    window.s = s;
    s.init();
    s.animate();
    s.loadNeuron('swc', 'ff0000', swc);
    s.render();
};
