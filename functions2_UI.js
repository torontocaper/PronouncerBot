





function onOpen() {
  //create a menu button to create pronouncer Doc from SS
  SpreadsheetApp.getUi().createMenu("Pronouncer Guide").addItem("Create pronouncer doc", "createNewPronouncerDoc").addToUi();
}
