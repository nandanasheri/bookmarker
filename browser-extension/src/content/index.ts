// // Who sent the message? React Extension or the Content Script?
// type Sender = "Popup" | "Content"

// interface ChromeMessage {
//   from: Sender;
//   message: any;
// }

// type MessageResponse = (response?: any) => void;

// // check to see whether the sender is from the Popup
// const validateSender = (
//   message: ChromeMessage,
//   sender: chrome.runtime.MessageSender
// ) => {
//   return sender.id === chrome.runtime.id && message.from === "Popup";
// };


// const messageFromPopup = (
//   message: ChromeMessage,
//   sender: chrome.runtime.MessageSender,
//   response: MessageResponse
// ) => {
    
//   const isValidated = validateSender(message, sender);

//     console.log(isValidated, message.message, message.from)
//     //  send back page URL, title and HTML
//   if (isValidated && message.message === "GET_PAGE_DATA") {
//     const title = document.title;
//     const url = window.location.href;

//     response({title, url});
//   }
// };

// const main = () => {
//   console.log("[content.ts] Main");
//   /**
//    * Fired when a message is sent from either an extension process or a content script.
//    */
//   console.log("message from content script")
//   chrome.runtime.onMessage.addListener(messageFromPopup);
// };

// main();

chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    console.log("content script received your message!")
    console.log(sender.tab ?
                "from a content script:" + sender.tab.url :
                "from the extension");
    if (request.type === "GET_PAGE_DATA")
      sendResponse({url: window.location.href, title : document.title, body: document.body.innerHTML});
  }
);