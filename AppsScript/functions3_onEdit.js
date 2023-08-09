function onEdit() {
    let spreadsheet = SpreadsheetApp.getActive();
    //sort by "Title"
    spreadsheet.getRange('B:B').activate();
    spreadsheet.getActiveSheet().sort(2, true);
  }  