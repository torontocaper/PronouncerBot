function createAlphabetArray() {
  
  let n = 0;
  let alphabet = [];

  for (n = 0; n <= 25; n++) {

    let letter = String.fromCharCode(65 + n);
    alphabet.push(letter);
    
  }
  
  Logger.log(alphabet);

}

function createHeadings() {
  
  let alphabet = createAlphabetArray();
  //Logger.log(alphabet);

}

function apiTest() {
  var fetch = UrlFetchApp.fetch("www.thecanadianpress.com");
  Logger.log(fetch.getContent.toString());
}
