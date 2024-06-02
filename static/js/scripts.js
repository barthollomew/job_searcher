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
      console.log("Successful retrieve. Clearing and populating table...");
      $("#resultsTable tbody").empty();

      response.forEach((item) => {
        $("#resultsTable tbody").append(
          `<tr>
                        <td>${item.Title}</td>
                        <td>${item.Company}</td>
                        <td>${item.Location}</td>
                        <td>${item.ContractType}</td>
                        <td>${item.Category}</td>
                        <td>${item.Salary}</td>
                        <td>${item.OpenDate}</td>
                        <td>${item.CloseDate}</td>
                    </tr>`,
        );
      });
    },
    error: (error) => {
      console.log("Error: ", error);
    },
  });
}

function addJob() {
  console.log("Adding job...");
  const formData = {
    title: $("input[name='title']").val(),
    description: $("textarea[name='description']").val(),
    salary: $("input[name='salary']").val(),
    location: $("input[name='location']").val(),
    contract_type: $("select[name='contract_type']").val(),
    category: $("input[name='category']").val(),
  };

  $.ajax({
    type: "POST",
    url: "/addingJob",
    data: JSON.stringify(formData),
    contentType: "application/json",
    success: (response) => {
      alert("Job added successfully!");
      console.log(response);
    },
    error: (error) => {
      console.log("Error: ", error);
    },
  });
}

function recommendCategory() {
  console.log("Recommending category...");
  const description = $("textarea[name='description']").val();

  $.ajax({
    type: "POST",
    url: "/recommendCategory",
    data: JSON.stringify({ description: description }),
    contentType: "application/json",
    success: (response) => {
      $("#categoryInput").val(response.recommended_category);
    },
    error: (error) => {
      console.log("Error: ", error);
    },
  });
}

document.addEventListener("DOMContentLoaded", () => {
  const searchButton = document.getElementById("searchButton");
  if (searchButton) {
    searchButton.addEventListener("click", () => {
      search();
    });
  }

  const addJobForm = document.getElementById("addJobForm");
  if (addJobForm) {
    addJobForm.addEventListener("submit", (event) => {
      event.preventDefault();
      addJob();
    });
  }

  const recommendCategoryButton = document.getElementById(
    "recommendCategoryButton",
  );
  if (recommendCategoryButton) {
    recommendCategoryButton.addEventListener("click", () => {
      recommendCategory();
    });
  }
});
