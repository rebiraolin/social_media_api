document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".btn-like").forEach(btn => {
    btn.addEventListener("click", () => {
      btn.classList.toggle("liked");
      btn.textContent = btn.classList.contains("liked") ? "Liked" : "Like";
    });
  });

  document.querySelectorAll(".btn-follow").forEach(btn => {
    btn.addEventListener("click", () => {
      btn.classList.toggle("following");
      btn.textContent = btn.classList.contains("following") ? "Following" : "Follow";
    });
  });

  document.querySelectorAll("form[onsubmit]").forEach(form => {
    form.addEventListener("submit", (e) => {
      if (!confirm("Are you sure?")) {
        e.preventDefault();
      }
    });
  });
});
