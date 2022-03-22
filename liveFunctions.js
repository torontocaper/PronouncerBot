function SortByTitle() {
  var spreadsheet = SpreadsheetApp.getActive();
  spreadsheet.getRange('B:B').activate();
  spreadsheet.getActiveSheet().sort(2, true);
}

function createNewPronouncerDoc() {

  //get existing doc template
  var doc = DocumentApp.openById("1HbkohjN85eOX_ioYAQUBvWnkl0X79qgycIKbjQJmUYc");

  //get URL 
  var url = doc.getUrl();
  
  //get date object and convert to string
  var date = new Date;
  var prettyDate = date.toDateString();

  //create new doc with date in title
  //var doc = DocumentApp.create(`The CP Pronouncer list for ${prettyDate}`);
  
  //add intro
  doc.getBody().insertParagraph(0, `The CP Pronouncer list for ${prettyDate}.`)
  doc.getBody().appendParagraph(`This is a work in progress. Questions? Comments? Contact Adam Burns (amb@cp.org).`)

  //get values in concatenated column
  var sheetValues = SpreadsheetApp.openById("17HucDwuBYfEqXIMz8_nxqMlN1C_06hh1RLccntmlsYI").getSheetByName("Form Responses 1").getSheetValues(2, 6, -1, -1);

  //iterate through alphabet
   
  for (n = 0; n <= 25; n++) {

    //letter variable starts at capital "A" (CharCode 65)
    let letter = String.fromCharCode(65 + n);

    //create a paragraph that is just that letter and make it a heading
    let par = doc.getBody().appendParagraph(letter);
    par.setHeading(DocumentApp.ParagraphHeading.HEADING3);

    //get an array of entries starting with the letter and add a new paragraph (under the heading) for each one
    let entries = sheetValues.filter(entry => entry.toString().startsWith(letter));
    
    entries.forEach(entry => doc.getBody().appendParagraph(entry.toString()));
    
  }

  //log URL and send as an alert
  Logger.log(url); 
  //SpreadsheetApp.getUi().alert(`Here's the link: ${url}`)

}

