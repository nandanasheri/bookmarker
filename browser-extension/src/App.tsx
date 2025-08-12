
function App() {

  function getPageInfo() {

  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    const tabId = tabs[0].id;
    
    if (chrome.runtime.lastError) {
      console.error(chrome.runtime.lastError.message);
      return;
    }

    // Send message to content script
    if (tabId !== undefined) {
      chrome.tabs.sendMessage(tabId, { type: "GET_PAGE_DATA" }, (response) => {
        console.log("Page info from content.ts:", response);
      });
    }
  });
}

  return (
    <>
      <h2>Bookmark this Page</h2>
      <input type="text" id="title" placeholder="Enter Notes" />
      <button id="bookmarkPage" onClick={getPageInfo}>Bookmark this Page</button>
    </>
  )
}

export default App
