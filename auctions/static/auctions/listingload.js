loadMoreListingsIsRunning = false;

window.onscroll = () =>
{
    if (window.innerWidth + window.scrollY >= document.body.offsetHeight)
    {
        if(!loadMoreListingsIsRunning)
        {
            loadMoreListings();
        }
        
    }
}

function scrollToTop()
{
    document.body.scrollTop = 0; // For Safari
    document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
}
function changeButtonAPI(listingID, clickedButton)
{
    
    fetch('/watchlistAddRemove',
    {
        method: "PUT",
        body: JSON.stringify
        ({
            operation: clickedButton.value,
            listingID: listingID
        })
    })
    .then(response => response.json())
    .then(result => 
    {
        clickedButton.value = result.newButtonText;
    });
    
}
//continue counting from 5 where 4 is the last post in index by default
var counter = 5;
//how much should be loaded each time
const quantity = 5;

function loadMoreListings()
{
    loadMoreListingsIsRunning = true;
    const start = counter - 1;
    const end = start + quantity;
    counter = end + 1;
    fetch(`/loadListings?start=${start}&end=${end}`)
    .then(response => response.json())
    .then(result => {
        console.log(result);
        result.listings.forEach(()=>
        {
            //generate programmatically all the posts
        })
        //for each of the obj, attach them to the end 

        setTimeout(()=>{
            loadMoreListingsIsRunning = false;
        }, 3000);
    });
}

 