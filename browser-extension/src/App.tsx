
function App() {

  function getPageInfo() {

    (async () => {
      const [tab] = await chrome.tabs.query({active: true, currentWindow: true});

      // sends message to content script
      if (tab.id !== undefined) {
        const response = await chrome.tabs.sendMessage(tab.id, {type: "GET_PAGE_DATA"});
        // do something with response here, not outside the function
        console.log(response);

        // call our API!
      }
    })();

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
