let signaturePad;

window.addEventListener('DOMContentLoaded', () => {

    const canvas = document.getElementById('signature-pad');

    signaturePad = new SignaturePad(canvas, {
        backgroundColor: 'rgb(255,255,255)'
    });

});

function clearSignature() {
    signaturePad.clear();
}

function submitForm() {

    const name = document.getElementById('name').value.trim();
    const idnumber = document.getElementById('idnumber').value.trim();
    const idtype = document.getElementById('idtype').value;
    const phone = document.getElementById('phone').value.trim();
    const company = document.getElementById('company').value.trim();
    const alcocheck = document.getElementById('alcocheck').value;

    // Validaciones
    if (!name || !idnumber || !phone || !company) {
        alert("Please complete all required fields.");
        return;
    }

    if (signaturePad.isEmpty()) {
        alert("Please provide your signature.");
        return;
    }

    const data = {
        name,
        idnumber,
        idtype,
        phone,
        company,
        alcocheck,
        signature: signaturePad.toDataURL()
    };

    console.log("Visitor Registration Data:", data);

    alert("Registration submitted successfully!");

    // Reset form
    document.getElementById('name').value = "";
    document.getElementById('idnumber').value = "";
    document.getElementById('phone').value = "";
    document.getElementById('company').value = "";

    signaturePad.clear();

}