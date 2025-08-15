
function App() {

  function postPageInfo() {
    const url = "http://127.0.0.1:5000/add";

    (async () => {
      const [tab] = await chrome.tabs.query({active: true, currentWindow: true});

      // sends message to content script
      if (tab.id !== undefined) {
        const web_page_content = await chrome.tabs.sendMessage(tab.id, {type: "GET_PAGE_DATA"});
        // do something with response here
        console.log(web_page_content);

        // POST request to add a bookmark with these contents
        try {
          const response = await fetch(url, {
            headers: {
              'Accept': 'application/json',
              'Content-Type': 'application/json'
            },
            method: "POST",
            body: JSON.stringify(web_page_content),
          });
          if (!response.ok) {
            throw new Error(`Response status: ${response.status}`);
          }
          const result = await response.json();
          console.log(result);
        } catch (error : any) {
          console.error(error.message);
        }
      }
    })();

}

  return (
    <>
      <h2>Bookmark this Page</h2>
      <input type="text" id="title" placeholder="Enter Notes" />
      <button id="bookmarkPage" onClick={postPageInfo}>Bookmark this Page</button>
    </>
  )
}

export default App
