// Get references to modals and buttons
const deleteModalOverlay = document.getElementById("deleteModalOverlay");
const closeDeleteModal = document.getElementById("closeDeleteModal");
const confirmDelete = document.getElementById("confirmDelete");
const cancelDelete = document.getElementById("cancelDelete");
const searchInput = document.getElementById("searchInput");

// Variables to track current user row
let currentUserRow = null;

// Delete User Buttons
document.querySelectorAll(".delete-user").forEach((button) => {
  button.addEventListener("click", (e) => {
    e.stopPropagation();
    currentUserRow = e.target.closest("tr");

    // set the action for the delete user form
    const deleteUrl = button.getAttribute('delete-url')
    document.getElementById('deleteUserForm').setAttribute('action', deleteUrl)

    deleteModalOverlay.classList.add("active");
  });
});


// Close Modals
closeDeleteModal.addEventListener("click", () => {
  deleteModalOverlay.classList.remove("active");
});

cancelDelete.addEventListener("click", () => {
  deleteModalOverlay.classList.remove("active");
});


// Search Functionality
searchInput.addEventListener("input", () => {
  const searchTerm = searchInput.value.toLowerCase();
  const rows = document.querySelectorAll(".users-table tbody tr");

  rows.forEach((row) => {
    const name = row.querySelector("td:nth-child(1)").textContent.toLowerCase();
    const email = row.querySelector("td:nth-child(2)").textContent.toLowerCase();

    if (name.includes(searchTerm) || email.includes(searchTerm)) {
      row.style.display = "";
    } else {
      row.style.display = "none";
    }
  });
});