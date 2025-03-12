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
    deleteModalOverlay.classList.add("active");
  });
});

// Activate/Deactivate User Buttons
document.querySelectorAll(".activate, .deactivate").forEach((button) => {
  button.addEventListener("click", (e) => {
    e.stopPropagation();
    const userRow = e.target.closest("tr");
    const activationStatus = userRow.querySelector(".activation-status");

    if (activationStatus.classList.contains("pending")) {
      // Activate the user
      activationStatus.innerHTML = `<i class="fas fa-check-circle"></i> DONE`;
      activationStatus.classList.remove("pending");
      activationStatus.classList.add("done");
      e.target.textContent = "Deactivate";
      e.target.classList.remove("activate");
      e.target.classList.add("deactivate");
    } else {
      // Deactivate the user
      activationStatus.innerHTML = `<i class="fas fa-clock"></i> PENDING`;
      activationStatus.classList.remove("done");
      activationStatus.classList.add("pending");
      e.target.textContent = "Activate";
      e.target.classList.remove("deactivate");
      e.target.classList.add("activate");
    }
  });
});

// Close Modals
closeDeleteModal.addEventListener("click", () => {
  deleteModalOverlay.classList.remove("active");
});

cancelDelete.addEventListener("click", () => {
  deleteModalOverlay.classList.remove("active");
});

// Confirm Delete
confirmDelete.addEventListener("click", () => {
  if (currentUserRow) {
    // Remove the user row from the DOM
    currentUserRow.remove();
    deleteModalOverlay.classList.remove("active");
  }
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