import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover"

import logo from "./assets/bookmark.png"


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
      <div className="bg-neutral-900 w-[350px] h-[300px] px-7 py-6 rounded-4xl">
        <div className="flex gap-3 mb-3 text-offwhite">
          <img src={logo} alt="bookmark_logo" width={40}></img>
          <h1 className="pb-2 text-3xl font-semibold tracking-tight">Keepr</h1>
        </div>
        <div className="border-t mb-6 mx-3"/>

        <div className="flex gap-6 mb-10 justify-center">
          <Button id="tags" className="bg-offwhite text-red-accent hover:text-offwhite ">Add Tags + </Button>

          <Popover>
            <PopoverTrigger asChild>
              <Button id="tags" className="bg-offwhite text-red-accent hover:text-offwhite ">Add Notes + </Button>

            </PopoverTrigger>
            <PopoverContent className="w-60">
              <div className="flex flex-col gap-4">
              <Input
                id="notes"
                placeholder="Add Notes here"
                className="h-8 w-full"
              />
              <Button className="w-fit">Save</Button>
              </div>
            </PopoverContent>
          </Popover>
                
        </div>
        <div className="flex justify-center">
          <Button id="bookmarkPage" variant="destructive" className="bg-red-accent text-lg" onClick={postPageInfo}>Bookmark this Page</Button>
        </div>

        
      </div>
    </>
  )
}

export default App
