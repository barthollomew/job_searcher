// JS is like middle layer between HTML and Flask
//   1. Receive input from HTML
//   2. Use AJAX to send input to Flask (json)
//   3. Receive response from Flask
//   4. Update HTML with response

console.log("Custom JS is working!");

function search() {
  console.log("Running similarity function!");
  const input = $("#searchInput").val();
  $.ajax({
    type: "POST",
    url: "/search",
    data: JSON.stringify({ keyword: input }),
    contentType: "application/json",
    success: (response) => {
      // On successful receive, do this:
      // 1. Clear table
      // 2. Populate table with array

      console.log(response);
      console.log("Successful retreive. Clearing and populating table...");
      $("#resultsTable tbody").empty();

      response.forEach((item) => {
        $("#resultsTable tbody").append(
          `<tr>
                  <td>${item.name}</td>
                  <td>${item.job}</td>
              </tr>`,
        );
      });
    },
    error: (error) => {
      console.log("Error: ", error);
    },
  });
}

// Run search() when button is clicked
document.addEventListener("DOMContentLoaded", () => {
  const searchButton = document.getElementById("searchButton");
  if (searchButton) {
    searchButton.addEventListener("click", () => {
      search();
    });
  }
});
