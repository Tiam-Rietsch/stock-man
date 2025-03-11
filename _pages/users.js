// Get references to modals and buttons
const addUserButton = document.getElementById("addUserButton");
const userModalOverlay = document.getElementById("userModalOverlay");
const closeUserModal = document.getElementById("closeUserModal");
const deleteModalOverlay = document.getElementById("deleteModalOverlay");
const closeDeleteModal = document.getElementById("closeDeleteModal");
const confirmDelete = document.getElementById("confirmDelete");
const cancelDelete = document.getElementById("cancelDelete");

// Variables to track current action and user
let currentUserRow = null;

// Add User Button
addUserButton.addEventListener("click", () => {
  userModalOverlay.classList.add("active");
});

// Edit User Buttons
document.querySelectorAll(".edit-user").forEach((button) => {
  button.addEventListener("click", (e) => {
    e.stopPropagation();
    currentUserRow = e.target.closest("tr");
    userModalOverlay.classList.add("active");
  });
});

// Delete User Buttons
document.querySelectorAll(".delete-user").forEach((button) => {
  button.addEventListener("click", (e) => {
    e.stopPropagation();
    currentUserRow = e.target.closest("tr");
    deleteModalOverlay.classList.add("active");
  });
});

// Close Modals
closeUserModal.addEventListener("click", () => {
  userModalOverlay.classList.remove("active");
});

closeDeleteModal.addEventListener("click", () => {
  deleteModalOverlay.classList.remove("active");
});

cancelDelete.addEventListener("click", () => {
  deleteModalOverlay.classList.remove("active");
});

// Confirm Delete
confirmDelete.addEventListener("click", () => {
  if (currentUserRow) {
    // Send a request to Django to delete the user
    // Django will handle the actual deletion and page reload
    deleteModalOverlay.classList.remove("active");
  }
});