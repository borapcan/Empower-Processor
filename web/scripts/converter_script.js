// Set background image using JavaScript
document.body.style.backgroundImage = "url('images/bg3.jpg')";


async function selectDirectory() {
    const directory = await eel.choose_directory()();
    document.getElementById("directoryPath").value = directory;
}

function toggleExportArea() {
    eel.toggle_export_area()().then(response => {
        console.log(response); // Logging the response for debugging
    });
}


function toggleStats() {
    eel.toggle_stats()().then(response => {
        console.log(response); // Logging the response for debugging
    });
}

function togglePlot() {
    eel.toggle_plot()().then(response => {
        console.log(response); // Logging the response for debugging
    });
}

function processFiles() {
    eel.process_files(document.getElementById("exportAreaCheckbox").checked)().then(response => {
        if (response.startsWith("Files processed successfully")) {
            // Show success alert
            document.getElementById("successAlert").innerText = response;
            document.getElementById("successAlert").style.display = "block";
            setTimeout(function() {
                document.getElementById("successAlert").style.display = "none";
            }, 5000); // Hide the alert after 5 seconds
        } else {
            // Show error alert
            document.getElementById("errorAlert").innerText = response;
            document.getElementById("errorAlert").style.display = "block";
            setTimeout(function() {
                document.getElementById("errorAlert").style.display = "none";
            }, 5000); // Hide the alert after 5 seconds
        }
        document.getElementById("directoryPath").value = ''
    });
}
