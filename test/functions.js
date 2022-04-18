function storeData() {
  let docProps = PropertiesService.getDocumentProperties();
  docProps.setProperty("documentID", "1HbkohjN85eOX_ioYAQUBvWnkl0X79qgycIKbjQJmUYc")
}

function readData() {
  let docProps = PropertiesService.getDocumentProperties();
  Logger.log(docProps.getProperty("documentID"))
}