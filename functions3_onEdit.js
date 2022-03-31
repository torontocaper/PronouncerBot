function onEdit() {
    let spreadsheet = SpreadsheetApp.getActive();
    spreadsheet.getRange('B:B').activate();
    spreadsheet.getActiveSheet().sort(2, true);
  }  