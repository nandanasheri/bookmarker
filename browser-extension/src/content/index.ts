
chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    console.log(sender.tab ?
                "from a content script:" + sender.tab.url :
                "from the extension");
    if (request.type === "GET_PAGE_DATA")
      sendResponse({url: window.location.href, title : document.title, body: document.body.innerHTML});
  }
);