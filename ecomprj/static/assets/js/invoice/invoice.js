// $(function() {
//     'use strict';

//     /**
//      * Generating PDF from HTML using jQuery
//      */
//     $(document).on('click', '#invoice_download_btn', function() {
//         var contentWidth = $("#invoice_wrapper").width();
//         var contentHeight = $("#invoice_wrapper").height();
//         var topLeftMargin = 20;
//         var pdfWidth = contentWidth + (topLeftMargin * 2);
//         var pdfHeight = (pdfWidth * 1.5) + (topLeftMargin * 2);

//         // Log contentWidth, contentHeight, pdfWidth, and pdfHeight to verify values
//         console.log('contentWidth:', contentWidth);
//         console.log('contentHeight:', contentHeight);
//         console.log('pdfWidth:', pdfWidth);
//         console.log('pdfHeight:', pdfHeight);

//         var canvasImageWidth = contentWidth;
//         var canvasImageHeight = contentHeight;
//         var totalPDFPages = Math.ceil(contentHeight / pdfHeight) - 1;

//         html2canvas($("#invoice_wrapper")[0], {
//             allowTaint: true
//         }).then(function(canvas) {
//             canvas.getContext('2d');
//             var imgData = canvas.toDataURL("image/jpeg", 1.0);

//             // Log imgData to verify its content
//             console.log('imgData:', imgData);

//             var pdf = new jsPDF('p', 'pt', [pdfWidth, pdfHeight]);
//             pdf.addImage(imgData, 'JPG', topLeftMargin, topLeftMargin, canvasImageWidth, canvasImageHeight);
            
//             for (var i = 1; i <= totalPDFPages; i++) {
//                 pdf.addPage(pdfWidth, pdfHeight);
//                 pdf.addImage(imgData, 'JPG', topLeftMargin, -(pdfHeight * i) + (topLeftMargin * 4), canvasImageWidth, canvasImageHeight);
//             }

//             // Save the PDF
//             pdf.save("invoice.pdf");
//         });
//     });
// });




//KINDA OKAY NA
// $(function() {
//     'use strict';

//     /**
//      * Generating PDF from HTML using jQuery
//      */
//     $(document).on('click', '#invoice_download_btn', function() {
//         var contentWidth = $("#invoice_wrapper").width();
//         var contentHeight = $("#invoice_wrapper").height();
//         var pdfWidth = contentWidth + 40; // Adding some extra width for margin
//         var pdfHeight = pdfWidth * 1.5;

//         // Create a new jsPDF instance
//         var pdf = new jsPDF('p', 'pt', [pdfWidth, pdfHeight]);

//         // Function to add an image to the PDF
//         function addImageToPDF(imgData, x, y, width, height) {
//             pdf.addImage(imgData, 'JPEG', x, y, width, height);
//         }

//         // HTML to canvas
//         html2canvas($("#invoice_wrapper")[0], {
//             allowTaint: true,
//             useCORS: true // Add this line to handle cross-origin content
//         }).then(function(canvas) {
//             var imgData = canvas.toDataURL("image/jpeg", 1.0);

//             // Add the image to the PDF
//             addImageToPDF(imgData, 20, 20, contentWidth, contentHeight);

//             // Save the PDF
//             pdf.save("invoice.pdf");
//         });
//     });
// });

$(document).ready(function() {
    'use strict';

    // Wait for asynchronous content (optional)
    setTimeout(function() {

        /**
         * Generating PDF from HTML using jQuery
         */
        $(document).on('click', '#invoice_download_btn', function() {
            var contentWidth = $("#invoice_wrapper").width();
            var contentHeight = $("#invoice_wrapper").height();
            var pdfWidth = contentWidth + 40; // Adding some extra width for margin
            var pdfHeight = pdfWidth * 1.5;

            // Create a new jsPDF instance
            var pdf = new jsPDF('p', 'pt', [pdfWidth, pdfHeight]);

            // Function to add an image to the PDF
            function addImageToPDF(imgData, x, y, width, height) {
                pdf.addImage(imgData, 'JPEG', x, y, width, height);
            }

            // HTML to canvas
            html2canvas($("#invoice_wrapper")[0], {
                allowTaint: true,
                useCORS: true // Add this line to handle cross-origin content
            }).then(function(canvas) {
                var imgData = canvas.toDataURL("image/jpeg", 1.0);

                // Add the image to the PDF
                addImageToPDF(imgData, 20, 20, contentWidth, contentHeight);

                // Save the PDF
                pdf.save("invoice.pdf");
            });
        });

    }, 50000); // Adjust the delay time as needed
});

